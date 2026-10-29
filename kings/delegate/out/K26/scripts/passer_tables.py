#!/usr/bin/env python3
"""K26 final: from logs/*_t2*_groups.jsonl (main search; every candidate with total leaks <= max(min+1, 2) was written) tabulate, per board and limit,
the number of placements with total leaks 0, 1, 2 at all 8 roots, with and without a textbook passed pawn (passW/passB; no e.p. flag exists at a root,
so textbook = e.p.-aware), and the minimum total over the passer-free placements.  Writes logs/passer_tables.json and prints markdown."""
import glob, json, os, re, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
rows = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
seen = collections.defaultdict(set)
for f in sorted(glob.glob(os.path.join(LOG, '*_t2*_groups.jsonl'))):
    m = re.match(r'^(flat|cyl)_(\d+x\d+)_(\d)(\d)_t2', os.path.basename(f))
    if not m:
        continue
    key = (m.group(1) + ':' + m.group(2), '%s+%s' % (m.group(3), m.group(4)))
    for line in open(f):
        d = json.loads(line)
        ident = (tuple(d['W']), tuple(d['B']), tuple(d['wp']), tuple(d['bp']))
        if ident in seen[key]:
            continue
        seen[key].add(ident)
        pas = bool(d['passW'] or d['passB'])
        allD = all(r[0] == 'D' for r in d['roots'])
        rows[key][d['total']][('passer' if pas else 'no passer')] += 1
out = {}
print('| board | pawns W+B | total 0 (passer / none) | total 1 (passer / none) | total 2 (passer / none) | min total among passer-free placements |')
print('|---|---|---|---|---|---|')
for key in sorted(rows, key=lambda k: (['flat:7x6', 'cyl:7x6', 'cyl:8x6', 'flat:8x6', 'flat:7x7'].index(k[0]), k[1])):
    r = rows[key]
    mp = None
    for t in sorted(r):
        if r[t]['no passer']:
            mp = t
            break
    cell = lambda t: '%d / %d' % (r[t]['passer'], r[t]['no passer']) if t in r else '0 / 0'
    out['%s %s' % key] = {str(t): dict(r[t]) for t in sorted(r)}
    out['%s %s' % key]['min_total_passer_free'] = mp
    print('| %s | %s | %s | %s | %s | %s |' % (key[0], key[1], cell(0), cell(1), cell(2), mp if mp is not None else '> 2 (not recorded beyond 2)'))
json.dump(out, open(os.path.join(LOG, 'passer_tables.json'), 'w'), indent=1)
