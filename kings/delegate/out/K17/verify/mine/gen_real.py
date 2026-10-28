"""my own generator of the real-king 'check at the root' family; usage: gen_real.py <spec> <files> <maxp> <prefix>"""
import sys, itertools, json
from myd import *
spec, files, maxp, pre = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3]), sys.argv[4]
kind, dims = spec.split(':'); w, h = map(int, dims.split('x')); bd = Bd(w, h, kind == 'cyl'); whole = make(bd)
sqs = [(f, r) for f in files for r in range(2, h)]
nctx = 0; cand = []
for nw in range(1, maxp + 1):
    for ws in itertools.combinations(sqs, nw):
        rest = [s for s in sqs if s not in ws]
        for nb in range(1, maxp + 1):
            for bs in itertools.combinations(rest, nb):
                pos = (frozenset(ws), frozenset(bs), None)
                if passed(bd, pos[0], pos[1], None, 'W') or passed(bd, pos[0], pos[1], None, 'B'): continue
                nctx += 1
                if whole(pos, 'B') == 'B': cand.append(pos)
def nm(s): return 'abcdefgh'[s[0]] + str(s[1])
qs = []
for r in range(2, h - 1):
    wz, bz, bk = (0, r), (0, r + 1), (1, r + 1)
    for f in (0, 1):
        for rk in range(1, h + 1):
            wk = (f, rk)
            if wk in (wz, bz, bk): continue
            if abs(wk[0] - bk[0]) <= 1 and abs(wk[1] - bk[1]) <= 1: continue
            for p in cand:
                toks = ['K' + nm(wk), 'k' + nm(bk), 'P' + nm(wz), 'p' + nm(bz)] + ['P' + nm(s) for s in sorted(p[0])] + ['p' + nm(s) for s in sorted(p[1])]
                qs.append(' '.join(toks) + ' b -')
open(pre + '.in', 'w').write('\n'.join(qs) + '\n')
print(spec, 'contexts', nctx, 'D(Black first)=Black', len(cand), 'queries', len(qs))
