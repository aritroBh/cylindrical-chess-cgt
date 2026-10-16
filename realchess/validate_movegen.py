"""Validate realchess.movegen against the Lichess tablebase "moves" lists.

Builds a deterministic, stratified set of <= 7-man positions (hand-made edge
cases plus seeded random positions: en passant, promotions, checks, double
checks, pins, stalemates, checkmates, general), probes each one through
realchess.probe (cache first), and compares the set of UCI moves.

    PYTHONPATH=. .venv/bin/python -m realchess.validate_movegen --cap 1200 \
        --ledger realchess/logs/ledger.jsonl --out realchess/results/movegen_validation.json

--list-only prints the positions without probing.
"""
from __future__ import annotations

import argparse
import json
import random

from . import movegen as mg
from .probe import Prober, CapReached, DEFAULT_LEDGER

HAND = [
    # (label, FEN)
    ("ep horizontal pin: bxc6 e.p. illegal", "8/8/8/KPp4r/8/8/8/7k w - c6 0 1"),
    ("ep horizontal pin, black side", "7K/8/8/8/R2Pp2k/8/8/8 b - d3 0 1"),
    ("ep diagonal pin along capture line (legal)", "8/8/8/1k6/2pP4/8/8/3K1B2 b - d3 0 1"),
    ("ep with capturer pinned off the capture line (illegal)", "8/8/4k3/8/2pP4/8/B7/3K4 b - d3 0 1"),
    ("ep captures the checking pawn", "8/8/8/2Pp4/4K3/8/8/k7 w - d6 0 1"),
    ("ep two capturers", "4k3/8/8/2PpP3/8/8/8/4K3 w - d6 0 1"),
    ("ep illegal: double step discovered a bishop check", "2b1k3/8/8/2Pp4/8/7K/8/8 w - d6 0 1"),
    ("ep, king may also capture the pushed pawn", "8/8/8/2Pp4/3K4/8/8/k7 w - d6 0 1"),
    ("promotion with captures both sides", "r1r4k/1P6/8/8/8/8/8/7K w - - 0 1"),
    ("black promotion with capture", "7k/8/8/8/8/8/1p6/R1R1K3 b - - 0 1"),
    ("promotion blocked, capture only", "rn5k/P7/8/8/8/8/8/K7 w - - 0 1"),
    ("promotion out of check", "2K2r2/4P3/8/8/8/8/8/3k4 w - - 0 1"),
    ("double check: only king moves", "4k3/8/8/8/8/5n2/8/4K2r w - - 0 1"),
    ("knight check", "4k3/8/8/8/8/3n4/8/4K3 w - - 0 1"),
    ("slider check, interpose possible", "4k3/4r3/8/8/8/8/3B4/4K3 w - - 0 1"),
    ("pinned rook may slide along pin", "4k3/4r3/8/8/8/8/4R3/4K3 w - - 0 1"),
    ("pinned knight cannot move", "4k3/4r3/8/8/8/8/4N3/4K3 w - - 0 1"),
    ("pinned bishop on diagonal", "7k/8/8/8/3q4/8/1B6/K7 w - - 0 1"),
    ("pinned pawn can capture pinner", "4k3/8/8/8/8/5b2/4P3/3K4 w - - 0 1"),
    ("pinned pawn may push along file", "4k3/4r3/8/8/8/8/4P3/4K3 w - - 0 1"),
    ("stalemate K+Q", "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"),
    ("stalemate corner", "k7/8/1Q6/8/8/8/8/7K b - - 0 1"),
    ("stalemate pawn", "8/8/8/8/8/5k2/5p2/5K2 w - - 0 1"),
    ("stalemate rook pawn", "7k/7P/7K/8/8/8/8/8 b - - 0 1"),
    ("checkmate back rank", "R5k1/5ppp/8/8/8/8/8/6K1 b - - 0 1"),
    ("checkmate K+Q", "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1"),
    ("checkmate, king cannot capture defended queen", "8/8/8/8/8/2k5/2q5/2K5 w - - 0 1"),
    ("checkmate via rook x-ray behind the king", "8/8/8/8/8/4k3/8/r3K3 w - - 0 1"),
    ("underpromotion to knight gives check", "8/P1k5/K7/8/8/8/8/8 w - - 0 1"),
    ("trebuchet sample (6 men)", "8/8/8/5Kp1/6Pk/8/8/8 w - - 0 1"),
]

