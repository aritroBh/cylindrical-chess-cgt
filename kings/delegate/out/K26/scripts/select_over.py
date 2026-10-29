#!/usr/bin/env python3
"""Pick diverse over_exact (one-sided zugzwang) groups for the context test: logs/groups_over.json.
  select_over.py N   (default 6): 2 groups from each of cyl:7x6, cyl:8x6, flat:7x6; prefers no textbook passer, fewest pawns."""
import glob, json, os, re, random, sys, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
pool = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(LOG, '*_t1*_groups.jsonl'))):
    name = os.path.basename(f)
    m = re.match(r'^(flat|cyl)_(\d+x\d+)_(\d)(\d)_t1', name)
    if not m or '_nf4' in name:
        continue
    kind, dims = m.group(1), m.group(2)
    board = kind + ':' + dims
    for line in open(f):
        d = json.loads(line)
        if d.get('class') != 'over_exact':
            continue
        gid = 'over_%s_%s_%s' % (board.replace(':', ''), ''.join(d['wp']) + '-' + ''.join(d['bp']), ''.join(d['W']))
        pool[board].append({'id': gid, 'board': board, 'class': 'over_exact', 'H': int(dims.split('x')[1]), 'wk': d['W'], 'bk': [d['b0']],
                            'wp': d['wp'], 'bp': d['bp'], 'passer_textbook': bool(d['passW'] or d['passB'])})
rnd = random.Random(26)
sel = []
for board in ('cyl:7x6', 'cyl:8x6', 'flat:7x6'):
    L = {g['id']: g for g in pool[board]}.values()
    L = sorted(L, key=lambda g: (g['passer_textbook'], len(g['wp']) + len(g['bp']), g['id']))
    cand = [g for g in L if not g['passer_textbook']][:20] or list(L)[:20]
    rnd.shuffle(cand)
    sel += cand[:2]
    print(board, 'pool', len(L), 'no-passer', sum(1 for g in L if not g['passer_textbook']), file=sys.stderr)
json.dump(sel, open(os.path.join(LOG, 'groups_over.json'), 'w'), indent=1)
for g in sel:
    print(g['id'], g['wk'], g['bk'], g['wp'], g['bp'], g['passer_textbook'])
