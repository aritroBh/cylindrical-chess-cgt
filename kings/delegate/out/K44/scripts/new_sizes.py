#!/usr/bin/env python3
"""K44: for every signature of the new runs that is absent from the K20-convention baseline, find the example root with the
smallest reachable game graph (and its bisimulation quotient), using lk3.py (third implementation).  Writes logs/new_sizes.tsv"""
import sys, os, collections, json
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from agg import load
from lk3 import LK, quotient, parse_cfg
extra = sys.argv[1] if len(sys.argv) > 1 else None
new, exn = load('new'); base, exb = load('base')
S0 = {r['sig'] for r in base}
if os.path.exists(D + '/logs/fsig_baseflat.txt'):
    pass
need = collections.defaultdict(list)   # (W, rg, cfg) -> [(sig, example roots)]
for r in new:
    if r['sig'] in S0: continue
    need[(r['W'], r['rg'], r['cfg'].strip())].append(r)
out = open(D + '/logs/new_sizes.tsv', 'w')
out.write('W\tregion\tconfig\tfaithful\tclass\tpairs\treach_nodes\tquotient_reach\troot\tsig\n')
done = 0
for (W, rg, cfg), rows in sorted(need.items()):
    region = None if rg == 'all' else set(range(int(rg.split('-')[0]), int(rg.split('-')[1]) + 1))
    g = LK(W, 6, True, parse_cfg(cfg), region)
    cls, QL, QR = quotient(g.L, g.R)
    byname = {g.name(i): i for i in range(len(g.nodes)) if g.nodes[i][0] == g.full}
    reachq = {}
    def rq(c):
        if c in reachq: return reachq[c]
        seen = {c}; st = [c]
        while st:
            x = st.pop()
            for t in QL[x] + QR[x]:
                if not isinstance(t, str) and t not in seen: seen.add(t); st.append(t)
        reachq[c] = len(seen); return len(seen)
    for r in rows:
        ex = exn.get((W, r['reg'], r['cfg'], r['sig']), '')
        best = None
        for e in ex.split(';'):
            e = e.strip()
            if e not in byname: continue
            c = cls[byname[e]]; k = rq(c)
            if best is None or k < best[0]: best = (k, e, c)
        if best is None: continue
        i = byname[best[1]]
        seen = {i}; st = [i]
        while st:
            x = st.pop()
            for t in g.L[x] + g.R[x]:
                if not isinstance(t, str) and t not in seen: seen.add(t); st.append(t)
        out.write('%d\t%s\t%s\t%d\t%s\t%d\t%d\t%d\t%s\t%s\n' % (W, rg, cfg, r['faith'], r['nm'], len(cfg.split()), len(seen), best[0], best[1], r['sig']))
    out.flush(); done += 1
print('configs', done)
