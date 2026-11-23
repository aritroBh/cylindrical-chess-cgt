"""K50: totals over the test (b) logs kings/delegate/out/K50/logs/solver_*.log.
Run from the project root: python3 kings/delegate/out/K50/scripts/summarize.py"""
import glob
import json
from collections import Counter

tot = Counter()
for f in sorted(glob.glob("kings/delegate/out/K50/logs/solver_*.log")):
    rows = [json.loads(l) for l in open(f) if l.startswith('{"pos"')]
    head = [l for l in open(f) if l.startswith("SUMMARY")]
    c = Counter()
    for r in rows:
        exact = r["P"][0] == r["P"][1]
        c[r["verdict"]] += 1
        if r["verdict"] == "CERTIFIED":
            c["cert_route_" + r["route"]] += 1
            c["cert_disagree"] += not (exact and r["D"] == r["P"][0])
            c["cert_F_differs_from_P"] += r["F"][0] != r["P"][0]
        if r["verdict"] == "FAILS":
            c["fails_P_draw"] += r["P"][0] == "D"
        if r["verdict"] == "UNDECIDED":
            c["undecided_P_eq_D"] += exact and r["D"] == r["P"][0]
    print(f.split("/")[-1], head[0].split("positions")[0].strip() if head else "", dict(c))
    tot.update(c)
print("TOTAL", dict(tot))
