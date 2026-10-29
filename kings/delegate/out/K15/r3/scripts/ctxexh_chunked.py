#!/usr/bin/env python3
"""K15 r3: exhaustive single-file contexts (3^(H-2) assignments of {empty, W, B} to X2..X(H-1), both sides to move) for one root, over/dud/under prediction
by fin2/confirm.solve_d, actual value by kp_p --pmodel (r3 build), run in chunks of CH positions each under ulimit -t 58 (nice 15; halved when a chunk does not finish).
usage: ctxexh_chunked.py BOARD ZTYPE FILE 'root' OUTFILE [CH=6]"""
import sys, itertools, subprocess, os, resource
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FIN2 = os.path.join(os.path.dirname(R3), 'fin2')
sys.path.insert(0, FIN2)
import confirm as C
board, z, X, root, outf = sys.argv[1:6]; CH = int(sys.argv[6]) if len(sys.argv) > 6 else 6
MAXP = int(sys.argv[7]) if len(sys.argv) > 7 else 99
MINP = int(sys.argv[8]) if len(sys.argv) > 8 else 0   # only contexts with at least MINP pawns
NOLIM = os.environ.get('NOLIMIT') == '1'            # no CPU limit (use under heavy.sh only)   # skip contexts with more than MAXP pawns (they do not fit one CPU-minute)
W, H = map(int, board.split(':')[1].split('x'))
root = ' '.join(t for t in root.split() if t not in ('w', 'b', '-'))
rows = []
for assign in itertools.product('.WB', repeat=H - 2):
    wl = [f'{X}{r}' for r, a in zip(range(2, H), assign) if a == 'W']; bl = [f'{X}{r}' for r, a in zip(range(2, H), assign) if a == 'B']
    if not (MINP <= sum(1 for a in assign if a != '.') <= MAXP): continue
    pw, pb = C.solve_d(H, [C.sq(x) for x in wl], [C.sq(x) for x in bl], z)
    ct = [f'P{x}' for x in wl] + [f'p{x}' for x in bl]
    for stm, pred in (('w', pw), ('b', pb)): rows.append((' '.join([root] + ct + [stm, '-']), pred, ''.join(assign)))
def run(lines):
    def pre():
        if not NOLIM: resource.setrlimit(resource.RLIMIT_CPU, (58, 58))
        os.nice(15)
    p = subprocess.run([os.path.join(R3, 'bin', 'kpp'), '--board', board, '--ep', 'on', '--cap', '0', '--pmodel'], input='\n'.join(lines) + '\n', capture_output=True, text=True, preexec_fn=pre)
    return {l.split(' | ')[0].strip(): l.split(' | ')[1].split() for l in p.stdout.splitlines() if ' | ' in l}
res = {}
def go(lines):
    r = run(lines); res.update(r)
    rest = [l for l in lines if l not in r]
    if rest:
        if len(rest) == 1: print('MISSING', rest[0], file=sys.stderr); return
        h = len(rest) // 2; go(rest[:h]); go(rest[h:])
allp = [r[0] for r in rows]
for i in range(0, len(allp), CH): go(allp[i:i + CH])
agree = dis = inex = miss = 0; bad = []
for pos, pred, a in rows:
    v = res.get(pos)
    if v is None: miss += 1; continue
    if v[0] != v[1]: inex += 1; continue
    if v[0] == pred: agree += 1
    else: dis += 1; bad.append((a, pos.split()[-2], pred, v[0]))
s = '%s %s file %s: %d contexts (%d to %d pawns) x 2 sides = %d positions: agree %d, DISAGREE %d, inexact %d, missing %d\n' % (root, z, X, len(rows) // 2, MINP, MAXP, len(rows), agree, dis, inex, miss)
for b in bad: s += '   context %s stm %s: predicted %s, kp_p %s\n' % b
open(outf, 'a').write(s); print(s)
