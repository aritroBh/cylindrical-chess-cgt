#!/usr/bin/env python3
"""K14: like filter_z.py but writes per-candidate statistics: number of roots (of 8) that are (D,D), number of
non-shuttle moves that do NOT lose at once (the 'leaks'), number of non-shuttle moves in total.
usage: stats_z.py OUT.jsonl CANDS...jsonl"""
import sys, json, subprocess, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAVY = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh'
# K14_DIRECT=1: run under plain nice (only for runs that are far below one CPU-minute, e.g. contexts of <= 3 pawns)
HCMD = ['nice', '-n', '15'] if os.environ.get('K14_DIRECT') else [HEAVY]
def nm(s, W=7): return chr(97 + s % W) + str(s // W + 1)
out_f = sys.argv[1]
seen, cands = set(), []
for f in sys.argv[2:]:
    for l in open(f):
        r = json.loads(l); key = json.dumps([r['board'], r['K'], r['k'], r['P'], r['p']])
        if key in seen: continue
        seen.add(key); cands.append(r)
byboard = {}
for c in cands: byboard.setdefault(c['board'], []).append(c)
out = open(out_f, 'w')
for board, cl in byboard.items():
    for i in range(0, len(cl), 400):
        chunk = cl[i:i + 400]; posl, meta = [], []
        for c in chunk:
            base = ' '.join(['P' + nm(s) for s in c['P']] + ['p' + nm(s) for s in c['p']])
            for a in c['K']:
                for b in c['k']:
                    for stm in 'wb':
                        posl.append(' '.join(('K%s k%s %s %s -' % (nm(a), nm(b), base, stm)).split())); meta.append((c, a, b, stm))
        p = subprocess.run(HCMD + [os.path.join(D, 'bin', 'kpp'), '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel', '--moves'],
                           input='\n'.join(posl) + '\n', capture_output=True, text=True)
        res = {}
        for line in p.stdout.splitlines():
            if ' | ' not in line: continue
            parts = [x.strip() for x in line.split(' | ')]
            res[parts[0]] = (parts[1].split(), [m.split(':') for m in parts[2].split()] if len(parts) > 2 else [])
        st = {}
        for pos, (c, a, b, stm) in zip(posl, meta):
            k = json.dumps(c); s = st.setdefault(k, {'dd': 0, 'roots': 0, 'other': 0, 'leak': 0, 'missing': 0, 'res': []})
            r = res.get(pos); s['roots'] += 1
            if r is None: s['missing'] += 1; continue
            s['dd'] += (r[0] == ['D', 'D']); s['res'].append(''.join(r[0]))
            kf = a if stm == 'w' else b
            shut = [x for x in (c['K'] if stm == 'w' else c['k']) if x != kf][0]
            bad = 'L' if stm == 'w' else 'W'
            for mv, v in r[1]:
                if mv != 'K' + nm(kf) + nm(shut):
                    s['other'] += 1; s['leak'] += (v != bad)
        for c in chunk:
            s = st[json.dumps(c)]; s['group'] = c; out.write(json.dumps(s) + '\n')
        out.flush(); print(board, i, flush=True)
