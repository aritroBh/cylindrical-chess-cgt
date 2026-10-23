from engine import *
n = 18
start = parse(P_toks(n))
order, edges = build(start)
K_moves = K_distinct = T_moves = T_distinct = Tpairs = 0
L = P = 0
for nd in order:
    for side in 'WB':
        cl = classify(nd[0], nd[1], side)
        ks = [(npos, nep) for c, npos, nep, *_ in cl if c == 'K']
        ts = [(npos, nep) for c, npos, nep, *_ in cl if c == 'T']
        K_moves += len(ks); K_distinct += len(set(ks))
        T_moves += len(ts); T_distinct += len(set(ts)); Tpairs += bool(ts)
        L += sum(1 for c, *_ in cl if c == 'L'); P += sum(1 for c, *_ in cl if c == 'P')
print('n=18 K moves', K_moves, 'distinct', K_distinct, '| T moves', T_moves, 'distinct', T_distinct, '| (node,side) with T', Tpairs, '| deleted L', L, 'P', P)