PIECE_POOL = "QRBNPPPP"


def _rand_pos(rng: random.Random, n_extra: int, pool=PIECE_POOL):
    b = [mg.EMPTY] * 64
    free = list(range(64))
    rng.shuffle(free)
    wk, bk = free.pop(), free.pop()
    b[wk], b[bk] = "K", "k"
    for _ in range(n_extra):
        pc = rng.choice(pool)
        pc = pc if rng.random() < 0.5 else pc.lower()
        for _ in range(20):
            s = free.pop()
            if pc in "Pp" and s // 8 in (0, 7):
                free.insert(0, s)
                continue
            b[s] = pc
            break
    stm = rng.choice([mg.WHITE, mg.BLACK])
    return mg.Position(tuple(b), stm, None, 0, 1)


def _between(a, b):
    """Squares strictly between a and b on a rank/file/diagonal (else None)."""
    fa, ra, fb, rb = a % 8, a // 8, b % 8, b // 8
    df, dr = (fb > fa) - (fb < fa), (rb > ra) - (rb < ra)
    if not (fa == fb or ra == rb or abs(fa - fb) == abs(ra - rb)):
        return None
    out, f, r = [], fa + df, ra + dr
    while (f, r) != (fb, rb):
        out.append(8 * r + f)
        f, r = f + df, r + dr
    return out


def _origins(pos, s):
    """Empty squares the piece on s could have come from in one move."""
    p = pos.board[s]
    u, out = p.upper(), []
    if u == "P":
        back = -1 if p == "P" else 1
        for df in (-1, 0, 1):
            t = mg._off(s, df, back)
            if t is not None and pos.board[t] == mg.EMPTY:
                out.append(t)
        return out
    if u == "N":
        return [t for t in mg._KN[s] if pos.board[t] == mg.EMPTY]
    if u == "K":
        return [t for t in mg._KG[s] if pos.board[t] == mg.EMPTY]
    rays = (mg._RAYS_R[s] if u in "RQ" else []) + (mg._RAYS_B[s] if u in "BQ" else [])
    for ray in rays:
        for t in ray:
            if pos.board[t] != mg.EMPTY:
                break
            out.append(t)
    return out


def _discovers(pos, slider, king, origins):
    line = _between(slider, king)
    u = pos.board[slider].upper()
    if line is None or u not in "QRB":
        return False
    straight = slider % 8 == king % 8 or slider // 8 == king // 8
    if (straight and u == "B") or (not straight and u == "R"):
        return False
    return any(o in line for o in origins)


def _ok(pos):
    """Valid AND retro-plausible checks (servers may reject impossible ones)."""
    if mg.validity_errors(pos):
        return False
    ch = mg.checkers(pos)
    k = pos.king(pos.stm)
    if len(ch) == 2:
        a, b = ch
        if not (_discovers(pos, b, k, _origins(pos, a)) or _discovers(pos, a, k, _origins(pos, b))):
            return False
    if pos.ep is not None and ch:
        pushed = pos.ep - 8 if pos.stm == mg.WHITE else pos.ep + 8
        start = pos.ep + 8 if pos.stm == mg.WHITE else pos.ep - 8
        for c in ch:
            if c != pushed and not _discovers(pos, c, k, [start]):
                return False
    return True


def _pinned(pos):
    """True if some non-king piece of the side to move is absolutely pinned."""
    if mg.in_check(pos):
        return False
    other = mg.BLACK if pos.stm == mg.WHITE else mg.WHITE
    k = pos.king(pos.stm)
    for s, p in pos.pieces(pos.stm):
        if p.upper() == "K":
            continue
        b = list(pos.board)
        b[s] = mg.EMPTY
        if mg.attacked(tuple(b), k, other):
            return True
    return False


