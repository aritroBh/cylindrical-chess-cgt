#!/usr/bin/env python3
"""gen_ctx.py ZGROUP CTXFILES MAXW MAXB RANKS  -> positions (both sides to move) for Z + every context.
ZGROUP e.g. 'Ka4 Pb3 kc3 pb4'; CTXFILES e.g. 'ef'; ranks lo-hi like 2-5 (squares where context pawns may stand)."""
import sys, itertools
z, files, maxw, maxb, rr = sys.argv[1:6]
maxw, maxb = int(maxw), int(maxb)
lo, hi = map(int, rr.split('-'))
sqs = [f + str(r) for f in files for r in range(lo, hi + 1)]
n = 0
for assign in itertools.product('.WB', repeat=len(sqs)):
    if assign.count('W') > maxw or assign.count('B') > maxb: continue
    toks = [('P' if a == 'W' else 'p') + s for a, s in zip(assign, sqs) if a != '.']
    for stm in 'wb':
        print(' '.join([z] + toks + [stm, '-']))
        n += 1
sys.stderr.write(f'{n} positions\n')
