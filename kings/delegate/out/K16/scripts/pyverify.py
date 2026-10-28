#!/usr/bin/env python3
"""pyverify.py BOARD VIOLFILE [LIMIT]: re-solve each violating position with the independent pure-Python P solver pyp.py
(and classify the failure of the strategy), print a summary."""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts')
import pyp, classify
from collections import Counter
spec, vf = sys.argv[1:3]
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
B = pyp.Board(spec)
c = Counter(); k = Counter(); n = 0; mism = 0
for l in open(vf):
    if n >= lim: break
    l = l.rstrip('\n')
    if l.startswith('shard') or l.startswith('seed'): l = l.split(': ', 1)[1]
    pos, res, certs = l.split(' | ')
    A = res.split()[0]
    v = pyp.solve(B, pyp.parse(B, pos))
    n += 1
    c[v] += 1
    if v != A: mism += 1; print("MISMATCH", l, v)
    for t in certs.split():
        b, p, _ = t.split(':')
        kind = classify.classify(spec, pos, 0 if b == 'W' else 1, p)[0]
        k[kind] += 1
print(spec, vf, "positions", n, "pyp values", dict(c), "disagreements with kp_p", mism, "strategy failure kinds", dict(k))
