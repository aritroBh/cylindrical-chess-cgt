"""(Y, m, r) triples for Theorem 2.7(a): Y random per Definition 2.1 with s to move, m any non-promoting Z-move of s,
r any non-promoting Z-move of sbar keeping its king on F_Z.  Q = after m, r.  LC_T via own code; truth via kpm."""
import sys, random, subprocess, json, time
from hc import Geo, Cert
seed, NY = int(sys.argv[1]), int(sys.argv[2]); geo = sys.argv[3]; FZ = [int(x) for x in sys.argv[4].split(',')]
tag = sys.argv[5]; Tmax = int(sys.argv[6])
kind, wh = geo.split(':'); W, H = map(int, wh.split('x'))
g = Geo(W, H, kind == 'cyl'); C = Cert(g, FZ); rng = random.Random(seed)
FZl = sorted(C.FZ); ctxf = C.ctxfiles
zsq = [r * W + f for r in range(1, H - 1) for f in FZl]
csq = [r * W + f for r in range(1, H - 1) for f in ctxf]
fzk = [r * W + f for r in range(H) for f in FZl]
inFZ = C.inFZ
def adj(f):
    o = []
    for df in (-1, 1):
        ff = f + df
        if g.wrap: ff %= W
        elif not 0 <= ff < W: continue
        o.append(ff)
    return o
def rand_Y():
    while True:
        s = rng.randint(0, 1)
        wk = rng.choice(fzk); bk = rng.choice(fzk)
        nzs, nzb = rng.choice([0, 1, 1, 2]), rng.choice([0, 1, 1, 2])
        ncs, ncb = rng.choice([0, 1, 2, 3]), rng.choice([0, 1, 2, 3])
        if nzs + ncs > 3 or nzb + ncb > 3: continue
        pz = zsq[:]; rng.shuffle(pz); pc = csq[:]; rng.shuffle(pc)
        sp = set(pz[:nzs]) | set(pc[:ncs]); sbp = set(pz[nzs:nzs + nzb]) | set(pc[ncs:ncs + ncb])
        wp, bp = (sp, sbp) if s == 0 else (sbp, sp)
        ep = -1
        pos = (wk, bk, frozenset(wp), frozenset(bp), s, ep)
        if g.legal(pos): return pos
rows = {}
t0 = time.time()
for iy in range(NY):
    Y = rand_Y(); s = Y[4]; sbar = 1 - s
    for m in g.moves(Y):
        kind_, frm, to, promo, Ym, _ = m
        if promo: continue
        if kind_ == 'P' and not inFZ[frm]: continue
        for r in g.moves(Ym):
            k2, f2, t2, p2, Q, _ = r
            if p2: continue
            if k2 == 'K' and not inFZ[t2]: continue
            if k2 == 'P' and not inFZ[f2]: continue
            T1 = C.L1_T(Q, False, Tmax)
            if T1 is None: continue
            mu = C.mu(Q, Tmax + 2, True)
            Ts = []
            for T in range(T1, Tmax + 1):
                if mu >= T + 1:
                    ok, an = C.L3(Q, T, False)
                    if an: Ts.append(['ANOM', T])
                    if ok: Ts.append(T)
            if Ts:
                rows[g.text(Q)] = [g.text(Y), (kind_, g.name(frm), g.name(to)), (k2, g.name(f2), g.name(t2)), Ts]
    if iy % 100 == 0:
        if hasattr(C, '_l1cache') and len(C._l1cache): C._l1cache.clear()
        print("Y", iy, "LC Q", len(rows), "%.0fs" % (time.time() - t0), file=sys.stderr, flush=True)
keys = sorted(rows)
bad = []
for i in range(0, len(keys), 20000):
    part = keys[i:i + 20000]
    res = subprocess.run(["./kpm", "--board", geo, "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"], input="\n".join(part) + "\n", capture_output=True, text=True)
    lines = res.stdout.splitlines(); assert len(lines) == len(part), res.stderr[-300:]
    for q, l in zip(part, lines):
        pv = l.split("|")[1].split(); stm = 0 if q.split()[-2] == 'w' else 1
        win = pv[0] == pv[1] == ('L' if stm == 0 else 'W')
        if not win: bad.append((q, rows[q], pv))
json.dump(rows, open(f"tr_{tag}.json", "w"))
print(tag, geo, FZ, "Y", NY, "LC Q (distinct)", len(rows), "NON-WINS", len(bad), "anom", sum(1 for v in rows.values() if any(isinstance(t, list) for t in v[3])))
for b in bad[:5]: print(" CE", b)
