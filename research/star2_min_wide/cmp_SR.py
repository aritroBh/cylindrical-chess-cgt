#!/usr/bin/env python3
"""cmp_SR.py W P NW [wide] : run scan_fixed2 (variant S: e.p. rights persist per component) and scan_R (variant R: any move clears all e.p.
rights = real-chess expiry) on flat width W, P pawns, split NW+(P-NW), default setting, and compare row by row.
Prints rows, rows that differ (outcome,nimber), R-variant *2 rows, and the first differing rows."""
import sys, subprocess, collections
W, P, NW = map(int, sys.argv[1:4]); NB = P - NW
def run(b): return subprocess.Popen(["nice", "-n", "15", b, "--flat", "--width", str(W), "--min", str(P), "--max", str(P), "--nw", str(NW), "--nb", str(NB),
                                     "--only-setting", "2", "--max-entries", "67108864"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
wide = len(sys.argv) > 4 and sys.argv[4] == "wide"
a, b = (run("./scan_wide"), run("./scan_wide_R")) if wide else (run("./scan_fixed2"), run("./scan_R"))
n = diff = r2 = s2 = 0; conf = collections.Counter(); ex = []
for la, lb in zip(a.stdout, b.stdout):
    if la.startswith("#"): continue
    pa, pb = la.rstrip("\n").split("\t"), lb.rstrip("\n").split("\t")
    assert pa[0] == pb[0]
    n += 1
    if pb[3].endswith(",2"): r2 += 1
    if pa[3].endswith(",2"): s2 += 1
    if pa[3] != pb[3]:
        diff += 1; conf[(pa[3], pb[3])] += 1
        if len(ex) < 5: ex.append((pa[0], "S", pa[3], "R", pb[3]))
print(f"w={W} p={P} split={NW}+{NB}: rows={n} S!=R rows={diff} *2 rows S={s2} R={r2}")
for k, v in sorted(conf.items()): print("   ", k, v)
for e in ex: print("   EXAMPLE", *e)
