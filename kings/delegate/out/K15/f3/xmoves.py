#!/usr/bin/env python3
"""CHECKED-2 of the empty-context move lists: kp_p (K7 P model) versus ref3m (K23 referee solver, independent code).
usage: xmoves.py BOARD GROUPFILE   (ref3 board syntax: cyl:7x6, flat7x6 for flat boards)
For every group: the king states by BFS over D-valued king moves (conf2.states_of), both sides to move; the move lists
(move:value sets) and the root values must agree between the two solvers."""
import sys, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conf2 as K
board, gfile = sys.argv[1], sys.argv[2]
rboard = board.replace('flat:', 'flat') if board.startswith('flat') else board
W, H = map(int, board.split(':')[1].split('x')) if ':' in board else map(int, board[4:].split('x'))
tot = bad = 0
for l in open(gfile):
    l = l.strip().split('\t')[0]
    if not l: continue
    p = K.parse(l)
    if board.startswith('cyl'): p = K.shift_left(p, W)
    toks = [f"{c}{K.FILES[f]}{r}" for c, f, r in sorted(p, key=lambda x: ('KkPp'.index(x[0]), x[1], x[2]))]
    sts = K.states_of(board.replace('flat7x6', 'flat:7x6'), W, toks)
    pw = [t for t in toks if t[0] in 'Pp']
    lines = []
    for ks in sts:
        for stm in 'wb': lines.append(' '.join([ks[0], ks[1]] + pw + [stm, '-']))
    a = subprocess.run([K.KPP, '--board', board.replace('flat7x6', 'flat:7x6'), '--ep', 'on', '--cap', '0', '--pmodel', '--moves'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
    b = subprocess.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref3m'), '--board', rboard, '--moves'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
    a = [x for x in a if ' | ' in x]; b = [x for x in b if ' | ' in x]
    for x, y in zip(a, b):
        px = x.split(' | '); py = y.split(' | ')
        ax = px[1].split()[0] if px[1].split()[0] == px[1].split()[1] else '?' if False else px[1].split()[0]
        rx = (px[0], px[1].split()[0], sorted(px[2].split()))
        # kp_p prints 'A B' (equal when exact); ref3m prints one letter then the moves
        ry = py[1].split(); ry0 = ry[0]; rmoves = sorted(ry[1:])
        tot += 1
        okv = (px[1].split()[0] == ry0 and px[1].split()[1] == ry0)
        # compare move sets ignoring the king-from-square spelling (both use KxyXY form); normalise kp_p's
        if not (okv and rx[2] == rmoves):
            bad += 1; print('MISMATCH', px[0], px[1], rx[2], '| ref3m', ry0, rmoves)
    print(f"{l}: states={len(sts)} positions={len(lines)}")
print(f"positions compared {tot}, mismatches {bad}")
