#!/usr/bin/env python3
"""Stratum G3 for the cap-1 spot check: White pawn on file c, e or f, Black pawn on file c, d or f (the files G1 and G2
do not touch).  110 uniform random positions per board from the kpsolve tables.  Run from the project root:
    .venv/bin/python -I research/kpkp/t44/make_checks_g3.py
Writes chk_cyl_G3.exp and chk_flat_G3.exp (`position | A B`, values from the table)."""
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(20261024)
for board in ('cyl', 'flat'):
    sel, n = [], 0
    for i in range(4):
        p = subprocess.Popen(['zstdcat', os.path.join(HERE, 'kpkp_%s_%d.out.zst' % (board, i))],
                             stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
        for line in p.stdout:
            t = line.split()
            if t[1][1] in 'cef' and t[3][1] in 'cdf':
                n += 1
                if len(sel) < 110:
                    sel.append(line.rstrip('\n'))
                else:
                    j = rng.randrange(n)
                    if j < 110:
                        sel[j] = line.rstrip('\n')
        p.wait()
    with open(os.path.join(HERE, 'chk_%s_G3.exp' % board), 'w') as f:
        f.write('\n'.join(sel) + '\n')
    print(board, 'G3 stratum size', n, 'sampled', len(sel))
