#!/usr/bin/env python3
"""analyze.py -- collect all results, list hits, check colour-reversal closure, ancestry of each hit (which C9 hit it contains
after deleting m-9 files), per-size statistics.  Writes hits_all.tsv, ancestry.tsv, stats.txt."""
import sys, os, itertools, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ringlib import *

res = {}      # canon ring -> (sig, nodes)
for fn in sorted(glob.glob(os.path.join(HERE, "res_*.tsv"))):
    for l in open(fn):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 3:
            res[canon(f[0])] = (f[1], int(f[2]), os.path.basename(fn))
base = [canon(l.strip()) for l in open(os.path.join(HERE, "hits7.txt")) if l.strip()]
baseid = {c: "H%d" % (i + 1) for i, c in enumerate(base)}
# fix base ids to match gen_step1 labels (H1..H7 in file order)
hits = {r: v for r, v in res.items() if v[0][2] == "P" or v[0][3] == "P"}
bysize = collections.defaultdict(list)
for r, v in hits.items():
    bysize[len(r.split())].append(r)
out = open(os.path.join(HERE, "hits_all.tsv"), "w")
anc = open(os.path.join(HERE, "ancestry.tsv"), "w")
out.write("files\tpawns\tsignature\tvalue\tring\tcolour_reversal_also_hit\n")
stats = []
for m in sorted(bysize):
    rs = sorted(bysize[m])
    for r in rs:
        s = hits[r][0]
        mir = canon(mirror(r))
        mh = mir in hits and hits[mir][0] == s
        out.write("%d\t%d\t%s\t%s\t%s\t%s\n" % (m, npawns(r), s, sigtype(s), r, "yes" if mh else ("self" if mir == r else "NO")))
        # ancestry: delete m-9 files leaving a C9 hit
        toks = r.split()
        found = collections.defaultdict(list)
        for dele in (itertools.combinations(range(m), m - 9) if m <= 13 else []):
            keep = [toks[i] for i in range(m) if i not in dele]
            c = canon(" ".join(keep))
            if c in baseid:
                found[baseid[c]].append(" ".join(toks[i] for i in dele))
        anc.write("%d\t%s\t%s\n" % (m, r, "; ".join("%s: {%s}" % (k, " | ".join(sorted(set(v)))) for k, v in sorted(found.items()))))
    stats.append((m, len(rs), sum(1 for r in rs if hits[r][0] == "NNPN"), sum(1 for r in rs if hits[r][0] == "NNNP"),
                  sum(1 for r in rs if canon(mirror(r)) in hits)))
out.close(); anc.close()
print("size: hits, *2, *3, colour-reversal-closed")
for s in stats: print(s)
print("total solved rings (distinct up to dihedral):", len(res))
unres = sum(1 for v in res.values() if v[0] == "UNRESOLVED")
print("UNRESOLVED rings:", unres)
print("non-*2/*3 P-at-h>=2 signatures:", [v[0] for v in hits.values() if v[0] not in ("NNPN", "NNNP")])
