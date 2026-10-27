#!/usr/bin/env python3
"""Aggregate the SUMMARY lines of logs/scan_*.txt into summary.json (and print a table)."""
import re, json, glob, collections, sys
rows = []
pat = re.compile(r'SUMMARY board=(\w+):(\d+)x(\d+) FZ=(\d+)\.\.(\d+) f=(\d+) wmax=(\d+) bmax=(\d+) safe=(\d) ep=(\d) \| roots=(\d+) wins=(\d+) \| attacked s-bar pawns 0: (\d+) roots (\d+) wins; 1: (\d+) roots (\d+) wins; >=2: (\d+) roots (\d+) wins \| s pawn on f\+-1: (\d+) roots (\d+) wins \| VIOLATIONS\(<=1 attacked, White wins\)=(\d+) \| layers=(\d+)')
seen = set()
viol_lines = 0
for fn in sorted(glob.glob('logs/scan_*.txt')):
    if fn.endswith('progress.txt'): continue
    for l in open(fn):
        if l.startswith('VIOLATION'): viol_lines += 1
        m = pat.match(l)
        if not m: continue
        g = m.groups()
        key = g[:10]
        if key in seen: continue
        seen.add(key)
        rows.append(dict(board=g[0], W=int(g[1]), H=int(g[2]), fzlo=int(g[3]), fzhi=int(g[4]), f=int(g[5]), wmax=int(g[6]), bmax=int(g[7]), safe=int(g[8]), ep=int(g[9]),
                         roots=int(g[10]), wins=int(g[11]), roots0=int(g[12]), wins0=int(g[13]), roots1=int(g[14]), wins1=int(g[15]), roots2=int(g[16]), wins2=int(g[17]),
                         roots_near=int(g[18]), wins_near=int(g[19]), violations=int(g[20]), layers=int(g[21])))
tot = collections.Counter()
for r in rows:
    for k in ('roots', 'wins', 'roots0', 'wins0', 'roots1', 'wins1', 'roots2', 'wins2', 'violations'): tot[k] += r[k]
cfgs = sorted({(r['board'], r['W'], r['H'], r['fzlo'], r['fzhi'], r['wmax'], r['bmax']) for r in rows})
out = dict(runs=len(rows), configs=['%s:%dx%d FZ=%d..%d wmax=%d bmax=%d' % c for c in cfgs], totals=dict(tot), violation_lines=viol_lines, rows=rows)
json.dump(out, open('summary.json', 'w'), indent=1)
print('runs', len(rows), 'configs', len(cfgs))
print(dict(tot), 'violation lines', viol_lines)
bycfg = collections.defaultdict(collections.Counter)
for r in rows:
    k = '%s:%dx%d FZ=%d..%d w<=%d b<=%d safe=%d' % (r['board'], r['W'], r['H'], r['fzlo'], r['fzhi'], r['wmax'], r['bmax'], r['safe'])
    for kk in ('roots', 'roots2', 'wins', 'wins2', 'violations'): bycfg[k][kk] += r[kk]
for k, v in bycfg.items(): print('%-48s roots %9d  roots(>=2 attacked) %7d  White wins %6d (all in >=2 class: %s)  violations %d' % (k, v['roots'], v['roots2'], v['wins'], v['wins'] == v['wins2'], v['violations']))
