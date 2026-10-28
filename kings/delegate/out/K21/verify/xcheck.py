import sys, random, time
sys.path.insert(0,'.'); sys.path.insert(0,'../scripts')
import ref, dsum
from tests1 import rnd_comp
conv = lambda o: dsum.PLUS if o == 'P' else (dsum.MINUS if o == 'M' else o)
rng = random.Random(4242); n = 0; bad = 0; t = time.time(); dis = 0
for it in range(1500):
    k = rng.choice((2, 3)); comps = [rnd_comp(rng, 4, short=(rng.random() < .3)) for _ in range(k)]
    B = rng.choice((1, 2, 4, 6))
    theirs = [dsum.Comp([[conv(o) for o in l] for l in c.L], [[conv(o) for o in r] for r in c.R], 0) for c in comps]
    Ys = ref.reach_tuples(comps)
    d1 = ref.d_results(comps, [(Y, m) for Y in Ys for m in (0, 1)])
    c1 = ref.cgt_solve(comps, B, [(tuple(('n', y) for y in Y), m) for Y in Ys for m in (0, 1)])
    d2 = dsum.d_results(theirs); c2 = dsum.cgt_results(theirs, B)
    for Y in Ys:
        for m in (0, 1):
            n += 1
            if ref.outcome(*d1[(Y, m)]) != d2[(Y, m)]: bad += 1
            if ref.outcome(*c1[(tuple(('n', y) for y in Y), m)]) != c2[(Y, m)]: bad += 1
    dd = dsum.dominance(theirs, B)[0]
    if dd != ref.dominance(comps, B): dis += 1
    cr2 = dsum.reserve_criterion(theirs, B)[0]
    if cr2 != ref.criterion(comps, B): dis += 1
print("states compared", n, "disagreements", bad, "dominance/criterion disagreements", dis, "%.0fs" % (time.time() - t))
