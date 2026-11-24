"""K57 referee: compare vgsum's r(H10 (+) T) with r(over_D (+) T) (toyref.over_vals). usage: cmp_h10.py T_FILE SUM_LOG"""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from toyref import over_vals, WT, BT  # noqa: E402

Ts = {}
for line in open(sys.argv[1]):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    name, k, body = line.split('|')
    k = int(k)
    L, R = [], []
    for part in body.split(';')[:k]:
        a, b = part.split('/')
        conv = lambda x: [WT if t == 'W' else BT if t == 'B' else int(t) for t in x.split(',') if t]  # noqa: E731
        L.append(conv(a))
        R.append(conv(b))
    Ts[name] = (L, R)
ov = {n: over_vals(T) for n, T in Ts.items()}
nres = ndiff = nterm = 0
for line in open(sys.argv[2]):
    if not line.startswith('SUM '):
        continue
    _, name, lab, side, vals = line.split()
    side = int(side)
    if '_q_' in lab:
        o = 1
    elif lab in ('rootA_w', 'rootA_b', 'rootB_w', 'rootB_b'):
        o = 0
    else:
        continue
    T = Ts[name]
    term = any(x in (WT, BT) for side_l in T for opts in side_l for x in opts)
    for t, v in enumerate(vals):
        nres += 1
        nterm += term
        if v != ov[name][(o, t, side)]:
            ndiff += 1
            print('DIFF', name, lab, t, side, 'H10', v, 'over', ov[name][(o, t, side)])
print(f'{nres} results compared ({nterm} beside T with terminals), {ndiff} differ from over')
