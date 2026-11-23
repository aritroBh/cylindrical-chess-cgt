import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lk3 import *
board, cfg, root = sys.argv[1], sys.argv[2], sys.argv[3]
wrap = board.startswith('cyl'); W, H = [int(v) for v in board.split(':')[1].split('x')]
g = LK(W, H, wrap, parse_cfg(cfg), None)
cls, QL, QR = quotient(g.L, g.R)
names, sig = signatures(QL, QR)
rn, refs = refsigs()
def nm(i):
    s = sig[cls[i]]; return '='.join(refs[s]) if s in refs else 'unnamed'
byname = {g.name(i): i for i in range(len(g.nodes))}
r = byname[root]
print('ROOT', root, nm(r))
for c, lst in (('Left', g.L[r]), ('Right', g.R[r])):
    for t in lst:
        print(' ', c, '->', t if isinstance(t, str) else g.name(t) + '  ' + nm(t))
