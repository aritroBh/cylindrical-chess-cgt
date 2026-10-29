#!/usr/bin/env python3
"""K15 fin2: markdown table of the kpsolve (chess) runs in fin2/chess (and, for reference, the earlier attempt's runs in ../final/chess).
Result 'A B' = lower and upper bound from White's point of view; A == B means exact."""
import glob, os, re
FIN2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pred = {'alone': 'D D', 'blocked': 'D D', 'onemove': 'D D', 'gap': 'D D', 'ctxWW': 'W W', 'ctxLL': 'L L', 'ctxWL': 'W L'}
rows = ['| source | board | cap | position (White to move / Black to move) | kpsolve (A B) | dud_D prediction | CPU s, peak RSS MB |', '|---|---|---|---|---|---|---|']
def one(f, src):
    err = open(f[:-4] + '.err').read() if os.path.exists(f[:-4] + '.err') else ''
    m = re.search(r'cyl:(\d+x\d+) ep=on cap=(\d+).*?, ([\d.]+)s', err)
    rss = re.search(r'peak rss (\d+) KB', err)
    name = os.path.basename(f)[:-4]
    board = ('cyl:' + m.group(1)) if m else name.split('_')[0] + ':' + name.split('_')[1]
    cap = m.group(2) if m else '?'
    cpu = m.group(3) if m else '?'
    lines = [l.strip() for l in open(f) if ' | ' in l and not l.startswith('[')]
    if not lines: 
        rows.append('| %s | %s | %s | (no output: %s) | | | %s |' % (src, board, cap, err.strip().splitlines()[0][:70] if err.strip() else 'none', ''))
        return
    key = None
    for k in pred:
        if k in name: key = k
    byroot = {}
    for l in lines:
        p = l.split(' | ')
        root = ' '.join(p[0].split()[:-2]); stm = p[0].split()[-2]
        byroot.setdefault(root, {})[stm] = p[1]
    for root, d in byroot.items():
        pr = pred.get(key, '') if key and ('Pg' in root or 'pg' in root or key == 'alone') else ''
        if 'Pe3 Pg' in root or True: pass
        rows.append('| %s | %s | %s | `%s`: %s / %s | %s | %s | %s s, %s MB |' % (src, board, cap, root, d.get('w', '?'), d.get('b', '?'), '', pr if pr and 'D2' not in root else '', cpu, (int(rss.group(1)) // 1024) if rss else '?'))
for f in sorted(glob.glob(os.path.join(FIN2, 'chess', '*_c?.out'))): one(f, 'fin2')
open(os.path.join(FIN2, 'logs', 'chess_table.md'), 'w').write('\n'.join(rows) + '\n')
print('\n'.join(rows))
