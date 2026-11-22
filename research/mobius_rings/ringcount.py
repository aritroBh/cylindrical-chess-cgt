#!/usr/bin/env python3
"""Independent count of Moebius root rings (task 3 check of mring.h): brute force over ALL placements of P pawns on
ranks 2..7 (no rank pre-filter), a pawn on every file, no passed pawn (cover-coordinate test), then orbits under
{id, mirror, kappa, mirror*kappa}.  usage: ringcount.py N P"""
import sys, itertools
n, P = int(sys.argv[1]), int(sys.argv[2])
sq = [(f, r, c) for f in range(n) for r in range(2, 8) for c in (0, 1)]
def has_passed(pawns):
    cov = []
    for (f, r, c) in pawns:
        d = 1 if c == 0 else -1
        cov.append((f, r, c, d)); cov.append((f + n, 9 - r, c, -d))
    L = 2 * n
    for (f, r, c) in pawns:
        d = 1 if c == 0 else -1; blocked = False
        for (g, s, c2, d2) in cov:
            if c2 != c and (g - f) % L in (0, 1, L - 1) and (s - r) * d > 0: blocked = True; break
        if not blocked: return True
    return False
def img(P, mir, kap):
    out = set()
    for (f, r, c) in P:
        if mir: f = n - 1 - f
        if kap: r, c = 9 - r, 1 - c
        out.add((f, r, c))
    return frozenset(out)
def key(P): return tuple(sorted(P))
seen = set(); nlab = 0
for comb in itertools.combinations(sq, P):
    if len({(f, r) for f, r, c in comb}) < P: continue
    if len({f for f, r, c in comb}) < n: continue
    if has_passed(comb): continue
    nlab += 1
    k = min(key(img(comb, m, kp)) for m in (0, 1) for kp in (0, 1))
    seen.add(k)
print("n=%d P=%d labelled_rings=%d orbits=%d" % (n, P, nlab, len(seen)))
