import sys, time
from engine import *
for n in map(int, sys.argv[1:]):
    t0 = time.time()
    start = parse(P_toks(n))
    order, edges = build(start)
    nK = sum(len(ks) for (nd, s), (h, ks) in edges.items())
    nTpairs = sum(1 for (nd, s), (h, ks) in edges.items() if h)
    flagged = sum(1 for nd in order if nd[1] is not None)
    touched = sorted({f for nd in order for f in range(n) if nd[0][f] != start[f]})
    print('n', n, 'nodes', len(order), 'K', nK, 'Tpairs', nTpairs, 'flagged', flagged, 'touched', touched, 'sig', solve_sig(order, edges), '%.1fs' % (time.time() - t0), flush=True)
