#!/usr/bin/env python3
"""K15 fin2: EXHAUSTIVE single-file contexts.  For a root (group + kings) and a context file X, every assignment of {empty, White pawn, Black
pawn} to the squares X2..X(H-1) (3^(H-2) contexts, no pawn can ever capture: one file), both sides to move.  The prediction is
r(G (+) Z_D) of confirm.solve_d (Theorem 3.4(a) for dud, Proposition 4.6 / its mirror for over, brute force); the actual value is kp_p (--pmodel, exact).
usage: ctx_exh.py BOARD(cyl:8x6) ZTYPE FILE 'root'  (root like 'Kc4 kd6 Pd3 Pd5 pa5 pd4')"""
import sys, itertools, subprocess
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2')
import confirm as C
board, z, X, root = sys.argv[1:5]
W, H = map(int, board.split(':')[1].split('x'))
root = ' '.join(t for t in root.split() if t not in ('w', 'b', '-'))
rows = []
for assign in itertools.product('.WB', repeat=H - 2):
    wl = [f'{X}{r}' for r, a in zip(range(2, H), assign) if a == 'W']
    bl = [f'{X}{r}' for r, a in zip(range(2, H), assign) if a == 'B']
    pw, pb = C.solve_d(H, [C.sq(x) for x in wl], [C.sq(x) for x in bl], z)
    ct = [f'P{x}' for x in wl] + [f'p{x}' for x in bl]
    for stm, pred in (('w', pw), ('b', pb)):
        rows.append((' '.join([root] + ct + [stm, '-']), pred, ''.join(assign)))
inp = '\n'.join(r[0] for r in rows) + '\n'
out = subprocess.run(['/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2/bin/kpp', '--board', board, '--ep', 'on', '--cap', '0', '--pmodel'],
                     input=inp, capture_output=True, text=True).stdout.splitlines()
res = {}
for l in out:
    if '|' in l:
        p, ab = l.split(' | ')[:2]; res[p.strip()] = ab.split()
agree = dis = inex = 0; bad = []
for pos, pred, a in rows:
    A, B = res[pos]
    if A != B: inex += 1; continue
    if A == pred: agree += 1
    else: dis += 1; bad.append((a, pos[-4:-3] if False else pos.split()[-2], pred, A))
print('%s %s file %s: %d contexts x 2 sides = %d positions: agree %d, DISAGREE %d, inexact %d' % (root, z, X, 3 ** (H - 2), len(rows), agree, dis, inex))
for b in bad[:12]: print('   context %s stm %s: predicted %s, kp_p %s' % b)
