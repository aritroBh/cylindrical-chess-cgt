#!/usr/bin/env python3
"""Referee's own re-run of K20's enumeration (the K44 baseline) with rk: at most two blocked pairs on distinct files
at file distance 1..3 (window 4), pair ranks 2..4, H = 6; cyl:6..10 and pln:6..8; free board and box(m), m = 0, 1, 2
(arc of the pawn files widened by m; on a cylinder every minimal arc; a box covering the whole width is the free run;
on a flat board the box is clipped to the board). Writes the set of B34 signatures of full-pawn-set roots.
usage: base_rk.py RKBIN"""
import subprocess, sys, os
rk = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
code = {'W': '0', 'D': '1', 'L': '2'}
L = 'abcdefghijklmnop'
def run(board, reg, pawns):
    out = subprocess.run([rk, board, reg, pawns], capture_output=True, text=True, env=dict(os.environ, RK_ALL='1')).stdout
    return {''.join(code[c] for p in l.split()[3:] for c in p.split(':')[-1]) for l in out.splitlines() if l.startswith('K')}
sig = {'cyl': set(), 'pln': set()}; sig0 = set(); cases = 0
for kind, widths in (('cyl', range(6, 11)), ('pln', range(6, 9))):
    for W in widths:
        board = f'{kind}:{W}x6'
        s0 = run(board, 'all', ''); sig0 |= s0; sig[kind] |= s0; cases += 1
        cfgs = []
        starts = [0] if kind == 'cyl' else range(W)
        for f in starts:
            for r in (2, 3, 4):
                cfgs.append(([f], [r]))
            for d in (1, 2, 3):
                g = f + d
                if kind == 'pln' and g >= W: continue
                for r in (2, 3, 4):
                    for q in (2, 3, 4):
                        cfgs.append(([f, g % W], [r, q]))
        for files, ranks in cfgs:
            pawns = ','.join(f'{L[a]}{b}' for a, b in zip(files, ranks))
            sig[kind] |= run(board, 'all', pawns); cases += 1
            # minimal arcs
            if len(files) == 1: arcs = [(files[0], files[0])]
            else:
                a, b = files; d = (b - a) % W if kind == 'cyl' else b - a
                arcs = [(a, b)]
                if kind == 'cyl' and W - d == d: arcs.append((b, a))
            for m in (0, 1, 2):
                for lo, hi in arcs:
                    span = ((hi - lo) % W if kind == 'cyl' else hi - lo) + 1 + 2 * m
                    if kind == 'cyl':
                        if span >= W: continue
                        reg = f'{(lo - m) % W}-{(hi + m) % W}'
                    else:
                        l2, h2 = max(0, lo - m), min(W - 1, hi + m)
                        if l2 == 0 and h2 == W - 1: continue
                        reg = f'{l2}-{h2}'
                    sig[kind] |= run(board, reg, pawns); cases += 1
allb = sig['cyl'] | sig['pln']
open(os.path.join(here, 'sigs_base.txt'), 'w').write(''.join(x + '\n' for x in sorted(allb)))
print(f'baseline cases {cases}: distinct signatures cyl {len(sig["cyl"])}, flat {len(sig["pln"])}, together {len(allb)}; pawnless {len(sig0)}')
