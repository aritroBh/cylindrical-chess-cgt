"""w+b<=5, e.p. on: cylinder-only (non-W) sets from the independent model under each
race rule; count-rule set compared key-by-key to the worker's main atlas (values.jsonl);
intersection over the three race rules.
  cd verify/cylatlas/C4-refute && ../../../.venv/bin/python analyze_le5.py
"""
import json
W = "../../../atlas/cylinder/"
idx = {}
for line in open(W + "value_index.jsonl"):
    x = json.loads(line); idx[x["vid"]] = x
wc, wf = set(), set()
for line in open(W + "values.jsonl"):
    x = json.loads(line)
    (wc if x["board"] == "cyl" else wf).add(x["vid"])
w_only = {idx[v]["key"] for v in wc - wf if not idx[v]["big"]}
w_cyl = {idx[v]["key"] for v in wc}; w_flat = {idx[v]["key"] for v in wf}
only = {}
for r in ("count", "mover", "opponent"):
    d = json.load(open(f"out/le5_{r}_ep1.json"))
    F = set(d["flat_single"]) | set(d["flat_pair"])
    R = d["ring"]
    only[r] = {k: R[k] for k in R if k not in F and not R[k][2]}
    print(f"{r}/epon w+b<=5: flat values {len(F)}, ring values {len(R)}, cylinder-only non-W {len(only[r])}")
    if r == "count":
        print("   worker main atlas: flat", len(w_flat), "cyl", len(w_cyl), "cyl-only non-W", len(w_only))
        print("   flat sets equal:", F == w_flat, "| cyl sets equal (F U rings):", (F | set(R)) == w_cyl,
              "| cyl-only non-W equal:", set(only[r]) == w_only)
I = set.intersection(*(set(o) for o in only.values()))
print(f"\ncylinder-only non-W under all three race rules (e.p. on, w+b<=5): {len(I)}")
for k in sorted(I):
    print("   ", k, {r: only[r][k][0] for r in only}, only["count"][k][3])
