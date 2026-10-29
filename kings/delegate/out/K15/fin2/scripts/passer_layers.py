#!/usr/bin/env python3
"""K15 fin2: cross-check of the root-passer filter of grp.c (compiled C) against cylcgt.pawns.passed: count the pawn layers
(all placements of <= wmax White and <= bmax Black pawns on the files a..F, ranks 2..H-1, at least one pawn) in which
cylcgt.passed holds for either side, and compare with `skipped_passer_layers` printed by grp (strict variant)."""
import sys, json, itertools
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import pawns as P
def count(Wd, H, F, wm, bm, flat):
    bd = P.Board(Wd, H, not flat, True)
    sq = [(f, r) for f in range(F) for r in range(2, H)]
    skipped = total = 0
    for i in range(wm + 1):
        for wset in itertools.combinations(sq, i):
            rest = [s for s in sq if s not in wset]
            for j in range(bm + 1):
                if i + j == 0: continue
                for bset in itertools.combinations(rest, j):
                    total += 1
                    pos = P.Pos(frozenset(wset), frozenset(bset), None)
                    if P.passed(bd, pos, 'W') or P.passed(bd, pos, 'B'): skipped += 1
    return total, skipped
def grp_skipped(fn, variant):
    t = open(fn).read(); dec = json.JSONDecoder(); i = 0
    while i < len(t):
        while i < len(t) and t[i].isspace(): i += 1
        if i >= len(t): break
        o, i = dec.raw_decode(t, i)
        if o['variant'] == variant: return o['skipped_passer_layers']
for (Wd, H, F, wm, bm, flat, fn) in ((7, 6, 3, 2, 2, True, 'runs/flat76_np.json'), (8, 6, 3, 3, 3, False, 'runs/npB_8x6_f3_33.json'), (8, 6, 4, 3, 2, False, 'runs/npB_8x6_f4_32.json')):
    tot, sk = count(Wd, H, F, wm, bm, flat)
    print('%s %dx%d F=%d <=%d+%d: layers %d, cylcgt passer layers %d, grp.c skipped_passer_layers %s' % ('flat' if flat else 'cyl', Wd, H, F, wm, bm, tot, sk, grp_skipped(fn, 'strict')))
