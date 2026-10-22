"""usage: hunt.py seed N board(cyl:7x6|flat:6x6) FZ(e.g. 0,1,2) Tmax maxp pep mode tag
mode: any | tight (keep only mu==T+1) ; pep = probability of an e.p. right at Q"""
import sys, random, subprocess, json, time
from kb import B
from cert import Cert
seed, N = int(sys.argv[1]), int(sys.argv[2])
kind, dims = sys.argv[3].split(':'); W, H = map(int, dims.split('x')); wrap = (kind == 'cyl')
FZ = [int(x) for x in sys.argv[4].split(',')]
Tmax = int(sys.argv[5]); maxp = int(sys.argv[6]); pep = float(sys.argv[7]); mode = sys.argv[8]; tag = sys.argv[9]
rng = random.Random(seed)
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
FZs = sorted(FZ); CTX = sorted(C.ctx)
zsq = [r * W + f for r in range(1, H - 1) for f in FZs]
csq = [r * W + f for r in range(1, H - 1) for f in CTX]
allsq = list(range(Bd.N)); fzk = [r * W + f for r in range(H) for f in FZs]

def pick(pool, k, taken):
    pool = [x for x in pool if x not in taken]
    rng.shuffle(pool)
    return pool[:k]

def gen():
    for _ in range(10000):
        s = rng.randint(0, 1); sb = 1 - s
        cnt = lambda: rng.choice([0, 1, 1, 2, 2, 3]) if maxp >= 3 else rng.choice([0, 1, 1, 2])
        zs, zb, cs, cb = [min(maxp, cnt()) for _ in range(4)]
        if zb + cb == 0: zb = 1
        if zs + cs > maxp: cs = max(0, maxp - zs)
        if zb + cb > maxp: cb = max(0, maxp - zb)
        taken = set()
        # advanced s-bar Z-pawns (promotion soon) with high probability
        sbz = []
        for _i in range(zb):
            cand = [x for x in zsq if x not in taken]
            if rng.random() < 0.7:
                # advanced for s-bar: low ranks if s-bar is Black (sb==1), high ranks if White
                key = (lambda x: (x // W)) if sb == 0 else (lambda x: -(x // W))
                cand.sort(key=lambda x: -key(x) + rng.random() * 1.5)
            else: rng.shuffle(cand)
            x = cand[0]; sbz.append(x); taken.add(x)
        szp = pick(zsq, zs, taken); taken |= set(szp)
        scp = pick(csq, cs, taken); taken |= set(scp)
        sbc = pick(csq, cb, taken); taken |= set(sbc)
        # e.p. right created by s-bar's last double step
        ep = -1
        if rng.random() < pep:
            mode_ep = rng.choice(['ctx', 'ctx', 'z'])
            files = CTX if mode_ep == 'ctx' else FZs
            f = rng.choice(files)
            land = 3 if sb == 0 else H - 4
            if 1 <= land <= H - 2:
                lsq = land * W + f
                skip = (land - 1 if sb == 0 else land + 1) * W + f
                orig = (land - 2 if sb == 0 else land + 2) * W + f
                if lsq not in taken and skip not in taken and orig not in taken:
                    taken |= {lsq}
                    (sbc if mode_ep == 'ctx' else sbz).append(lsq)
                    if rng.random() < 0.85:
                        nf = rng.choice([(f - 1) % W, (f + 1) % W]) if wrap else rng.choice([x for x in (f - 1, f + 1) if 0 <= x < W])
                        nsq = land * W + nf
                        if nsq not in taken and (nf in C.FZ or nf in C.ctx):
                            taken.add(nsq); (szp if nf in C.FZ else scp).append(nsq)
                    ep = skip
        if len(sbz) + len(sbc) > maxp or len(szp) + len(scp) > maxp: continue
        # kings
        skpool = allsq if rng.random() < 0.6 else fzk
        # near-context bias for s king
        if rng.random() < 0.5 and (scp or sbc):
            tgt = rng.choice(scp + sbc)
            skpool = [x for x in allsq if Bd.kdist(x, tgt) <= 2]
        sk = rng.choice(skpool); bkk = rng.choice(fzk)
        if sk in taken or bkk in taken or sk == bkk: continue
        wk, bk = (sk, bkk) if s == 0 else (bkk, sk)
        wp = frozenset((szp + scp) if s == 0 else (sbz + sbc)); bp = frozenset((sbz + sbc) if s == 0 else (szp + scp))
        if len(wp) > maxp or len(bp) > maxp: continue
        pos = (wk, bk, wp, bp, s, ep)
        if not Bd.legal_pos(pos): continue
        sbctx = [p for p in (bp if s == 0 else wp) if not C.inz(p)]
        if sk in Bd.attacked_by_pawns(sbctx, sb): continue
        if ep >= 0:
            d = -1 if sb == 0 else 1  # origin is two ranks back for sb
            orig = ep + (-W if sb == 0 else W)
            if sk in Bd.att[sb][orig]: continue
            if ep in (wk, bk) or orig in (wk, bk): continue
            lsq2 = ep + (W if sb == 0 else -W)
            spawns = bp if s == 0 else wp
            if not any(ep in Bd.att[s][p] for p in spawns): continue
            # the s-bar king must not be adjacent... (retro) ignore
        return pos
    raise RuntimeError

rows = []; t0 = time.time(); stats = dict(L1=0)
for i in range(N):
    Q = gen()
    TP = C.minT(Q, Tmax)
    if TP is None: continue
    stats['L1'] += 1
    m0 = C.mu(Q, use_ep=False); m1 = C.mu(Q, use_ep=True)
    row = dict(Q=Bd.text(Q), TP=TP, m0=m0, m1=m1, T={})
    for T in range(TP, Tmax + 1):
        if m1 >= T + 1 or m0 >= T + 1:
            h, fl = C.L3(Q, T)
            row['T'][T] = [bool(h), sorted(fl)]
    if not row['T']: continue
    if mode == 'tight' and not any(m1 == T + 1 for T in row['T']): continue
    rows.append(row)
    if len(C.lmemo) > 3_000_000: C.lmemo.clear()
t1 = time.time()
qs = [r['Q'] for r in rows]
out = subprocess.run(["./kp", "--board", f"{kind}:{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input="\n".join(qs) + "\n", capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(rows), (len(out), len(rows))
n_lc = n_bad = n_lc_old = n_bad_old = n_tight = n_tight_bad = 0; n_flag = 0
for r, l in zip(rows, out):
    parts = l.split("|")[1].split(); stm = 0 if r['Q'].split()[-2] == 'w' else 1
    sbwin = 'L' if stm == 0 else 'W'   # result letter (White POV) meaning s-bar wins
    win = parts[0] == sbwin and parts[1] == sbwin
    r['P'] = parts; r['win'] = win
    for T, (h, fl) in r['T'].items():
        T = int(T)
        if not h: continue
        if 'spromo' in fl and r['m1'] >= T + 1:
            n_flag += 1; print("SPROMO-IN-LC", tag, r['Q'], "T", T, "mu", r['m1'], parts, flush=True)
        if r['m0'] >= T + 1:
            n_lc_old += 1
            if not win: n_bad_old += 1
        if r['m1'] >= T + 1:
            n_lc += 1
            if r['m1'] == T + 1: n_tight += 1
            if not win:
                n_bad += 1
                print("COUNTEREXAMPLE", tag, r['Q'], "T", T, "mu", r['m1'], parts, flush=True)
            if r['m1'] == T + 1 and not win: n_tight_bad += 1
json.dump(rows, open(f"rows_{tag}.json", "w"))
print(f"{tag} {sys.argv[3]} FZ={FZs} N={N} L1={stats['L1']} rows={len(rows)} LC_new={n_lc} (tight {n_tight}) nonwins_new={n_bad} | LC_noEPclause={n_lc_old} nonwins={n_bad_old} | spromo-flag={n_flag} | gen {t1-t0:.0f}s total {time.time()-t0:.0f}s", flush=True)
