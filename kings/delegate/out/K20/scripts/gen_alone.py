#!/usr/bin/env python3
"""Bridge D -> P: for every root of the named value classes in faithful configs, write kp_p positions (both sides
to move) and the D-model prediction (the 'alone' entry of the battery signature)."""
import sys, os, re, gzip
sys.path.insert(0, os.path.dirname(__file__))
from classes import parse, order
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
board = sys.argv[1]; classes = set(sys.argv[2].split(';')); out = sys.argv[3]
n = board.replace(':', '_')
lg = D + '/logs/%s_free.log' % n
faith = {}
for l in open(lg):
    m = re.match(r'CONFIG (.*?) : nodes (\d+)  faithful (\d)', l)
    if m: faith[m.group(1).strip()] = int(m.group(3))
rf = D + '/logs/roots_%s.txt' % n
op = open(rf) if os.path.exists(rf) else gzip.open(rf + '.gz', 'rt')
k = 0
with open(out + '.pos', 'w') as fp, open(out + '.pred', 'w') as fq:
    for l in op:
        cn, pos, nm, sh, sig = parse(l)
        if nm not in classes or not faith.get(cn.strip(), 0): continue
        # order pawns: kpsolve wants any order
        for s, ch in (('w', 'W'), ('b', 'B')):
            r = 'WDL'[int(sig[0 if s == 'w' else 1])]
            fp.write('%s %s -\n' % (pos, s))
            fq.write('%s %s - | %s | %s | %s\n' % (pos, s, nm, cn.strip(), r))
        k += 1
print(board, 'roots', k)
