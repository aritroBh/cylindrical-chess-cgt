"""Probe: flag-free roots near the no-(E) witness (does the failure survive without a root right?)."""
import sys
sys.path.insert(0, "kings/delegate/out/K52/integrate")
from verify import *  # noqa  (prints verify's own checks first)

print("== probe: flag-free predecessors")
for text in ("W: a2 b3 e2 / B: a5 b4 e4", "W: a2 b2 b3 e2 e4 / B: a5 b4 b6 e6", "W: a2 b3 e2 / B: a5 b4 e5",
             "W: a2 b3 d2 / B: a5 b4 d4", "W: a2 b3 e3 / B: a5 b4 e5"):
    report("flag-free", b57, Pos.parse(text))
