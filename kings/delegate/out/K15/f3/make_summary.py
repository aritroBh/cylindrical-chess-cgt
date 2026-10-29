#!/usr/bin/env python3
"""assemble ../summary.json from f3/runs/*.json (census), f3/cf/*.cmp.txt and *.table.json (confirmations)"""
import json, glob, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
dec = json.JSONDecoder()
def docs(f):
    s = open(f).read(); i = 0; out = []
    while i < len(s):
        while i < len(s) and s[i].isspace(): i += 1
        if i >= len(s): break
        o, i = dec.raw_decode(s, i); out.append(o)
    return out
census = []
for f in sorted(glob.glob(HERE + '/runs/pA_*.json') + glob.glob(HERE + '/runs/npB_*.json') + glob.glob(HERE + '/runs/flat76_np.json') + glob.glob(HERE + '/../v2/runs/np_*.json')):
    nm = os.path.basename(f)[:-5]
    notion = 'B' if ('npB' in nm or nm.startswith('np_') or nm.startswith('flat76_np')) else 'A'
    for o in docs(f):
        census.append(dict(run=nm, notion=notion, board=o['board'], files=o['files'], wmax=o['wmax'], bmax=o['bmax'], root_passers=o['root_passers'], roots=o['roots'],
                           roots_by_class=o['total'], distinct_by_class=o['distinct_groups']))
tempo = []
for f in sorted(glob.glob(HERE + '/runs/tp_*.json') + glob.glob(HERE + '/../v2/runs/tp_*.json')):
    for o in docs(f):
        tempo.append(dict(run=os.path.basename(f)[:-5], board=o['board'], files=o['files'], wmax=o['wmax'], bmax=o['bmax'], root_passers=o['root_passers'], roots=o['roots'], total=o['total']))
conf = {}
for t in sorted(glob.glob(HERE + '/cf/*.table.json')):
    rows = json.load(open(t)); by = collections.OrderedDict()
    for r in rows:
        k = r['group']; d = by.setdefault(k, dict(positions=0, agree=0, differ=0, ztype=r['z'], states=r.get('nstates'), differing_contexts=set()))
        d['positions'] += 1
        if r.get('status') == 'agree': d['agree'] += 1
        else: d['differ'] += 1; d['differing_contexts'].add(r['ctx'])
    for d in by.values(): d['differing_contexts'] = sorted(d['differing_contexts'])[:12]
    conf[os.path.basename(t)[:-11]] = by
out = dict(task='K15', date='2026-10-27', census=census, tempo_signature_census=tempo, confirmations_P_model=conf,
           note='confirmation keys: e7x6 / e8x6 = dud groups on cyl:7x6 / 8x6 (40 contexts); cf_zb* = Z_B itself; dflat = flat 7x6 groups (30 contexts); d8x8 = Z_88 (14 contexts); '
                'a8x8f = notion-A groups on cyl:8x8; o7x6 / o8x6 = over-signature candidates (40 contexts, root only); n7 / n8 = nearest misses with more contexts. '
                'Counts of roots are exact; distinct = distinct canonical state closures.')
json.dump(out, open(os.path.join(HERE, '..', 'summary.json'), 'w'), indent=1)
print('summary.json written:', len(census), 'census rows,', len(tempo), 'tempo rows,', len(conf), 'confirmation sets')
