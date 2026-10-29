#!/usr/bin/env python3
"""K26 final: EXHAUSTIVE small contexts (an unbiased rate, unlike the 60-context samples, half of which are chosen among D-decisive contexts).
  ctx_exh.py GROUP BOARD FILES MAXPAWNS i/n OUT.json
GROUP: ZB | ZC (the group placements of zc_boards.py; kings on their shuttles, 8 roots per context).  FILES: context files, e.g. efg.
Contexts: every placement of <= MAXPAWNS context pawns (total, either colour) on the given files, ranks 2..H-1.  Each root is solved in the P model by
kpp (values only) and compared with the D-model prediction for dud_D (dmodel.py, own implementation, cross-checked against K14's: dm_crosscheck.log).
Shard i of n: contexts i, i+n, ...  Output: per context the 8 P values, the 8 D values, 'bad' flag."""
import sys, os, json, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import *
import dmodel
safe_nice()
grp, board, files, maxp, shard, ofile = sys.argv[1:7]
maxp = int(maxp); si, sn = map(int, shard.split('/'))
GROUPS = {'ZC': (['c2', 'c3'], ['a4', 'a5'], ['a2', 'c4'], ['a3', 'c5']), 'ZB': (['b2', 'c3'], ['a4', 'b5'], ['a3', 'b4'], ['b3', 'c4'])}
wk, bk, wp, bp = GROUPS[grp]
H = int(board.split(':')[1].split('x')[1])
fl = [FILES.index(ch) + 1 for ch in files]
sqs = [(f, r) for f in fl for r in range(2, H)]
ctxs = []
for kw in range(maxp + 1):
    for w in itertools.combinations(sqs, kw):
        for kb in range(maxp + 1 - kw):
            for b in itertools.combinations([s for s in sqs if s not in w], kb):
                ctxs.append((frozenset(w), frozenset(b)))
ctxs = [c for i, c in enumerate(ctxs) if i % sn == si]
nm = lambda s: FILES[s[0] - 1] + str(s[1])
roots = [(w, b, None, s) for (w, b) in ctxs for s in (0, 1)]
pred = dmodel.solve(roots, 'dud', H)
lines = []
for (w, b) in ctxs:
    for a in wk:
        for k in bk:
            for s in 'wb':
                lines.append(' '.join(['K' + a, 'k' + k] + ['P' + x for x in wp] + ['p' + x for x in bp] + ['P' + nm(q) for q in sorted(w)] + ['p' + nm(q) for q in sorted(b)] + [s, '-']))
res = []
CH = 800
for lo in range(0, len(lines), CH):
    r, _ = run_solver(lines[lo:lo + CH], board, 'kpp', moves=False)
    res += r
vals = [x.rsplit('|', 1)[1].split()[0] for x in res]
out = []
bad = 0
i = 0
for (w, b) in ctxs:
    pv = vals[i:i + 8]; i += 8
    dv = [pred[(w, b, None, s)] for a in wk for k in bk for s in (0, 1)]
    isbad = pv != dv
    bad += isbad
    out.append({'W': sorted(nm(q) for q in w), 'B': sorted(nm(q) for q in b), 'P': ''.join(pv), 'D': ''.join(dv), 'bad': isbad})
json.dump({'group': grp, 'board': board, 'files': files, 'maxpawns': maxp, 'shard': shard, 'contexts': len(ctxs), 'bad_contexts': bad, 'rows': out}, open(ofile, 'w'))
print(grp, board, files, 'contexts', len(ctxs), 'bad', bad, file=sys.stderr)
