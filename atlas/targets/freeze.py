#!/usr/bin/env python3
"""Can a pawn component be put on the flat 8x8 board next to a trebuchet freeze?

Geometry. The freeze is a trebuchet: W pawn on g(r), B pawn on g(r+1), one king on
the f-file and the other on the h-file (orientation A: WK f(r+1), BK h(r);
orientation B: BK f(r), WK h(r+1)); r = 2..6. Every king move drops that side's
g-pawn (model convention: the opponent then has a passed pawn = +-W). The freeze
may share files with kings but not with pawns, and the component must be
separated from the g-file by a pawn-free file. So on 8 files:

  width <= 4: component on a-d (or narrower), e pawn-free, kings f/h. No component
              pawn ever reaches the e-file, so no pawn can ever touch a king.
  width  = 5: component on a-e, f pawn-free but holding a king, which stands next
              to the e-file. (The mirror image, component on d-h with the
              trebuchet on b and kings a/c, is the same test on the mirrored
              component.)
  width >= 6: impossible: w + 3 files are needed (component, a pawn-free file
              holding a king, the trebuchet file, the other king's file), and an
              edge trebuchet (kings on the same side) has the kings adjacent.

Freeze condition (conservative, model level; the same as atlas/cylinder/freeze.py):
at every position reachable in the component's game tree (either side moving, in
any order; terminal passer positions included but not expanded; e.p. on, and a
position is expanded unless it is terminal under the e.p.-aware test, which
reaches a superset of the textbook test's positions), no pawn stands on a square
the enemy king attacks (the king could take it) or attacks the enemy king (check).

Legality (necessary conditions only, as atlas/flat8/rerun reach_check): every pawn
of the full 8x8 position (component + trebuchet) is assigned a distinct start
file, needing |file shift| <= ranks advanced captures, and each side's total
pawn captures must not exceed the number of enemy men missing from the board.

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python atlas/targets/freeze.py "W: a2 b2 / B: a6 c5" 3 [...]
  PYTHONPATH=. .venv/bin/python atlas/targets/freeze.py --json work/freeze_in.json --out freeze_SCOPE.json
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from collections import deque
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
EPWT = "/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt"


def _load_aware_pawns():
    """cylcgt.pawns from the ep-aware-passed worktree (read-only), PASSED_RESPECTS_EP=True,
    loaded as a separate package so that it can coexist with the main checkout's cylcgt."""
    import importlib
    if "cylcgt_epwt" not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            "cylcgt_epwt", os.path.join(EPWT, "cylcgt", "__init__.py"),
            submodule_search_locations=[os.path.join(EPWT, "cylcgt")])
        mod = importlib.util.module_from_spec(spec)
        sys.modules["cylcgt_epwt"] = mod
        spec.loader.exec_module(mod)
    pawns = importlib.import_module("cylcgt_epwt.pawns")
    assert getattr(pawns, "PASSED_RESPECTS_EP", None) is True, pawns.__file__
    return pawns


pawns = _load_aware_pawns()
sys.path.insert(0, HERE)
import common as C  # noqa: E402


def reachable(width, Wp, Bp):
    board = pawns.Board(width, 8, False, True)
    start = pawns.Pos(frozenset(Wp), frozenset(Bp))
    seen = {start}
    dq = deque([start])
    while dq:
        p = dq.popleft()
        if pawns.passed(board, p, "W") or pawns.passed(board, p, "B"):
            continue  # terminal (included, not expanded)
        plain = pawns.Pos(p.white, p.black, None)
        for side in ("W", "B"):
            src = p if (p.ep and p.ep[2] == side) else plain
            for q in pawns.moves(board, src, side):
                if q not in seen:
                    seen.add(q)
                    dq.append(q)
    return seen


def occupancy(width, Wp, Bp):
    """Squares ever occupied by a white / black pawn in the reachable set."""
    occW, occB = set(), set()
    n = 0
    for p in reachable(width, Wp, Bp):
        n += 1
        occW |= set(p.white)
        occB |= set(p.black)
    return occW, occB, n


def king_ok(ksq, kcolour, occW, occB):
    """No enemy pawn ever adjacent to (or checking) the king on ksq."""
    kf, kr = ksq
    enemy = occB if kcolour == "W" else occW
    for (f, r) in enemy:
        if max(abs(f - kf), abs(r - kr)) == 1:
            return False
    # checks: a white pawn on (kf+-1, kr-1) checks a black king; a black pawn on
    # (kf+-1, kr+1) checks a white king -- both squares are adjacent, so covered.
    return True


def min_captures(pawn_list, white):
    best = None
    for starts in permutations(range(8), len(pawn_list)):
        tot = 0
        for (f, r), f0 in zip(pawn_list, starts):
            need = abs(f - f0)
            adv = (r - 2) if white else (7 - r)
            if need > adv:
                break
            tot += need
        else:
            best = tot if best is None else min(best, tot)
    return best


