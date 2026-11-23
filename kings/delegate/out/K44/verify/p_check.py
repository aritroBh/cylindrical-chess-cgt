#!/usr/bin/env python3
"""Referee check of K44 item 3: (a) the D 'alone' column of each key file is recomputed with rk (own LK solver);
(b) ref3m and kp_p results are compared line by line; (c) D = P agreement is counted.
usage: p_check.py RKBIN BOARD PREFIX   (PREFIX = logs/p7, logs/p8, logs/p7n, logs/o2)"""
import lzma, subprocess, sys, os, collections
rk, board, pre = sys.argv[1:4]
here = os.path.dirname(os.path.abspath(__file__)); base = os.path.dirname(here)
rd = lambda suf: [l.rstrip('\n') for l in lzma.open(os.path.join(base, pre + suf + '.xz'), 'rt')]
key = rd('.key'); kpp = rd('.kpp'); ref = rd('.ref3')
assert len(key) == len(kpp) == len(ref)
cfgs = collections.defaultdict(list)
for l in key:
    pos, nm, cn, d = [x.strip() for x in l.rsplit(' | ', 3)]
    cfgs[cn].append((pos, d))
mine = {}
for cn in [c for c in cfgs if c != 'n0']:
    pawns = ','.join(cn.split()) if cn not in ('none', '') else ''
    out = subprocess.run([rk, board, 'all', pawns], capture_output=True, text=True, env=dict(os.environ, RK_ALL='1')).stdout
    for l in out.splitlines():
        if l.startswith('K'):
            p = l.split(); a = p[3].split(':')[1]
            mine[(cn, p[0], p[1], 'w')] = a[0]; mine[(cn, p[0], p[1], 'b')] = a[1]
dbad = dmiss = 0
for cn, lst in cfgs.items():
    for pos, d in lst:
        t = pos.split(); k = (cn, t[0], t[1], t[-2])
        if k not in mine: dmiss += 1; continue
        if mine[k] != d: dbad += 1
diff = legal = agree = 0; bound_gap = 0
for lk, lp, lr in zip(key, kpp, ref):
    pos, nm, cn, d = [x.strip() for x in lk.rsplit(' | ', 3)]
    p1, b = lp.rsplit('|', 1); b = b.split(); p2, r = lr.rsplit('|', 1); r = r.strip()
    assert p1.strip() == pos and p2.strip() == pos
    if len(b) == 2 and b[0] != b[1]: bound_gap += 1
    if b[0] != r: diff += 1
    if r == 'X': continue
    legal += 1; agree += (r == d)
print(f'{pre}: lines {len(key)}, D column recomputed by rk: {len(key)-dmiss} found, {dbad} differ, {dmiss} not roots of rk;'
      f' ref3m vs kp_p differ {diff}, kp_p bound gaps {bound_gap}; legal {legal}, D = P {agree} ({100*agree/max(1,legal):.1f} percent)')
