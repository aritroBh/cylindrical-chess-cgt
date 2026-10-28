#!/usr/bin/env python3
"""xmoves.py BOARD N SEED : compare the legal move lists of chk.c (gen_moves) and pyp.py on random legal positions."""
import sys, random, subprocess
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts')
import pyp
spec, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
B = pyp.Board(spec)
random.seed(seed)
W, H = B.W, B.H

def name(s):
    f, r = B.fr(s); return chr(97 + f) + str(r + 1)

def fmt(st):
    wk, bk, wp, bp, stm, ep = st
    t = ["K" + name(wk), "k" + name(bk)] + ["P" + name(s) for s in sorted(wp)] + ["p" + name(s) for s in sorted(bp)]
    return " ".join(t) + (" w " if stm == 0 else " b ") + (name(ep) if ep >= 0 else "-")

def rand_pos():
    while True:
        n = W * H
        sqs = random.sample(range(n), 2 + random.randint(0, 7))
        wk, bk = sqs[0], sqs[1]
        if B.kdist(wk, bk) <= 1: continue
        pw, pb = set(), set()
        ok = True
        for s in sqs[2:]:
            if s // W in (0, H - 1): ok = False; break
            (pw if random.random() < .5 else pb).add(s)
        if not ok: continue
        stm = random.randint(0, 1)
        ep = -1
        if random.random() < .3:
            mover = 1 - stm
            d = 1 if mover == 0 else -1
            cand = []
            for s in (pw if mover == 0 else pb):
                if s // W == (3 if mover == 0 else H - 4):
                    cand.append(s - d * W)
            if cand: ep = random.choice(cand)
        st = (wk, bk, frozenset(pw), frozenset(pb), stm, ep)
        # legal: side not to move not in check; ep sanity
        if pyp.in_check(B, st, 1 - stm): continue
        if ep >= 0:
            mover = 1 - stm; d = 1 if mover == 0 else -1
            land = ep + d * W; orig = ep - d * W
            occ = set(pw) | set(pb) | {wk, bk}
            if ep in occ or orig in occ: continue
            if not any(ep in B.pawn_att(stm, q) for q in (pb if mover == 0 else pw)): continue
        return st

poss = [rand_pos() for _ in range(N)]
inp = "\n".join(fmt(s) for s in poss) + "\n"
out = subprocess.run(["/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/work/chk2", "--board", spec, "--mode", "moves"], input=inp, capture_output=True, text=True).stdout.split("\n")
i = 0
bad = 0
tot = 0
for st in poss:
    n = int(out[i]); i += 1
    cs = set()
    for _ in range(n):
        cs.add(out[i]); i += 1
    mv = pyp.moves(B, st)
    ps = set(("PROMO " if k == "promo" else "") + fmt(ns) for k, ns in mv)
    tot += len(ps)
    if cs != ps or n != len(mv):
        bad += 1
        if bad <= 5: print("DIFF", fmt(st), sorted(cs ^ ps)[:6], n, len(mv))
print("xmoves", spec, "positions", N, "moves", tot, "mismatching positions", bad)