def legal_ok(Wfull, Bfull):
    cw, cb = min_captures(Wfull, True), min_captures(Bfull, False)
    if cw is None or cb is None:
        return False, cw, cb
    missing_black = 16 - (len(Bfull) + 1)
    missing_white = 16 - (len(Wfull) + 1)
    return (cw <= missing_black and cb <= missing_white), cw, cb


def fen_of(Wfull, Bfull, WK, BK, to_move="w"):
    board = {}
    for q in Wfull:
        board[q] = "P"
    for q in Bfull:
        board[q] = "p"
    board[WK] = "K"; board[BK] = "k"
    rows = []
    for r in range(8, 0, -1):
        s, e = "", 0
        for f in range(8):
            c = board.get((f, r))
            if c is None:
                e += 1
            else:
                s += (str(e) if e else "") + c
                e = 0
        rows.append(s + (str(e) if e else ""))
    return "/".join(rows) + f" {to_move} - - 0 1"


def placements(position, width):
    """All trebuchet placements (and component mirror images) that pass the
    conservative freeze test, with the necessary legality check."""
    W0, B0 = C.parse_pos(position)
    out = []
    if width >= 6:
        return {"width": width, "fits": False, "reason": "width >= 6 cannot sit beside a trebuchet on 8 files"}
    for mir, off in [(m, o) for m in (False, True) for o in range(0, max(1, 5 - width) if width <= 4 else 1)]:
        Wc = [((width - 1 - f) if mir else f, r) for f, r in W0]
        Bc = [((width - 1 - f) if mir else f, r) for f, r in B0]
        occW, occB, nreach = occupancy(width, Wc, Bc)
        # a component narrower than 4 files may also sit on b.., c.. (file e stays empty)
        Wc = [(f + off, r) for f, r in Wc]
        Bc = [(f + off, r) for f, r in Bc]
        occW = {(f + off, r) for f, r in occW}
        occB = {(f + off, r) for f, r in occB}
        for r in range(2, 7):
            for orient in ("A", "B"):
                if orient == "A":
                    WK, BK = (5, r + 1), (7, r)
                else:
                    WK, BK = (7, r + 1), (5, r)
                Wfull = Wc + [(6, r)]
                Bfull = Bc + [(6, r + 1)]
                fk, fcol = (WK, "W") if orient == "A" else (BK, "B")
                ok_freeze = king_ok(fk, fcol, occW, occB) and king_ok(WK if fcol == "B" else BK,
                                                                       "W" if fcol == "B" else "B", occW, occB)
                ok_leg, cw, cb = legal_ok(Wfull, Bfull)
                out.append({"mirror": mir, "offset": off, "treb_rank": r, "orientation": orient,
                            "WK": f"{'abcdefgh'[WK[0]]}{WK[1]}", "BK": f"{'abcdefgh'[BK[0]]}{BK[1]}",
                            "freeze_ok": ok_freeze, "legal_necessary_ok": ok_leg,
                            "white_pawn_captures": cw, "black_pawn_captures": cb,
                            "fen_w": fen_of(Wfull, Bfull, WK, BK, "w"), "reachable_positions": nreach})
    # list the task's standard embedding first (W g4 / B g5, WK f5, BK h4; component unmirrored)
    out.sort(key=lambda p: (p["treb_rank"] != 4 or p["orientation"] != "A", p["mirror"], p["offset"], p["treb_rank"], p["orientation"]))
    good = [p for p in out if p["freeze_ok"] and p["legal_necessary_ok"]]
    return {"width": width, "fits": bool(good), "n_placements": len(out), "n_freeze_ok": sum(p["freeze_ok"] for p in out),
            "n_both_ok": len(good), "placements": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="*")
    ap.add_argument("--json")
    ap.add_argument("--out")
    a = ap.parse_args()
    todo = []
    if a.json:
        with open(a.json) as fh:
            todo = [(d["position"], d["width"], d.get("label", "")) for d in json.load(fh)]
    for i in range(0, len(a.items), 2):
        todo.append((a.items[i], int(a.items[i + 1]), ""))
    res = []
    for p, w, lab in todo:
        r = placements(p, w)
        r.update({"position": p, "label": lab})
        res.append(r)
        good = [x for x in r.get("placements", []) if x["freeze_ok"] and x["legal_necessary_ok"]]
        print(f"{lab:30s} {p:34s} w{w}: fits={r['fits']} freeze-ok {r.get('n_freeze_ok', 0)}/{r.get('n_placements', 0)}"
              f" both {r.get('n_both_ok', 0)}" + (f"  e.g. {good[0]['fen_w']}" if good else ""))
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
