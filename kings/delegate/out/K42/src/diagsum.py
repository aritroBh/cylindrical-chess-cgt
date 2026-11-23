#!/usr/bin/env python3
"""classify failures from diag.sh output dirs. usage: diagsum.py DIR [DIR...]
m1: stalemate of White counts as a Black win; m2: White's king confined to F_Z and the buffer files; m3: both."""
import sys, glob, os, collections
c = collections.Counter(); ex = {}
for d in sys.argv[1:]:
    for sf in sorted(glob.glob(os.path.join(d, "s_*.txt"))):
        cid = os.path.basename(sf)[2:-4]
        n = sum(1 for _ in open(sf))
        res = {}
        for m in ("m1", "m2", "m3"):
            fn = os.path.join(d, f"{m}_{cid}.txt")
            if not os.path.exists(fn): break
            r = {}
            for l in open(fn):
                p = l.rstrip("\n").split(" | ")
                if p[0] == "FAIL": r[(p[2], p[3])] = p[6]
                elif p[0] == "SUM": r["sum"] = p[2]
            if "sum" not in r: break
            res[m] = r
        if len(res) < 3: continue
        for l in open(sf):
            p = l.rstrip("\n").split(" | "); k = (p[0], p[1])
            # original outcome from the FAIL line is not in s_ file; recover from m-files: the sortie is listed again
            key = tuple(res[m].get(k, "L") for m in ("m1", "m2", "m3"))
            c[key] += 1
            ex.setdefault(key, (cid, p[0], p[1]))
print("(m1, m2, m3) -> count   [L = Black wins under that variant]")
for k in sorted(c): print(k, c[k], ex[k])
print("total", sum(c.values()))
