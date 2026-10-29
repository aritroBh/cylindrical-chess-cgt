#!/usr/bin/env python3
# own context generator (referee K29): own_ctx.py "<group tokens>" FILES MAXW MAXB LO HI  -> positions, both stm, one per line
import sys, itertools
z, files, mw, mb, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
sq = [f + str(r) for f in files for r in range(lo, hi + 1)]
def subsets(k):
    for c in range(k + 1):
        yield from itertools.combinations(sq, c)
n = 0
for Wp in subsets(mw):
    for Bp in subsets(mb):
        if set(Wp) & set(Bp): continue
        toks = [z] + ['P' + s for s in Wp] + ['p' + s for s in Bp]
        for stm in 'wb': print(' '.join(toks + [stm, '-']))
        n += 1
sys.stderr.write('%d contexts\n' % n)
