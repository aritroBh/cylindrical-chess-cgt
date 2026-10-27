# Step 1: re-evaluate the C7/C8 *2/*3 hits (sum-model scanner values) with the whole-board engine
import glob, sys
from lib import *
ev = Evaluator("results.tsv")
base = "/Users/aritro/Downloads/Research/Chessendgames/research/star26_rings"
rows = []
for n, path in ((7, base + "/c7/p10_5_5/MERGE.txt"), (8, base + "/c8/p10_5_5/MERGE.txt")):
    for line in open(path):
        if "\t" not in line or not line.startswith("W:"): continue
        pos, nf, npw, v = line.rstrip("\n").split("\t")
        rows.append((n, pos, v))
print(len(rows), "rows")
out = open("c78_rings.tsv", "w")
from collections import Counter
cnt = Counter()
for n, pos, v in rows:
    ring = from_coord(pos, n)
    s = ev.sig(ring)
    cnt[(n, v, nimber(s))] += 1
    out.write(f"{n}\t{v}\t{S(ring)}\t{s}\t{nimber(s)}\n")
for k, c in sorted(cnt.items(), key=str): print(k, c)
