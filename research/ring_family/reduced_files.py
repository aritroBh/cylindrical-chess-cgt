import sys
sys.path.insert(0, "research/ring_family")
from reduced import *
ring = from_cstr(sys.argv[1]); n = len(ring)
red = Reducer(n); pos = Pos.parse(to_text(ring))
g = red.value(pos)
print("value", cgt.show(g), "nodes", red.nodes)
cnt = moved_files(red, ring)
files = {}
for (side, f, _), c in cnt.items(): files.setdefault(f, {}).setdefault(side, 0); files[f][side] += c
print("ring files:", " ".join(f"{pawns.FILES[i]}:{c}" for i, c in enumerate(cstr(ring).split())))
for f in range(n): print("  file", pawns.FILES[f], cstr(ring).split()[f], "kept moves from this file:", files.get(f, {}))
