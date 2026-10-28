#!/usr/bin/env python3
"""compare lg.cpp (--kmax 3 --query) with lg2k.py on the positions lg2k.py finished."""
import re
lg = {}
for l in open("logs/k_xcheck_lg.txt"):
    p, r = l.rstrip().split(" | ")
    lg[p] = dict(x.split("=") for x in r.split())
n = bad = 0
for l in open("logs/k_xcheck_out.txt"):
    if " | " not in l: continue
    p, r = l.rstrip().split(" | ")
    m = re.match(r"k=(\d+) q=(\d) n=(\S+)", r)
    k, q, v = int(m.group(1)), int(m.group(2)), m.group(3)
    ref = lg[p][("Q" if q else "P") + f"/k{k}"]
    n += 1
    if ref != v: bad += 1; print("MISMATCH", p, k, q, ref, v)
print("budget values compared:", n, "mismatches:", bad)
