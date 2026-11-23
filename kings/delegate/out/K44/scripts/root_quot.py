import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lk3 import *
board, cfg, root = sys.argv[1], sys.argv[2], sys.argv[3]
region = None
if len(sys.argv) > 4 and sys.argv[4] != 'all':
    a, b = sys.argv[4].split('-'); region = set(range(int(a), int(b) + 1))
wrap = board.startswith('cyl'); W, H = [int(v) for v in board.split(':')[1].split('x')]
g = LK(W, H, wrap, parse_cfg(cfg), region)
rid = [i for i in range(len(g.nodes)) if g.name(i) == root]
assert len(rid) == 1, root
r = rid[0]
seen = {r}; st = [r]
while st:
    x = st.pop()
    for t in g.L[x] + g.R[x]:
        if not isinstance(t, str) and t not in seen: seen.add(t); st.append(t)
print('reachable nodes', len(seen), 'of', len(g.nodes))
cls, QL, QR = quotient(g.L, g.R)
rc = cls[r]
sc = {rc}; st = [rc]
while st:
    x = st.pop()
    for t in QL[x] + QR[x]:
        if not isinstance(t, str) and t not in sc: sc.add(t); st.append(t)
print('quotient classes total', len(QL), 'reachable from root', len(sc))
