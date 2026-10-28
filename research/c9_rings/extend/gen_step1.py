#!/usr/bin/env python3
"""gen_step1.py -- base rings (7 hits + colour reversals), insert single (C10, 11 pawns) and pair (C11, 12 pawns);
write candidate lists, legality statistics, cross-check legality with cylcgt.pawns.passed."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ringlib import *

HERE = os.path.dirname(os.path.abspath(__file__))
hits = [l.strip() for l in open(os.path.join(HERE, "hits7.txt")) if l.strip()]
base = []   # (ring, tag)
for i, h in enumerate(hits):
    base.append((h, "H%d" % (i + 1)))
    base.append((mirror(h), "H%dr" % (i + 1)))
# orbit structure
orbit = collections.defaultdict(list)
for r, tag in base:
    orbit[canon(r)].append(tag)
print("base rings: %d, distinct dihedral orbits: %d" % (len(base), len(orbit)))
for c, tags in orbit.items():
    print("  ", tags, "pawns", npawns(c), "legal", passed_free(c), "|", c)

# legality cross-check with cylcgt
os.chdir(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.getcwd())
from cylcgt import pawns
def cyl_legal(ring):
    cfg = parse(ring); n = len(cfg)
    W = frozenset((f, r) for f, (w, b) in enumerate(cfg) for r in w)
    B = frozenset((f, r) for f, (w, b) in enumerate(cfg) for r in b)
    bd = pawns.Board(n, 8, True, True)
    p = pawns.Pos(W, B)
    return not pawns.passed(bd, p, "W") and not pawns.passed(bd, p, "B")

for k, label in ((1, "C10_p11"), (2, "C11_p12")):
    cand = {}          # canon -> list of (basetag, cut, inserted)
    total = 0; legal_n = 0; mism = 0
    for r, tag in base:
        for c, ins, new in insertions(r, k):
            total += 1
            a = passed_free(new)
            if a != cyl_legal(new):
                mism += 1
            if a:
                legal_n += 1
                cand.setdefault(canon(new), []).append((tag, c, "+".join(ins)))
    print("%s: generated %d, legal %d, distinct up to dihedral %d, legality mismatches vs cylcgt %d" % (label, total, legal_n, len(cand), mism))
    with open(os.path.join(HERE, "cand_%s.tsv" % label), "w") as f:
        for ring in sorted(cand):
            f.write("%s\t%s\n" % (ring, ";".join("%s@%d:%s" % x for x in cand[ring])))
