#!/usr/bin/env python3
"""K44: for every B34 signature of the new runs that is absent from the K20-convention baseline, recompute the signature of the
example root(s) with lk3.py (third implementation) and compare it with kg44's.  Writes logs/verify_new.tsv and a summary line."""
import sys, os, collections
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from agg import load
from lk3 import LK, parse_cfg, battery, dsum
base_sigs = None
new, exn = load('new'); base, exb = load('base')
S0 = {r['sig'] for r in base}
MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'
flat = os.path.exists(D + '/logs/flat_sigs.txt')
if flat: S0 |= set(open(D + '/logs/flat_sigs.txt').read().split())
need = collections.defaultdict(list)
pick = {}
for r in new:
    if r['sig'] in S0: continue
    if MODE == 'faithful' and not r['faith']: continue
    k = (r['W'], len(r['cfg'].split()), r['rg'] != 'all')
    if r['sig'] not in pick or k < pick[r['sig']][0]: pick[r['sig']] = (k, r)
for sg, (k, r) in pick.items(): need[(r['W'], r['rg'], r['cfg'].strip())].append(r)
C = battery(); names = list(C)
def reach(g, r):
    seen = {r}; st = [r]
    while st:
        x = st.pop()
        for t in g.L[x] + g.R[x]:
            if not isinstance(t, str) and t not in seen: seen.add(t); st.append(t)
    order = sorted(seen); ix = {x: i for i, x in enumerate(order)}
    L = [[t if isinstance(t, str) else ix[t] for t in g.L[x]] for x in order]
    R = [[t if isinstance(t, str) else ix[t] for t in g.R[x]] for x in order]
    return L, R, ix[r]
out = open(D + '/logs/verify_new%s.tsv' % ('' if MODE == 'all' else '_' + MODE), 'w')
ok = bad = 0
for (W, rg, cfg), rows in sorted(need.items()):
    region = None if rg == 'all' else set(range(int(rg.split('-')[0]), int(rg.split('-')[1]) + 1))
    g = LK(W, 6, True, parse_cfg(cfg), region)
    byname = {g.name(i): i for i in range(len(g.nodes)) if g.nodes[i][0] == g.full}
    for r in rows:
        e = exn.get((W, r['reg'], r['cfg'], r['sig']), '').split(';')[0].strip()
        if e not in byname: continue
        L, R, s = reach(g, byname[e])
        sig = ''
        for nm in names:
            KL, KR = C[nm]
            res = dsum(L, R, KL, KR)[s][0]
            sig += '%d%d' % res
        good = sig == r['sig']
        ok += good; bad += (not good)
        out.write('%d\t%s\t%s\t%s\t%s\t%d\n' % (W, rg, cfg, e, r['nm'], good)); out.flush()
out.write('SUMMARY signatures checked %d agree %d disagree %d\n' % (ok + bad, ok, bad)); out.close()
print('checked', ok + bad, 'agree', ok, 'disagree', bad)
