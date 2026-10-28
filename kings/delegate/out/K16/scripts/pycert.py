#!/usr/bin/env python3
"""pycert.py BOARD N SEED [KV]: a second, independent implementation (Python, BFS over G_omega states) of the hypotheses
(H1), (H2), (H4), (H5 with the king), (SQ) of the conjecture; compares its certificates with chk.c (--mode cert) on N random
legal positions (both sides to move, e.p. rights).  Uses pyp.py only for parsing and move rules of kings/pawns in the
legality test of the generated position."""
import sys, random, subprocess
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts')
import pyp
spec, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
KV = int(sys.argv[4]) if len(sys.argv) > 4 else 0
B = pyp.Board(spec); W, H = B.W, B.H
random.seed(seed)

def name(s):
    f, r = B.fr(s); return chr(97 + f) + str(r + 1)

def fmt(st):
    wk, bk, wp, bp, stm, ep = st
    t = ["K" + name(wk), "k" + name(bk)] + ["P" + name(s) for s in sorted(wp)] + ["p" + name(s) for s in sorted(bp)]
    return " ".join(t) + (" w " if stm == 0 else " b ") + (name(ep) if ep >= 0 else "-")

def rho(s, beta):
    r = s // W + 1
    return r if beta == 0 else H + 1 - r

def filedist(a, b):
    d = abs(a % W - b % W)
    return min(d, W - d) if B.wrap else d

def certify(st, beta):
    wk, bk, wp, bp, stm, ep = st
    om = 1 - beta
    bpaw = set(wp if beta == 0 else bp); opaw = set(bp if beta == 0 else wp)
    bking, oking = (wk, bk) if beta == 0 else (bk, wk)
    out = []
    # H2
    if any(filedist(s, bking) == 1 for s in (bpaw | opaw)):
        return out
    for p in sorted(bpaw):
        rp = rho(p, beta)
        f = p % W
        # H1 passed
        if any(filedist(q, p) <= 1 and rho(q, beta) > rp for q in opaw):
            continue
        d_ = 1 if beta == 0 else -1
        if stm == om and ep >= 0 and ep == p - d_ * W and any(ep in B.pawn_att(om, q) for q in opaw):
            continue
        # path
        path = []
        r = p // W + d_
        while 0 <= r < H:
            path.append(r * W + f); r += d_
        if any(s in (wp | bp) or s in (wk, bk) for s in path):
            continue
        # H4
        if any(filedist(q, p) == 1 and rho(q, beta) > rp + 1 for q in bpaw - {p}):
            continue
        d = H - rp - (1 if rp == 2 else 0)
        e = d if stm == om else d - 1
        # SQ
        qs = [p]
        cur = p
        for j in range(1, d + 1):
            cur = cur + d_ * W * (2 if (j == 1 and rp == 2) else 1)
            qs.append(cur)
        ok = True
        for j, q in enumerate(qs):
            if j == 0 and stm != om: continue
            nj = j if stm == om else j - 1
            if B.kdist(oking, q) < nj + 2: ok = False
        if not ok:
            continue
        # H5 : BFS over G_omega
        if e >= 1 and opaw:
            lastr = (H - 1) if om == 0 else 0
            startr = 1 if om == 0 else H - 2
            dd = 1 if om == 0 else -1
            others = frozenset(bpaw - {p})
            start = (frozenset(opaw), others, oking)
            level = {start}
            seen = {(start, True)}
            found = False
            cur_level = [(start, True)]
            for step in range(e):
                nxt = []
                for (ops, bs, ok_), first in cur_level:
                    occ = set(ops) | set(bs) | {bking, ok_}
                    for s in ops:
                        t = s + dd * W
                        if t not in occ:
                            if t // W == lastr: found = True; break
                            nxt.append(((ops - {s} | {t}, bs, ok_), False))
                            t2 = t + dd * W
                            if s // W == startr and t2 not in occ:
                                nxt.append(((ops - {s} | {t2}, bs, ok_), False))
                        for c in B.pawn_att(om, s):
                            if c in bs:
                                nxt.append(((ops - {s} | {c}, bs - {c}, ok_), False))
                            elif first and stm == om and ep >= 0 and c == ep and (ep + d_ * W) in bs:
                                nxt.append(((ops - {s} | {c}, bs - {ep + d_ * W}, ok_), False))
                    if found: break
                    if KV != 2:
                        for t in B.king_steps(ok_):
                            if t in ops or t == bking or B.kdist(t, bking) <= 1: continue
                            if KV == 1 and any(t in B.pawn_att(beta, q) for q in bs): continue
                            nxt.append(((ops, bs - {t}, t), False))
                if found: break
                cur_level = list({x for x in nxt})
            if found:
                continue
        out.append(name(p))
    return out

def rand_pos():
    while True:
        n = W * H
        k = 2 + random.randint(1, 6)
        sqs = random.sample(range(n), k)
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
            mover = 1 - stm; d = 1 if mover == 0 else -1
            cand = [s - d * W for s in (pw if mover == 0 else pb) if s // W == (3 if mover == 0 else H - 4)]
            if cand: ep = random.choice(cand)
        st = (wk, bk, frozenset(pw), frozenset(pb), stm, ep)
        if pyp.in_check(B, st, 1 - stm): continue
        if ep >= 0:
            mover = 1 - stm; d = 1 if mover == 0 else -1
            orig = ep - d * W; occ = set(pw) | set(pb) | {wk, bk}
            if ep in occ or orig in occ: continue
            if not any(ep in B.pawn_att(stm, q) for q in (pb if mover == 0 else pw)): continue
        return st

def near_certifiable():
    """positions biased towards satisfying the hypotheses: shelter the beta king, pass p"""
    while True:
        st = rand_pos()
        if certify(st, 0) or certify(st, 1) or random.random() < .15: return st

poss = [near_certifiable() for _ in range(N)]
inp = "\n".join(fmt(s) for s in poss) + "\n"
out = subprocess.run(["/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/work/chk3", "--board", spec, "--mode", "cert", "--kv", str(KV)],
                     input=inp, capture_output=True, text=True).stdout.strip().split("\n")
bad = ncert = 0
for st, line in zip(poss, out):
    c = line.split(" | ")[1].split()
    c = sorted(t.split(":")[0] + ":" + t.split(":")[1] for t in c if t != "-")
    mine = sorted(["W:" + s for s in certify(st, 0)] + ["B:" + s for s in certify(st, 1)])
    ncert += len(mine)
    if c != mine:
        bad += 1
        if bad < 6: print("DIFF", fmt(st), c, mine)
print("pycert", spec, "kv", KV, "positions", N, "certified instances", ncert, "mismatching positions", bad)
