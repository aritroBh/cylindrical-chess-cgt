# Step 2: for every C7/C8 *2/*3 ring (whole-board verified) and every cut, attach alternating walls (W2/B4)
# of length 2..7 starting with W2 or B4, and record the single-core ring value.
import sys, json
from lib import *
ev = Evaluator("results.tsv")
rings = []
for line in open("c78_rings.tsv"):
    n, v, rs, sig, nim = line.rstrip("\n").split("\t")
    rings.append((f"C{n}:{v}", R(rs)))
for name, s in (("P8", "W5 B7 W4 W4B7 B6 W3B6 W2 B4"), ("Q8", "W4 B7 W3B6 W3 W2B5 B5 W2 B4"), ("X3", "W5 B7 W4 W4B7 B6 W3B6 W2 B5"),
                ("X2core", "W5 B7 W4 W4B7 B6 W3B6")):
    rings.append((name, R(s)))
rows = []   # (ringname, ringstr, cut, f, L, sig)
t0 = time.time()
for name, ring in rings:
    n = len(ring)
    for c in range(n):
        A = ring[c:] + ring[:c]
        for f in "WB":
            for L in range(2, 8):
                full = A + wall(L, f)
                if not legal_start(full): sig = "ILLEGAL"
                else: sig = ev.sig(full)
                rows.append((name, S(A), c, f, L, sig))
print("evaluated", len(rows), "rows; new engine calls", ev.n_new, f"{time.time()-t0:.0f}s")
with open("c78_cuts.tsv", "w") as o:
    for r in rows: o.write("\t".join(map(str, r)) + "\n")
