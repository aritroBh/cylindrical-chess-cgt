#!/usr/bin/env python3
import os, json, collections, subprocess
T = os.path.dirname(os.path.abspath(__file__))
subprocess.run(["python3", T + "/aggregate.py"], capture_output=True); subprocess.run(["python3", T + "/hits_report.py"], capture_output=True)
table = open(T + "/results/table.md").read(); hits = open(T + "/results/hits_at_minimum.md").read().split("\n", 2)[2]
# merged level data -> totals
rows = collections.defaultdict(dict)
for line in open(T + "/results/levels.tsv"):
    F, w, R, p, tot, proc, comp, cpu, cnt, ps = line.rstrip("\n").split("\t")
    k = (int(F), int(w), int(R), int(p)); d = rows[k]
    if not d or int(proc) >= d["proc"]: rows[k] = {"proc": int(proc), "cnt": json.loads(cnt), "cpu": float(cpu) + d.get("cpu", 0)}
    else: d["cpu"] += float(cpu)
solved = sum(v["proc"] for v in rows.values()); cpu = sum(v["cpu"] for v in rows.values())
bynim = collections.Counter()
for v in rows.values():
    for kk, c in v["cnt"].items(): bynim[kk] += c
val1 = open(T + "/results/validation1.txt").read(); val3 = open(T + "/results/validation3.txt").read().splitlines()
nm = sum(1 for l in val3 if l.startswith("MATCH"))
tpl = open(T + "/REPORT.tpl").read()
open(T + "/REPORT.md", "w").write(tpl.replace("{{TABLE}}", table).replace("{{HITS}}", hits).replace("{{SOLVED}}", f"{solved:,}")
    .replace("{{CPU}}", f"{cpu/3600:.1f}").replace("{{BYNIM}}", ", ".join(f"{k}: {v:,}" for k, v in sorted(bynim.items()) if k != "other"))
    .replace("{{VAL1}}", val1.strip()).replace("{{VAL3N}}", str(nm)).replace("{{VAL3T}}", str(len(val3))))
print("ok", solved, cpu)
