import sys, random, json, time
sys.path.insert(0,'.')
from exh import *
rng = random.Random(5); A = all1(); st = dict(n=0, crit_not_dom=0, dom_not_eq=0, dom_ev=0, crit_ev=0, dom_nocrit=0, nondom_eq=0); t=time.time()
for it in range(1200):
    check([rng.choice(A) for _ in range(3)], 2, st)
print("triples sample", json.dumps(st), "%.0fs"%(time.time()-t))
