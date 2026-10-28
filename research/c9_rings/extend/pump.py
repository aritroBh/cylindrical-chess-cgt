#!/usr/bin/env python3
"""pump.py K1 K2 OUT_CAND.tsv -- for every (base C9 hit, cut, ordered pair x+y) that produced a *2/*3 on C11 (12 pawns), build the
rings with the pair inserted k times at the same cut, k = K1..K2 (C_{9+2k} with 10+2k pawns = n+1).  Prints, for k already solved
(res_*.tsv), how many of the pumped rings are *2/*3.  Writes candidates (ring <TAB> provenance) for the unsolved ones."""
import sys, os, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ringlib import *
K1, K2, outfn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
ONLY_STAR2_AT_2 = "--star2-at-2" in sys.argv
hits7 = [l.strip() for l in open(os.path.join(HERE, "hits7.txt")) if l.strip()]
bases = {}
for i, h in enumerate(hits7):
    bases["H%d" % (i + 1)] = h; bases["H%dr" % (i + 1)] = mirror(h)
res = {}
for fn in glob.glob(os.path.join(HERE, "res_*.tsv")):
    for l in open(fn):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 3: res[canon(f[0])] = f[1]
# provenance of the C11 hits (step 1 candidates)
prov = collections.defaultdict(set)    # (basetag, cut, x, y) -> set of C11 hit canon rings
for l in open(os.path.join(HERE, "cand_C11_p12.tsv")):
    ring, pv = l.rstrip("\n").split("\t")
    s = res.get(canon(ring), "")
    if s in ("NNPN", "NNNP"):
        for e in pv.split(";"):
            tag, rest = e.split("@"); c, toks = rest.split(":"); x, y = toks.split("+")
            prov[(tag, int(c), x, y)].add(canon(ring))
print("pump generators (base, cut, x, y) that give a C11 hit: %d" % len(prov))
cands = {}
rows = []
for (tag, c, x, y), _ in sorted(prov.items()):
    t = bases[tag].split()
    if ONLY_STAR2_AT_2 and res.get(canon(" ".join(t[:c] + [x, y] * 2 + t[c:]))) != "NNPN":
        continue
    line = []
    for k in range(K1, K2 + 1):
        ring = " ".join(t[:c] + [x, y] * k + t[c:])
        legal = passed_free(ring)
        cr = canon(ring)
        s = res.get(cr, "-")
        line.append((k, legal, s))
        if legal and cr not in res:
            cands.setdefault(cr, []).append("%s@%d:(%s+%s)^%d" % (tag, c, x, y, k))
    rows.append(((tag, c, x, y), line))
for key, line in rows:
    print(key, " ".join("k%d:%s%s" % (k, "" if lg else "ILLEGAL/", s) for k, lg, s in line))
with open(outfn, "w") as f:
    for r in sorted(cands):
        f.write("%s\t%s\n" % (r, ";".join(cands[r][:3])))
print("candidates to solve:", len(cands))
