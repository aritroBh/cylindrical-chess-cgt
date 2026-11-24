"""K60: for bad Black moves failing (C_B) on the battery, which test games witness the failure?"""
import random, sys
from collections import Counter
from k60lib import ORD, sum_with, over_vals, exact_over, bad_black_moves, aux_win
from k60games import named_battery, rand_T, random_group, tempo_group
seed, ngroups, nrand, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(seed)
tests = named_battery() + [("r%d" % i, rand_T(rng)) for i in range(nrand)]
ovs = [over_vals(T) for _, T in tests]
wit = Counter(); nfail = 0; only = Counter(); kinds = Counter()
seen = set(); n = 0
while n < ngroups:
    G = random_group(rng) if mode == "random" else tempo_group(rng)
    if G is None or G.key() in seen or exact_over(G) is None:
        continue
    seen.add(G.key()); n += 1
    bads = bad_black_moves(G)
    fails = {bm: set() for bm in bads}
    for (name, T), ov in zip(tests, ovs):
        sv = sum_with(G, T)
        for bm in bads:
            (_, y, d) = bm
            for t in range(len(T[0])):
                a, b = sv[(y, d, t, 0)], ov[(0, t, 1)]
                if ORD[a] < ORD[b]:
                    fails[bm].add(name)
                    kinds[(a, b)] += 1
    for bm, fs in fails.items():
        if fs:
            nfail += 1
            for f in fs:
                wit[f] += 1
            if len(fs) == 1:
                only[next(iter(fs))] += 1
print("failing bad moves", nfail, "kinds (x,omegaB)", dict(kinds))
print("witness counts", wit.most_common(25))
print("sole witness", only.most_common(10))
