#!/usr/bin/env python3
"""pump3.py OUT_CAND.tsv -- candidate families of rings *3 with n+1 pawns.  Takes every ring that rg found *3 (NNNP)
with n+1 pawns on C11, C12, C13 (../extend/res_C1[123]_p1[234].tsv) and, for every cut c, repeats the two files
c, c+1 k = 1..4 more times (the insertion of the wall-family proofs; it keeps n+1 pawns iff those two files hold one
pawn each).  Writes the legal (no passed pawn) rings not yet solved, with provenance base@c^k."""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "extend"))
from ringlib import canon, passed_free, npawns
EXT = os.path.join(HERE, "..", "extend")
bases = []
for fn in sorted(glob.glob(os.path.join(EXT, "res_C1[123]*_p1[234].tsv"))):
    for l in open(fn):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 2 and f[1] == "NNNP":
            bases.append(f[0])
seen, uniq = set(), []
for b in bases:
    if canon(b) not in seen:
        seen.add(canon(b)); uniq.append(b)
print("bases (distinct *3 rings with n+1 pawns):", len(uniq))
cands = {}
for bi, b in enumerate(uniq):
    t = b.split(); n = len(t)
    for c in range(n):
        pair = [t[c], t[(c + 1) % n]]
        if len(pair[0]) != 2 or len(pair[1]) != 2:      # keep n+1 pawns: one pawn on each repeated file
            continue
        for k in range(1, 5):
            r = t[c:] + t[:c]                       # rotate so that files c, c+1 come first
            tt = r[:2] + pair * k + r[2:]           # repeat files c, c+1 after c+1
            ring = " ".join(tt)
            if not passed_free(ring):
                continue
            assert npawns(ring) == len(tt) + 1
            cands.setdefault(canon(ring), []).append("B%d@%d^%d" % (bi, c, k))
with open(sys.argv[1], "w") as f:
    for r in sorted(cands):
        f.write("%s\t%s\n" % (r, ";".join(cands[r][:4])))
with open(os.path.join(HERE, "bases.txt"), "w") as f:
    for bi, b in enumerate(uniq):
        f.write("B%d\t%s\n" % (bi, b))
print("candidates:", len(cands))
