#!/usr/bin/env python3
"""random K+P positions for cross-checking two P solvers. usage: randpos.py W H N seed"""
import sys, random
W, H, N, seed = map(int, sys.argv[1:5]); random.seed(seed)
def nm(f, r): return "abcdefghi"[f] + str(r + 1)
out = []
while len(out) < N:
    nw, nb = random.randint(0, 4), random.randint(0, 4)
    sqs = [(f, r) for f in range(W) for r in range(1, H - 1)]
    ps = random.sample(sqs, nw + nb)
    wp, bp = ps[:nw], ps[nw:]
    occ = set(ps)
    free = [(f, r) for f in range(W) for r in range(H) if (f, r) not in occ]
    wk, bk = random.sample(free, 2)
    side = random.choice("wb")
    ep = "-"
    if random.random() < 0.3:
        # make an e.p. right: last mover double-stepped
        if side == "b":
            cand = [(f, r) for (f, r) in wp if r == 3 and (f, 2) not in occ and (f, 1) not in occ and (f, 2) not in (wk, bk) and (f, 1) not in (wk, bk)]
            if cand: f, r = random.choice(cand); ep = nm(f, 2)
        else:
            cand = [(f, r) for (f, r) in bp if r == H - 4 and (f, H - 3) not in occ and (f, H - 2) not in occ and (f, H - 3) not in (wk, bk) and (f, H - 2) not in (wk, bk)]
            if cand: f, r = random.choice(cand); ep = nm(f, H - 3)
    toks = ["K" + nm(*wk), "k" + nm(*bk)] + ["P" + nm(*s) for s in wp] + ["p" + nm(*s) for s in bp]
    out.append(" ".join(toks) + f" {side} {ep}")
print("\n".join(out))
