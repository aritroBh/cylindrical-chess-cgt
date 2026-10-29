#!/usr/bin/env python3
"""K26 audit: candidate counts from a from-scratch enumerator (no solver, no K26 library).
t2 = both kings on an adjacent pair of F_Z squares, K1 (no pair square attacked by an enemy pawn of the group, none occupied),
K2 (every White-pair square at king distance >= 2 from every Black-pair square).
t1 = White on an adjacent pair, Black king on one single square (K1, K2 against both pair squares).
usage: count_cands.py H nW nB   (files a-c; ranks 1..H; pawns on ranks 2..H-1)"""
import sys, itertools
H, nW, nB = map(int, sys.argv[1:4])
S = [(f, r) for f in range(3) for r in range(1, H + 1)]
P = [s for s in S if 2 <= s[1] <= H - 1]
dist = lambda a, b: max(abs(a[0]-b[0]), abs(a[1]-b[1]))
pairs = [(a, b) for i, a in enumerate(S) for b in S[i+1:] if dist(a, b) == 1]
def att(color, p):   # squares of F_Z attacked by a pawn of the colour
    d = 1 if color == 'w' else -1
    return {(p[0]+df, p[1]+d) for df in (-1, 1) if 0 <= p[0]+df <= 2 and 1 <= p[1]+d <= H}
cfgs = 0; t2 = 0; t1 = 0
for kw in range(nW + 1):
  for wp in itertools.combinations(P, kw):
    for kb in range(nB + 1):
      for bp in itertools.combinations(P, kb):
        if set(wp) & set(bp): continue
        cfgs += 1
        occ = set(wp) | set(bp)
        wa = set().union(*[att('w', p) for p in wp]) if wp else set()
        ba = set().union(*[att('b', p) for p in bp]) if bp else set()
        wok = [pr for pr in pairs if not (set(pr) & (occ | ba))]
        bok = [pr for pr in pairs if not (set(pr) & (occ | wa))]
        bsq = [s for s in S if s not in occ and s not in wa]
        for z in wok:
            for w in bok:
                if all(dist(x, y) >= 2 for x in z for y in w): t2 += 1
            for s in bsq:
                if all(dist(x, s) >= 2 for x in z): t1 += 1
print('H', H, 'limits', nW, nB, 'configs', cfgs, 't2', t2, 't1', t1)
