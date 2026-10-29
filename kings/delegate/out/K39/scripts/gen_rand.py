#!/usr/bin/env python3
"""K39: random test positions for comparing own39 with kpsolve/kp39. usage: gen_rand.py W H N SEED [maxpawns] [epfrac]
Kings anywhere, 0..maxpawns pawns on ranks 2..H-1, at most one officer, some positions with an e.p. right
(a pawn that has just double-stepped, with an enemy pawn beside it). Illegal ones are left in (both solvers say X)."""
import random, sys
W, H, n, seed = map(int, sys.argv[1:5]); maxp = int(sys.argv[5]) if len(sys.argv) > 5 else 4
epfrac = float(sys.argv[6]) if len(sys.argv) > 6 else 0.25
rnd = random.Random(seed)
def nm(f, r): return "abcdefgh"[f] + str(r + 1)
out = set()
while len(out) < n:
    occ = {}
    sqs = [(f, r) for f in range(W) for r in range(H)]
    rnd.shuffle(sqs)
    wk, bk = sqs.pop(), sqs.pop()
    occ[wk] = 'K'; occ[bk] = 'k'
    np = rnd.randint(1, maxp)
    ep = '-'; stm = rnd.choice('wb')
    if rnd.random() < epfrac:
        # mover = side not to move double-stepped
        mover = 'b' if stm == 'w' else 'w'
        f = rnd.randrange(W)
        if mover == 'w': fr, lr, sk = 1, 3, 2
        else: fr, lr, sk = H - 2, H - 4, H - 3
        cf = (f + rnd.choice((-1, 1))) % W
        if any(x in occ for x in [(f, fr), (f, sk), (f, lr), (cf, lr)]): continue
        occ[(f, lr)] = 'P' if mover == 'w' else 'p'
        occ[(cf, lr)] = 'p' if mover == 'w' else 'P'
        ep = nm(f, sk)
        sqs = [s for s in sqs if s not in occ and s not in [(f, fr), (f, sk)]]
        np -= 2
    for _ in range(max(0, np)):
        s = sqs.pop()
        if s[1] in (0, H - 1): continue
        occ[s] = rnd.choice('Pp')
    if rnd.random() < 0.4:
        s = sqs.pop()
        occ[s] = rnd.choice('QRBNqrbn')
    toks = [occ[s] + nm(*s) for s in sorted(occ, key=lambda s: ("KkPpQRBNqrbn".index(occ[s]), s))]
    out.add(" ".join(toks) + " " + stm + " " + ep)
for l in sorted(out): print(l)
