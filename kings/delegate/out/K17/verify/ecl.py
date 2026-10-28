"""Referee's own re-run of the clause-(E) search (roots with a fresh, usable e.p. right for the side to move), using
my own dgame.py (no cylcgt/, no lemmas/).  For every root (context, side to move s, right owned by s):
   dw  = D_whole  (global right, expires after one move)                       [chess e.p.]
   df  = D_fix    (disjunctive sum of the ROOT components, rights persist while another component is played)
   hss = (V4) exactly: every chess-reachable (alternating) non-decisive position has pairwise safe components,
         tau(component) = signs of passers reachable by either side in any order (not past a passer).
Prints counts and every root with df != dw, with its hss flag.
usage: ecl.py <spec> <files> <maxp>"""
import sys, itertools, time
from functools import lru_cache
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from dgame import *

def comps_of(bd, pos):
    wp, bp, ep = pos
    occ = sorted({f for f, _ in wp | bp})
    if not occ: return []
    groups = []
    for f in occ:
        if groups and f == groups[-1][-1] + 1: groups[-1].append(f)
        else: groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.w - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        fs = set(g)
        e = ep if (ep and ep[0][0] in fs) else None
        out.append((frozenset(p for p in wp if p[0] in fs), frozenset(p for p in bp if p[0] in fs), e))
    return out

def make(bd):
    alt = make_alt(bd)

    @lru_cache(maxsize=None)
    def tau(pos):
        out = set()
        if passed_set(bd, pos, 'W'): out.add(1)
        if passed_set(bd, pos, 'B'): out.add(-1)
        if not out:
            for side in 'WB':
                for c in gen(bd, pos, side):
                    out |= tau(c)
        return frozenset(out)

    def safe(pos):
        ts = [tau(c) for c in comps_of(bd, pos)]
        for i, a in enumerate(ts):
            for j, b in enumerate(ts):
                if i != j and 1 in a and -1 in b: return False
        return True

    def hss_exact(root, s):
        seen = set(); stack = [(root, s)]
        while stack:
            k = stack.pop()
            if k in seen: continue
            seen.add(k)
            p, side = k
            if not safe(p): return False
            o = 'B' if side == 'W' else 'W'
            for c in gen(bd, p, side):
                if terminal(bd, c) is None and (c, o) not in seen:
                    stack.append((c, o))
        return True

    @lru_cache(maxsize=None)
    def dfix(comps, s):
        o = 'B' if s == 'W' else 'W'
        for i, comp in enumerate(comps):
            src = comp if (comp[2] and comp[2][2] == s) else (comp[0], comp[1], None)
            for c in gen(bd, src, s):
                t = terminal(bd, c)
                if t is not None:
                    res = ('W' if t == 1 else 'B') if t != 0 else race_winner(bd, c, s)
                else:
                    res = dfix(tuple(sorted(comps[:i] + (c,) + comps[i + 1:], key=key)), o)
                if res == s: return s
        return o
    return alt, hss_exact, dfix

def key(c): return (sorted(c[0] | c[1]), c[2] is not None, str(c[2]))

def contexts(bd, files, maxp):
    sqs = [(f, r) for f in files for r in range(2, bd.h)]
    for w in range(0, maxp + 1):
        for ws in itertools.combinations(sqs, w):
            rest = [s for s in sqs if s not in ws]
            for bl in range(0, maxp + 1):
                for bs in itertools.combinations(rest, bl):
                    if not ws or not bs: continue
                    pos = (frozenset(ws), frozenset(bs), None)
                    if terminal(bd, pos) is not None: continue
                    yield pos

def with_rights(bd, p):
    wp, bp, _ = p
    for s in 'WB':
        o = 'B' if s == 'W' else 'W'
        mine, theirs = (wp, bp) if s == 'W' else (bp, wp)
        dest = 4 if o == 'W' else bd.h - 3
        r0 = 2 if o == 'W' else bd.h - 1
        r1 = 3 if o == 'W' else bd.h - 2
        occ = wp | bp
        for (f, r) in theirs:
            if r != dest: continue
            if (f, r1) in occ or (f, r0) in occ: continue
            ok = False
            for d in (-1, 1):
                g = bd.nb(f, d)
                if g is not None and (g, r) in mine: ok = True
            if not ok: continue
            yield (wp, bp, ((f, r1), (f, r), s)), s

def main(spec, files, maxp):
    kind, dims = spec.split(':'); w, h = map(int, dims.split('x'))
    bd = Bd(w, h, kind == 'cyl')
    alt, hss_exact, dfix = make(bd)
    t0 = time.time(); n = nroots = nmulti = nhss = nhss_multi = 0; diffs = []
    for p in contexts(bd, files, maxp):
        n += 1
        for q, s in with_rights(bd, p):
            if terminal(bd, q) is not None: continue
            nroots += 1
            cs = comps_of(bd, q); multi = len(cs) >= 2
            nmulti += multi
            dw = 'W' if alt(q, s) == 'W' else 'L'
            df = 'W' if dfix(tuple(sorted(cs, key=key)), s) == 'W' else 'L'
            hss = hss_exact(q, s)
            if hss:
                nhss += 1; nhss_multi += multi
            if df != dw:
                diffs.append((q, s, dw, df, hss, multi))
    print(spec, files, maxp, 'contexts', n, 'roots', nroots, 'multi', nmulti, 'hss', nhss, 'hss_multi', nhss_multi,
          'D_fix!=D_whole', len(diffs), 'of which hss', sum(d[4] for d in diffs), 'time %.0f' % (time.time() - t0))
    def nm(s): return chr(97 + s[0]) + str(s[1])
    for q, s, dw, df, hss, multi in diffs[:60]:
        print('W:', ' '.join(sorted(map(nm, q[0]))), '/ B:', ' '.join(sorted(map(nm, q[1]))), '(ep', nm(q[2][0]) + ')', 'stm', s, 'D_whole', dw, 'D_fix', df, 'hss', hss)

if __name__ == '__main__':
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3]))
