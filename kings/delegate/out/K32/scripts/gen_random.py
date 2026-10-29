"""K32: random terminal-free stoppers with exactly n reachable nodes (all reachable from node 0), printed in the
hex format l/r per node (bit y of l = Left option to node y).  usage: gen_random.py n count seed"""
import sys, random
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32/scripts")
from stopsA import is_stopper, reach_from

n, count, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
out = 0
while out < count:
    p = rng.choice([0.12, 0.2, 0.3])
    L = [[y for y in range(n) if rng.random() < p] for _ in range(n)]
    R = [[y for y in range(n) if rng.random() < p] for _ in range(n)]
    seen = reach_from(L, R, 0)
    if len(seen) != n or not is_stopper(L, R):
        continue
    print(" ".join("%x/%x" % (sum(1 << y for y in L[x]), sum(1 << y for y in R[x])) for x in range(n)))
    out += 1
