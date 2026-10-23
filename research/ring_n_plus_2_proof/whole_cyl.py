import sys, time
sys.path.insert(0, '.')
sys.setrecursionlimit(1000000)
from cylcgt import pawns
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
pawns.components = lambda b, p: [p]
for n in map(int, sys.argv[1:]):
    W = {(0,5),(2,4),(3,4),(5,3)}; B = {(1,7),(3,7),(4,6),(5,6)}
    for k in range((n-6)//2): W.add((6+2*k,2)); B.add((7+2*k,4))
    p = pawns.Pos(frozenset(W), frozenset(B)); bd = pawns.Board(n, 8, True, True)
    pawns._value.cache_clear(); t = time.time(); v = pawns._value(bd, p)
    print(f"P n={n} pawns={len(W)+len(B)} whole-board cylcgt value {v} ({time.time()-t:.0f}s)", flush=True)
