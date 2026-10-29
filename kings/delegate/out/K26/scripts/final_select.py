#!/usr/bin/env python3
"""Final selection of up to 20 diverse exact groups for the report (logs/groups_final.json): every exact dud (<= 10), then passer-free
exact on groups spread over the boards, then passer-free exact over (S-zugzwang) groups from logs/groups_over.json.
Run select_groups.py first (it writes logs/exact_groups_all.json)."""
import json, os, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(OUT, 'logs')
allg = json.load(open(os.path.join(L, 'exact_groups_all.json')))
over = json.load(open(os.path.join(L, 'groups_over.json')))
sel = [g for g in allg if g['class'] == 'dud']
sel.sort(key=lambda g: (g['board'], g['passer_textbook'], g['id']))
import glob
tested = set()
for f in glob.glob(os.path.join(L, 'ctx_phase*.json')):
    tested |= {r['id'].rstrip('~') for r in json.load(open(f))}
on = [g for g in allg if g['class'] == 'on_strong' and not g['passer_textbook'] and g['id'] in tested]
by = collections.defaultdict(list)
for g in sorted(on, key=lambda g: (len(g['wp']) + len(g['bp']), g['id'])):
    by[g['board']].append(g)
quota = {'cyl:7x6': 2, 'cyl:8x6': 2, 'flat:7x6': 1}
for b, q in quota.items():
    sel += by[b][:q]
sel += over[:20 - len(sel)]
sel = sel[:20]
json.dump(sel, open(os.path.join(L, 'groups_final.json'), 'w'), indent=1)
for g in sel:
    print(g['id'], g['board'], g['class'], g['wk'], g['bk'], g['wp'], g['bp'])
print(len(sel))
