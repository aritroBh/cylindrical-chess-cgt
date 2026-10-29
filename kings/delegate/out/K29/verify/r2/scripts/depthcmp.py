#!/usr/bin/env python3
# depthcmp.py BOARD ENUMFILE [N] : compare K29 enum loss depths (plies) with my own mini.py solver, first N groups (or all)
import sys, subprocess
sys.argv_ = sys.argv
board, ef = sys.argv[1], sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
sys.argv = ['mini', board, 'x']
import importlib.util
spec = importlib.util.spec_from_file_location('mini', '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2/scripts/mini.py'); m = importlib.util.module_from_spec(spec)
sys.argv = ['mini', board, 'x']; spec.loader.exec_module(m)
bad = n = 0
import random
lines = [l.strip() for l in open(ef) if l.strip() and max(map(int, l.split(' | ')[1].split())) <= 14]
if N < len(lines): random.seed(5); lines = random.sample(lines, N)
for l in lines:
    z, d = l.split(' | '); a, b = map(int, d.split())
    wk, bk, wp, bp = m.parse(z)
    r = []
    for stm in (0, 1):
        dd = None
        for k in range(2, 17, 2):
            if m.lost(stm, wk, bk, wp, bp, None, k): dd = k; break
        r.append(dd)
    n += 1
    if r != [a, b]: bad += 1; print('DIFF', z, 'K29', a, b, 'mine', r)
    m.lost.cache_clear(); m.win.cache_clear()
print(ef, 'groups', n, 'depth differences', bad)
