"""Exhaustive enumeration (small universe) of window positions Q (s = White to move; rank reflection + colour swap makes this wlog)
for Theorem 2.7(b).  Produces the list of positions where (L1_P),(L2 with e.p. clause),(L3) hold for some T <= Tmax.
usage: exh.py geo FZ Tmax nZs nZsb nCs nCsb out [part nparts]
   nZs  = max s Z-pawns, nZsb = max sbar Z-pawns, nCs = max s context pawns, nCsb = max sbar context pawns
"""
import sys, itertools, time, json
from hc import Geo, Cert

geo = sys.argv[1]; FZ = [int(x) for x in sys.argv[2].split(',')]; Tmax = int(sys.argv[3])
nZs, nZsb, nCs, nCsb = map(int, sys.argv[4:8]); out = sys.argv[8]
part = int(sys.argv[9]) if len(sys.argv) > 9 else 0
nparts = int(sys.argv[10]) if len(sys.argv) > 10 else 1
kind, wh = geo.split(':'); W, H = map(int, wh.split('x'))
g = Geo(W, H, kind == 'cyl'); C = Cert(g, FZ)
inFZ = C.inFZ
FZl = sorted(C.FZ)
interior = range(1, H - 1)
zsq = [r * W + f for r in interior for f in FZl]
csq = [r * W + f for r in interior for f in C.ctxfiles]
fzk = [r * W + f for r in range(H) for f in FZl]
S, SB = 0, 1   # s = White, sbar = Black
land = H - 4            # Black double-step landing rank (index)
skiprank = land + 1; origrank = land + 2

def subsets(pool, kmax):
    for k in range(kmax + 1):
        for c in itertools.combinations(pool, k):
            yield c

def adjf(f):
    out = []
    for df in (-1, 1):
        ff = f + df
        if g.wrap: ff %= W
        elif not (0 <= ff < W): continue
        out.append(ff)
    return out

t0 = time.time()
cnt = dict(qz=0, qz_ok=0, ctx=0, legal=0, lc=0)
found = {}
idx = 0
zs_sets = list(subsets(zsq, nZs)); zsb_sets = list(subsets(zsq, nZsb))
cs_sets = list(subsets(csq, nCs)); csb_sets = list(subsets(csq, nCsb))
for bk in fzk:
    for wk in range(g.N):
        if wk == bk or wk in g.knset[bk]: continue
        for zs in zs_sets:
            if wk in zs or bk in zs: continue
            for zsb in zsb_sets:
                if wk in zsb or bk in zsb or set(zs) & set(zsb): continue
                # e.p. on F_Z: a Black Z-pawn that has just double-stepped, with a White Z-pawn beside it
                ep_opts = [-1]
                for p in zsb:
                    if p // W == land:
                        skip = skiprank * W + p % W; orig = origrank * W + p % W
                        if skip in zs or skip in zsb or orig in zs or orig in zsb or skip in (wk, bk) or orig in (wk, bk): continue
                        if any((land * W + ff) in zs for ff in adjf(p % W)):
                            if not g.attacked_by_pawns(wk, {orig}, SB):
                                ep_opts.append(skip)
                for epz in ep_opts:
                    idx += 1
                    if idx % nparts != part: continue
                    cnt['qz'] += 1
                    QZ = (wk, bk, frozenset(zs), frozenset(zsb), S, epz)
                    if not g.legal(QZ): continue
                    T1 = C.L1_T(QZ, False, Tmax)
                    if T1 is None: continue
                    cnt['qz_ok'] += 1
                    for cs in cs_sets:
                        if wk in cs or bk in cs: continue
                        cs_f = frozenset(cs)
                        for csb in csb_sets:
                            if wk in csb or bk in csb or set(cs) & set(csb): continue
                            # context e.p. options (target off F_Z): a Black ctx pawn at the landing rank with an adjacent White ctx pawn
                            ep_c = [-1]
                            if epz < 0:
                                for p in csb:
                                    if p // W == land:
                                        skip = skiprank * W + p % W; orig = origrank * W + p % W
                                        occ = set(cs) | set(csb) | {wk, bk} | set(zs) | set(zsb)
                                        if skip in occ or orig in occ: continue
                                        if any((land * W + ff) in cs for ff in adjf(p % W)) and not g.attacked_by_pawns(wk, {orig}, SB):
                                            ep_c.append(skip)
                            for epc in ep_c:
                                ep = epz if epz >= 0 else epc
                                cnt['ctx'] += 1
                                Q = (wk, bk, frozenset(zs) | cs_f, frozenset(zsb) | frozenset(csb), S, ep)
                                if not g.legal(Q): continue
                                # s king must not be attacked by an sbar context pawn
                                if g.attacked_by_pawns(wk, set(csb), SB): continue
                                cnt['legal'] += 1
                                mu = C.mu(Q, Tmax + 1, True)
                                if mu < T1 + 1: continue
                                Ts = []
                                for T in range(T1, Tmax + 1):
                                    if mu >= T + 1:
                                        ok, an = C.L3(Q, T, False)
                                        if an: Ts.append(('ANOM', T))
                                        if ok: Ts.append(T)
                                if Ts:
                                    cnt['lc'] += 1
                                    found[g.text(Q)] = [T1, mu, Ts]
                    if cnt['qz_ok'] % 200 == 0:
                        C._l1cache.clear() if hasattr(C, '_l1cache') else None
                        print("%.0fs" % (time.time() - t0), cnt, file=sys.stderr, flush=True)
json.dump(found, open(out, 'w'))
print("DONE", cnt, "positions with LC:", len(found), "%.0fs" % (time.time() - t0))
