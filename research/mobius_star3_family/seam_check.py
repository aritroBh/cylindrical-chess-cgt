"""seam_check.py FAM m c -- seam facts for PROOF.md section 2, on the reduced strip graph R_m of FAM (TT or SS).
Per node: arc c-4..c+5 equal to the start (pattern files); file 0 / file n-1 changed or not.
Over all nodes and both sides: classes of moves of the pawns on files n-1 and 0, and of every move whose
capture crosses the seam (file n-1 <-> file 0, ordinary or e.p.); K-moves that touch the arc."""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
sys.setrecursionlimit(1000000)
import rgraph
from fgame import FBoard
rgraph.Board = FBoard
from rgraph import reduced
from fverify_lib import *  # noqa (sets rgraph.Board)
FAM = {'TT': lambda m: 'B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2' + ' B4 W2' * m,
       'SS': lambda m: 'B6 W3' + ' W2 B4' * m + ' W6B7 W3 B7 B6 W3 W2 B6 W2 B4'}
def cls(B, ch, side):
    c = B.classify(ch, side)
    if c > 0: return 'T'
    if c < 0: return 'L'
    return 'P' if any(B.classify(g, 1 - side) > 0 for _, g in B.moves(ch, 1 - side)) else 'K'
fam, m, c = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
B, root, nodes = reduced(FAM[fam](m)); n = len(root[0]); arc = range(c - 4, c + 6)
print('%s(%d) n=%d nodes=%d cut=%d arc=%d..%d' % (fam, m, n, len(nodes), c, c - 4, c + 5))
bad_arc = sum(1 for p in nodes if any(p[0][f] != root[0][f] for f in arc) or p[1] is not None)
ch0 = sum(1 for p in nodes if p[0][0] != root[0][0]); chl = sum(1 for p in nodes if p[0][n - 1] != root[0][n - 1])
print('nodes with arc != start or with a flag: %d' % bad_arc)
print('nodes with file 0 != start: %d ; with file n-1 = %d != start: %d' % (ch0, n - 1, chl))
own = collections.Counter(); seam = collections.Counter(); karc = 0
for p in nodes:
    for side in (0, 1):
        for d, ch in B.moves(p, side):
            f0, r0, k, f1, r1 = d; x = cls(B, ch, side)
            if f0 in (0, n - 1): own[(f0, k, x)] += 1
            if k in 'xe' and {f0, f1} == {0, n - 1}: seam[(f0, f1, k, x)] += 1
            if x == 'K' and (f0 in arc or f1 in arc): karc += 1
print('moves of pawns on files 0 and n-1 (file, kind s/d/x/e, class): count')
for k in sorted(own): print('  ', k, own[k])
print('captures across the seam (from, to, kind, class): count  [none listed = none exist]')
for k in sorted(seam): print('  ', k, seam[k])
print('K-moves touching the arc: %d' % karc)
