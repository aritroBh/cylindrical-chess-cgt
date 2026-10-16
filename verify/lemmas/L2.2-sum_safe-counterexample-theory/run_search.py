"""Independent random search (no project imports): single-component, non-terminal 8x8 positions
(2-4 pawns a side on ranks 2..7), o(S) vs o(W) under each race rule. Usage: run_search.py SEED N [cyl] [ep]"""
import sys, random, time
sys.path.insert(0, ".")
from indep import B, make_solvers, comps, has_passer, show
seed, N = int(sys.argv[1]), int(sys.argv[2])
cyl = (sys.argv[3] == "cyl") if len(sys.argv) > 3 else True
ep = (sys.argv[4] == "ep") if len(sys.argv) > 4 else False
rng = random.Random(seed)
bd = B(8, 8, cyl, ep)
sq = [(f, r) for f in range(8) for r in range(2, 8)]
solvers = {r: make_solvers(bd, r, 256) for r in ("count", "mover", "opponent")}
tried, bad, t0 = 0, {r: [] for r in solvers}, time.time()
while tried < N:
    nw, nb = rng.randint(2, 4), rng.randint(2, 4)
    pick = rng.sample(sq, nw + nb)
    p = (frozenset(pick[:nw]), frozenset(pick[nw:]), None)
    if has_passer(bd, p, "W") or has_passer(bd, p, "B") or len(comps(bd, p)) != 1:
        continue
    tried += 1
    for r, (oW, oS, _, _) in solvers.items():
        s, w = oS(p), oW(p)
        if s != w:
            bad[r].append((show(p), s, w))
print(f"seed {seed} cyl={cyl} ep={ep}: {tried} single components, {time.time()-t0:.0f}s")
for r in bad:
    print(f"  {r}: {len(bad[r])} disagreements", bad[r][:4])
