#!/usr/bin/env python3
"""Flip test under each race rule's CGT labels, and rule sensitivity of the N/P labels.
Run from the project root: .venv/bin/python verify/engines/C2-reproduce/rule_sens.py  (needs rerun_rows.json)"""
import json, statistics
from collections import Counter
from pathlib import Path
H = Path(__file__).resolve().parent
rows = json.loads((H / "rerun_rows.json").read_text())
cnt = [x for x in rows if x["o"] in "NP"]
print("N/P (count rule) whose class differs under some other rule:", sum(len(set(x["o_all"].values())) > 1 for x in cnt), "of", len(cnt))
print("transitions count->(mover,opponent):", Counter((x["o"], x["o_all"]["mover"], x["o_all"]["opponent"]) for x in cnt))
for rule in ("count", "mover", "opponent"):
    for o in "NP":
        rs = [x for x in rows if x["o_all"][rule] == o]
        good = (lambda d: d > 0) if o == "N" else (lambda d: d < 0)
        print(f"rule {rule:8s} {o}: n={len(rs):3d} SF right {sum(good(x['sf_delta']) for x in rs):3d}  Lc0 right {sum(good(x['lc_delta']) for x in rs):3d}")
    rs = [x for x in rows if all(x["o_all"][r] == x["o_all"]["count"] for r in x["o_all"])]
for o in "NP":
    rs = [x for x in rows if set(x["o_all"].values()) == {o}]
    good = (lambda d: d > 0) if o == "N" else (lambda d: d < 0)
    print(f"rule-INsensitive {o}: n={len(rs)} SF right {sum(good(x['sf_delta']) for x in rs)} Lc0 right {sum(good(x['lc_delta']) for x in rs)}")
for o in "LR":
    rs = [x for x in rows if x["o"] == o]
    d = [x["sf_delta"] for x in rs]
    print(o, "SF delta mean %+.2f median %+.2f; |orig eval| median %.2f" % (statistics.mean(d), statistics.median(d), statistics.median(abs(x["sf_orig"]) for x in rs)))
