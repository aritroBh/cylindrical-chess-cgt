#!/usr/bin/env python3
"""mkR.py NAME SCREENFILE_OR_A [B] -> data/R_NAME.txt: one R line per class representative: failing groups from phase A or B (first failing context),
survivors from B (or from A if phase A already covered all contexts).  Order of the rep file."""
import sys, re
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/'
name = sys.argv[1]; files = sys.argv[2:]
res = {}
for fn in files:
    for l in open(D + fn):
        m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+)', l)
        if not m: continue
        z = m.group(1)
        if z in res and res[z][1] > 0: continue       # a recorded failure stays
        res[z] = (l.rstrip('\n'), int(m.group(3)))
with open(D + 'R_%s.txt' % name, 'w') as f:
    for z, (l, d) in res.items(): f.write(l + '\n')
print(name, len(res), 'groups,', sum(1 for v in res.values() if v[1] > 0), 'fail,', sum(1 for v in res.values() if v[1] == 0), 'survive')
