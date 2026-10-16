"""Can a pawn component be frozen next to a trebuchet on an 8-file board?

Geometry.  A trebuchet uses three files: pawns on file x (White P(x,r), Black
P(x,r+1)) and the kings on x-1 and x+1 (WK (x+s, r+1), BK (x-s, r), s = +-1).
We put it on files f, g, h (x = g).  The kings' files carry no pawns, so the
other pawns live on files a..e:
  * flat 8x8: a..e is bounded by the board edge on the left and by the f-king;
  * 8-file cylinder: a..e is bounded by the h-king (across the seam) on the
    left and by the f-king on the right.
Pawns cannot capture onto a king file (no enemy pawn is ever there), so the
component is played exactly as on a flat strip of its own width, whichever
board it sits on.  Hence on the 8-file cylinder the component is always a FLAT
segment of width <= 5 (<= 3 if it may not touch either king file, 4 if it may
touch one).

Freeze condition (conservative).  At every position reachable in the
component's game tree (either side moving, any order, terminal passer
positions included), no pawn may
  * stand on a square the enemy king attacks (the king could capture it), or
  * attack the enemy king's square (a check forces a king move).
Pawns never reach a king file, so these are the only interactions.

This is a MODEL-level test only: it does not check that the chess game really
follows the CGT model (passed pawn = win, kings never leave), which needs a
whole-board search (workstream A2).

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python atlas/cylinder/freeze.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402

FILES = "abcdefgh"
X = 6  # trebuchet pawn file g; kings on f (5) and h (7)


def kmoves(s, wrap, n=8):
    f, r = s
    out = set()
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == dr == 0:
                continue
            g, q = f + df, r + dr
            if wrap:
                g %= n
            if 0 <= g < n and 1 <= q <= 8:
                out.add((g, q))
    return out


def pawn_att(p, colour, wrap, n=8):
    f, r = p
    q = r + (1 if colour == "W" else -1)
    out = set()
    for df in (-1, 1):
        g = f + df
        if wrap:
            g %= n
        if 0 <= g < n:
            out.add((g, q))
    return out


def reachable(width, W, B, ep=True):
    """All pawn configurations reachable in the component's game tree on a flat
    strip of the given width (both sides may move in any order).  Terminal
    nodes (some passed pawn) are included but not expanded."""
    board = Board(width, 8, False, ep)
    start = Pos(frozenset(W), frozenset(B))
    seen = {start}
    dq = deque([start])
    while dq:
        p = dq.popleft()
        if pawns.passed(board, p, "W") or pawns.passed(board, p, "B"):
            continue
        for side in ("W", "B"):
            for q in pawns.moves(board, p, side):
                if q not in seen:
                    seen.add(q)
                    dq.append(q)
    return {(p.white, p.black) for p in seen}


def placements(width):
    """(offset, mirror, s, r) for a component of `width` files on a..e."""
    for o in range(0, 5 - width + 1):
        for mirror in (False, True):
            for s in (1, -1):
                for r in range(2, 7):
                    yield o, mirror, s, r


def kings(s, r):
    wk = ((X + s) % 8, r + 1)
    bk = ((X - s) % 8, r)
    return wk, bk


def check_placement(nodes, width, o, mirror, s, r, wrap):
    wk, bk = kings(s, r)
    wk_att, bk_att = kmoves(wk, wrap), kmoves(bk, wrap)
    mp = (lambda c: o + (width - 1 - c)) if mirror else (lambda c: o + c)
    for Wp, Bp in nodes:
        for f, q in Bp:
            sqb = (mp(f), q)
            if sqb in wk_att or wk in pawn_att(sqb, "B", wrap):
                return False, f"black pawn {FILES[sqb[0]]}{q} vs WK {FILES[wk[0]]}{wk[1]}"
        for f, q in Wp:
            sqw = (mp(f), q)
            if sqw in bk_att or bk in pawn_att(sqw, "W", wrap):
                return False, f"white pawn {FILES[sqw[0]]}{q} vs BK {FILES[bk[0]]}{bk[1]}"
    return True, ""


def fen(W, B, width, o, mirror, s, r):
    mp = (lambda c: o + (width - 1 - c)) if mirror else (lambda c: o + c)
    wk, bk = kings(s, r)
    board = {}
    for f, q in W:
        board[(mp(f), q)] = "P"
    for f, q in B:
        board[(mp(f), q)] = "p"
    board[(X, r)] = "P"
    board[(X, r + 1)] = "p"
    board[wk] = "K"
    board[bk] = "k"
    rows = []
    for q in range(8, 0, -1):
        row, e = "", 0
        for f in range(8):
            c = board.get((f, q))
            if c:
                row += (str(e) if e else "") + c
                e = 0
            else:
                e += 1
        rows.append(row + (str(e) if e else ""))
    return "/".join(rows) + " w - - 0 1"


def parse(text):
    w_part, b_part = text.split("/")
    sqs = lambda part: [(FILES.index(t[0]), int(t[1:])) for t in part.split(":")[1].split()]
    return sqs(w_part), sqs(b_part)


def trim(W, B):
    lo = min(f for f, _ in W + B)
    hi = max(f for f, _ in W + B)
    return [(f - lo, r) for f, r in W], [(f - lo, r) for f, r in B], hi - lo + 1


def analyse(text, label="", verbose=True):
    W, B = parse(text)
    W, B, width = trim(W, B)
    out = {"pos": text, "label": label, "width": width}
    if width > 5:
        out["note"] = "wider than 5 files: cannot be placed beside a trebuchet on 8 files"
        return out
    nodes = reachable(width, W, B)
    out["nodes"] = len(nodes)
    for wrap in (False, True):
        ok = []
        fails = {}
        for o, mirror, s, r in placements(width):
            good, why = check_placement(nodes, width, o, mirror, s, r, wrap)
            if good:
                ok.append((o, mirror, s, r))
            else:
                fails[why] = fails.get(why, 0) + 1
        key = "cyl8" if wrap else "flat8"
        out[key] = {"n_ok": len(ok), "n_total": len(list(placements(width))),
                    "examples": [fen(W, B, width, *p) for p in ok[:3]],
                    "typical_failures": sorted(fails.items(), key=lambda kv: -kv[1])[:3]}
    if verbose:
        print(json.dumps(out, ensure_ascii=False))
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", help="JSONL with {'pos':..., 'label':...} per line")
    ap.add_argument("positions", nargs="*")
    a = ap.parse_args()
    items = [(p, "") for p in a.positions]
    if a.candidates:
        with open(a.candidates) as fh:
            for line in fh:
                d = json.loads(line)
                items.append((d["pos"], d.get("label", "")))
    if not items:
        items = [("W: a2 c2 / B: b7 d7", "flat-4 *2 candidate (count/mover rule)")]
    for p, lab in items:
        analyse(p, lab)
