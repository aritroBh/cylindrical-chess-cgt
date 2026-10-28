"""My own re-run of the clause-(E) search.  usage: myecl.py <spec> <files> <maxp> [sample_os]
Roots: context pawns (>=1 per side, ranks 2..H-1, no passer) plus a FRESH e.p. right owned by the side s to move (the other
side has just double-stepped next to a pawn of s, both skipped squares empty), s to move, no passer at the root.
D_whole = whole-board game with chess e.p. (right lasts one move);  D_fix = disjunctive sum of the ROOT components (files
separated by an empty file) with component-local rights that persist while other components are played;  HSS = every
alternating-reachable non-decisive position has pairwise safe re-split components (tau by either player)."""
import sys, itertools, time
from functools import lru_cache
from myd import *
spec = sys.argv[1]; files = [int(x) for x in sys.argv[2].split(',')]; maxp = int(sys.argv[3])
kind, dims = spec.split(':'); w, h = map(int, dims.split('x')); bd = Bd(w, h, kind == 'cyl'); whole = make(bd)
def nm(s): return 'abcdefgh'[s[0]] + str(s[1])
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
def hss(root, s):
    seen = set(); st = [(root, s)]
    while st:
        k = st.pop()
        if k in seen: continue
        seen.add(k); p, side = k
        if not safe(p): return False
        o = 'B' if side == 'W' else 'W'
        for c in moves(bd, p, side):
            if outcome_after(bd, c, side) is None and (c, o) not in seen: st.append((c, o))
    return True
ck = lambda c: (sorted(c[0] | c[1]), str(c[2]))
@lru_cache(maxsize=None)
def dfix(cs, s):
    o = 'B' if s == 'W' else 'W'
    for i, c in enumerate(cs):
        for n in moves(bd, c, s):          # moves() drops a right owned by the other side
            t = outcome_after(bd, n, s)
            if t == s: return s
            if t is None and dfix(tuple(sorted(cs[:i] + (n,) + cs[i + 1:], key=ck)), o) == s: return s
    return o
t0 = time.time(); n = nroots = nmulti = nh = nhm = 0; diffs = []; sample = []
sqs = [(f, r) for f in files for r in range(2, h)]
for nw in range(1, maxp + 1):
    for ws in itertools.combinations(sqs, nw):
        rest = [x for x in sqs if x not in ws]
        for nb in range(1, maxp + 1):
            for bs in itertools.combinations(rest, nb):
                W, B = frozenset(ws), frozenset(bs)
                if passed(bd, W, B, None, 'W') or passed(bd, W, B, None, 'B'): continue
                n += 1; occ = W | B
                for s in 'WB':
                    o = 'B' if s == 'W' else 'W'
                    mine, theirs = (W, B) if s == 'W' else (B, W)
                    dest = 4 if o == 'W' else h - 3; r0 = 2 if o == 'W' else h - 1; r1 = 3 if o == 'W' else h - 2
                    for (f, r) in theirs:
                        if r != dest or (f, r1) in occ or (f, r0) in occ: continue
                        if not any(bd.f(f + d) is not None and (bd.f(f + d), r) in mine for d in (-1, 1)): continue
                        q = (W, B, ((f, r), s))
                        if passed(bd, W, B, q[2], 'W') or passed(bd, W, B, q[2], 'B'): continue
                        nroots += 1; cs = comps(q); multi = len(cs) >= 2; nmulti += multi
                        dw = 'W' if whole(q, s) == 'W' else 'L'; df = 'W' if dfix(tuple(sorted(cs, key=ck)), s) == 'W' else 'L'
                        hs = hss(q, s)
                        if hs: nh += 1; nhm += multi; sample.append((q, s, dw))
                        if dw != df: diffs.append((q, s, dw, df, hs))
print(spec, files, maxp, 'contexts', n, 'roots', nroots, 'multi', nmulti, 'hss', nh, 'hss_multi', nhm, 'D_fix!=D_whole', len(diffs), 'of which hss', sum(d[4] for d in diffs), 'time %.0f' % (time.time() - t0))
import pickle; pickle.dump((sample, diffs), open('myecl_%s_%d.pkl' % (spec.replace(':', '_'), maxp), 'wb'))
