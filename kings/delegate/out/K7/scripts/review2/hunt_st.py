"""stalemate/zugzwang-focused family: s has few moves (locked pawn pairs, cramped king).  usage: hunt_st.py seed N board FZ Tmax tag"""
import sys, random, subprocess, json, time
from kb import B
from cert import Cert
seed, N = int(sys.argv[1]), int(sys.argv[2])
kind, dims = sys.argv[3].split(':'); W, H = map(int, dims.split('x')); wrap = (kind == 'cyl')
FZ = [int(x) for x in sys.argv[4].split(',')]; Tmax = int(sys.argv[5]); tag = sys.argv[6]
rng = random.Random(seed)
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
FZs = sorted(FZ); CTX = sorted(C.ctx)
fzk = [r * W + f for r in range(H) for f in FZs]
def gen():
    while True:
        s = rng.randint(0, 1); sb = 1 - s
        up = 1 if s == 0 else -1     # s moves in direction up
        wps = set(); bps = set(); taken = set()
        def add(sq, col):
            (wps if col == 0 else bps).add(sq); taken.add(sq)
        # locked pairs: s pawn on rank r, s-bar pawn directly in front
        nl = rng.choice([0, 1, 1, 2])
        for _ in range(nl):
            f = rng.choice(CTX + FZs if rng.random() < 0.3 else CTX)
            r = rng.randint(1, H - 3) if s == 0 else rng.randint(2, H - 2)
            a = r * W + f; b = (r + up) * W + f
            if a in taken or b in taken or not (1 <= r + up <= H - 2): continue
            add(a, s); add(b, sb)
        # s-bar free Z-pawn(s), advanced
        for _ in range(rng.choice([1, 1, 2])):
            f = rng.choice(FZs); r = rng.randint(1, H - 2)
            if rng.random() < 0.7: r = (1 if sb == 1 else H - 2) + rng.choice([0, 0, 1, 2]) * (1 if sb == 1 else -1)
            r = min(max(r, 1), H - 2)
            sq = r * W + f
            if sq not in taken: add(sq, sb)
        # extra s pawns (Z or ctx) occasionally
        if rng.random() < 0.4:
            f = rng.choice(FZs + CTX); r = rng.randint(1, H - 2); sq = r * W + f
            if sq not in taken: add(sq, s)
        if len(wps) > 3 or len(bps) > 3: continue
        # cramped s king: edge / near pawns
        cand = [x for x in range(Bd.N) if x not in taken and (x // W in (0, H - 1) or (not wrap and x % W in (0, W - 1)) or any(Bd.kdist(x, p) <= 1 for p in taken))]
        sk = rng.choice(cand); bk = rng.choice(fzk)
        if bk in taken or sk == bk: continue
        wk, bkk = (sk, bk) if s == 0 else (bk, sk)
        pos = (wk, bkk, frozenset(wps), frozenset(bps), s, -1)
        if not Bd.legal_pos(pos): continue
        if any(not (C.inz(p) or (p % W) in C.ctx) for p in wps | bps): continue
        sbctx = [p for p in (bps if s == 0 else wps) if not C.inz(p)]
        if sk in Bd.attacked_by_pawns(sbctx, sb): continue
        return pos
rows = []; t0 = time.time(); nstale = 0
for i in range(N):
    Q = gen(); TP = C.minT(Q, Tmax)
    if TP is None: continue
    m0 = C.mu(Q, use_ep=False); m1 = C.mu(Q, use_ep=True)
    row = dict(Q=Bd.text(Q), TP=TP, m1=m1, T={})
    for T in range(TP, Tmax + 1):
        if m1 >= T + 1:
            h, fl = C.L3(Q, T); row['T'][T] = [bool(h), sorted(fl)]
            if 'stale' in fl: nstale += 1
    if not row['T']: continue
    rows.append(row)
    if len(C.lmemo) > 3_000_000: C.lmemo.clear()
qs = [r['Q'] for r in rows]
out = subprocess.run(["./kp", "--board", f"{kind}:{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"], input="\n".join(qs) + "\n", capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(rows)
n = bad = nf = nfdraw = 0
for r, l in zip(rows, out):
    parts = l.split("|")[1].split(); stm = 0 if r['Q'].split()[-2] == 'w' else 1
    letter = 'L' if stm == 0 else 'W'
    win = parts[0] == letter and parts[1] == letter
    for T, (h, fl) in r['T'].items():
        if h:
            n += 1
            if not win: bad += 1; print("COUNTEREXAMPLE", tag, r['Q'], "T", T, "mu", r['m1'], parts, flush=True)
        else:
            nf += 1
            if not win: nfdraw += 1
print(f"{tag} {sys.argv[3]} FZ={FZs} N={N} rows={len(rows)} LC(L3 holds)={n} nonwins={bad} | L3 fails (L1,L2 hold): {nf}, of which not P-wins {nfdraw} | stale-flag seen {nstale} | {time.time()-t0:.0f}s", flush=True)
