# new (this note): how many nodes / K-captures of the reduced game of P_n split into >= 2 components (cylcgt component rule)
import sys
from eng import *
from red import build
def ngroups(pos):
    n = len(pos); occ = [1 if (w or b) else 0 for w, b in pos]
    if all(occ): return 1
    # number of maximal cyclic runs of occupied files
    return sum(1 for f in range(n) if occ[f] and not occ[(f - 1) % n])
for n in map(int, sys.argv[1:]):
    pos0 = ring('P', n)
    ids, order, info = build(pos0)
    multi = sum(1 for (p, e) in order if ngroups(p) > 1)
    emp = sum(1 for (p, e) in order if not all((w or b) for w, b in p))
    kcap = ksplit = ktot = 0
    for nd in order:
        p, e = nd
        for s in 'WB':
            for (q, qe) in info[nd][s][1]:
                ktot += 1
                if npawns(q) < npawns(p):
                    kcap += 1
                    if ngroups(q) > 1: ksplit += 1
    print('P', n, 'nodes', len(order), 'nodes with an empty file', emp, 'nodes that split into >=2 components', multi,
          'K-edges', ktot, 'K-captures', kcap, 'of which split', ksplit)
