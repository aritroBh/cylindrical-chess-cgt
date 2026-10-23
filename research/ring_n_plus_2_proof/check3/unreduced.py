# unreduced search (no poison pruning) for G+*h, h=0..3, with the independent engine eng.py: python3 -B unreduced.py 8 10 ...
import sys
from eng import *
for n in map(int, sys.argv[1:]):
    pos = ring("P", n); sig, nodes = outcomes(pos)
    print("P", n, "pawns", npawns(pos), "unreduced sig", sig, "nodes", nodes, flush=True)
