"""cyl_compare.py FAM m -- reduced graph of FAM(m) on the strip and on the cylinder (same chart, twist off):
are the node sets, K-children and T-counts identical?"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
sys.setrecursionlimit(1000000)
import rgraph
from fgame import FBoard
rgraph.Board = FBoard
from rgraph import reduced, stats
FAM = {'TT': lambda m: 'B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2' + ' B4 W2' * m}
fam, m = sys.argv[1], int(sys.argv[2])
_, rs, ns = reduced(FAM[fam](m), True); _, rc, nc = reduced(FAM[fam](m), False)
print('%s(%d) strip %s' % (fam, m, stats(ns, rs))); print('%s(%d) cyl   %s' % (fam, m, stats(nc, rc)))
same = set(ns) == set(nc)
diff = sum(1 for p in ns if p in nc and [(i[0], sorted(i[3])) for i in ns[p]] != [(i[0], sorted(i[3])) for i in nc[p]])
print('same node set: %s; nodes with different T-count or K-children: %d' % (same, diff))
