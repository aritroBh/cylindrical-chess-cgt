"""Negative control for the value P-test: pair each val row with a WRONG gold value
(gold of the next row with a different value string, and gold + *); the P-test must fail."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import G, parse_value, job_line, run_jobs, load
rows = load("val")
lines, kinds = [], []
for i, r in enumerate(rows):
    j = (i + 1) % len(rows)
    while rows[j]["value_ascii"] == r["value_ascii"]:
        j = (j + 1) % len(rows)
    for kind, gold_fn in (("other-row", lambda gm: parse_value(gm, rows[j]["value_ascii"])),
                          ("gold+*", lambda gm: gm.add(parse_value(gm, r["value_ascii"]), gm.star(1)))):
        gm = G()
        H = gm.export(gm.neg(gold_fn(gm)))
        lines.append(job_line(len(lines), r, "count", 1, 1, 20_000_000, 1, H))
        kinds.append(kind)
res = run_jobs(lines, 4, "negctl_val")
from collections import Counter
c = Counter()
for i, k in enumerate(kinds):
    o = res[i]
    allr = [m[5] for m in o["M"]] + [h[2] for h in o["H"]]
    c[(k, "P (wrongly accepted)" if all(x == 0 for x in allr) else "rejected" if any(x == 1 for x in allr) else "unknown")] += 1
print(dict(c))
