#!/usr/bin/env python3
"""K43: collect the RESULT lines of logs/*.out into one table (text)."""
import glob, re, os, sys
rows = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "*.out"))):
    tag = os.path.basename(f)[:-4]
    res = {}
    for l in open(f):
        if l.startswith("RESULT "):
            kv = dict(re.findall(r"(\w+(?:\([^)]*\))?)=(-?\d+)", l))
            who = "under" if "white(under)" in l else "over"
            res[who] = (l, kv)
    if not res: continue
    rows.append((tag, res))
def g(kv, k):
    for kk, v in kv.items():
        if kk.startswith(k): return int(v)
    return None
print("%-26s %-6s %14s %13s %12s %11s %8s %5s %9s %6s" % ("run", "who", "placements", "U1", "U1+U2", "U3(loose)", "one-fr", "F4", "someZero", "half"))
for tag, res in rows:
    for who in ("under", "over"):
        if who not in res: continue
        kv = res[who][1]
        print("%-26s %-6s %14d %13d %12d %11d %8d %5d %9s %6s" % (tag, who, g(kv, "placements"), g(kv, "F1"), g(kv, "F2"), g(kv, "F3"), g(kv, "F3one"), g(kv, "F4"),
              str(g(kv, "someZero")), str(g(kv, "halfExact"))))
