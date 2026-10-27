"""iso_small.py -- information only: for odd n = 11..17 (below the note's n0 = 19) the cuts c at which ins_c : G_n -> G_(n+2) is an
isomorphism of the reduced graphs (nodes onto nodes, K- and T-children).  The note says n < 19 has no ten-file arc and rests on the direct
searches C2; this shows what the graphs themselves do.   Usage: python iso_small.py [LO HI]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oddeng as O          # noqa: E402
from run_c import iso       # noqa: E402

lo = int(sys.argv[1]) if len(sys.argv) > 1 else 11
hi = int(sys.argv[2]) if len(sys.argv) > 2 else 17
for fam in ('R', 'Qo'):
    G = {n: O.Graph(O.start(fam, n)) for n in range(lo, hi + 3, 2)}
    for n in range(lo, hi + 1, 2):
        okc = [c for c in range(0, n - 1) if iso(G[n], G[n + 2], c)['ok']]
        print(f'{fam} n={n}->{n + 2}: nodes {len(G[n].order)} -> {len(G[n + 2].order)}; iso holds for cuts {okc}', flush=True)
