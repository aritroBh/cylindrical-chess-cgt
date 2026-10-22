"""(a)-form: random Y (kings on F_Z), every non-promoting Z-move m of s, every admissible reply r; LC_T at Q=Y.m.r ?  then s-bar must win P after m.
usage: hunt_a.py seed N board FZ Tmax maxp pep tag"""
import sys, random, subprocess, json, time
from kb import B
from cert import Cert
seed, N = int(sys.argv[1]), int(sys.argv[2])
kind, dims = sys.argv[3].split(':'); W, H = map(int, dims.split('x')); wrap = (kind == 'cyl')
FZ = [int(x) for x in sys.argv[4].split(',')]
Tmax = int(sys.argv[5]); maxp = int(sys.argv[6]); pep = float(sys.argv[7]); tag = sys.argv[8]
rng = random.Random(seed)
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
FZs = sorted(FZ); CTX = sorted(C.ctx)
zsq = [r * W + f for r in range(1, H - 1) for f in FZs]
csq = [r * W + f for r in range(1, H - 1) for f in CTX]
fzk = [r * W + f for r in range(H) for f in FZs]
def pick(pool, k, taken):
    pool = [x for x in pool if x not in taken]; rng.shuffle(pool); return pool[:k]
def genY():
    while True:
        s = rng.randint(0, 1); sb = 1 - s
        zs, zb, cs, cb = [rng.choice([0, 1, 1, 2, 2]) for _ in range(4)]
        if zb == 0: zb = 1
        taken = set()
        sbz = pick(zsq, zb, taken); taken |= set(sbz)
        szp = pick(zsq, zs, taken); taken |= set(szp)
        scp = pick(csq, cs, taken); taken |= set(scp)
        sbc = pick(csq, cb, taken); taken |= set(sbc)
        ep = -1
        if rng.random() < pep:
            f = rng.choice(CTX); land = 3 if sb == 0 else H - 4
            lsq = land * W + f; skip = (land - 1 if sb == 0 else land + 1) * W + f; orig = (land - 2 if sb == 0 else land + 2) * W + f
            if lsq not in taken and skip not in taken and orig not in taken:
                taken.add(lsq); sbc.append(lsq)
                nf = rng.choice([(f - 1) % W, (f + 1) % W]) if wrap else rng.choice([x for x in (f - 1, f + 1) if 0 <= x < W])
                nsq = land * W + nf
                if nsq not in taken and nf in C.ctx: taken.add(nsq); scp.append(nsq)
                ep = skip
        sk = rng.choice(fzk); bkk = rng.choice(fzk)
        if sk in taken or bkk in taken or sk == bkk: continue
        wk, bk = (sk, bkk) if s == 0 else (bkk, sk)
        wp = frozenset((szp + scp) if s == 0 else (sbz + sbc)); bp = frozenset((sbz + sbc) if s == 0 else (szp + scp))
        if len(wp) > maxp or len(bp) > maxp: continue
        pos = (wk, bk, wp, bp, s, ep)
        if not Bd.legal_pos(pos): continue
        if ep >= 0:
            orig = ep + (-W if sb == 0 else W)
            if ep in (wk, bk) or orig in (wk, bk): continue
            if sk in Bd.att[sb][orig]: continue
            if not any(ep in Bd.att[s][p] for p in (bp if s == 0 else wp)): continue
        return pos
rows = []; t0 = time.time(); nY = 0
for i in range(N):
    Y = genY(); s = Y[4]; sb = 1 - s
    found = 0
    for kind_m, frm, to, promo, Qm in Bd.moves(Y):
        if promo: continue
        # Z-move: king move or a pawn on F_Z
        if kind_m == 'P' and not C.inz(frm): continue
        # r: admissible replies
        for kind_r, frm2, to2, promo2, Q in Bd.moves(Qm):
            if promo2: continue
            if kind_r == 'P' and not C.inz(frm2): continue
            if kind_r == 'K' and not C.inz(to2): continue
            TP = C.minT(Q, Tmax)
            if TP is None: continue
            m1 = C.mu(Q, True)
            for T in range(TP, Tmax + 1):
                if m1 >= T + 1:
                    h, fl = C.L3(Q, T)
                    if h:
                        rows.append(dict(Y=Bd.text(Y), m=Bd.name(frm) + Bd.name(to), r=Bd.name(frm2) + Bd.name(to2), Qm=Bd.text(Qm), Q=Bd.text(Q), T=T, mu=m1, fl=sorted(fl)))
                        found += 1
                    break   # smallest T holding is enough; larger T only strengthens L3 differently -> also test the next
    nY += 1
    if len(C.lmemo) > 3_000_000: C.lmemo.clear()
t1 = time.time()
qs = [r['Qm'] for r in rows] + [r['Q'] for r in rows]
out = subprocess.run(["./kp", "--board", f"{kind}:{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input="\n".join(qs) + "\n", capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(qs)
n = len(rows); bad = 0; tight = 0
for i, r in enumerate(rows):
    for j, tagq in ((i, 'Qm'), (n + i, 'Q')):
        parts = out[j].split("|")[1].split()
        stm = 0 if r[tagq].split()[-2] == 'w' else 1
        # s-bar wins: after m the mover is s-bar; at Q the mover is s
        sbwin_letter = 'W' if (1 - int(r['Y'].split()[-2] == 'b')) is None else None
        sb_col = 1 - (0 if r['Y'].split()[-2] == 'w' else 1)          # colour index of s-bar
        letter = 'W' if sb_col == 0 else 'L'
        win = parts[0] == letter and parts[1] == letter
        r['P_' + tagq] = parts
        if not win:
            bad += 1; print("COUNTEREXAMPLE(a)", tag, r, flush=True)
    if r['mu'] == r['T'] + 1: tight += 1
json.dump(rows, open(f"rowsA_{tag}.json", "w"))
print(f"{tag} (a)-form {sys.argv[3]} FZ={FZs} Y={nY} triples-with-LC={n} (tight {tight}) nonwins={bad} gen {t1-t0:.0f}s", flush=True)
