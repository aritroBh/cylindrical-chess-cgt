"""K55 part 2, fourth battery: D-game candidates with a decisive Black threat, tD = {0 || 0 | ⊖} (root A) and
uD = {0 | tD} (root B), their negatives -tD = {{⊕ | 0} | 0}, -uD = {-tD | 0} (for the order tests) and a few sums.
Terminals are written W (White has won) and B (Black has won).  usage: python3 gen55d.py > ../tests55d.txt"""
from games55 import G, line
def dsum(a, b):   # sum of two D-games; terminal options are kept as they are
    (La, Ra), (Lb, Rb) = a, b; nb = len(Lb); idx = lambda i, j: i * nb + j
    L = [[] for _ in range(len(La) * nb)]; R = [[] for _ in range(len(La) * nb)]
    for i in range(len(La)):
        for j in range(nb):
            for (X, Y, out) in ((La, Lb, L), (Ra, Rb, R)):
                out[idx(i, j)] += [idx(x, j) if x >= 0 else x for x in X[i]] + [idx(i, y) if y >= 0 else y for y in Y[j]]
    return (L, R)
def dneg(g): return ([[(-1 if x == -2 else -2 if x == -1 else x) for x in r] for r in g[1]], [[(-1 if x == -2 else -2 if x == -1 else x) for x in l] for l in g[0]])
tD = ([[1], [], [1]], [[2], [], [-2]])
uD = ([[1], [], [1], [1]], [[3], [], [-2], [2]])
out = [('tD', tD), ('uD', uD), ('negtD', dneg(tD)), ('neguD', dneg(uD)), ('negtD+neguD', dsum(dneg(tD), dneg(uD))),
       ('tD+neguD', dsum(tD, dneg(uD))), ('uD+negtD', dsum(uD, dneg(tD)))]
for a in ('*', 'up', 'down', 'tiny2', 'miny2', 'over', 'under'):
    out.append(('negtD+%s' % a, dsum(dneg(tD), G[a]))); out.append(('neguD+%s' % a, dsum(dneg(uD), G[a])))
for name, g in out: print(line(name, g))
