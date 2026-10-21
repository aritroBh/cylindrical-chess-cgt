"""Compare own-driver re-runs of rebuilt binaries with engine/ablation/results/{base,RFP}.json.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C4-reproduce/compare_rerun.py"""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
E = H.parents[2] / "engine" / "ablation" / "results"
for name, mine in (("base", "base_rebuilt"), ("RFP", "RFP_rebuilt")):
    w = {r["id"]: r for r in json.loads((E / f"{name}.json").read_text())["results"]}
    m = json.loads((H / f"rerun_{mine}.json").read_text())
    same = tot = 0; bad = []
    for i, r in w.items():
        for d, x in r["iters"].items():
            tot += 1
            y = m[i].get(d)
            if y and y == [x["score"], x["nodes"], x["pv0"]]: same += 1
            else: bad.append((i, d, x, y))
    extra = sum(len(m[i]) for i in m) - tot
    print(f"{name}: {same}/{tot} iterations identical (score, nodes, pv0); extra iterations in rerun {extra}; first mismatches {bad[:3]}")
