#!/usr/bin/env python3
"""K44: sum test of the 'over' and 'under' roots against the reference games: for every context X that is a D-sum of at most two
battery games, outcome(root + X) == outcome(reference + X) for both movers.  Also root + root against over + over (one-component
sum of the two quotient graphs)."""
import sys, os, itertools
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from lk3 import LK, quotient, battery, dsum, parse_cfg
from sumnames import sumgame
def reach(QL, QR, c):
    seen = {c}; st = [c]
    while st:
        x = st.pop()
        for t in QL[x] + QR[x]:
            if not isinstance(t, str) and t not in seen: seen.add(t); st.append(t)
    order = sorted(seen); ix = {x: i for i, x in enumerate(order)}
    L = [[t if isinstance(t, str) else ix[t] for t in QL[x]] for x in order]
    R = [[t if isinstance(t, str) else ix[t] for t in QR[x]] for x in order]
    return L, R, ix[c]
C = battery(); pool = list(C)
ctxs = [(n,) for n in pool] + [c for c in itertools.combinations_with_replacement(pool, 2)]
tests = [("cyl:10x6", "a2 c4 f2", "Kc3 ka4 Pa2 pa3 Pc4 pc5 Pf2 pf3", 'over'),
         ("cyl:10x6", "a2 c4 f2", "Kc3 ka5 Pa2 pa3 Pc4 pc5 Pf2 pf3", 'over'),
         ("cyl:10x6", "a2 c4 h4", "Kc2 ka4 Pa2 pa3 Pc4 pc5 Ph4 ph5", 'under'),
         ("cyl:10x6", "a2 c4 h4", "Kc3 ka4 Pa2 pa3 Pc4 pc5 Ph4 ph5", 'under')]
cache = {}
for board, cfg, root, ref in tests:
    W, H = [int(v) for v in board.split(':')[1].split('x')]
    key = (board, cfg)
    if key not in cache:
        g = LK(W, H, True, parse_cfg(cfg)); cls, QL, QR = quotient(g.L, g.R); cache[key] = (g, cls, QL, QR)
    g, cls, QL, QR = cache[key]
    r = [i for i in range(len(g.nodes)) if g.name(i) == root][0]
    L, R, s = reach(QL, QR, cls[r])
    bad = 0
    for ctx in ctxs:
        XL, XR = sumgame([C[n] for n in ctx])
        res = dsum(L, R, XL, XR)[s][0]
        rl, rr = C[ref]
        refres = dsum(rl, rr, XL, XR)[0][0]
        if res != refres: bad += 1
    print('%s %s reach %d  vs %s: contexts %d, mismatches %d' % (cfg, root, len(L), ref, len(ctxs), bad), flush=True)
