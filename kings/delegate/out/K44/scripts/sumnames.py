#!/usr/bin/env python3
"""K44: name unclassified B34 signatures as sums of named battery games (independent of kg44/lk: uses lk3.py)."""
import sys, itertools, collections, json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from lk3 import battery, dsum, signatures, refsigs
C = battery(); names = list(C)
def sumgame(games):
    """D-sum of several small games (each (L, R) option lists); terminals P/M kept."""
    dims = [len(g[0]) for g in games]
    idx = list(itertools.product(*[range(d) for d in dims]))
    pos = {t: i for i, t in enumerate(idx)}
    L = [[] for _ in idx]; R = [[] for _ in idx]
    for t in idx:
        i = pos[t]
        for c, out in ((0, L[i]), (1, R[i])):
            for j, g in enumerate(games):
                for o in g[c][t[j]]:
                    if isinstance(o, str): out.append(o)
                    else:
                        u = list(t); u[j] = o; out.append(pos[tuple(u)])
    return L, R
def sig_of(games):
    L, R = sumgame(games)
    _, sig = signatures(L, R)
    return sig[0]
if __name__ == '__main__':
    kmax = int(sys.argv[1])
    skip = {'0'}
    pool = [n for n in names if n != '0']
    found = {}
    for k in range(1, kmax + 1):
        for combo in itertools.combinations_with_replacement(pool, k):
            s = sig_of([C[n] for n in combo])
            found.setdefault(s, ' + '.join(combo))
        print('k', k, 'distinct sum signatures', len(found), flush=True)
    json.dump(found, open(D + '/logs/sum_names_k%d.json' % kmax, 'w'))
