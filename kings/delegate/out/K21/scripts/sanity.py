from dsum import *
# reserves of named loopy games, B=4
for name, f in NAMED.items():
    c = f()
    lam, rho = reserves(c, 4, 12)
    print(name, lam, rho, "stopper" if c.is_stopper() else "NOT stopper")
# {+|} + off  (D says Left wins; translation does not)
A = Comp([[PLUS]], [[]])
for nm in ("on","off","dud","over"):
    S = NAMED[nm]()
    d = d_results([A,S])[((0,0),0)], d_results([A,S])[((0,0),1)]
    for B in (3,6):
        c = cgt_results([A,S],B)
        print(nm, "D", d, "CGT B=%d"%B, (c[((0,0),0)], c[((0,0),1)]), "dominance", dominance([A,S],B)[0], "crit", reserve_criterion([A,S],B)[0])
