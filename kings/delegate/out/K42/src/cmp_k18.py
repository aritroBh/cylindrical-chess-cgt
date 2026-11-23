#!/usr/bin/env python3
"""compare k42 plain-only flags with K18's lg.cpp search output on K18's roots. usage: cmp_k18.py K18_search.gz k42_sorties.txt"""
import sys, gzip, re, collections
def canon(y):
    t = y.split(); return (tuple(sorted(t[:-2])), t[-2], t[-1])
k18 = {"P": {}, "Q": {}}
for line in gzip.open(sys.argv[1], "rt"):
    p = [x.strip() for x in line.split("|")]
    if p[0] not in ("P", "Q"): continue
    mv = {}
    for s in re.findall(r"\[([^\]]*)\]", p[4]):
        t = s.split(); m0 = t[0].replace("-", "").replace("x", ""); mv[m0 if m0[0] == "K" else "P" + m0] = t[1]
    k18[p[0]][canon(p[1])] = mv
mine = collections.defaultdict(dict)
for line in open(sys.argv[2]):
    p = line.rstrip("\n").split(" | ")
    f = p[3]; mine[canon(p[0])][p[1].replace("x", "").replace("ep", "")] = f
res = collections.Counter()
for var, idx in (("P", 0), ("Q", 2)):
    for Y, mv in k18[var].items():
        po18 = {m for m, c in mv.items() if c == "PLAIN-ONLY"}
        mm = mine.get(Y, {})
        po = {m for m, f in mm.items() if f[idx] == "1" and f[idx + 1] == "0"}
        if po18 == po: res[var, "same"] += 1
        else:
            res[var, "diff"] += 1
            if res[var, "diff"] <= 5: print(var, Y, sorted(po18), sorted(po))
print(dict(res))
