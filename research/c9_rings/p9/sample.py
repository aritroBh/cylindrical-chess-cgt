#!/usr/bin/env python3
"""sample.py -- draw random rings from pyenum.py's set of 9-pawn root rings on C9 (all splits together, 948,860 rings).

  sample/sample300.txt        300 rings, uniform over the whole set, random.Random(20261027).sample   (the requested sample)
  sample/sample300_meta.tsv   position in the set, split, ring
  sample/bonus100.txt         25 rings from each of the four non-empty splits (3+6, 4+5, 5+4, 6+3), random.Random(20261028)
  sample/bonus100_meta.tsv
The set is read in the fixed order split 1+8 .. 8+1, file order inside a split (the order pyenum.py wrote)."""
import os, random

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "sample"), exist_ok=True)
rings, split = [], []
for nw in range(1, 9):
    nb = 9 - nw
    with open(os.path.join(HERE, "py", "py_rings_%d_%d.txt" % (nw, nb))) as f:
        for line in f:
            if line.strip():
                rings.append(line.strip()); split.append("%d+%d" % (nw, nb))
print("set size", len(rings))
idx = sorted(random.Random(20261027).sample(range(len(rings)), 300))
random.Random(7).shuffle(idx)             # unsorted order so that a prefix of the file is itself a uniform sample
with open(os.path.join(HERE, "sample", "sample300.txt"), "w") as f, open(os.path.join(HERE, "sample", "sample300_meta.tsv"), "w") as m:
    for i in idx:
        f.write(rings[i] + "\n"); m.write("%d\t%s\t%s\n" % (i, split[i], rings[i]))
cnt = {}
for i in idx:
    cnt[split[i]] = cnt.get(split[i], 0) + 1
print("sample300 per split", dict(sorted(cnt.items())))
bonus = []
r2 = random.Random(20261028)
for sp in ("3+6", "4+5", "5+4", "6+3"):
    ids = [i for i in range(len(rings)) if split[i] == sp]
    bonus += r2.sample(ids, 25)
with open(os.path.join(HERE, "sample", "bonus100.txt"), "w") as f, open(os.path.join(HERE, "sample", "bonus100_meta.tsv"), "w") as m:
    for i in bonus:
        f.write(rings[i] + "\n"); m.write("%d\t%s\t%s\n" % (i, split[i], rings[i]))
print("bonus100 written")
