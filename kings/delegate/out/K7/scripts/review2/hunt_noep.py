"""Random structured hunt for counterexamples to Theorem 2.7(b) (final version).
usage: hunt.py seed N geo FZspec tag Tmax [epfrac]
   geo = cyl:7x6 | flat:6x6 ...;   FZspec = comma list of file indices, e.g. 0,1,2  or  2,3 (any arc / interval)
"""
import sys, random, subprocess, json, time
from hc import Geo, Cert

seed, N = int(sys.argv[1]), int(sys.argv[2])
geo = sys.argv[3]; FZ = [int(x) for x in sys.argv[4].split(',')]
tag = sys.argv[5]; Tmax = int(sys.argv[6])
epfrac = float(sys.argv[7]) if len(sys.argv) > 7 else 0.5
maxp = int(sys.argv[8]) if len(sys.argv) > 8 else 3
kind, wh = geo.split(':'); W, H = map(int, wh.split('x'))
g = Geo(W, H, kind == 'cyl')
C = Cert(g, FZ)
rng = random.Random(seed)
ctxf, bufff = C.ctxfiles, C.bufffiles
assert ctxf, "no context files"
FZl = sorted(C.FZ)
interior = range(1, H - 1)
zsq = [r * W + f for r in interior for f in FZl]
csq = [r * W + f for r in interior for f in ctxf]
fzk = [r * W + f for r in range(H) for f in FZl]
allk = list(range(g.N))

def adj_files(f):
    out = []
    for df in (-1, 1):
        ff = f + df
        if g.wrap: ff %= W
        elif not (0 <= ff < W): continue
        out.append(ff)
    return out

def rand_Q():
    while True:
        s = rng.randint(0, 1); sbar = 1 - s
        mode = rng.random()
        sk = rng.choice(allk) if rng.random() < 0.75 else rng.choice(fzk)
        bk_ = rng.choice(fzk)
        nzs = rng.choice([0, 0, 1, 1, 2]); nzb = rng.choice([0, 1, 1, 2])
        ncs = rng.choice([0, 1, 1, 2, 2, 3]); ncb = rng.choice([0, 1, 1, 2, 2, 3])
        if nzs + ncs > maxp or nzb + ncb > maxp:
            continue
        pz = zsq[:]; rng.shuffle(pz); pc = csq[:]; rng.shuffle(pc)
        s_z = pz[:nzs]; sb_z = pz[nzs:nzs + nzb]; s_c = pc[:ncs]; sb_c = pc[ncs:ncs + ncb]
        spawns = set(s_z + s_c); sbpawns = set(sb_z + sb_c)
        ep = -1
        if rng.random() < epfrac:
            on_ctx = rng.random() < 0.7
            files = ctxf if on_ctx else FZl
            f = rng.choice(files)
            land = 3 if sbar == 0 else H - 4
            if land < 1 or land > H - 2: continue
            skip = (land - 1 if sbar == 0 else land + 1) * W + f
            orig = (land - 2 if sbar == 0 else land + 2) * W + f
            lsq = land * W + f
            sbpawns.add(lsq)
            if rng.random() < 0.85:
                cand = [ff for ff in adj_files(f) if (ff in ctxf if on_ctx else ff in C.FZ)]
                if cand:
                    spawns.add(land * W + rng.choice(cand))
            ep = skip
        else:
            skip = orig = None
        if len(spawns) > maxp or len(sbpawns) > maxp: continue
        wp, bp = (spawns, sbpawns) if s == 0 else (sbpawns, spawns)
        wk, bk = (sk, bk_) if s == 0 else (bk_, sk)
        pos = (wk, bk, frozenset(wp), frozenset(bp), s, ep)
        if ep >= 0:
            occ = set([wk, bk]) | wp | bp
            if skip in occ or orig in occ: continue
        if not g.legal(pos): continue
        # window-form hypotheses
        if any(((p % W) not in C.FZ and (p % W) not in ctxf) for p in list(wp) + list(bp)): continue
        sb_ctx = [p for p in sbpawns if (p % W) not in C.FZ]
        if g.attacked_by_pawns(sk, set(sb_ctx), sbar): continue
        if ep >= 0 and g.attacked_by_pawns(sk, {orig}, sbar): continue   # s king was not in check before the double step
        return pos

rows = []
t0 = time.time()
stat = dict(n=0, L1=0, lc=0)
for i in range(N):
    Q = rand_Q()
    stat['n'] += 1
    T1 = C.L1_T(Q, False, Tmax)       # (L1_P) : no queen clause
    if T1 is None:
        continue
    T1q = C.L1_T(Q, True, Tmax)
    stat['L1'] += 1
    m_ep = C.mu(Q, Tmax + 2, False)
    m_no = C.mu(Q, Tmax + 2, False)
    ent = dict(Q=g.text(Q), T1=T1, T1q=T1q, m_ep=m_ep, m_no=m_no, L3={})
    for T in range(T1, Tmax + 1):
        # compute L3 only if mu allows (to save time) -- also record L3 when mu fails for diagnostics at T1 only
        if m_ep >= T + 1 or T == T1:
            ok, anom = C.L3(Q, T, False)
            ent['L3'][T] = [bool(ok), anom]
    rows.append(ent)
    if len(C._l1cache) and i % 400 == 0:
        # keep memory down
        if len(rows) % 5 == 0:
            C._l1cache.clear()
    if i % 500 == 0:
        print("gen", i, "rows", len(rows), "%.0fs" % (time.time() - t0), file=sys.stderr, flush=True)

inp = "\n".join(r['Q'] for r in rows) + "\n"
out = subprocess.run(["./kpm", "--board", geo, "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input=inp, capture_output=True, text=True)
if out.returncode: print(out.stderr[-500:])
out = out.stdout.splitlines()
assert len(out) == len(rows), (len(out), len(rows))
nlc = 0; bad = []
anoms = []
for r, line in zip(rows, out):
    parts = line.split("|")[1].split()
    stm = 0 if r['Q'].split()[-2] == 'w' else 1
    win = parts[0] == parts[1] and parts[0] == ('L' if stm == 0 else 'W')
    r['P'] = parts; r['win'] = win
    for T, (ok, an) in r['L3'].items():
        if an and r['m_ep'] >= T + 1: anoms.append((r['Q'], T, r['m_ep'], an))
        if ok and r['m_ep'] >= T + 1:
            nlc += 1
            if not win:
                bad.append((r['Q'], T, r['m_ep'], parts))
json.dump(rows, open(f"hunt_{tag}.json", "w"))
print(tag, geo, "FZ", FZ, "gen", stat['n'], "L1_P holds", len(rows), "LC pairs", nlc, "COUNTEREXAMPLES", len(bad), "anomalies(s promotes in guided play)", len(anoms))
for b in bad[:10]: print("  CE", b)
for a in anoms[:5]: print("  ANOM", a)
