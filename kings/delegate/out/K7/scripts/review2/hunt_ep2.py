"""structured e.p. family (s=White): W context pawn blocked by a B pawn, a B pawn that just double-stepped beside it; B Z-pawn(s); random extras.
usage: hunt_ep2.py seed N board FZ Tmax tag"""
import sys, random, subprocess, json, time
from kb import B
from cert import Cert
seed, N = int(sys.argv[1]), int(sys.argv[2])
kind, dims = sys.argv[3].split(':'); W, H = map(int, dims.split('x')); wrap = (kind == 'cyl')
FZ = [int(x) for x in sys.argv[4].split(',')]; Tmax = int(sys.argv[5]); tag = sys.argv[6]
rng = random.Random(seed)
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
FZs = sorted(FZ); CTX = sorted(C.ctx)
zsq = [r * W + f for r in range(1, H - 1) for f in FZs]
csq = [r * W + f for r in range(1, H - 1) for f in CTX]
fzk = [r * W + f for r in range(H) for f in FZs]
land = H - 4   # black's double step lands here (white capturer stands on the same rank)
def nbrs(f):
    return [x for x in ((f - 1) % W, (f + 1) % W)] if wrap else [x for x in (f - 1, f + 1) if 0 <= x < W]
def gen():
    while True:
        taken = set()
        f = rng.choice(CTX); nf = rng.choice([x for x in nbrs(f) if x in C.ctx] or [None])
        if nf is None: continue
        ep_b = land * W + f; skip = (land + 1) * W + f; orig = (land + 2) * W + f
        wpn = land * W + nf
        wps = {wpn}; bps = {ep_b}
        # blocker(s) above the white pawn
        if rng.random() < 0.85:
            for k in range(1, rng.choice([1, 1, 2])):
                pass
            bl = (land + 1) * W + nf
            bps.add(bl)
        zb = rng.choice([1, 1, 2])
        allsq = set(wps) | set(bps) | {skip, orig}
        zs = [x for x in zsq if x not in allsq]; rng.shuffle(zs)
        for x in zs[:zb]: bps.add(x)
        if rng.random() < 0.3:
            x = rng.choice(zsq)
            if x not in allsq and x not in bps: wps.add(x)
        if rng.random() < 0.3:
            x = rng.choice(csq)
            if x not in allsq and x not in bps and x not in wps: wps.add(x)
        if rng.random() < 0.2:
            x = rng.choice(csq)
            if x not in allsq and x not in bps and x not in wps: bps.add(x)
        if len(wps) > 3 or len(bps) > 3: continue
        occ = wps | bps | {skip, orig}
        wk = rng.choice(range(Bd.N)); bk = rng.choice(fzk)
        if wk in occ or bk in occ or wk == bk: continue
        pos = (wk, bk, frozenset(wps), frozenset(bps), 0, skip)
        if not Bd.legal_pos(pos): continue
        # retro: white king not attacked by the black pawn at orig
        if wk in Bd.att[1][orig]: continue
        if not any(skip in Bd.att[0][p] for p in wps): continue
        if wk in Bd.attacked_by_pawns([p for p in bps if not C.inz(p)], 1): continue
        return pos
rows = []; t0 = time.time()
for i in range(N):
    Q = gen()
    TP = C.minT(Q, Tmax)
    if TP is None: continue
    m0 = C.mu(Q, use_ep=False); m1 = C.mu(Q, use_ep=True)
    row = dict(Q=Bd.text(Q), TP=TP, m0=m0, m1=m1, T={})
    for T in range(TP, Tmax + 1):
        if m1 >= T + 1 or m0 >= T + 1:
            h, fl = C.L3(Q, T); row['T'][T] = [bool(h), sorted(fl)]
    if not row['T']: continue
    rows.append(row)
    if len(C.lmemo) > 3_000_000: C.lmemo.clear()
qs = [r['Q'] for r in rows]
out = subprocess.run(["./kp", "--board", f"{kind}:{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input="\n".join(qs) + "\n", capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(rows)
n_new = b_new = n_old = b_old = 0; diff = 0
for r, l in zip(rows, out):
    parts = l.split("|")[1].split()
    win = parts[0] == 'L' and parts[1] == 'L'   # s = White, s-bar = Black wins
    r['win'] = win
    if r['m1'] != r['m0']: diff += 1
    for T, (h, fl) in r['T'].items():
        T = int(T)
        if not h: continue
        if r['m0'] >= T + 1:
            n_old += 1; b_old += (not win)
        if r['m1'] >= T + 1:
            n_new += 1
            if not win: b_new += 1; print("COUNTEREXAMPLE", tag, r['Q'], "T", T, "mu", r['m1'], parts, flush=True)
json.dump(rows, open(f"rows_{tag}.json", "w"))
print(f"{tag} {sys.argv[3]} FZ={FZs} N={N} rows={len(rows)} (mu differs with e.p.: {diff}) LC_new={n_new} nonwins={b_new} | LC_noEPclause={n_old} nonwins={b_old} | {time.time()-t0:.0f}s", flush=True)
