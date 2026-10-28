import sys, random
sys.path.insert(0,'.')
from ref import *
from tests1 import rnd_comp
from tests2 import M
rng = random.Random(8); chk = viol = 0
for it in range(2500):
    c = rnd_comp(rng, 4, short=True)
    for B in (1, 3, 8):
        r = reserves(c, B, 30)
        for x, (lam, rho) in r.items():
            sub = G(c.L, c.R); 
            # re-root at x for M computation
            def Mx(who):
                memo = {}
                def f(y):
                    if y in memo: return memo[y]
                    best = 0
                    for o in c.L[y]:
                        best = max(best, (1 if who == 0 else 0) + (f(o) if isinstance(o, int) else 0))
                    for o in c.R[y]:
                        best = max(best, (1 if who == 1 else 0) + (f(o) if isinstance(o, int) else 0))
                    memo[y] = best; return best
                return f(x)
            reachx = set(); st = [x]
            while st:
                y = st.pop()
                if y in reachx: continue
                reachx.add(y); st += [o for o in c.L[y] + c.R[y] if isinstance(o, int)]
            evs = {o for y in reachx for o in c.L[y] + c.R[y] if o in ('P', 'M')}
            if 'M' not in evs:
                chk += 1
                if lam is None or lam > Mx(1): viol += 1; print("lam viol", c, x, B, lam, Mx(1))
            if 'P' not in evs:
                chk += 1
                if rho is None or rho > Mx(0): viol += 1; print("rho viol", c, x, B, rho, Mx(0))
print("checks", chk, "violations", viol)
