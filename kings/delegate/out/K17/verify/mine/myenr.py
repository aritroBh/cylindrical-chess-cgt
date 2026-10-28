"""my own no-right-at-root (E)-violation search: contexts with no e.p. right at the root; for each stm s, is (E) violated at
some alternating-reachable non-decisive Y (>= 2 components and a USABLE e.p. capture for the side to move)?  For violating
contexts compare D_whole and D_fix for both sides.  usage: myenr.py <spec> <files> <maxp>"""
import sys, itertools, os
sys.argv_save = sys.argv
from myd import *
import importlib
spec = sys.argv[1]; files = [int(x) for x in sys.argv[2].split(',')]; maxp = int(sys.argv[3])
sys.argv = ['x', spec, sys.argv[2], sys.argv[3]]
# reuse components/dfix from myecl without running its main loop
src = open('myecl.py').read().split("t0 = time.time()")[0]
exec(src)
def usable(p, side):
    W, B, ep = p
    if ep is None or ep[1] != side: return False
    v = ep[0]; mine = W if side == 'W' else B
    if os.environ.get('LOOSE'):
        theirs = B if side == 'W' else W
        return any(v in theirs and v not in (c[1] if side == 'W' else c[0]) for c in moves(bd, p, side))
    return any(bd.f(v[0] + d) is not None and (bd.f(v[0] + d), v[1]) in mine for d in (-1, 1))
def eviol(root, s, regular_victim_capture=False):
    seen = set(); st = [(root, s)]
    while st:
        k = st.pop()
        if k in seen: continue
        seen.add(k); p, side = k
        if len(comps(p)) >= 2 and usable(p, side): return True
        o = 'B' if side == 'W' else 'W'
        for c in moves(bd, p, side):
            if outcome_after(bd, c, side) is None and (c, o) not in seen: st.append((c, o))
    return False
n = nE = 0; diffs = []
sqs = [(f, r) for f in files for r in range(2, h)]
for nw in range(1, maxp + 1):
    for ws in itertools.combinations(sqs, nw):
        rest = [x for x in sqs if x not in ws]
        for nb in range(1, maxp + 1):
            for bs in itertools.combinations(rest, nb):
                W, B = frozenset(ws), frozenset(bs); p = (W, B, None)
                if passed(bd, W, B, None, 'W') or passed(bd, W, B, None, 'B'): continue
                n += 1
                if not (eviol(p, 'W') or eviol(p, 'B')): continue
                nE += 1; cs = tuple(sorted(comps(p), key=ck))
                for s in 'WB':
                    dw = 'W' if whole(p, s) == 'W' else 'L'; df = 'W' if dfix(cs, s) == 'W' else 'L'
                    if dw != df: diffs.append((p, s, dw, df, hss(p, s)))
print(spec, files, maxp, 'contexts', n, '(E)-violating contexts', nE, 'D_fix!=D_whole roots', len(diffs), 'of which hss', sum(d[4] for d in diffs))
