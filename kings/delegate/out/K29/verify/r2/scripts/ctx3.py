#!/usr/bin/env python3
# ctx3.py FILES LO HI MAXW MAXB TOTAL [SAMPLE SEED] : contexts (one per line, tokens) with <=MAXW white, <=MAXB black pawns on FILES x ranks LO..HI, exactly TOTAL pawns; optional random sample
import sys, itertools, random
files, lo, hi, mw, mb, tot = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
sq = [f + str(r) for f in files for r in range(lo, hi + 1)]
out = []
for a in range(mw + 1):
    b = tot - a
    if b < 0 or b > mb: continue
    for Wp in itertools.combinations(sq, a):
        rest = [s for s in sq if s not in Wp]
        for Bp in itertools.combinations(rest, b):
            out.append(' '.join(['P' + s for s in Wp] + ['p' + s for s in Bp]))
if len(sys.argv) > 7:
    random.seed(int(sys.argv[8])); out = sorted(random.sample(out, min(int(sys.argv[7]), len(out))))
print('\n'.join(out))
sys.stderr.write('%d contexts\n' % len(out))
