#!/usr/bin/env python3
"""sums_span9.py -- the two-component sums with at most 8 pawns that the C scanner (boards of width <= 8) cannot hold.

Two components with p1 + p2 <= 8 pawns, placed with a single-file gap, span w1 + w2 + 1 files (w_i <= p_i).  Span >= 9 forces
p1 + p2 = 8 and w_i = p_i, i.e. both components have exactly one pawn per file:  (p1,p2) = (4,4), (3,5), (2,6).
(All sums with three or more components and <= 8 pawns, and the pairs (2,2) ... (2,5), were done by sums_le8.py; pairs with
span <= 8 are inside the C scan of widths <= 8.)
Method: every one-pawn-per-file component with 2..6 pawns and no passed pawn is valued with cylcgt (default setting); games are
canonical and interned, so G1 + G2 = *3  <=>  G2 is the object  *3 - G1: one subtraction per G1 and a set lookup.
"""
import itertools, os, sys, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt

pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
T0 = time.time()


def one_per_file(p):
    """dict Game -> example position text, over all colourings/ranks with one pawn on each of p files"""
    bd = pawns.Board(p, 8, False, True)
    vals = {}
    n = 0
    for colours in itertools.product((0, 1), repeat=p):
        if all(colours) or not any(colours):
            continue
        rank_choices = [range(2, 7) if c == 0 else range(3, 8) for c in colours]
        for ranks in itertools.product(*rank_choices):
            w = frozenset((f, r) for f, (c, r) in enumerate(zip(colours, ranks)) if c == 0)
            b = frozenset((f, r) for f, (c, r) in enumerate(zip(colours, ranks)) if c == 1)
            pos = pawns.Pos(w, b)
            if pawns.passed(bd, pos, "W") or pawns.passed(bd, pos, "B"):
                continue
            n += 1
            vals.setdefault(pawns._value(bd, pos), str(pos))
    print(f"p={p}: {n} one-pawn-per-file components without passed pawns, {len(vals)} distinct values ({time.time()-T0:.0f}s)", flush=True)
    return vals


def main():
    V = {p: one_per_file(p) for p in range(2, 7)}
    star3 = cgt.nimber(3)
    total_found = 0
    for p1, p2 in ((4, 4), (3, 5), (2, 6)):
        found = []
        for g1, ex1 in V[p1].items():
            target = cgt.add(star3, cgt.neg(g1))
            if target in V[p2]:
                found.append((ex1, V[p2][target]))
        print(f"sizes ({p1},{p2}): {len(V[p1])} x {len(V[p2])} value pairs; sums equal to *3: {len(found)}", flush=True)
        for f in found[:10]:
            print("  FOUND", f)
        total_found += len(found)
    print(f"TOTAL sums equal to *3: {total_found}  ({time.time()-T0:.0f}s)")


if __name__ == "__main__":
    main()
