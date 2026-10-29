#!/usr/bin/env python3
"""Print markdown tables from logs/merged.json (run merge.py first)."""
import json, os, sys
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(OUT, 'logs', 'merged.json')))
rows = {}
for k, r in m.items():
    key = (r['board'], tuple(r['limits']))
    rows.setdefault(key, {})[r['type']] = r
order = ['flat:7x6', 'cyl:7x6', 'cyl:8x6', 'flat:8x6', 'flat:7x7']
H = ['board', 'pawns W+B', 'two-shuttle placements', 'exact duds (total leaks 0)', 'min total leaks', '#placements with total 1', '#total 2',
     'one-shuttle placements', 'on_strong', 'on_weak', 'over_pre', 'over_exact (S-zugzwang)', 'over_mutual']
print('| ' + ' | '.join(H) + ' |')
print('|' + '---|' * len(H))
for b in order:
    for lim in ((2, 2), (3, 2), (2, 3)):
        r = rows.get((b, lim))
        if not r:
            continue
        t2, t1 = r.get('t2'), r.get('t1')
        c = lambda k: str(t1['classes'].get(k, 0)) if t1 else '-'
        if t2:
            h2 = t2['stage2_hist_evaluated']
            compl = t2['stage2_hist_complete_up_to_total']
            n1 = h2.get('1', 0) if compl >= 1 else '>=%s' % h2.get('1', 0)
            n2 = h2.get('2', 0) if compl >= 2 else '>=%s' % h2.get('2', 0)
            if not t2['complete']:
                n1 = n2 = 'partial'
        print('| %s | %d+%d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            b, lim[0], lim[1],
            '{:,}'.format(t2['candidates']) if t2 else '-',
            t2['exact_dud'] if t2 else '-',
            (str(t2['min_total_leaks_8roots']) + ('' if t2['min_exact'] else '*')) if t2 else '-',
            n1 if t2 else '-', n2 if t2 else '-',
            '{:,}'.format(t1['candidates']) if t1 else '-',
            c('on_strong'), c('on_weak'), t1['over_pre'] if t1 else '-', c('over_exact'), c('over_mutual')))
