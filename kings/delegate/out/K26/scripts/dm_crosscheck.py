#!/usr/bin/env python3
"""K26 audit: my D-model solver (dmodel.py) against K14's independent least-fixed-point solver (K14/scripts/dmodel.py, read only)
on every pawn-only context with <= 2+2 pawns on files f, g (flat 7x6, ranks 2..5), for the reservoirs dud, on, off and none
(G alone), both sides to move.  Prints the number of (context, side, reservoir) triples and the disagreements."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec0 = importlib.util.spec_from_file_location('k26dm', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dmodel.py'))
mine = importlib.util.module_from_spec(spec0); spec0.loader.exec_module(mine)
spec = importlib.util.spec_from_file_location('k14dm', '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K14/scripts/dmodel.py')
k14 = importlib.util.module_from_spec(spec); spec.loader.exec_module(k14)
W, H = 7, 6
ctx = k14.Ctx(W, H, True)
sq = [(f, r) for f in (6, 7) for r in range(2, H)]      # (file 1..7, rank 1..6): f, g
ctxs = []
for kw in range(3):
    for wp in itertools.combinations(sq, kw):
        for kb in range(3):
            for bp in itertools.combinations(sq, kb):
                if set(wp) & set(bp):
                    continue
                ctxs.append((frozenset(wp), frozenset(bp)))
roots = [(w, b, None, s) for (w, b) in ctxs for s in (0, 1)]
n = bad = 0
for res in ('dud', 'on', 'off', 'none'):
    P = mine.solve(roots, res, H)
    for (w, b) in ctxs:
        k = k14.solve(ctx, frozenset((r - 1) * W + (f - 1) for f, r in w), frozenset((r - 1) * W + (f - 1) for f, r in b), -1, res)
        for s in (0, 1):
            n += 1
            if P[(w, b, None, s)] != k[s]:
                bad += 1
                if bad <= 5:
                    print('MISMATCH', res, sorted(w), sorted(b), s, P[(w, b, None, s)], k[s])
print('contexts', len(ctxs), 'triples', n, 'disagreements', bad)

# sanity of the over / under reservoirs of dmodel.py against Proposition 4.6 (PROVED) and its mirror
Pn = mine.solve(roots, 'none', H); Po = mine.solve(roots, 'over', H); Pu = mine.solve(roots, 'under', H)
t = viol = 0
for (w, b) in ctxs:
    if Pn[(w, b, None, 1)] == 'W':              # White wins G moving second
        t += 1
        viol += not (Po[(w, b, None, 0)] == 'W' and Po[(w, b, None, 1)] == 'W')
    if Pn[(w, b, None, 0)] == 'L':              # Black wins G moving second
        t += 1
        viol += not (Pu[(w, b, None, 0)] == 'L' and Pu[(w, b, None, 1)] == 'L')
print('Proposition 4.6 (and mirror) premises', t, 'violations', viol)
