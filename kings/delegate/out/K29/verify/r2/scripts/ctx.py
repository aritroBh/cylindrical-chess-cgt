#!/usr/bin/env python3
# referee-2 own context generator: ctx.py "<group tokens or empty>" FILES MAXW MAXB LO HI -> one position per line, both stm, e.p. '-'
# contexts = sets of white pawns (<=MAXW) and black pawns (<=MAXB) on distinct squares of FILES x ranks LO..HI
import sys, itertools
z, files, mw, mb, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
sq = [f + str(r) for f in files for r in range(lo, hi + 1)]
n = 0
for a in range(mw + 1):
  for Wp in itertools.combinations(sq, a):
    for b in range(mb + 1):
      for Bp in itertools.combinations(sq, b):
        if set(Wp) & set(Bp): continue
        toks = ([z] if z else []) + ['P' + s for s in Wp] + ['p' + s for s in Bp]
        for stm in 'wb': print(' '.join(toks + [stm, '-']))
        n += 1
sys.stderr.write('%d contexts\n' % n)
