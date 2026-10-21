"""Rebuild the C3 comparison (w+b<=5, count rule, e.p. on) from single components only:
  flat value set = flat single components  U  sums of two flat single components with p1+p2<=5
  cylinder value set (union of widths 3..8) = flat value set U ring values (3-,4-,5-file rings)
  cylinder-only W-free = W-free ring values not in the flat value set.
Mode 'textbook': singles and rings taken from the worker's atlas (values.jsonl + value_index keys) -> control.
Mode 'aware'   : singles and rings from verify/cylatlas/C3-theory/ep/*.jsonl (e.p.-aware passed test).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/ep_analyze.py textbook
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/ep_analyze.py aware
"""
import glob, json, re, sys
from collections import defaultdict
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import parse, key
from cylcgt import cgt

def isbig(k):
    # numbers in a key: integers or a/b; nimbers are written *k
    for t in re.findall(r"(\*?)(-?\d+)(?:/(\d+))?", k):
        if t[0] == "*": continue
        if abs(int(t[1])) >= 128 * (int(t[2]) if t[2] else 1): return True
    return False

mode = sys.argv[1]
singles = defaultdict(dict)  # pawns -> key -> example pos
rings = defaultdict(dict)    # n -> key -> example pos
if mode == "atlas":
    idx = {}
    for line in open("atlas/cylinder/value_index.jsonl"):
        d = json.loads(line); idx[d["vid"]] = d["key"]
    for line in open("atlas/cylinder/values.jsonl"):
        r = json.loads(line)
        k = idx[r["vid"]]; p = r["w"] + r["b"]
        if r["board"] == "flat" and r["ncomp"] == 1:
            singles[p].setdefault(k, r["pos"])
        if r["board"] == "cyl" and r["ring"]:
            rings[r["n"]].setdefault(k, r["pos"])
else:
    for f in glob.glob(f"verify/cylatlas/C3-theory/{ {'aware': 'ep', 'tb': 'tb', 'indep': 'indep'}[mode] }/*.jsonl"):
        for line in open(f):
            r = json.loads(line); p = r["w"] + r["b"]
            if r["kind"] == "flat": singles[p].setdefault(r["key"], r["pos"])
            else: rings[r["n"]].setdefault(r["key"], r["pos"])
flat = {}
for p, d in singles.items():
    for k, pos in d.items(): flat.setdefault(k, pos)
for p1 in singles:
    for p2 in singles:
        if p1 > p2 or p1 + p2 > 5: continue
        for k1, pos1 in singles[p1].items():
            g1 = parse(k1)
            for k2, pos2 in singles[p2].items():
                k = key(cgt.add(g1, parse(k2)))
                flat.setdefault(k, f"[{pos1}] + [{pos2}]")
ringall = {}
for n in sorted(rings):
    for k, pos in rings[n].items(): ringall.setdefault(k, (n, pos))
flatW = {k for k in flat if not isbig(k)}
cyl = set(flat) | set(ringall)
cylW = {k for k in cyl if not isbig(k)}
only = {k: ringall[k] for k in ringall if k not in flat and not isbig(k)}
print(f"mode={mode}: singles per pawn count", {p: len(d) for p, d in sorted(singles.items())},
      "rings per n", {n: len(d) for n, d in sorted(rings.items())})
print(f"flat W-free values {len(flatW)}; cylinder W-free values {len(cylW)}; total values cyl {len(cyl)} flat {len(flat)}")
from collections import Counter
print(f"cylinder-only W-free: {len(only)} by smallest ring width", Counter(v[0] for v in only.values()))
json.dump({k: v for k, v in only.items()}, open(f"verify/cylatlas/C3-theory/only_{mode}.json", "w"), indent=0)
json.dump(sorted(flatW), open(f"verify/cylatlas/C3-theory/flatW_{mode}.json", "w"))
for k, (n, pos) in sorted(only.items(), key=lambda kv: kv[1]):
    print(n, pos, cgt.show(parse(k)))
