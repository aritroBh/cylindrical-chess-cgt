"""Run the existing cylcgt.dawson.solve for n <= N (partizan canonical forms of the start diagram).
    PYTHONPATH=. .venv/bin/python -u dawson/run_cylcgt_dawson.py 7 > dawson/cylcgt_dawson_small.txt
"""
import sys, time
from cylcgt import dawson, cgt
for n in range(1, int(sys.argv[1]) + 1):
    for wrap in (False, True):
        if wrap and n < 3: continue
        t = time.time()
        v = dawson.solve(n, wrap)
        print(f"{'cyl' if wrap else 'flat'} n={n}: value {cgt.show(v)}  outcome {cgt.outcome(v)}  ({time.time()-t:.1f}s)", flush=True)
