#!/usr/bin/env python3
"""K44: third implementation (lk3.py, Python) against kg44 class counts on config/region cases.  usage: cmp_lk3.py W reg[,reg] [maxcases]"""
import sys, os, collections, time
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from agg import load
from lk3 import LK, quotient, signatures, refsigs, parse_cfg
W = int(sys.argv[1]); regs = sys.argv[2].split(',')
rows, _ = load('new')
kg = collections.defaultdict(collections.Counter); kgd = collections.defaultdict(set)
for r in rows:
    key = (r['W'], r['reg'], r['cfg'].strip())
    kg[key]['other' if r['nm'] == 'UNMATCHED' else r['nm'].split('=')[0]] += r['cnt']
    if r['nm'] == 'UNMATCHED': kgd[key].add(r['sig'])
rn, refs = refsigs()
nbad = ntot = 0
out = open(D + '/logs/cmp_lk3_%d_%s.txt' % (W, '_'.join(regs)), 'w')
for reg in regs:
    for line in open(D + '/cfg/cyl%dx6_w6_%s.txt' % (W, reg)):
        line = line.strip()
        if not line: continue
        rg, cfg = line.split('|')
        region = None if rg == 'all' else set(range(int(rg.split('-')[0]), int(rg.split('-')[1]) + 1))
        g = LK(W, 6, True, parse_cfg(cfg), region)
        cls, QL, QR = quotient(g.L, g.R)
        names, sig = signatures(QL, QR)
        cnt = collections.Counter(); od = set()
        for i, (m, wk, bk) in enumerate(g.nodes):
            if m != g.full: continue
            s = sig[cls[i]]
            if s in refs: cnt[refs[s][0]] += 1
            else: cnt['other'] += 1; od.add(s)
        key = (W, reg, cfg.strip())
        ok = (cnt == kg[key]) and (len(od) == len(kgd[key]))
        ntot += 1
        if not ok: nbad += 1; out.write('DIFF %s %s %s\n' % (key, dict(cnt), dict(kg[key]))); 
        out.flush()
out.write('TOTAL cases %d with differences %d\n' % (ntot, nbad)); out.close()
print('W', W, regs, 'cases', ntot, 'differences', nbad)