def _ep_pos(rng):
    """Random position right after a double step, with an adjacent capturer."""
    for _ in range(10000):
        stm = rng.choice([mg.WHITE, mg.BLACK])
        f = rng.randrange(8)
        df = rng.choice([-1, 1])
        if not 0 <= f + df < 8:
            continue
        b = [mg.EMPTY] * 64
        if stm == mg.WHITE:  # black just played f7-f5
            pawn, ep, start, cap = 8 * 4 + f, 8 * 5 + f, 8 * 6 + f, 8 * 4 + f + df
            b[pawn], b[cap] = "p", "P"
        else:
            pawn, ep, start, cap = 8 * 3 + f, 8 * 2 + f, 8 * 1 + f, 8 * 3 + f + df
            b[pawn], b[cap] = "P", "p"
        used = {pawn, ep, start, cap}
        free = [s for s in range(64) if s not in used]
        rng.shuffle(free)
        b[free.pop()] = "K"
        b[free.pop()] = "k"
        for _ in range(rng.randrange(0, 4)):
            s = free.pop()
            pc = rng.choice("QRBNP")
            pc = pc if rng.random() < 0.5 else pc.lower()
            if pc in "Pp" and s // 8 in (0, 7):
                continue
            b[s] = pc
        pos = mg.Position(tuple(b), stm, ep, 0, 1)
        if _ok(pos):
            return pos
    raise RuntimeError("no ep position found")


def build(seed: int = 20261015):
    rng = random.Random(seed)
    out = [(lab, mg.normal_fen(f)) for lab, f in HAND]
    want = {"ep": 30, "check": 20, "double": 8, "pin": 18, "promo": 20,
            "stalemate": 8, "mate": 8, "general": 18}
    got = {k: 0 for k in want}
    seen = {f for _, f in out}
    tries = 0
    while any(got[k] < want[k] for k in want) and tries < 3_000_000:
        tries += 1
        if got["ep"] < want["ep"] and tries % 7 == 0:
            pos, cls = _ep_pos(rng), "ep"
        else:
            n = rng.choice([1, 2, 3, 3, 4, 4, 5, 5])
            pos = _rand_pos(rng, n)
            if not _ok(pos):
                continue
            st = mg.status(pos)
            nchk = len(mg.checkers(pos))
            if st == "stalemate":
                cls = "stalemate"
            elif st == "checkmate":
                cls = "mate"
            elif nchk == 2:
                cls = "double"
            elif nchk == 1:
                cls = "check"
            elif any(m.promo for m in mg.legal_moves(pos)):
                cls = "promo"
            elif _pinned(pos):
                cls = "pin"
            else:
                cls = "general"
        if got[cls] >= want[cls]:
            continue
        fen = mg.normal_fen(pos)
        if fen in seen or mg.parse_fen(fen).men() > 7:
            continue
        seen.add(fen)
        got[cls] += 1
        out.append((cls, fen))
    return out


def compare(fen: str, rec: dict):
    mine = mg.legal_uci(fen)
    data = rec.get("data") or {}
    theirs = {m["uci"] for m in data.get("moves", [])}
    return {"fen": fen, "http": rec.get("status"), "root_category": data.get("category"),
            "n_mine": len(mine), "n_lichess": len(theirs),
            "only_mine": sorted(mine - theirs), "only_lichess": sorted(theirs - mine),
            "match": rec.get("status") == 200 and mine == theirs,
            "my_status": mg.status(mg.parse_fen(fen)),
            "lichess_checkmate": data.get("checkmate"), "lichess_stalemate": data.get("stalemate")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, required=False, default=0)
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    ap.add_argument("--out", default="realchess/results/movegen_validation.json")
    ap.add_argument("--list-only", action="store_true")
    a = ap.parse_args()
    positions = build()
    if a.list_only:
        from collections import Counter
        print(Counter(l if l in ("ep", "check", "double", "pin", "promo", "stalemate", "mate", "general")
                      else "hand" for l, _ in positions))
        for lab, f in positions:
            print(lab, "|", f)
        return
    pr = Prober(a.cap, a.ledger, tag="movegen-validation", verbose=True)
    rows = []
    for lab, fen in positions:
        try:
            rec = pr.probe(fen)
        except CapReached as e:
            print("STOP:", e)
            break
        r = compare(fen, rec)
        r["label"] = lab
        rows.append(r)
    ok = sum(r["match"] for r in rows)
    http_ok = [r for r in rows if r["http"] == 200]
    summary = {"positions": len(rows), "http_200": len(http_ok), "exact_match": ok,
               "mismatches": [r for r in http_ok if not r["match"]],
               "http_errors": [r for r in rows if r["http"] != 200],
               "requests_this_run": pr.requests_this_process, "cache_hits": pr.hits,
               "ledger_total": pr.ledger_count()}
    with open(a.out, "w") as fh:
        json.dump({"summary": summary, "rows": rows}, fh, indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("mismatches", "http_errors")}))
    print("mismatches:", len(summary["mismatches"]), "http errors:", len(summary["http_errors"]))


if __name__ == "__main__":
    main()
