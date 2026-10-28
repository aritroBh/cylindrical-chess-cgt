#!/usr/bin/env python3
"""compare.py -- compare the ring sets of enum_rings.c (c/c_rings_*) and pyenum.py (py/py_rings_*) split by split.
Both sides are re-canonicalised here under the dihedral group (min over the 18 images of the token tuple), so the comparison
does not depend on either program's choice of orbit representative.  Writes compare.txt."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def canon(line):
    t = line.split()
    n = len(t)
    best = None
    for s in range(n):
        for im in (tuple(t[(i + s) % n] for i in range(n)), tuple(t[(s - i) % n] for i in range(n))):
            if best is None or im < best:
                best = im
    return best


def load(path):
    rings = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rings.append(line.rstrip("\n"))
    return rings


out = []
allok = True
for nw in range(1, 9):
    nb = 9 - nw
    c = load(os.path.join(HERE, "c", "c_rings_%d_%d.txt" % (nw, nb)))
    p = load(os.path.join(HERE, "py", "py_rings_%d_%d.txt" % (nw, nb)))
    cs = set(canon(r) for r in c)
    ps = set(canon(r) for r in p)
    same_raw = set(c) == set(p)
    ok = (cs == ps) and len(cs) == len(c) == len(p) == len(ps)
    allok &= ok
    out.append("split %d+%d: enum_rings.c %d rings (%d distinct orbits) | pyenum.py %d rings (%d distinct orbits) | "
               "only-in-C %d, only-in-py %d | identical as raw strings: %s | AGREE: %s"
               % (nw, nb, len(c), len(cs), len(p), len(ps), len(cs - ps), len(ps - cs), same_raw, ok))
out.append("ALL SPLITS AGREE" if allok else "DISAGREEMENT")
open(os.path.join(HERE, "compare.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
