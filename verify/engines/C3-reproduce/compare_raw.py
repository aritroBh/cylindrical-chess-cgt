#!/usr/bin/env python3
"""Compare raw UCI output of base vs NMP vs SHALLOW (from raw_runner.py), stricter than analyze.py:
for every iteration, the final exact-bound multipv-1 info line with ALL fields except time/nps/hashfull
(i.e. depth, seldepth, multipv, score, nodes, tbhits, full PV). Also cross-checks against the
run_ablation-style (score, nodes, pv0) parsing."""
import json, sys
from pathlib import Path
H = Path(__file__).resolve().parent
def final_lines(lines):
    it = {}
    for l in lines:
        t = l.split()
        if not t or t[0] != "info" or "pv" not in t or "score" not in t:
            continue
        if "lowerbound" in t or "upperbound" in t:
            continue
        if "multipv" in t and t[t.index("multipv") + 1] != "1":
            continue
        d = int(t[t.index("depth") + 1])
        keep, i = [], 0
        while i < len(t):
            if t[i] in ("time", "nps", "hashfull"):
                i += 2; continue
            keep.append(t[i]); i += 1
        it[d] = " ".join(keep)
    return it
raw = {v: json.loads((H / "raw" / f"{v}.json").read_text()) for v in ("base", "NMP", "SHALLOW")}
ids = [k for k in raw["base"] if not k.startswith("_")]
bounds = sum(1 for v in raw for k in ids for l in raw[v][k] if "lowerbound" in l or "upperbound" in l)
print("positions", len(ids), "| bound lines seen", bounds)
for v in ("NMP", "SHALLOW"):
    first = {}
    for k in ids:
        a, b = final_lines(raw["base"][k]), final_lines(raw[v][k])
        assert sorted(a) == list(range(1, 17)) and sorted(b) == list(range(1, 17)), k
        first[k] = next((d for d in range(1, 17) if a[d] != b[d]), None)
    from collections import Counter
    c = Counter(first.values())
    print(v, "first full-line difference:", dict(sorted(((str(x), n) for x, n in c.items()))))
    print("  identical through iteration 5 in all positions:", all(f is None or f >= 6 for f in first.values()),
          "| through 2:", all(f is None or f >= 3 for f in first.values()))
    # compare with analyze.py-style (score,nodes,pv0) first-diff from the worker's JSON
    W = json.loads(Path("engine/ablation/results/%s.json" % v).read_text())
    B = {r["id"]: r for r in json.loads(Path("engine/ablation/results/base.json").read_text())["results"]}
    fw = {r["id"]: next((d for d in range(1, 17) if r["iters"][str(d)] != B[r["id"]]["iters"][str(d)]), None) for r in W["results"]}
    print("  full-line first-diff == worker (score,nodes,pv0) first-diff in all positions:", fw == first)
    print("  positions with first diff <= 6:", sorted((f, k) for k, f in first.items() if f is not None and f <= 6))
    print("  never differ:", [k for k, f in first.items() if f is None])
