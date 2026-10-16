"""Enumerate small pawn positions and tabulate which CGT values occur.

  .venv/bin/python -m cylcgt.explore --files 3 --white 2 --black 2
"""
import argparse
import itertools
import time
from collections import Counter

from . import cgt, pawns
from .pawns import Board, Pos, RaceError, passed, value


def has_big(g, seen=None):
    seen = seen if seen is not None else set()
    if g.id in seen:
        return False
    seen.add(g.id)
    if g.num is not None:
        return abs(g.num) >= pawns.BIG // 2
    return any(has_big(x, seen) for x in g.L + g.R)


def enumerate_values(board: Board, nw: int, nb: int, ring_only=False):
    sqs = [(f, r) for f in range(board.files) for r in range(2, board.ranks)]
    vals = Counter()
    examples = {}
    for W in itertools.combinations(sqs, nw):
        rest = [s for s in sqs if s not in W]
        for B in itertools.combinations(rest, nb):
            pos = Pos(frozenset(W), frozenset(B))
            if passed(board, pos, "W") or passed(board, pos, "B"):
                continue
            if ring_only and not pawns.is_ring(board, pos):
                continue
            try:
                g = value(board, pos)
            except RaceError:
                continue
            if has_big(g):
                key = "(involves passed-pawn threats)"
            else:
                key = cgt.show(g)
            vals[key] += 1
            examples.setdefault(key, str(pos))
    return vals, examples


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", type=int, default=3)
    ap.add_argument("--ranks", type=int, default=8)
    ap.add_argument("--white", type=int, default=2)
    ap.add_argument("--black", type=int, default=2)
    ap.add_argument("--ring-only", action="store_true")
    ap.add_argument("--no-ep", action="store_true")
    a = ap.parse_args()
    for wrap in (True, False):
        b = Board(a.files, a.ranks, wrap, not a.no_ep)
        t = time.time()
        vals, ex = enumerate_values(b, a.white, a.black, ring_only=a.ring_only and wrap)
        print(f"\n## {a.files}x{a.ranks} {'cylinder' if wrap else 'flat'}  {a.white}W+{a.black}B  "
              f"({sum(vals.values())} positions, {len(vals)} distinct values, {time.time()-t:.1f}s)")
        for k, c in sorted(vals.items(), key=lambda kv: -kv[1]):
            print(f"  {c:7d}  {k:40s} e.g. {ex[k]}")
