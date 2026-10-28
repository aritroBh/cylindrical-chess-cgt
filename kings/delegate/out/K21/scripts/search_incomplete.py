"""K21: smallest instance where dominance holds (non-vacuously) but the reserve criterion fails."""
import random
from dsum import *
import run_tests as rt
rng = random.Random(5)
best = None
for it in range(20000):
    comps = rt.rand_instance(rng)
    comps = comps[:2]
    if not any(c.events() for c in comps): continue
    B = 5
    dom = dominance(comps, B)[0]
    if not dom: continue
    crit = reserve_criterion(comps, B)[0]
    if crit: continue
    size = sum(c.n for c in comps)
    if best is None or size < best[0]:
        best = (size, [comp_str(c) for c in comps])
        print(best, flush=True)
