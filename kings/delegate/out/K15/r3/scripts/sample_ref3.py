#!/usr/bin/env python3
"""K15 r3: draw a seeded random sample of lines from confirmation inputs (cf/*.in) and split it into chunks of 25 lines.
usage: sample_ref3.py TAG BOARD N SEED  -> r3/xs/TAG.chunkNN.in  (positions) and r3/xs/TAG.sample.txt (line numbers)"""
import sys, random, os
tag, board, n, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FIN2 = os.path.join(os.path.dirname(R3), 'fin2')
lines = [l.rstrip('\n') for l in open(os.path.join(FIN2, 'cf', tag + '.in')) if l.strip()]
idx = sorted(random.Random(seed).sample(range(len(lines)), min(n, len(lines))))
open(os.path.join(R3, 'xs', tag + '.sample.txt'), 'w').write('\n'.join(str(i) for i in idx) + '\n')
for c in range(0, len(idx), 25):
    open(os.path.join(R3, 'xs', '%s.chunk%02d.in' % (tag, c // 25)), 'w').write('\n'.join(lines[i] for i in idx[c:c + 25]) + '\n')
print(tag, len(idx), 'lines in', (len(idx) + 24) // 25, 'chunks')
