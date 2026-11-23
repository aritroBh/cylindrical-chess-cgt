# random K+P positions on cyl:Wx6 for the solver cross-check (seeded)
import random, sys
W, H, n, seed = int(sys.argv[1]), 6, int(sys.argv[2]), int(sys.argv[3])
rnd = random.Random(seed)
F = 'abcdefghijklmnop'
def nm(f, r): return F[f] + str(r + 1)
for _ in range(n):
    while True:
        nw, nb = rnd.randint(0, 4), rnd.randint(0, 4)
        files = rnd.sample(range(W), rnd.randint(1, min(5, W)))
        occ = {}
        ok = True
        for c, k in (('P', nw), ('p', nb)):
            for _ in range(k):
                for _t in range(20):
                    s = (rnd.choice(files), rnd.randint(1, H - 2))
                    if s not in occ: occ[s] = c; break
        free = [(f, r) for f in range(W) for r in range(H) if (f, r) not in occ]
        wk, bk = rnd.sample(free, 2)
        stm = rnd.choice('wb')
        ep = '-'
        if rnd.random() < 0.25:
            # give an e.p. square: the side not to move just double-stepped
            if stm == 'w':
                cands = [(f, r) for (f, r), c in occ.items() if c == 'p' and r == H - 4 and (f, H - 3) not in occ and (f, H - 2) not in occ and (f, H - 3) not in (wk, bk) and (f, H - 2) not in (wk, bk)]
                if cands: f, r = rnd.choice(cands); ep = nm(f, H - 3)
            else:
                cands = [(f, r) for (f, r), c in occ.items() if c == 'P' and r == 3 and (f, 2) not in occ and (f, 1) not in occ and (f, 2) not in (wk, bk) and (f, 1) not in (wk, bk)]
                if cands: f, r = rnd.choice(cands); ep = nm(f, 2)
        toks = ['K' + nm(*wk), 'k' + nm(*bk)] + [c + nm(f, r) for (f, r), c in sorted(occ.items())]
        print(' '.join(toks), stm, ep)
        break
