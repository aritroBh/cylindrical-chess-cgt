"""My own (second-round referee) twin check.  usage: mytwin.py gen <spec> <hits.json> <pre>  -> <pre>.tin (ref3m queries)
                                                   mytwin.py eval <spec> <hits.json> <pre> <pre>.tout
For each real-king hit (X: Black king b(r+1) in check from Pa(r)), the twins have the Black king on b(r+2) or b(r).
A twin is CLEAN iff: both sides to move legal; at every chess-reachable position Y before the first decisive event
(context pawn moves only; decisive = a context pawn is passed after the move) : V1a (legal non-Z moves == D-options,
which includes 'no check'), V1b (a legal move exists), V2 (decisive events are P-wins for the beneficiary), V3 (every Z
move loses for the mover in P), V4 (HSS: all re-split components pairwise safe at every reachable Y), and P == D at the root for both sides."""
import sys, json, re
from functools import lru_cache
from myd import *
spec = sys.argv[2]; kind, dims = spec.split(':'); w, h = map(int, dims.split('x')); bd = Bd(w, h, kind == 'cyl'); whole = make(bd)
FZ = {0, 1}
def nm(s): return 'abcdefgh'[s[0]] + str(s[1])
def parse(t): return ('abcdefgh'.index(t[0]), int(t[1:]))
def parse_hit(s):
    t = s.split()[:-2]; wk = bk = None; wz = []; bz = []; W = set(); B = set()
    for x in t:
        sq = parse(x[1:])
        if x[0] == 'K': wk = sq
        elif x[0] == 'k': bk = sq
        elif x[0] == 'P': (wz if sq[0] in FZ else W).add(sq) if False else (wz.append(sq) if sq[0] in FZ else W.add(sq))
        else: (bz.append(sq) if sq[0] in FZ else B.add(sq))
    return wk, bk, wz, bz, frozenset(W), frozenset(B)
def tostr(wk, bk, wz, bz, pos, s):
    W, B, ep = pos
    toks = ['K' + nm(wk), 'k' + nm(bk)] + ['P' + nm(x) for x in wz] + ['p' + nm(x) for x in bz] + ['P' + nm(x) for x in sorted(W)] + ['p' + nm(x) for x in sorted(B)]
    e = '-'
    if ep is not None and ep[1] == s:
        v = ep[0]; d = 1 if ep[1] == 'B' else -1   # victim belongs to the other side of capturer
        e = nm((v[0], v[1] - d)) if ep[1] == 'B' else nm((v[0], v[1] - d))
    return ' '.join(toks) + (' w ' if s == 'W' else ' b ') + e
def reach(root, s):
    seen = {}; st = [(root, s)]
    while st:
        k = st.pop()
        if k in seen: continue
        p, side = k; o = 'B' if side == 'W' else 'W'; ev = []
        for c in moves(bd, p, side):
            ben = outcome_after(bd, c, side); ev.append((c, ben))
            if ben is None and (c, o) not in seen: st.append((c, o))
        seen[k] = ev
    return seen
def twins(wk, bk, r):
    out = []
    import os
    for rr in ((r + 2,) if os.environ.get('ONLYUP') else (r + 2, r)):
        if 1 <= rr <= h: out.append((1, rr))
    return out
def comps(p):
    W, B, ep = p
    occ = sorted({f for f, _ in W | B})
    if not occ: return []
    gr = []
    for f in occ:
        if gr and f == gr[-1][-1] + 1: gr[-1].append(f)
        else: gr.append([f])
    if bd.wrap and len(gr) > 1 and gr[0][0] == 0 and gr[-1][-1] == bd.w - 1: gr[0] = gr.pop() + gr[0]
    res = []
    for g in gr:
        fs = set(g); res.append((frozenset(x for x in W if x[0] in fs), frozenset(x for x in B if x[0] in fs), ep if (ep and ep[0][0] in fs) else None))
    return res
