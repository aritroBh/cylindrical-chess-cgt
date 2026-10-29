#!/usr/bin/env python3
# depthcmp.py NAME BOARD : own exact-depth check of K29's enum file (ref3d), both sides to move.
import sys, subprocess, os
name, board = sys.argv[1:3]
K = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
B = K + 'verify/bin/ref3d'
rows = []
for l in open(K + 'data/enum_%s.txt' % name):
    z, d = l.rsplit(' | ', 1); rows.append((z.strip(), tuple(map(int, d.split()))))
ins = []
for z, _ in rows: ins += [z + ' w -', z + ' b -']
r = subprocess.run([B, '--board', board, '--moves'], input='\n'.join(ins) + '\n', capture_output=True, text=True)
out = [l for l in r.stdout.splitlines() if ' | ' in l]
assert len(out) == len(ins), (len(out), len(ins))
bad = 0; nlw = 0; res = []
for i, (z, (dw, db)) in enumerate(rows):
    a = out[2*i].rsplit(' | ', 1)[1].split(); b = out[2*i+1].rsplit(' | ', 1)[1].split()
    ok = a[0] == 'L' and b[0] == 'W'
    nlw += ok
    mydw = int(a[1][2:]); mydb = int(b[1][2:])
    # per-move punisher lengths: T_P(m) = (d+1)/2
    tw = sorted(set((int(x.split(':')[2]) + 1) // 2 for x in a[2:] if x.split(':')[1] == 'L'))
    tb = sorted(set((int(x.split(':')[2]) + 1) // 2 for x in b[2:] if x.split(':')[1] == 'W'))
    if not ok or (mydw, mydb) != (dw, db): bad += 1; print('MISMATCH', z, (dw, db), (mydw, mydb), a[0], b[0])
    res.append((z, mydw, mydb, tw, tb))
print(name, 'groups', len(rows), 'LW-ok', nlw, 'depth mismatches vs K29 enum', bad, 'min over groups of max depth', min(max(r[1], r[2]) for r in res), 'max', max(max(r[1], r[2]) for r in res))
with open(K + 'verify/me/depth_%s.txt' % name, 'w') as f:
    for z, a, b, tw, tb in res: f.write('%s | %d %d | T_P(m) values white %s black %s\n' % (z, a, b, tw, tb))
