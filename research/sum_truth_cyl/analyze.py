import json, glob, collections
PRED = {"L": ("W", "W"), "R": ("L", "L"), "N": ("W", "L"), "P": ("L", "W")}
items = json.load(open('pairs.json'))
fz = {}
for s in json.load(open('frozen_out/frozen_all.json'))['stdout']:
    a, b = s.split('|'); fz[a.strip()] = tuple(b.split())
real = {}; killed = []
for f in glob.glob('jobs/*_cap1.json'):
    r = json.load(open(f))
    if r['name'].startswith('pair'):
        if r['killed_over_limit']: killed.append((r['name'], r['secs'], r['maxrss_bytes']))
        continue
    for s in r['stdout']:
        a, b = s.split('|'); real[a.strip()] = tuple(b.split())
def pr(lines, d):
    w, b = d[lines[0]], d[lines[1]]
    return (w[0], b[0]) if w[0] == w[1] and b[0] == b[1] else None
out = []
tab = collections.Counter()
for i, it in enumerate(items):
    row = {'i': i, 'A': it['A'], 'B': it['B']}
    for key in ('textbook', 'ep-aware'):
        o = it[key]['outcome']
        row[key + '_sum'] = (it[key]['value'], o, it[key]['sum_safe'])
        pred = PRED.get(o)
        fp = pr((it['wtm'], it['btm']), fz)
        row[key + '_frozen_pair'] = 'race/none' if pred is None else ('match' if fp == pred else 'MISMATCH')
        # components alone
        comp = {}
        for t in 'AB':
            c = it[key + '_' + t]; pc = PRED.get(c['outcome'])
            fs = pr(it['solo' + t], fz); rs = pr(it['solo' + t], real)
            comp[t] = {'model': c['outcome'], 'frozen': 'match' if fs == pc else 'MISMATCH', 'real_cap1': 'undetermined' if rs is None else ('match' if rs == pc else 'MISMATCH')}
        row[key + '_comp'] = comp
        # classification of frozen-pair disagreements
        if row[key + '_frozen_pair'] == 'MISMATCH':
            cls = 'component error (frozen)' if any(comp[t]['frozen'] == 'MISMATCH' for t in 'AB') else 'sum (interaction) error'
        else: cls = row[key + '_frozen_pair']
        row[key + '_class'] = cls
        tab[(key, cls)] += 1
    out.append(row)
json.dump(out, open('pair_table.json', 'w'), indent=1)
for k, v in sorted(tab.items()): print(k, v)
print('pairs with sum_safe False:', sum(1 for it in items if not it['textbook']['sum_safe']))
print('cylcgt outcome classes (textbook):', collections.Counter(it['textbook']['outcome'] for it in items))
print('textbook vs ep-aware sum outcome differ:', sum(1 for it in items if it['textbook']['outcome'] != it['ep-aware']['outcome']))
cc = collections.Counter()
for r in out:
    for t in 'AB': cc[(r['textbook_comp'][t]['real_cap1'])] += 1
print('real cap1 solo status of the components in the 100 slots:', cc)
print('pair real runs killed over 3.6GB:', killed)
