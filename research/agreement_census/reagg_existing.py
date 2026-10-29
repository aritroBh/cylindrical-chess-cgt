"""Step 2: re-aggregate kings/results/exp_*_conv.jsonl (42+42+812 = 896 components)."""
import json
from collections import Counter
R = "/Users/aritro/Downloads/Research/Chessendgames/kings/results/"
PRED = {"L": ("W","W"), "R": ("L","L"), "N": ("W","L"), "P": ("L","W")}
out = {}
for name in ["cyl6x6", "flat5x6", "cyl7x6"]:
    rows = [json.loads(l) for l in open(R + f"exp_{name}_epon_Q_conv.jsonl")]
    for rule in ["textbook", "ep-aware"]:
        c = Counter()
        for r in rows:
            v = r[f"verdict_{rule}"]; c[v] += 1
            if v == "MISMATCH":
                pred = tuple(r[f"predicted_{rule}"]); fz = (r["frozen"]["wtm"][0], r["frozen"]["btm"][0]) if r["frozen"]["wtm"][0]==r["frozen"]["wtm"][1] and r["frozen"]["btm"][0]==r["frozen"]["btm"][1] else None
                c["king_effect" if fz == pred else "convention"] += 1
        out[f"{name}/{rule}"] = dict(c, n=len(rows))
tot = {}
for rule in ["textbook", "ep-aware"]:
    t = Counter()
    for name in ["cyl6x6", "flat5x6", "cyl7x6"]:
        t.update({k: v for k, v in out[f"{name}/{rule}"].items()})
    out[f"ALL/{rule}"] = dict(t)
json.dump(out, open("reagg_existing.json", "w"), indent=1)
for k, v in out.items(): print(k, v)
