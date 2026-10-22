#!/usr/bin/env python3
"""Reads the TSV of frontier_split1_fixed2 (one setting column) on stdin.
Writes <prefix>.hits.tsv (every row with nimber >= 2) and <prefix>.summary (rows, outcome x nimber histogram)."""
import sys, collections
prefix = sys.argv[1]
hist = collections.Counter(); rows = 0
with open(prefix + ".hits.tsv", "w") as hits:
    for line in sys.stdin:
        if line.startswith("#"):
            hits.write(line); continue
        p = line.rstrip("\n").split("\t")
        o, n = p[3].split(","); n = int(n)
        rows += 1; hist[(o, n)] += 1
        if n >= 2:
            hits.write(line)
n2 = sum(c for (o, n), c in hist.items() if n == 2)
n3 = sum(c for (o, n), c in hist.items() if n >= 3)
mx = max([n for (o, n) in hist] + [-1])
with open(prefix + ".summary", "w") as s:
    s.write(f"rows={rows}\nstar2={n2}\nstar_ge3={n3}\nmax_nimber={mx}\n")
    for (o, n), c in sorted(hist.items()):
        s.write(f"outcome={o} nimber={n} count={c}\n")
