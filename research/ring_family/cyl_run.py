"""cyl_run.py "<cstr>" [whole]  -- evaluate a ring with cylcgt (default setting), print value and time."""
import sys, time, resource
sys.path.insert(0, "research/ring_family")
from ringlib import *
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos
ring = from_cstr(sys.argv[1]); n = len(ring)
whole = len(sys.argv) > 2 and sys.argv[2] == "whole"
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True; pawns._value.cache_clear()
if whole:
    pawns.components = lambda b, p: [p]
text = to_text(ring)
print(f"C{n} pawns={nparts(ring)} whole={whole}: {text}", flush=True)
t0 = time.time()
g = pawns.value(Board(n, 8, True, True), Pos.parse(text))
print(f"value = {cgt.show(g)}  time {time.time()-t0:.1f}s  maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20:.0f} MB", flush=True)
