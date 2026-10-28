#!/usr/bin/env python3
"""aggregate.py -- per-split signature histograms of the bulk solves, cross-run comparison, *2/*3 hits.  Writes aggregate.txt."""
import os, gzip, collections, glob

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {"PNNN": "0", "NPNN": "*1", "NNPN": "*2", "NNNP": "*3", "NNNN": "fuzzy (N for h=0..3)", "LLLL": "G>0 (Left wins)",
         "RRRR": "G<0 (Right wins)"}
SPL = ["3_6", "4_5", "5_4", "6_3"]
RUNS = [("orig_c", "original rg on the enum_rings.c set"), ("copy_c", "rg_copy on the enum_rings.c set"),
        ("orig_py", "original rg on the pyenum.py set")]
out = []


def hist(run, sp):
    h = collections.Counter()
    fn = os.path.join(HERE, "solve", "%s_%s.hist.tsv" % (run, sp))
    if not os.path.exists(fn):
        return None
    for l in open(fn):
        k, v = l.split()
        h[k] += int(v)
    return h


tot = {}
for run, desc in RUNS:
    out.append("== %s: %s" % (run, desc))
    T = collections.Counter()
    for sp in SPL:
        h = hist(run, sp)
        if h is None:
            out.append("  split %s: missing" % sp); continue
        s = open(os.path.join(HERE, "solve", "%s_%s.summary.txt" % (run, sp))).read()
        kv = dict(l.split("\t", 1) for l in s.splitlines() if "\t" in l)
        out.append("  split %s: rings %s, solved %s, unresolved %s, redone singly %s, nodes total %s, max %s, wall %ss"
                   % (sp.replace("_", "+"), kv["rings"], kv["solved"], kv["unresolved"], kv["redone_singly"], kv["nodes_total"],
                      kv["nodes_max"], kv["wall_seconds"]))
        T.update(h)
    tot[run] = T
    out.append("  signature counts, all splits: " + ", ".join("%s %d" % (k, v) for k, v in sorted(T.items(), key=lambda x: -x[1])))
    out.append("  rings with *2 (NNPN): %d, *3 (NNNP): %d, any P at h=2 or h=3: %d"
               % (T["NNPN"], T["NNNP"], sum(v for k, v in T.items() if len(k) == 4 and (k[2] == "P" or k[3] == "P"))))
    out.append("")

out.append("== signature counts by split (original rg on the enum_rings.c set)")
sigs_all = sorted(set(k for sp in SPL for k in (hist("orig_c", sp) or {})))
out.append("  %-12s" % "signature" + "".join("%12s" % sp.replace("_", "+") for sp in SPL) + "%12s" % "total")
for s in sigs_all:
    row = [(hist("orig_c", sp) or {}).get(s, 0) for sp in SPL]
    out.append("  %-12s" % (s + (" " + NAMES[s] if s in NAMES else ""))[:12] + "".join("%12d" % x for x in row) + "%12d" % sum(row))
out.append("")

out.append("== cross-run comparison")
for sp in SPL:
    fns = {r: os.path.join(HERE, "solve", "%s_%s.sigs.gz" % (r, sp)) for r, _ in RUNS}
    if os.path.exists(fns["orig_c"]) and os.path.exists(fns["copy_c"]):
        a = gzip.open(fns["orig_c"], "rt").read().split(); b = gzip.open(fns["copy_c"], "rt").read().split()
        out.append("  split %s: original rg vs rg_copy, per-ring signature lists (same enumeration order): %d vs %d rings, identical: %s"
                   % (sp.replace("_", "+"), len(a), len(b), a == b))
    ho, hp = hist("orig_c", sp), hist("orig_py", sp)
    if ho is not None and hp is not None:
        out.append("  split %s: histogram of C-enumerated set == histogram of Python-enumerated set (same orbits, different representatives): %s"
                   % (sp.replace("_", "+"), ho == hp))
open(os.path.join(HERE, "aggregate.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
