"""K21: search for a minimal counterexample to C1 (T-regime translation correct)."""
import random, sys, itertools
from dsum import *
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
B = 14
Ks = [Comp([[1], []], [[MINUS, 1], []], 0),            # {1 | -,1}, 1 = 0
      Comp([[PLUS, 1], []], [[1], []], 0),
      Comp([[1], [PLUS]], [[], []], 0),
      Comp([[PLUS], []], [[1], []], 0),
      Comp([[], []], [[MINUS], []], 0),
      Comp([[], []], [[MINUS, 1], []], 0),
      Comp([[PLUS], [MINUS]], [[MINUS],[PLUS]], 0)]
best = None
seen = set()
for it in range(int(sys.argv[2]) if len(sys.argv) > 2 else 20000):
    S = rand_loopy(rng, nmax=3, nopt=2, terms=False)
    if not S.is_stopper() or S.is_short(): continue
    kS = S.key()
    for ki, K in enumerate(Ks):
        if (kS, ki) in seen: continue
        seen.add((kS, ki))
        kt = [(0,)] ; kts = product_nodes([K])
        sn = S.reach()
        r_off = solve([K, mk_off()], [(k, 0) for (k,) in kts]); r_on = solve([K, mk_on()], [(k, 0) for (k,) in kts])
        r_D = solve([K, S], [(k, s) for (k,) in kts for s in sn])
        r_C = solve([translate(K, B)[0], S], [(k, s) for (k,) in kts for s in sn])
        for (k,) in kts:
            for m in (0, 1):
                PL = r_off[((k, 0), m)] == "W"; PR = r_on[((k, 0), m)] == "L"
                if PL or PR: continue
                for s in sn:
                    if r_D[((k, s), m)] != r_C[((k, s), m)]:
                        size = S.prune().n
                        if best is None or size < best[0]:
                            best = (size, ki, comp_str(K), comp_str(S), k, s, m, r_D[((k, s), m)], r_C[((k, s), m)])
                            print(best, flush=True)
