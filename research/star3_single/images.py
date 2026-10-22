#!/usr/bin/env python3
"""images.py WIDTH FILE [ring]: print every distinct image of each position under file mirror and colour reversal
(rank r -> 9-r, colours swapped); with 'ring' also all cyclic file shifts.  Colour reversal maps a nimber to itself."""
import re, sys
width = int(sys.argv[1]); ring = len(sys.argv) > 3 and sys.argv[3] == "ring"
def parse(l):
    w, b = l.split("/")
    f = lambda s: [(ord(x[0]) - 97, int(x[1:])) for x in re.findall(r"[a-h][1-8]", s)]
    return frozenset(f(w)), frozenset(f(b))
def fmt(w, b):
    n = lambda s: " ".join(sorted(f"{chr(97+f)}{r}" for f, r in s))
    return f"W: {n(w)} / B: {n(b)}"
seen = []
for line in open(sys.argv[2]):
    line = line.strip()
    if not line or line.startswith("#"): continue
    w, b = parse(line)
    for rev in (0, 1):
        ww, bb = (frozenset((f, 9 - r) for f, r in b), frozenset((f, 9 - r) for f, r in w)) if rev else (w, b)
        for refl in (0, 1):
            for sh in (range(width) if ring else [0]):
                def m(s):
                    out = []
                    for f, r in s:
                        g = width - 1 - f if refl else f
                        out.append(((g + sh) % width if ring else g, r))
                    return frozenset(out)
                p = fmt(m(ww), m(bb))
                if p not in seen: seen.append(p)
print("\n".join(seen))
