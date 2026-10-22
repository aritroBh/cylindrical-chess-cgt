#!/usr/bin/env python3
"""Compare scan/*.summary rows with the expected mirror-reduced root counts (root_counts.txt) and tabulate *2 / *k>=3."""
import re, glob, collections
exp = {}
for l in open("root_counts.txt"):
    t = l.split(); w, p, nw, nb = map(int, t[:4]); exp[(w, p, nw, nb)] = int(t[6].split("=")[1])
tab = collections.defaultdict(lambda: [0, 0, 0, -1, 0]); bad = []
for f in sorted(glob.glob("scan/*.summary")):
    m = re.match(r"scan/w(\d+)p(\d+)_(\d+)_(\d+)\.summary", f); w, p, nw, nb = map(int, m.groups())
    d = dict(l.strip().split("=", 1) for l in open(f) if "outcome" not in l)
    rows = int(d["rows"]); 
    if rows != exp[(w, p, nw, nb)]: bad.append((w, p, nw, nb, rows, exp[(w, p, nw, nb)]))
    t = tab[(w, p)]; t[0] += rows; t[1] += int(d["star2"]); t[2] += int(d["star_ge3"]); t[3] = max(t[3], int(d["max_nimber"])); t[4] += 1
print("row-count mismatches vs independent counter:", bad)
print(" w  p  splits  roots(scanned)    *2   *k>=3  max_nimber")
for (w, p), t in sorted(tab.items()):
    print(f"{w:2d} {p:2d} {t[4]:6d} {t[0]:14d} {t[1]:5d} {t[2]:6d} {t[3]:6d}")
