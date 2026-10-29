#!/usr/bin/env python3
"""Collect near-miss two-shuttle placements (total leak count 1, and 2 on cyl:7x6/8x6 <= 2+2) from logs/*_t2*_groups.jsonl,
write logs/groups_near.json (<= 3 per (board, limit, total)), to be checked by confirm.py (kpp vs ref3m, full move lists)."""
import glob, json, os, re, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
pick = collections.defaultdict(dict)
for f in sorted(glob.glob(os.path.join(LOG, '*_t2*_groups.jsonl'))):
    m = re.match(r'^(flat|cyl)_(\d+x\d+)_(\d)(\d)_t2', os.path.basename(f))
    if not m:
        continue
    board = m.group(1) + ':' + m.group(2)
    lim = m.group(3) + '+' + m.group(4)
    for line in open(f):
        d = json.loads(line)
        t = d['total']
        if t == 0 or t > 2 or (t == 2 and not (board.startswith('cyl') and lim == '2+2')):
            continue
        key = (board, lim, t)
        gid = 'near%d_%s_%s_%s' % (t, board.replace(':', ''), ''.join(d['wp']) + '-' + ''.join(d['bp']), ''.join(d['W']))
        if len(pick[key]) < 3:
            pick[key].setdefault(gid, {'id': gid, 'board': board, 'class': 'near_miss_%d' % t, 'H': int(m.group(2).split('x')[1]),
                                       'wk': d['W'], 'bk': d['B'], 'wp': d['wp'], 'bp': d['bp'], 'limits': lim})
out = [g for k in sorted(pick) for g in pick[k].values()]
json.dump(out, open(os.path.join(LOG, 'groups_near.json'), 'w'), indent=1)
print(len(out), 'near-miss groups')
