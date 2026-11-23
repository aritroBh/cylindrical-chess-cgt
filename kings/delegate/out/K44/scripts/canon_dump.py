#!/usr/bin/env python3
"""K44: dump the bisimulation-minimal game graph of a root (nodes numbered by breadth-first order from the root; options
listed in increasing node number; P / M = terminal won by White / Black).  usage: canon_dump.py board "cfg" "root" out.txt [region lo-hi]"""
import sys, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from lk3 import LK, quotient, parse_cfg, signatures, refsigs
board, cfg, root, outp = sys.argv[1:5]
region = None
if len(sys.argv) > 5 and sys.argv[5] != 'all':
    a, b = sys.argv[5].split('-'); region = set(range(int(a), int(b) + 1))
W, H = [int(v) for v in board.split(':')[1].split('x')]
g = LK(W, H, board.startswith('cyl'), parse_cfg(cfg), region)
cls, QL, QR = quotient(g.L, g.R)
r = [i for i in range(len(g.nodes)) if g.name(i) == root][0]
order = [cls[r]]; ix = {cls[r]: 0}
for x in order:
    for t in sorted([t for t in QL[x] + QR[x] if not isinstance(t, str)], key=lambda t: t):
        if t not in ix: ix[t] = len(order); order.append(t)
# example representative position of each class (for readability)
rep = {}
for i in range(len(g.nodes)):
    c = cls[i]
    if c in ix and c not in rep: rep[c] = g.name(i)
with open(outp, 'w') as f:
    f.write('# bisimulation-minimal graph of %s on %s (%s); %d nodes; node 0 = root; L/R = Left (White) / Right (Black) options; P/M = terminal for White/Black\n' % (root, board, cfg, len(order)))
    for c in order:
        l = ','.join(str(ix[t]) if not isinstance(t, str) else t for t in sorted(QL[c], key=lambda t: (isinstance(t, str), ix.get(t, 0) if not isinstance(t, str) else 0, str(t))))
        rr = ','.join(str(ix[t]) if not isinstance(t, str) else t for t in sorted(QR[c], key=lambda t: (isinstance(t, str), ix.get(t, 0) if not isinstance(t, str) else 0, str(t))))
        f.write('%d\tL[%s]\tR[%s]\t# %s\n' % (ix[c], l, rr, rep[c]))
print('nodes', len(order), 'edges', sum(len(QL[c]) + len(QR[c]) for c in order))
