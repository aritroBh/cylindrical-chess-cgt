"""Cylinder-only (non-W) sets from the independent model (out/*.json), their counts,
intersections over race rules / e.p., and a key-by-key comparison with the worker's
parts_sens_all data (worker_data/, extracted from atlas/cylinder/parts_sens.tar.gz).
  cd verify/cylatlas/C4-refute && ../../../.venv/bin/python analyze_indep.py
"""
import glob, json, re
from collections import defaultdict
combos = [("count",1),("mover",1),("opponent",1),("count",0),("mover",0),("opponent",0)]
name = lambda r,e: f"{r}/ep{'on' if e else 'off'}"
mine = {}
for r,e in combos:
    d = json.load(open(f"out/{r}_ep{e}.json"))
    F = set(d["flat_single"]) | set(d["flat_pair"])
    R = {**d["ring3"], **d["ring4"]}
    big = {k: v[2] for k, v in list(d["flat_single"].items()) + list(d["flat_pair"].items()) + list(R.items())}
    only = {k for k in R if k not in F and not R[k][2]}
    mine[name(r,e)] = dict(F=F, R=R, only=only, heads=d["heads"], big=big)
    print(f"{name(r,e):16s} cyl-only non-W = {len(only):3d}   flat values = {len(F)}  ring values = {len(R)}")
# worker sets (union over widths 3..8)
vals = {}
for vf in glob.glob("worker_data/parts_sens_all/*.vals"):
    for line in open(vf):
        x = json.loads(line); vals.setdefault(x["vid"], x)
wk = defaultdict(lambda: defaultdict(set))
for pf in glob.glob("worker_data/parts_sens_all/*.jsonl"):
    m = re.search(r"(cyl|flat)(\d)_w\db\d_(count|mover|opponent)_ep(\d)_", pf)
    board, rule, ep = m.group(1), m.group(3), int(m.group(4))
    for line in open(pf):
        x = json.loads(line); wk[name(rule, ep)][board].add(vals[x["vid"]]["key"])
print("\nkey-by-key comparison with worker (w+b<=4, widths 3..8):")
for c in mine:
    wF, wC = wk[c]["flat"], wk[c]["cyl"]
    my_allC = mine[c]["F"] | set(mine[c]["R"])  # cut lemma: cylinders = flat(<=7) U rings
    wonly = {k for k in wC - wF if not any(v["key"] == k and v["big"] for v in [])}
    wonly = {k for k in wC - wF}
    wonly_nonW = {k for k in wonly if not next(v for v in vals.values() if v["key"] == k)["big"]}
    print(f"  {c:16s} flat equal: {mine[c]['F'] == wF} (mine {len(mine[c]['F'])}, worker {len(wF)});"
          f" cyl equal: {my_allC == wC} (mine {len(my_allC)}, worker {len(wC)});"
          f" cyl-only non-W equal: {mine[c]['only'] == wonly_nonW}")
def inter(names):
    return set.intersection(*(mine[n]["only"] for n in names))
groups = {"race rules, e.p. on": ["count/epon","mover/epon","opponent/epon"],
          "race rules, e.p. off": ["count/epoff","mover/epoff","opponent/epoff"],
          "all six": list(mine)}
for g, ns in groups.items():
    I = inter(ns)
    print(f"\ncyl-only non-W under ALL of [{g}]: {len(I)}")
    for k in sorted(I):
        print("   ", k, {n: mine[n]["R"][k][0] for n in ns})
print("\nheadline positions (independent model):")
for h in mine["count/epon"]["heads"]:
    print("  ", h, {c: mine[c]["heads"][h][1] for c in mine})
