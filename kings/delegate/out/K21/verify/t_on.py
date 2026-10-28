import sys, random
sys.path.insert(0,'.')
from ref import *
from tests1 import rnd_comp
from tests2 import M
A = G([[]],[['P']]); C = G([['M']],[[]])
print("3.8(b) reserves of {|P}:", {B: (big_lam_rho(A,B)[:2]) for B in (1,3)}, " {M|}:", {B: big_lam_rho(C,B)[:2] for B in (1,3)})
rng = random.Random(9); n = bad = 0; nev = 0
for it in range(3000):
    K = [rnd_comp(rng, 3, short=True) for _ in range(rng.choice((1,2)))]
    evs = [c.events() for c in K]
    if any('P' in evs[i] and 'M' in evs[j] for i in range(len(K)) for j in range(len(K)) if i != j): continue
    for S, forbid in ((ON(), 'M'), (OFF(), 'P')):
        if any(forbid in e for e in evs): continue
        B = 1 + max(sum(M(c,0) for c in K), sum(M(c,1) for c in K))
        comps = [S] + K
        n += 1; nev += any(evs)
        Ys = reach_tuples(comps)
        ds = d_results(comps, [(Y,m) for Y in Ys for m in (0,1)]); cs = cgt_solve(comps, B, [(tuple(('n',y) for y in Y),m) for Y in Ys for m in (0,1)])
        ok = criterion(comps, B) and all(outcome(*ds[(Y,m)]) == outcome(*cs[(tuple(('n',y) for y in Y),m)]) for Y in Ys for m in (0,1))
        bad += (not ok)
print("on/off beside safe short K with no opposite event: instances", n, "with events", nev, "failures", bad)
