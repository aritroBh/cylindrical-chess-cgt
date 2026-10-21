"""Compare indep_*.json (brute force) with worker parts_sens_all, and compute
intersections of cylinder-only sets over subsets of settings.
  cd verify/cylatlas/C4-reproduce && ../../../.venv/bin/python compare_sets.py
"""
import glob, json, re
from collections import defaultdict
vals = {}
for vf in glob.glob("parts_sens_all/*.vals"):
    for line in open(vf):
        d = json.loads(line); vals.setdefault(d["vid"], d)
sets = defaultdict(lambda: defaultdict(set))
for pf in glob.glob("parts_sens_all/*.jsonl"):
    m = re.search(r"(cyl|flat)(\d)_w\db\d_(count|mover|opponent)_ep(\d)_", pf)
    c = (m.group(3), int(m.group(4)))
    for line in open(pf):
        sets[c][m.group(1)].add(json.loads(line)["vid"])
ind = {}
for r in ("count", "mover", "opponent"):
    for e in (1, 0):
        d = json.load(open(f"indep_{r}_ep{e}.json"))
        ind[(r, e)] = d
        S = sets[(r, e)]
        wk = {vals[v]["key"] for v in S["cyl"] - S["flat"] if not vals[v]["big"]}
        mine = set(d["cyl_only_nonW"])
        print(r, e, "worker", len(wk), "indep", len(mine), "equal" if wk == mine else f"DIFF {wk ^ mine}")
def co(r, e): return set(ind[(r, e)]["cyl_only_nonW"])
def show(k):
    for d in ind.values():
        if k in d["cyl_only_nonW"]: return d["cyl_only_nonW"][k]["show"], d["cyl_only_nonW"][k]["ex"]
for e in (1, 0):
    I = co("count", e) & co("mover", e) & co("opponent", e)
    print(f"cyl-only under all 3 race rules, ep{e}: {len(I)}", [show(k) for k in sorted(I)])
for r in ("count", "mover", "opponent"):
    I = co(r, 1) & co(r, 0)
    print(f"cyl-only under {r}, ep on and off: {len(I)}")
A = set.intersection(*(co(r, e) for r in ("count", "mover", "opponent") for e in (1, 0)))
print("all six:", len(A))
# max number of settings in which a single value is cyl-only
cnt = defaultdict(list)
for (r, e), d in ind.items():
    for k in d["cyl_only_nonW"]: cnt[k].append(f"{r}/ep{e}")
best = sorted(cnt.items(), key=lambda kv: -len(kv[1]))[:8]
for k, l in best: print(len(l), show(k)[0], l)
