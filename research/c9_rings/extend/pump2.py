#!/usr/bin/env python3
"""pump2.py SRC_RES SIZE_STEP K1 K2 OUT_CAND.tsv [--star2-at K] -- generalised pumping.
SRC_RES: result file whose *2/*3 rings are the sources.  For every source ring, every cut c and every ordered pair (x,y) of single-pawn
tokens whose single insertion (k=1) is itself a *2/*3 in the known results (res_*.tsv), build the ring with (x,y) inserted k times at
cut c, k = K1..K2, and print the signature of those already solved.  --star2-at K : keep only generators whose k=K ring is NNPN.
Writes unsolved candidates to OUT_CAND.tsv."""
import sys, os, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ringlib import *
a = sys.argv[1:]
src_res, K1, K2, outfn = a[0], int(a[2]), int(a[3]), a[4]
starK = int(a[a.index("--star2-at") + 1]) if "--star2-at" in a else None
res = {}
for fn in glob.glob(os.path.join(HERE, "res_*.tsv")):
    for l in open(fn):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 3: res[canon(f[0])] = f[1]
srcs = sorted(set(canon(l.split("\t")[0]) for l in open(src_res) if l.split("\t")[1][2:3] == "P" or l.split("\t")[1][3:4] == "P"))
print("sources:", len(srcs), "of size C%d" % len(srcs[0].split()))
cands = {}; table = []; ngen = 0
for si, r in enumerate(srcs):
    t = r.split(); n = len(t)
    for c in range(n):
        for x in SINGLES:
            for y in SINGLES:
                r1 = " ".join(t[:c] + [x, y] + t[c:])
                if not passed_free(r1) or res.get(canon(r1)) not in ("NNPN", "NNNP"):
                    continue
                if starK is not None:
                    rk = " ".join(t[:c] + [x, y] * starK + t[c:])
                    if not passed_free(rk) or res.get(canon(rk)) != "NNPN":
                        continue
                ngen += 1
                row = []
                for k in range(K1, K2 + 1):
                    rk = " ".join(t[:c] + [x, y] * k + t[c:])
                    cr = canon(rk); lg = passed_free(rk)
                    row.append((k, lg, res.get(cr, "-")))
                    if lg and cr not in res:
                        cands.setdefault(cr, []).append("src%d@%d:(%s+%s)^%d" % (si, c, x, y, k))
                table.append(((si, c, x, y), row))
print("generators (source, cut, x, y) with k=1 a *2/*3 and passing the filter: %d" % ngen)
for key, row in table:
    print(key, " ".join("k%d:%s%s" % (k, "" if lg else "ILLEGAL/", s) for k, lg, s in row))
with open(outfn, "w") as f:
    for r in sorted(cands):
        f.write("%s\t%s\n" % (r, ";".join(cands[r][:3])))
print("candidates to solve:", len(cands))
