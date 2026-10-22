import sys, subprocess
sys.path.insert(0, "research/ring_family")
from known import KNOWN
from ringlib import *
for n, L in KNOWN.items():
    seen = {}
    for t in L:
        c = canon(to_ring(t, n))
        seen.setdefault(c, []).append(t)
    print(f"C{n}: {len(L)} listed, {len(seen)} classes")
    for c in seen: print("   ", cstr(c), "   ", evaluate([c])[0])
