"""Recount T3 from the worker's values.jsonl (read-only): split by smallest width, ring flags.
  cd atlas/cylinder && ../../.venv/bin/python ../../verify/cylatlas/C3-reproduce/worker_t3.py
"""
import json
from collections import defaultdict
idx = {json.loads(l)["vid"]: json.loads(l) for l in open("value_index.jsonl")}
sets = defaultdict(set); ringonly = defaultdict(lambda: defaultdict(set))
for l in open("values.jsonl"):
    r = json.loads(l)
    if r["w"] + r["b"] > 5 or r["n"] < 3 or r["n"] > 8: continue
    sets[(r["board"], r["n"])].add(r["vid"])
    if r["board"] == "cyl": ringonly[r["n"]][r["vid"]].add(r["ring"])
C = set().union(*(sets[("cyl", n)] for n in range(3, 9))); F = set().union(*(sets[("flat", n)] for n in range(3, 9)))
g = C - F; nw = {v for v in g if not idx[v]["big"]}
print("cyl-only total", len(g), "non-W", len(nw))
from collections import Counter
mn = Counter(min(n for n in range(3, 9) if v in sets[("cyl", n)]) for v in nw); print("smallest n", dict(mn))
both = [v for v in nw if v in sets[("cyl", 3)] and v in sets[("cyl", 4)]]; print("non-W on both C3 and C4:", len(both))
nonring = [v for v in nw for n in range(3, 9) if 0 in ringonly[n].get(v, set())]; print("non-W cyl-only values seen at a non-ring position:", len(nonring))
print("on C4 only (not C3):", len([v for v in nw if v in sets[("cyl",4)] and v not in sets[("cyl",3)]]))
print("C5 non-W cyl-only:", len([v for v in nw if v in sets[("cyl",5)]]))
print("flat-only:", len(F - C), "cyl7==flat7", sets[("cyl",7)] == sets[("flat",7)], "cyl8==flat8", sets[("cyl",8)] == sets[("flat",8)])
json.dump(sorted(nw), open("/Users/aritro/Downloads/Research/Chessendgames/verify/cylatlas/C3-reproduce/worker_nonW_cylonly_vids.json", "w"))
json.dump({k: sorted(v) for k, v in {"C": C, "F": F}.items()}, open("/Users/aritro/Downloads/Research/Chessendgames/verify/cylatlas/C3-reproduce/worker_sets.json", "w"))
