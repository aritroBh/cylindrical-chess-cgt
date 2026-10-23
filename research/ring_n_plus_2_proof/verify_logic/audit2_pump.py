"""Pumping check with the fresh engine: R_{n+2} == ins_c(R_n) (nodes, K-edges, T-flags), for several cuts c.
Cuts 11 and 12 satisfy the hypotheses (arc c-4..c+5 outside the zone {0,2..6}); cuts <= 10 do not and are a sensitivity control."""
import sys, time
from engine import *

def pump(n, c):
    s0 = parse(P_toks(n)); s1 = parse(P_toks(n + 2))
    if ins(s0, c) != s1:
        return 'start-not-mapped'
    o0, e0 = build(s0); o1, e1 = build(s1)
    img = {ins_nd(nd, c) for nd in o0}
    nodes_ok = (img == set(o1)) and len(o0) == len(o1)
    bad_edges = bad_T = 0
    for nd in o0:
        for side in 'WB':
            T0, K0 = e0[(nd, side)]
            nd1 = ins_nd(nd, c)
            if nd1 not in set(o1) and False: pass
            if (nd1, side) not in e1:
                bad_edges += 1; continue
            T1, K1 = e1[(nd1, side)]
            if T0 != T1: bad_T += 1
            if {ins_nd(k, c) for k in K0} != set(K1): bad_edges += 1
    return nodes_ok, bad_edges, bad_T, len(o0), len(o1)

if __name__ == '__main__':
    cuts = [int(x) for x in sys.argv[1].split(',')]
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1, 2):
        for c in cuts:
            if c + 5 > n - 1 and c + 5 >= n:  # arc must fit
                pass
            t0 = time.time()
            print('pump n=%d->%d c=%d' % (n, n + 2, c), pump(n, c), '%.1fs' % (time.time() - t0), flush=True)
