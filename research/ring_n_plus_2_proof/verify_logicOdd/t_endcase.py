"""H3 end case: in the nodes of R_19 / Qo_19, the moves of the W2 pawn on file 10 (right end of the arc): which move is L, and why."""
import sys
from collections import Counter
from common import *
fam = sys.argv[1]; n = 19
start = parse(TOKS[fam](n)); order, edges = build(start)
c = Counter(); why = Counter()
for nd in order:
    pos, ep = nd
    for npos, nep, src, kd in moves(pos, ep, 'W'):
        if src != 10: continue
        st = status(npos, nep, 'W')
        k = 'L' if st == 'B' else ('T' if st == 'W' else 'nonterm')
        c[(kd, k)] += 1
        if k == 'L':
            # who has the passer and where
            bp = passed_list(npos, nep, 'B')
            why[(tuple(bp), 'file12 has white pawn at rank<4: %s' % any(r < 4 for r in pos[12][0]), 'file12 white=%s' % (pos[12][0],))] += 1
print(fam, dict(c))
print(' passers of Black after the L move, and file-12 content:', dict(why))
