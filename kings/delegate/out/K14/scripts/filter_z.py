#!/usr/bin/env python3
"""K14 stage 2: Z-alone filter.  For every candidate group (4 combined king states x 2 sides to move = 8 roots) run
kpp --pmodel --moves (P model, real kings) once, and keep the candidates for which
  (1) all 8 roots are (D,D),
  (2) the side to move has its shuttle move with value D, and EVERY other legal move loses at once for the mover
      (value L for White's moves, W for Black's moves, both from White's point of view).
These are necessary conditions for (T1)-(T4) in the P model (the other Z-moves are P-losses in the empty context).
usage: filter_z.py OUT.jsonl CANDS...jsonl   (env BOARDOPT for the --board string is taken from each candidate)"""
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
print('candidates', len(cands), file=sys.stderr)
byboard = {}
for c in cands: byboard.setdefault(c['board'], []).append(c)
res = {}
keep = []
for board, cl in byboard.items():
    for i in range(0, len(cl), 400):
        chunk = cl[i:i + 400]
        posl, meta = [], []
        for c in chunk:
            base = ' '.join(['P' + nm(s) for s in c['P']] + ['p' + nm(s) for s in c['p']])
            for a in c['K']:
                for b in c['k']:
                    for stm in 'wb':
                        posl.append(' '.join(('K%s k%s %s %s -' % (nm(a), nm(b), base, stm)).split())); meta.append((c, a, b, stm))
        p = subprocess.run(HCMD + [os.path.join(D, 'bin', 'kpp'), '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel', '--moves'],
                           input='\n'.join(posl) + '\n', capture_output=True, text=True)
        for line in p.stdout.splitlines():
            if ' | ' not in line: continue
            parts = [x.strip() for x in line.split(' | ')]
            res[parts[0]] = (parts[1].split(), [m.split(':') for m in parts[2].split()] if len(parts) > 2 else [])
        okc = {}
        for pos, (c, a, b, stm) in zip(posl, meta):
            k = json.dumps(c)
            r = res.get(pos)
            ok = r is not None and r[0] == ['D', 'D']
            if ok:
                kingfrom = a if stm == 'w' else b
                shut = [x for x in ([c['K'][0], c['K'][1]] if stm == 'w' else [c['k'][0], c['k'][1]]) if x != kingfrom][0]
                bad = 'L' if stm == 'w' else 'W'
                sh = nm(kingfrom) + nm(shut)
                have = False
                for mv, v in r[1]:
                    if mv == ('K' if stm == 'w' else 'K') + sh:
                        have = True; ok &= (v == 'D')
                    else:
                        ok &= (v == bad)
                ok &= have
            okc[k] = okc.get(k, True) and ok
        for c in chunk:
            if okc[json.dumps(c)]: keep.append(c)
        print(board, i, 'kept so far', len(keep), file=sys.stderr, flush=True)
with open(out_f, 'w') as f:
    for c in keep: f.write(json.dumps(c) + '\n')
print('kept', len(keep), file=sys.stderr)
