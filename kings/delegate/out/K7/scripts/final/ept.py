"""K7b: window-form test of Theorem 2.7(b) with e.p. rights at Q.
usage: ept.py seed N W H cyl|flat tag Tmax mode   (mode: ctx = e.p. target off F_Z, z = target on F_Z, mix)"""
import sys, random, subprocess, json, time
sys.path.insert(0, '..')
from kpgen import Board
from lc import Cert
seed, N, W, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
wrap = sys.argv[5] == 'cyl'; tag = sys.argv[6]; Tmax = int(sys.argv[7]); mode = sys.argv[8]
random.seed(seed)
B = Board(W, H, wrap); FZ = [0, 1, 2]; C = Cert(B, FZ)
ctxf = list(range(4, W - 1)) if wrap else list(range(4, W))
fzk = [r * W + f for r in range(H) for f in FZ]
zsq = [r * W + f for r in range(1, H - 1) for f in FZ]
csq = [r * W + f for r in range(1, H - 1) for f in ctxf]
allk = list(range(B.N))

def mu_ep(Q, use_ep=True):
    """context-pawn mu with the e.p. right of Q (target off F_Z) usable as first move."""
    base = C.mu(Q, False)
    wk, bk, wp, bp, stm, ep = Q
    if not use_ep or ep < 0 or (ep % W) in C.FZ:
        return base
    s = stm; d = 1 if s == 0 else -1
    own = set(wp) if s == 0 else set(bp); opp = set(bp) if s == 0 else set(wp)
    ok = wk if s == 0 else bk
    best = base
    capsq = ep - d * W
    for p in own:
        if (p % W) in C.FZ: continue
        if ep in B.patt[s][p] and capsq in opp:
            ownc = frozenset(x for x in own if x != p and (x % W) not in C.FZ) | {ep}
            oppc = frozenset(x for x in opp if x != capsq and (x % W) not in C.FZ)
            Q2 = (ok, bk, ownc, oppc, 0, -1) if s == 0 else (wk, ok, oppc, ownc, 1, -1)
            best = min(best, 1 + C.mu(Q2, False))
    return best

def rand_Q():
    while True:
        s = random.randint(0, 1); sbar = 1 - s
        sk = random.choice(allk if random.random() < 0.6 else fzk); bk_ = random.choice(fzk)
        nz = (random.choice([0, 1, 2]), random.choice([0, 1, 2])); nc = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        if nz[0] + nc[0] > 3 or nz[1] + nc[1] > 3: continue
        pool = zsq[:]; random.shuffle(pool); cp = csq[:]; random.shuffle(cp)
        wz = pool[:nz[0]]; bz = pool[nz[0]:nz[0] + nz[1]]; wc = cp[:nc[0]]; bc = cp[nc[0]:nc[0] + nc[1]]
        wp = set(wz + wc); bp = set(bz + bc)
        wk, bk = (sk, bk_) if s == 0 else (bk_, sk)
        # choose an e.p. right: an s-bar pawn that has just double stepped
        m = mode if mode != 'mix' else random.choice(['ctx', 'z'])
        files = ctxf if m == 'ctx' else FZ
        f = random.choice(files)
        land = 3 if sbar == 0 else H - 4
        skip = (land - 1 if sbar == 0 else land + 1) * W + f
        orig = (land - 2 if sbar == 0 else land + 2) * W + f
        lsq = land * W + f
        pawns_sbar = wp if sbar == 0 else bp
        pawns_s = bp if sbar == 0 else wp
        # place the double-stepped pawn; optionally add an s pawn beside it
        pawns_sbar.add(lsq)
        if random.random() < 0.85:
            nf = random.choice([(f - 1) % W, (f + 1) % W]) if wrap else random.choice([x for x in (f - 1, f + 1) if 0 <= x < W])
            pawns_s.add(land * W + nf)
        if len(wp) > 3 or len(bp) > 3: continue
        pos = (wk, bk, frozenset(wp), frozenset(bp), s, skip)
        occ = [wk, bk] + list(wp) + list(bp)
        if len(set(occ)) != len(occ) or skip in occ or orig in occ: continue
        if not B.legal_pos(pos): continue
        # all pawns must be Z-pawns on F_Z or context pawns on context files
        if any(((p % W) not in FZ and (p % W) not in ctxf) for p in list(wp) + list(bp)): continue
        sbar_ctx = [p for p in (bp if s == 0 else wp) if (p % W) not in FZ]
        if sk in B.pawn_attacked(sbar_ctx, sbar): continue
        # retro: s king was not attacked by the pawn at its origin square
        if sk in B.pawn_attacked([orig], sbar): continue
        return pos

rows = []
t0 = time.time()
for i in range(N):
    Q = rand_Q()
    TP = C.L1(Q, False, Tmax)
    if TP is None: continue
    m0 = C.mu(Q, False); m1 = mu_ep(Q)
    r = dict(Q=B.to_text(Q), TP=TP, m0=m0, m1=m1, L3={})
    for T in range(TP, Tmax + 1):
        if m1 >= T + 1 or m0 >= T + 1:
            e, a, bad = C.L3(Q, T, False)
            r['L3'][T] = bool(e)
    rows.append(r)
qs = [r['Q'] for r in rows]
out = subprocess.run(["../kp", "--board", ("cyl" if wrap else "flat") + f":{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input="\n".join(qs) + "\n", capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(rows), (len(out), len(rows))
nold = nnew = bold = bnew = 0; nonep = 0
for r, l in zip(rows, out):
    parts = l.split("|")[1].split(); stm = 0 if r['Q'].split()[-2] == 'w' else 1
    win = parts[0] == parts[1] and parts[0] == ('L' if stm == 0 else 'W')
    r['win'] = win; r['P'] = parts
    for T, e in r['L3'].items():
        if not e: continue
        if r['m0'] >= T + 1:
            nold += 1
            if not win: bold += 1
        if r['m1'] >= T + 1:
            nnew += 1
            if not win: bnew += 1; print("COUNTEREXAMPLE(new)", r['Q'], T, r['m1'], parts)
json.dump(rows, open(f"ept_{tag}.json", "w"))
print(tag, "rows(L1 holds)", len(rows), "LC_old(noEP in Q°) pairs", nold, "nonwins", bold, "| LC_new pairs", nnew, "nonwins", bnew)
