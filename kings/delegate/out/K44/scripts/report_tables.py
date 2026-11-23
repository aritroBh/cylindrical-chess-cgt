#!/usr/bin/env python3
import sys, os, collections, json
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from agg import load, cls_of
new, ex = load('new'); base, exb = load('base')
def arcL(cfg, W):
    fs = sorted({ord(t[0]) - 97 for t in cfg.split()})
    best = W
    for s in fs:
        L = max(((f - s) % W) for f in fs) + 1
        best = min(best, L)
    return best
def band(cfg, W):
    L = arcL(cfg, W)
    return 'L<=4' if L <= 4 else ('L=5' if L == 5 else 'L=6')
out = []
# 1. per (pairs, band, faithful) class presence over W=6..10 free
for reg in ('free', 'm0', 'm1', 'm2'):
    out.append('\n### region %s: classes present (roots over the 5 widths), faithful configurations only' % reg)
    tab = collections.defaultdict(lambda: collections.Counter())
    nconf = collections.Counter(); seen = set()
    for r in new:
        if r['reg'] != reg or not r['faith']: continue
        k = (len(r['cfg'].split()), band(r['cfg'], r['W']))
        tab[k][cls_of(r['nm'], r['sig'])] += r['cnt']
        key = (r['W'], r['cfg'], r['rg'])
        if key not in seen: seen.add(key); nconf[k] += 1
    for k in sorted(tab):
        out.append('pairs %d window %s: %d configs (widths 6-10 together): %s' % (k[0], k[1], nconf[k], json.dumps(dict(sorted(tab[k].items())))))
# 2. rare classes
out.append('\n### where do the rare classes occur (any region, faithful flag, config, width)')
rare = {'over', 'under', '{1|0}', '{0|-1}', '*', '+1', '-1', 'tis', 'tisn', '{on|off}'}
occ = collections.defaultdict(set)
for r in new:
    if r['nm'].split('=')[0] in rare: occ[r['nm']].add((r['W'], r['reg'], r['cfg'], r['faith']))
for nm in sorted(occ):
    L = sorted(occ[nm])
    out.append('%s: %d (config,width,region) cases; faithful %d; widths %s; pairs %s' % (nm, len(L), sum(1 for x in L if x[3]), sorted({x[0] for x in L}), sorted({len(x[2].split()) for x in L})))
open(D + '/logs/tables.md', 'w').write('\n'.join(out))
print('\n'.join(out))
