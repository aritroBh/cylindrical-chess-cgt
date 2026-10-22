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
        d = 1 if s == 0 else -1
        # s context pawn p with an sbar blocker in front (usually), king nearby to capture it
        f = rng.choice(ctxf)
        rs = rng.randint(1, H - 3) if s == 0 else rng.randint(2, H - 2)
        p = rs * W + f
        spawns = {p}; sbpawns = set()
        r_b = rs + d
        if 1 <= r_b <= H - 2 and rng.random() < 0.8:
            sbpawns.add(r_b * W + f)
        # optional guards / extra context pawns
        for _ in range(rng.choice([0, 1, 2])):
            ff = rng.choice(ctxf); rr = rng.randint(1, H - 2)
            (spawns if rng.random() < 0.5 else sbpawns).add(rr * W + ff)
        # Z pawns
        pz = zsq[:]; rng.shuffle(pz)
        nzs = rng.choice([0, 0, 1]); nzb = rng.choice([1, 1, 2])
        sz = pz[:nzs]; sbz = pz[nzs:nzs + nzb]
        spawns |= set(sz); sbpawns |= set(sbz)
        # kings
        blk = list(sbpawns - set(sbz))
        anchor = rng.choice(blk) if blk else p
        near = [q for q in allk if g.fdist(q % W, anchor % W) <= 3 and abs(q // W - anchor // W) <= 3]
        sk = rng.choice(near) if rng.random() < 0.85 else rng.choice(allk)
        bk_ = rng.choice(fzk)
        ep = -1; skip = orig = None
        if rng.random() < epfrac:
            on_ctx = rng.random() < 0.7
            files = ctxf if on_ctx else FZl
            ff = rng.choice(files)
            land = 3 if sbar == 0 else H - 4
            if 1 <= land <= H - 2:
                skip = (land - 1 if sbar == 0 else land + 1) * W + ff
                orig = (land - 2 if sbar == 0 else land + 2) * W + ff
                sbpawns.add(land * W + ff)
                if rng.random() < 0.85:
                    cand = [x for x in adj_files(ff) if (x in ctxf if on_ctx else x in C.FZ)]
                    if cand: spawns.add(land * W + rng.choice(cand))
                ep = skip
        if len(spawns) > maxp or len(sbpawns) > maxp: continue
        wp, bp = (spawns, sbpawns) if s == 0 else (sbpawns, spawns)
        wk, bk = (sk, bk_) if s == 0 else (bk_, sk)
        pos = (wk, bk, frozenset(wp), frozenset(bp), s, ep)
        if ep >= 0:
            occ = set([wk, bk]) | wp | bp
            if skip in occ or orig in occ: continue
        if not g.legal(pos): continue
        if any(((q % W) not in C.FZ and (q % W) not in ctxf) for q in list(wp) + list(bp)): continue
        sb_ctx = [q for q in sbpawns if (q % W) not in C.FZ]
        if g.attacked_by_pawns(sk, set(sb_ctx), sbar): continue
        if ep >= 0 and g.attacked_by_pawns(sk, {orig}, sbar): continue
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
    m_ep = C.mu(Q, Tmax + 2, True)
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
