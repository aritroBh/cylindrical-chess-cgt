#!/usr/bin/env python3
"""Markdown list of the placements with the smallest positive total leak count (<= 2) of the <= 2+2 two-shuttle searches (logs/*_22_t2*_groups.jsonl).
A promotion leak is counted once per piece in these logs (kpp prints one entry per promotion piece)."""
import glob, json, os, re, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
rows = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(LOG, '*_22_t2*_groups.jsonl'))):
    m = re.match(r'^(flat|cyl)_(\d+x\d+)_22_t2', os.path.basename(f))
    if not m:
        continue
    board = m.group(1) + ':' + m.group(2)
    for l in open(f):
        d = json.loads(l)
        if 1 <= d['total'] <= 2:
            rows[board].append(d)
for board in ('flat:7x6', 'cyl:7x6', 'cyl:8x6', 'flat:8x6', 'flat:7x7'):
    L = sorted(rows.get(board, []), key=lambda d: (d['total'], ''.join(d['wp']), ''.join(d['bp'])))
    print('### %s (total 1: %d, total 2: %d)' % (board, sum(1 for d in L if d['total'] == 1), sum(1 for d in L if d['total'] == 2)))
    for d in L:
        lk = []
        for rl in d.get('leaks', []):
            lk += ['%s:%s' % (x[0], x[1]) for x in rl]
        print('- total %d: W king %s, B king %s, pawns W %s / B %s; root values %s; first leaks %s' % (
            d['total'], '/'.join(d['W']), '/'.join(d['B']), ' '.join(d['wp']) or '-', ' '.join(d['bp']) or '-',
            ''.join(r[0] for r in d['roots']), ' '.join(lk[:4])))
