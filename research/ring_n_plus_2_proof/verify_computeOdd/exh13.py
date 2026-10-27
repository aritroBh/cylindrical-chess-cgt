"""exh13.py -- the no-early-exit (every child, every heap move) search for R_13 only ('keep'), h = 0..4; about 4 million states.
Usage: python exh13.py [FAM] [N]"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oddeng as O          # noqa: E402

fam = sys.argv[1] if len(sys.argv) > 1 else 'R'
n = int(sys.argv[2]) if len(sys.argv) > 2 else 13
t0 = time.time()
F = O.Full('keep', exhaustive=True)
sig = F.signature(O.start(fam, n), range(5))
print(f'exh {fam}_{n} pawns={n + 2} exhaustive-keep: {sig} ({len(F.memo)} states, {time.time() - t0:.0f}s)', flush=True)
