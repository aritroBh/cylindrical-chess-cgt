import collections
from engine import *
n = 18
start = parse(P_toks(n)); order, edges = build(start)
kk = collections.Counter(); flagmoves = collections.Counter()
for nd in order:
    for side in 'WB':
        for c, npos, nep, src, kind, pr in classify(nd[0], nd[1], side):
            kk[(c, kind)] += 1
            if nep is not None: flagmoves[c] += 1
print('class x kind over all moves from nodes of R_18:'); 
for k, v in sorted(kk.items()): print('  ', k, v)
print('moves that create an e.p. flag, by class:', dict(flagmoves))
