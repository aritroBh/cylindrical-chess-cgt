"""ext_a.py -- extension of (a) beyond n = 25: my engine (mode keep), R_n and Qo_n for odd n = LO..HI, h = 0..5.   Usage: python ext_a.py LO HI"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oddeng as O          # noqa: E402

lo, hi = int(sys.argv[1]), int(sys.argv[2])
for fam, k in (('R', 2), ('Qo', 3)):
    want = ''.join('P' if h == k else 'N' for h in range(6))
    for n in range(lo, hi + 1, 2):
        t0 = time.time()
        F = O.Full('keep')
        sig = F.signature(O.start(fam, n), range(6))
        print(f'ext {fam}_{n} pawns={n + 2}: {sig} ({len(F.memo)} states, {time.time() - t0:.0f}s) {"== *%d" % k if sig == want else "DIFFERENT from " + want}', flush=True)
