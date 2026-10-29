#!/usr/bin/env python3
"""K15 fin2: summarise cf/*.cmp.txt (output of conf2.py cmp) into logs/conf_table.md and logs/conf_table.json.
Each cmp line: GROUP <TAB> n=.. agree=.. DISAGREE=.. inexact=.. missing=.. <TAB> bad contexts: [...]"""
import glob, os, re, json
FIN2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
names = {'c7x6': ('cyl:7x6', 'dud', 'all distinct dud groups of the census (A or B reading), 24 contexts'), 'c8x6': ('cyl:8x6', 'dud', 'same, 24 contexts'),
         'c8x8': ('cyl:8x8', 'dud', 'same, 8 contexts'), 'strictA8': ('cyl:8x6', 'dud', 'the two A-dud groups without root passer, 40 contexts'),
         'o7x6': ('cyl:7x6', 'over', 'tempo-signature over candidates, root only, 40 contexts'), 'o8x6': ('cyl:8x6', 'over', 'same'),
         'no7x6': ('cyl:7x6', 'over', 'structural near-over roots (A), root only, 40 contexts'), 'no8x6': ('cyl:8x6', 'over', 'same'), 'no8x8': ('cyl:8x8', 'over', 'same, 20 contexts'),
         'no7x7': ('cyl:7x7', 'over', 'same, 20 contexts'), 'no8x7': ('cyl:8x7', 'over', 'same, 20 contexts'),
         'nol7x6': ('cyl:7x6', 'over', 'near-over roots, the four named contexts'), 'nol8x6': ('cyl:8x6', 'over', 'near-over roots, the four named contexts'), 'nol8x8': ('cyl:8x8', 'over', 'near-over roots, the four named contexts'), 'nol7x7': ('cyl:7x7', 'over', 'near-over roots, the four named contexts'), 'nol8x7': ('cyl:8x7', 'over', 'near-over roots, the four named contexts'),
         'nul7x6': ('cyl:7x6', 'under', 'near-under roots, the four named contexts'), 'nul8x6': ('cyl:8x6', 'under', 'near-under roots, the four named contexts'), 'nul8x8': ('cyl:8x8', 'under', 'near-under roots, the four named contexts'),
         'nu7x6': ('cyl:7x6', 'under', 'structural near-under roots (A), root only, 40 contexts'), 'nu8x6': ('cyl:8x6', 'under', 'same'), 'nu8x8': ('cyl:8x8', 'under', 'same, 20 contexts')}
out = []; js = {}
for tag, (board, z, desc) in names.items():
    f = os.path.join(FIN2, 'cf', tag + '.cmp.txt')
    if not os.path.exists(f): continue
    rows = []
    for l in open(f):
        p = l.rstrip('\n').split('\t')
        if len(p) < 3: continue
        m = re.match(r'n=(\d+) agree=(\d+) DISAGREE=(\d+) inexact=(\d+) missing=(\d+)', p[1])
        if not m: continue
        n, a, d, i, ms = map(int, m.groups())
        rows.append((p[0], n, a, d, i, ms, p[2].replace('bad contexts: ', '')))
    tot = [sum(r[k] for r in rows) for k in (1, 2, 3, 4, 5)]
    allagree = sum(1 for r in rows if r[3] == 0 and r[4] == 0 and r[5] == 0)
    js[tag] = {'board': board, 'class': z, 'description': desc, 'groups': len(rows), 'positions': tot[0], 'agree': tot[1], 'disagree': tot[2], 'inexact': tot[3], 'missing': tot[4],
               'groups_with_no_disagreement_and_no_missing': allagree, 'rows': rows}
    out.append('### %s (%s, %s): %s\n\n%d groups, %d positions: agree %d, DISAGREE %d, inexact %d, missing %d; %d groups agree at every position.\n' % (tag, board, z, desc, len(rows), tot[0], tot[1], tot[2], tot[3], tot[4], allagree))
    out.append('| group (root) | positions | agree | DISAGREE | inexact | missing | contexts with a disagreement (up to 6) |\n|---|---|---|---|---|---|---|')
    for r in rows: out.append('| `%s` | %d | %d | %d | %d | %d | %s |' % r)
    out.append('')
open(os.path.join(FIN2, 'logs', 'conf_table.md'), 'w').write('\n'.join(out))
json.dump(js, open(os.path.join(FIN2, 'logs', 'conf_table.json'), 'w'), indent=0)
for t, v in js.items(): print(t, v['board'], v['class'], 'groups', v['groups'], 'positions', v['positions'], 'agree', v['agree'], 'DISAGREE', v['disagree'], 'inexact', v['inexact'], 'missing', v['missing'], 'groups fully agreeing', v['groups_with_no_disagreement_and_no_missing'])
