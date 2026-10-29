#!/usr/bin/env python3
# K31: tables for FINDINGS.md from logs/sweep_*.jsonl (records of scripts/sweep.py).
import json, os, collections
L = os.path.dirname(os.path.abspath(__file__)) + '/../logs/'
recs = {}
for f in ['sweep_small', 'sweep_h4', 'sweep_main', 'sweep_ext', 'sweep_wide']:
    for l in open(L + f + '.jsonl'):
        r = json.loads(l); recs[(r['W'], r['H'], r['rank'])] = r
out = []
out.append('Table 1: roots of value +1 / -1 (lk, B34 names) per pair rank r (white pawn on rank r, black pawn on r+1), single pair on file a, free board')
out.append('W  H | ' + ' | '.join('r=%d' % r for r in range(2, 7)) + ' | total +1/-1 | both solvers')
for H in range(5, 9):
    for W in range(5, 13):
        row = []; tp = tm = 0; ag = True
        for r in range(2, 7):
            x = recs.get((W, H, r))
            if r > H - 2: row.append('  -  '); continue
            row.append('%d/%d' % (x['lk_p1'], x['lk_m1'])); tp += x['lk_p1']; tm += x['lk_m1']
            ag = ag and x.get('agree_sets') is True and x.get('agree_classes') is True
        out.append('%2d %2d | %s | %d/%d | %s' % (W, H, ' | '.join('%5s' % c for c in row), tp, tm, 'kg=lk' if ag else 'DIFF'))
out.append('')
out.append('Table 2: widest range run, even W only (odd W: 0/0 in every row, see Table 3)')
for H in range(4, 13):
    for W in sorted({k[0] for k in recs if k[1] == H}):
        if W % 2 or W < 4: continue
        row = ['%d/%d' % (recs[(W, H, r)]['lk_p1'], recs[(W, H, r)]['lk_m1']) for r in range(2, H - 1)]
        if W in (4, 6, 8, 2 * H - 4, 2 * H - 2, 2 * H, 24):
            out.append('H=%2d W=%2d  %s' % (H, W, ' '.join(row)))
out.append('')
out.append('Table 3: odd W and W<=4 (all ranks): total +1/-1 roots, number of (W,H,r) cases')
odd = [(k, v) for k, v in recs.items() if k[0] % 2 or k[0] <= 4]
out.append('cases %d, with a +1 or -1 root: %d' % (len(odd), sum(1 for k, v in odd if v['lk_p1'] or v['lk_m1'])))
odd_w = sorted({k[0] for k, v in odd if k[0] % 2})
out.append('odd W run: %s; H run: %s' % (odd_w, sorted({k[1] for k, v in odd})))
both = [v for v in recs.values() if v.get('agree_sets') is not None]
out.append('')
out.append('records %d (distinct W,H,r); both solvers (kg or kgw, and lk) ran on %d, class counts and +-1 root sets agree on %d; lk only on %d (W*H > 127)' % (
    len(recs), len(both), sum(1 for v in both if v['agree_sets'] and v['agree_classes']), len(recs) - len(both)))
print('\n'.join(out))
