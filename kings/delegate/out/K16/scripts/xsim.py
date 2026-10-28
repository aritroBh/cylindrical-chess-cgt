#!/usr/bin/env python3
"""xsim.py META...: compare the strategy-simulation flags of chk.c (meta files) with the independent Python search classify.py
(pyp.py move generator): mask==0 <-> 'strategy_wins', bit 16 <-> omega_stalemated_at_y, bit 1 only <-> omega_stalemated."""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts')
import classify
spec = sys.argv[1]
n = bad = 0
from collections import Counter
c = Counter()
for f in sys.argv[2:]:
    for l in open(f):
        pos, toks = l.rstrip('\n').split(' | ')
        for tok in toks.split():
            b, p, fl = tok.split(':')
            mask = int(fl.split('.')[0], 16)
            kind = classify.classify(spec, pos, 0 if b == 'W' else 1, p)[0]
            exp = 'strategy_wins' if mask == 0 else ('omega_stalemated_at_y' if mask & 16 else ('omega_stalemated' if mask == 1 else 'other'))
            n += 1; c[kind] += 1
            if kind != exp:
                bad += 1
                if bad < 6: print("DIFF", pos, tok, kind, exp)
print("xsim", spec, "instances", n, "disagreements", bad, dict(c))