@lru_cache(maxsize=None)
def tau(p):
    out = set()
    if passed(bd, p[0], p[1], p[2], 'W'): out.add(1)
    if passed(bd, p[0], p[1], p[2], 'B'): out.add(-1)
    if not out:
        for s in 'WB':
            for c in moves(bd, p, s): out |= tau(c)
    return frozenset(out)
def safe(p):
    ts = [tau(c) for c in comps(p)]
    return not any(i != j and 1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts))
def hss(root, s): return all(safe(p) for (p, _) in reach(root, s))
def fromto(a, b, side):
    A = a[0] if side == 'W' else a[1]; Bn = b[0] if side == 'W' else b[1]
    fr = A - Bn; to = Bn - A
    return (next(iter(fr)), next(iter(to)))

if sys.argv[1] == 'gen':
    hits = json.load(open(sys.argv[3])); qs = set()
    for hs in hits:
        wk, bk, wz, bz, W, B = parse_hit(hs); r = wz[0][1]; root = (W, B, None)
        for t in twins(wk, bk, r):
            for s in 'WB':
                for (p, side) in reach(root, s): qs.add(tostr(wk, t, wz, bz, p, side))
        qs.add(hs)
    open(sys.argv[4] + '.tin', 'w').write('\n'.join(sorted(qs)) + '\n'); print('queries', len(qs))
else:
    hits = json.load(open(sys.argv[3])); R = {}
    for ln in open(sys.argv[5]):
        if ' | ' not in ln: continue
        pos, rest = ln.rstrip('\n').split(' | ', 1); tk = rest.split()
        R[pos] = (tk[0], [(m[:-2], m[-1]) for m in tk[1:]])
    nclean = 0; nhss = 0; nx_ok = 0; why = {}
    cleanlist = []
    for hs in hits:
        wk, bk, wz, bz, W, B = parse_hit(hs); r = wz[0][1]; root = (W, B, None)
        h_ok = hss(root, 'B') and hss(root, 'W'); nhss += h_ok
        anyclean = False
        for t in twins(wk, bk, r):
            ok = True; reason = ''
            for s in 'WB':
                if R[tostr(wk, t, wz, bz, root, s)][0] == 'X': ok = False; reason = 'illegal'
            if not ok: why[reason] = why.get(reason, 0) + 1; continue
            for s in 'WB':
                head = R[tostr(wk, t, wz, bz, root, s)][0]
                dw = whole(root, s); dwv = 'W' if dw == 'W' else 'L'
                if head != dwv: ok = False; reason = 'P!=D'
                for (p, side), ev in reach(root, s).items():
                    key = tostr(wk, t, wz, bz, p, side); hd, mv = R[key]
                    if not mv: ok = False; reason = 'V1b'
                    nonz = {}; 
                    for m, v in mv:
                        fr, to = parse(m[1:3]), parse(m[3:5])
                        isz = m[0] in 'Kk' or fr[0] in FZ
                        if isz:
                            lose = 'L' if side == 'W' else 'W'
                            if v != lose: ok = False; reason = 'V3'
                        else: nonz[(fr, to)] = v
                    dopt = {fromto(p, c, side): ben for c, ben in ev}
                    if set(nonz) != set(dopt): ok = False; reason = 'V1a'
                    for k_, ben in dopt.items():
                        if ben is not None and k_ in nonz:
                            if nonz[k_] != ('W' if ben == 'W' else 'L'): ok = False; reason = 'V2'
                    if not safe(p): ok = False; reason = 'V4'
            if not ok: why[reason] = why.get(reason, 0) + 1
            if ok: anyclean = True
        nclean += anyclean
        if anyclean: cleanlist.append(hs)
    print('hits', len(hits), 'hss-true hits', nhss, 'hits with a clean twin', nclean, 'fail reasons (per twin)', why)
    json.dump(cleanlist, open(sys.argv[4] + '.clean.json', 'w'))
