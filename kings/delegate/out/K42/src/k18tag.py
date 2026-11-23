#!/usr/bin/env python3
"""write the set of (root, move) pairs that K18's search lists as PLAIN-ONLY at a NOESC root (variant P and Q).
usage: k18tag.py K18_search.gz OUT.json"""
import sys, gzip, re, json
out = {"P": [], "Q": []}
for line in gzip.open(sys.argv[1], "rt"):
    p = [x.strip() for x in line.split("|")]
    if p[0] not in out or p[3] != "NOESC": continue
    Y = " ".join(sorted(p[1].split()[:-2])) + " " + " ".join(p[1].split()[-2:])
    for s in re.findall(r"\[([^\]]*)\]", p[4]):
        t = s.split()
        if t[1] != "PLAIN-ONLY": continue
        m0 = t[0].replace("-", "").replace("x", ""); m0 = m0 if m0[0] == "K" else "P" + m0
        out[p[0]].append([Y, m0])
json.dump(out, open(sys.argv[2], "w")); print({k: len(v) for k, v in out.items()})
