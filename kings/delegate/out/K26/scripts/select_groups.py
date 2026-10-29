#!/usr/bin/env python3
"""Collect every exact group found (dud: total leaks 0 and all 8 root values D; on_strong; over_mutual) from logs/*_groups.jsonl
and write logs/exact_groups_all.json (all of them) and logs/groups_selected.json (up to N diverse ones, Z_B first).
  select_groups.py [N=20]"""
import glob, json, os, re, sys, collections, random
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
H_of = lambda dims: int(dims.split('x')[1])
allg = []
for f in sorted(glob.glob(os.path.join(LOG, '*_groups.jsonl'))):
    name = os.path.basename(f)[:-len('_groups.jsonl')]
    m = re.match(r'^(flat|cyl)_(\d+x\d+)_(\d)(\d)_(t1|t2)(?:_s\d+of\d+)?$', name)
    if not m:
        continue
    kind, dims, nw, nb, typ = m.groups()[:5]
    board = kind + ':' + dims
    for line in open(f):
        d = json.loads(line)
        if typ == 't2':
            if d['total'] != 0 or not all(r[0] == 'D' for r in d['roots']):
                continue
            cls = 'dud'
            wk, bk = d['W'], d['B']
        else:
            cls = d.get('class')
            if cls not in ('on_strong', 'over_mutual'):
                continue
            wk, bk = d['W'], [d['b0']]
        gid = '%s_%s_%s_%s' % (cls, board.replace(':', ''), ''.join(d['wp']) + '-' + ''.join(d['bp']), ''.join(wk))
        allg.append({'id': gid, 'board': board, 'class': cls, 'H': H_of(dims), 'wk': wk, 'bk': bk, 'wp': d['wp'], 'bp': d['bp'],
                     'limits': [int(nw), int(nb)], 'passer_textbook': bool(d['passW'] or d['passB'])})
# unique by id
seen = {}
for g in allg:
    seen.setdefault(g['id'], g)
allg = list(seen.values())
json.dump(allg, open(os.path.join(LOG, 'exact_groups_all.json'), 'w'), indent=1)
print('exact groups', len(allg), dict(collections.Counter((g['board'], g['class']) for g in allg)))
# selection: Z_B and mirror first, then one per (board,class) round robin, favouring different pawn counts
sel = []
def add(g):
    if g not in sel and len(sel) < N:
        sel.append(g)
zb = [g for g in allg if g['class'] == 'dud' and g['wp'] == ['a3', 'b4'] and g['bp'] == ['b3', 'c4'] or
      g['class'] == 'dud' and g['wp'] == ['b4', 'c3'] and g['bp'] == ['a4', 'b3']]
for g in sorted(zb, key=lambda g: (g['board'], g['id'])):
    add(g)
rnd = random.Random(26)
pools = collections.defaultdict(list)
for g in allg:
    if g in sel:
        continue
    pools[(g['class'], g['board'])].append(g)
for k in pools:
    rnd.shuffle(pools[k])
    pools[k].sort(key=lambda g: (len(g['wp']) + len(g['bp'])))   # cheaper contexts first, stable shuffle among equals
keys = sorted(pools, key=lambda k: (k[0] != 'over_mutual', k[0] != 'dud', k))
progress = True
while progress and len(sel) < N:
    progress = False
    for k in keys:
        if pools[k]:
            # alternate between the cheapest and a random member to diversify pawn counts
            used = {(x['class'], tuple(x['wk']), tuple(x['bk'])) for x in sel}
            fresh = [i for i, x in enumerate(pools[k]) if (x['class'], tuple(x['wk']), tuple(x['bk'])) not in used]
            g = pools[k].pop(fresh[0] if fresh else 0)     # prefer a king configuration not yet represented (cheapest first)
            add(g)
            progress = True
        if len(sel) >= N:
            break
json.dump(sel, open(os.path.join(LOG, 'groups_selected.json'), 'w'), indent=1)
print('selected', len(sel))
for g in sel:
    print(g['id'], g['board'], g['class'], 'W', g['wk'], 'B', g['bk'], g['wp'], g['bp'])
