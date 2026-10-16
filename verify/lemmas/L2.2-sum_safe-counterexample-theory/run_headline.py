import sys, time
sys.path.insert(0, ".")
from indep import B, parse, make_solvers, reach, comps, threats, has_passer
bd = B(8, 8, True, False)
x = parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
print("components:", len(comps(bd, x)))
R = reach(bd, x)
print("reachable (stop at passer):", len(R))
for BIG in [int(a) for a in sys.argv[1:]] or [64]:
    t = time.time()
    oW, oS, Wg, Sg = make_solvers(bd, "count", BIG)
    print("BIG", BIG, "o(W) =", oW(x), "o(S) =", oS(x), f"{time.time()-t:.1f}s", "Sg states", Sg.cache_info().currsize, flush=True)
