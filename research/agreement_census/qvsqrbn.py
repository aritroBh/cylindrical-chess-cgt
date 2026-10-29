"""Step 1: Q (cap 2) vs QRBN (cap 1, exact only where its two bounds agree), per position, per board."""
import csv
from collections import Counter, defaultdict
rows = list(csv.DictReader(open('census.tsv'), delimiter='\t'))
q = {(r['board'], r['mode'], r['P']): r for r in rows if r['promo'] == 'Q' and r['cap'] == '2'}
c = defaultdict(Counter)
for r in rows:
    if r['promo'] != 'QRBN' or r['mode'] != 'le2': continue
    k = (r['board'], r['mode'], r['P']); x = q.get(k)
    if not x: continue
    b = (r['board'], 'QRBN cap' + r['cap'])
    if r['exact'] != 'True': c[b]['QRBN undetermined (bounds differ)'] += 1
    elif (x['real_wtm'], x['real_btm']) == (r['real_wtm'], r['real_btm']): c[b]['QRBN exact, equals Q cap2'] += 1
    else: c[b]['QRBN exact, DIFFERS from Q cap2'] += 1
    if r['exact'] != 'True':
        # bounds consistent with Q value? (Q value lies within the QRBN bounds is not guaranteed; record the QRBN bound strings)
        pass
for k, v in sorted(c.items()): print(k, dict(v), 'of', sum(v.values()))
