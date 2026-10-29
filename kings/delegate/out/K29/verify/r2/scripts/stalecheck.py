#!/usr/bin/env python3
# stalecheck.py : for every 'STALE' line of K29 data/M_*.txt, test with MY move generator (mini.py) that the side to move has no legal move and is not in check
import sys, glob, os, importlib.util
cfgb = {}
for l in open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/scripts/configs.txt'):
    if l.startswith('#') or not l.strip(): continue
    n, b = l.split()[:2]; cfgb[n] = b
tot = ok = 0
for fn in sorted(glob.glob('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/M_*.txt')):
    name = os.path.basename(fn)[2:-4]; board = cfgb[name]
    sys.argv = ['mini', board, 'x']
    spec = importlib.util.spec_from_file_location('mini_' + name, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2/scripts/mini.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for l in open(fn):
        p = [x.strip() for x in l.rstrip('\n').split('|')]
        if len(p) < 6 or 'STALE' not in p[5]: continue
        z, ctx, stm = p[0], p[1], p[2]
        wk, bk, wp, bp = m.parse(z + ' ' + ctx)
        s = 0 if stm == 'w' else 1
        ms = m.moves(s, wk, bk, wp, bp, None)
        inchk = m.incheck(s, wk, bk, wp, bp)
        tot += 1; good = (len(ms) == 0 and not inchk); ok += good
        if not good: print('NOT STALEMATE?', name, l.strip()[:120], len(ms), inchk)
print('STALE lines', tot, 'confirmed stalemate by own move generator', ok)
