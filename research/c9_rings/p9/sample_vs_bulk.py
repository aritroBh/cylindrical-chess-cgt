#!/usr/bin/env python3
"""sample_vs_bulk.py -- the signatures of the sampled rings (fresh original-rg process per batch of 40) must equal the signatures
the bulk run (orig_py, persistent process) gave to the same rings.  Writes sample/sample_vs_bulk.txt."""
import os, gzip, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sizes = {"3+6": 28160, "4+5": 446270, "5+4": 446270, "6+3": 28160}
offset = {}; o = 0
for sp in ("3+6", "4+5", "5+4", "6+3"):
    offset[sp] = o; o += sizes[sp]
bulk = {sp: gzip.open(os.path.join(HERE, "solve", "orig_py_%s.sigs.gz" % sp.replace("+", "_")), "rt").read().split() for sp in sizes}
out = []
for name in ("sample300", "bonus100"):
    meta = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "sample", name + "_meta.tsv"))]
    sig = gzip.open(os.path.join(HERE, "sample", "orig_%s.sigs.gz" % name), "rt").read().split()
    assert len(meta) == len(sig)
    bad = 0; per = collections.Counter(); star = 0
    for (i, sp, ring), s in zip(meta, sig):
        j = int(i) - offset[sp]
        per[sp] += 1
        if bulk[sp][j] != s:
            bad += 1
        if s[2] == "P" or s[3] == "P":
            star += 1
    out.append("%s: %d rings %s; signature differs from the bulk run for %d rings; rings with *2/*3-type P at h=2 or 3: %d"
               % (name, len(meta), dict(sorted(per.items())), bad, star))
open(os.path.join(HERE, "sample", "sample_vs_bulk.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
