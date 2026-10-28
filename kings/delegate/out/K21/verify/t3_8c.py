import sys, random
sys.path.insert(0,'.')
from ref import *
from tests1 import rnd_comp
rng = random.Random(77); n=0; viol=0; tot=0
for it in range(4000):
    a = rnd_comp(rng, 3); b = rnd_comp(rng, 3)
    for B in (1,2,4,6):
        for (j,i) in ((0,1),(1,0)):
            comps=[a,b]
            cj, ci = comps[j], comps[i]
            for sg in ('P','M'):
                if sg in cj.events():
                    Lam,Rho,r = big_lam_rho(ci,B)
                    inf = (Lam is None) if sg=='P' else (Rho is None)
                    if inf:
                        tot+=1
                        # claim: dominance fails
                        if dominance(comps,B): viol+=1; print("VIOL",comps,B)
print("cases with inf reserve opposite event:",tot,"dominance holds in",viol)
