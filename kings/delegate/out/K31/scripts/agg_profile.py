#!/usr/bin/env python3
import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
N = int(sys.argv[2])
def hist(key, rows):
    h = collections.Counter()
    for r in rows: h[r[key]] += r['n']
    return dict(sorted(h.items()))
groups = {'all': rows, 'faithful': [r for r in rows if r['faithful']], 'single pair': [r for r in rows if ',' not in r['pairs']], 'two pairs': [r for r in rows if ',' in r['pairs']]}
for g, rs in groups.items():
    print('==', g, 'roots', sum(r['n'] for r in rs), 'configs', len(set((r['board'], r['pairs']) for r in rs)))
    for k in ('Lw', 'Fw', 'Lb', 'Fb'):
        print('  ', k, hist(k, rs))
# any root with 2 <= lead < N
mid = [r for r in rows if any(2 <= r[k] < N for k in ('Lw', 'Lb', 'Fw', 'Fb'))]
print('profiles with a lead k, 2 <= k < N:', len(mid), 'roots', sum(r['n'] for r in mid))
for r in mid[:10]: print('  ', r)
# which labels carry Lw = 1 / Lb = 1
lab = collections.Counter()
for r in rows:
    if r['Lw'] == 1 or r['Lb'] == 1:
        for t in r['labels'].split():
            nm, c = t.rsplit('=', 1); lab[(nm, r['Lw'], r['Lb'])] += int(c)
print('labels with Lw=1 or Lb=1:', dict(lab))
# Lw = 1 roots: which boards
b = collections.Counter()
for r in rows:
    if r['Lw'] == 1: b[(r['board'].split(':')[0], r['pairs'].count(',') + 1)] += r['n']
print('Lw=1 by (kind, pairs)', dict(b))
