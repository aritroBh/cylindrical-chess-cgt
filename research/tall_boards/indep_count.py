#!/usr/bin/env python3
"""Independent root counter (brute force over labelled placements, orbit counting by canonical minimum; no shared code with tw.c).
Class: W pawns on ranks 2..R-2, B pawns on ranks 3..R-1, distinct squares, every file occupied, no passed pawn (W/B), orbits under
mirror (flat) / rotations+reflections (cylinder); colour reversal (ranks flipped, colours swapped) identified when nw == nb.
usage: indep_count.py F wrap R nw nb"""
import sys, itertools
F, wrap, R, nw, nb = map(int, sys.argv[1:6])
WS = [(f, r) for f in range(F) for r in range(2, R - 1)]; BS = [(f, r) for f in range(F) for r in range(3, R)]
def nbrs(f): return [(f + d) % F for d in (-1, 0, 1)] if wrap else [g for g in (f - 1, f, f + 1) if 0 <= g < F]
def ok(W, B):
    if len({f for f, _ in W} | {f for f, _ in B}) < F: return False
    for f, r in W:
        if not any(g in nbrs(f) and s > r for g, s in B): return False
    for f, r in B:
        if not any(g in nbrs(f) and s < r for g, s in W): return False
    return True
def images(W, B):
    maps = [lambda f: f, lambda f: F - 1 - f] if not wrap else [(lambda f, s=s, m=m: (m * f + s) % F) for s in range(F) for m in (1, -1)]
    for m in maps:
        yield frozenset((m(f), r) for f, r in W), frozenset((m(f), r) for f, r in B)
        if nw == nb:
            yield frozenset((m(f), R + 1 - r) for f, r in B), frozenset((m(f), R + 1 - r) for f, r in W)
seen = set(); n = 0
for W in itertools.combinations(WS, nw):
    for B in itertools.combinations(BS, nb):
        if set(W) & set(B) or not ok(W, B): continue
        key = min((tuple(sorted(a)), tuple(sorted(b))) for a, b in images(W, B))
        if key not in seen: seen.add(key); n += 1
print(f"indep F={F} wrap={wrap} R={R} split={nw}+{nb} roots={n}")
