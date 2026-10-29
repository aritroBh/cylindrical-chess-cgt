"""r2_x.py: exact solve of the whole P7 game (Ke6 Pd7 kd8 pe7) in P, EPW, EPB on cyl / flat, own code."""
import sys, time
from r2_lib import *
kind = sys.argv[1]
B = Board(kind)
X = parse(B, 'Ke6 Pd7 kd8 pe7 w -')
t0 = time.time()
ids, states, succ, term, chk = build(B, [X])
print(kind, 'reachable states from X:', len(states), 'build %.1fs' % (time.time() - t0))
print('moves at X:', sorted(l for l, k, n in gen(B, X)))
for model in ('P', 'EPW', 'EPB'):
    WW, BW = solve(states, succ, term, chk, model)
    print(model, 'X =', value(WW, BW, ids[X]))
    for lab, k, n in sorted(gen(B, X)):
        print('   ', lab, value(WW, BW, ids[n]))
    # value counts over all reachable
    import collections
    c = collections.Counter(value(WW, BW, i) for i in range(len(states)))
    print('   all reachable states', dict(c))
print('cpu %.1fs' % (time.process_time()))
