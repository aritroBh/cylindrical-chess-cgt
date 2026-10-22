#!/usr/bin/env python3
"""Build hit_table.txt from cylcgt_results.tsv (cylcgt = scanner in every cell) and the codex_*.tsv files.
Run (project root): .venv/bin/python research/star27_textbook3/make_table.py > research/star27_textbook3/hit_table.txt
"""
import csv, glob, re
D = "research/star27_textbook3/"


def short(v, out=None):
    v = v.replace(" | ", "|")
    for _ in range(2):
        v = re.sub(r"\{(-?\d+)\|\1\}", r"\1*", v)  # the solver prints {3|3} for 3*
    v = v.replace("|", "∣")  # divides sign, keeps markdown tables intact
    if len(v) <= 22:
        return v
    return "not a nimber" + (f" ({out})" if out else "")


cyl, order = {}, []
for r in csv.DictReader(open(D + "cylcgt_results.tsv"), delimiter="\t"):
    if r["position"] not in cyl:
        cyl[r["position"]] = {}
        order.append(r["position"])
    cyl[r["position"]][r["setting"]] = r
codex = {}
for f in glob.glob(D + "codex_*.tsv"):
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 5:
            codex[(p[0], p[1])] = p[2]


def cx(pos, key):
    v = codex.get((pos, key))
    return "-" if v is None else short(v)


def cell(c, s):
    return short(c[s]["cylcgt_value"], c[s]["cylcgt_outcome"])


print("Table A. Values from cylcgt (identical to the scanner's outcome and nimber in all 26 x 9 = 234 cells). "
      "C = count, M = mover; T = e.p. on with the textbook passed test, off = e.p. off, aware = e.p. on with the "
      "e.p.-aware test.\n")
print("| # | position | C/T | C/off | C/aware | M/T | M/off | M/aware |")
print("|--:|---|---|---|---|---|---|---|")
for i, pos in enumerate(order, 1):
    c = cyl[pos]
    print(f"| {i} | `{pos}` | " + " | ".join(cell(c, s) for s in (
        "count/epon", "count/epoff", "count/epon/aware", "mover/epon", "mover/epoff", "mover/epon/aware")) + " |")
print("\nTable B. Independent whole-board solver (`verify_ext/codex/solver.py`), 6 files, same positions. "
      "'-' = not run (cell is not a T24 hit).\n")
print("| # | C/off | M/off | C/T | M/T | C/aware |")
print("|--:|---|---|---|---|---|")
for i, pos in enumerate(order, 1):
    print(f"| {i} | " + " | ".join([cx(pos, "count/ep-off/aware"), cx(pos, "mover/ep-off/aware"),
                                    cx(pos, "count/ep-on/textbook"), cx(pos, "mover/ep-on/textbook"),
                                    cx(pos, "count/ep-on/aware")]) + " |")
