"""K55 referee: the candidate B_n = {0 | tiny-n} at the d5 root of Z_O. (1) writes rv55 tests -B_n (n = 20, 30, 40);
(2) predicts r(B_30 + T) for the games of tests55c and tests55d (K47 format, W/B terminals) and compares with the
investigator's Z_O column (za) at the d5 root."""
import sys; sys.path.insert(0, '.')
import gen_rv as g
def B(n):
    t = g.tiny(n); k = len(t[0])
    L = [[1]] + [[x + 1 for x in o] for o in t[0]]; R = [[1]] + [[x + 1 for x in o] for o in t[1]]
    return (L, R)        # node 0 = {0 | tiny-n}; node 1 = tiny-n's node 0 shifted
with open('tests_negB.tsv', 'w') as f:
    for n in (20, 30, 40):
        gm = g.neg(B(n)); cells = ['negB%d' % n, str(len(gm[0]))]
        for x in range(len(gm[0])): cells += [','.join(map(str, gm[0][x])) or '-', ','.join(map(str, gm[1][x])) or '-']
        f.write('\t'.join(cells) + '\n')
print('B20 - B20', g.res(g.add(B(20), g.neg(B(20)))), ' B30 - B30', g.res(g.add(B(30), g.neg(B(30)))))
# K47-format games with terminals: option 'W' = White has won, 'B' = Black has won
def readK47(fn):
    out = []
    for l in open(fn):
        if not l.strip() or l[0] == '#': continue
        nm, n, rest = [x.strip() for x in l.split('|', 2)]; n = int(n); L = [[] for _ in range(n)]; R = [[] for _ in range(n)]
        for part in rest.split(';'):
            i = int(part.split(':')[0]); ls = part.split('L=')[1].split()[0] if 'L=' in part and part.split('L=')[1].strip() and not part.split('L=')[1].strip().startswith('R=') else ''
            rs = part.split('R=')[1].strip() if 'R=' in part else ''
            conv = lambda s: [('W' if x == 'W' else 'B' if x == 'B' else int(x)) for x in s.split(',') if x]
            L[i] = conv(ls); R[i] = conv(rs)
        out.append((nm, (L, R)))
    return out
def add2(a, b):          # sum with terminals: a terminal option ends the game
    idx = {(0, 0): 0}; order = [(0, 0)]; L = []; R = []; i = 0
    while i < len(order):
        x, y = order[i]; i += 1; l = []; r = []
        for side, out in ((0, l), (1, r)):
            for o in a[side][x]:
                if isinstance(o, str): out.append(o); continue
                if (o, y) not in idx: idx[(o, y)] = len(order); order.append((o, y))
                out.append(idx[(o, y)])
            for o in b[side][y]:
                if isinstance(o, str): out.append(o); continue
                if (x, o) not in idx: idx[(x, o)] = len(order); order.append((x, o))
                out.append(idx[(x, o)])
        L.append(l); R.append(r)
    return (L, R)
def res2(gm):
    n = len(gm[0]); v = {}; ch = True
    while ch:
        ch = False
        for x in range(n):
            for s in (0, 1):
                if (x, s) in v: continue
                me = 1 if s == 0 else 2; opp = 3 - me; mine = 'W' if s == 0 else 'B'; rs = []
                for o in gm[s][x]:
                    if isinstance(o, str): rs.append(me if o == mine else opp)
                    else: rs.append(v.get((o, 1 - s), 0))
                if me in rs: v[(x, s)] = me; ch = True
                elif all(r == opp for r in rs): v[(x, s)] = opp; ch = True
    c = {1: 'W', 2: 'L', 0: 'D'}; return c[v.get((0, 0), 0)] + c[v.get((0, 1), 0)]
root = 'Kf5 kd5 Pb2 Pb4 Pe2 pa4 pb5 pe5'
for tf, lf in (('../tests55c.txt', '../logs/p2c_za_G8.out'), ('../tests55d.txt', '../logs/p2d_za_G8.out')):
    Z = {}
    for l in open(lf):
        t = [x.strip() for x in l.split('|')]
        if t[1] == root: Z.setdefault(t[0], {})[t[2]] = t[3][-1]
    n = d = 0
    for nm, T in readK47(tf):
        p = res2(add2(B(30), T)); z = Z[nm]['w'] + Z[nm]['b']; n += 2
        if p != z: d += sum(1 for a, b in zip(p, z) if a != b); print(tf, nm, 'B30+T', p, 'Z_O d5', z)
    print(tf, ': %d results, %d differ' % (n, d))
