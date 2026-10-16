"""Score Stockfish runs on the CGT suite two ways: did it pick a winning move (solved),
and does its evaluation agree with the tablebase result at the root (eval_ok).
Run: .venv/bin/python engine/runs/analyze_sf.py engine/runs/sf19_nodes.json engine/runs/sf19_depth.json"""
import json, re, sys
from collections import defaultdict

tb = {}
cls = {}
for path in ["engine/suite/cgt_verified.epd", "engine/suite/cgt_disagree.epd"]:
    for line in open(path):
        if not line.strip():
            continue
        i = re.search(r'id "([^"]+)"', line).group(1)
        tb[i] = re.search(r"tablebase root: (\w+)", line).group(1)
        m = re.search(r'c5 "class ([^;]+);', line)
        cls[i] = m.group(1) if m else "?"

def verdict(score):
    kind, v = score.split()[0], int(score.split()[1])
    if kind == "mate":
        return "win" if v > 0 else "loss"
    return "win" if v >= 150 else "loss" if v <= -150 else "draw"

for path in sys.argv[1:]:
    d = json.load(open(path))
    agg = defaultdict(lambda: [0, 0, 0])
    bycls = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    wrong = defaultdict(list)
    for r in d["results"]:
        a = agg[r["limit"]]
        a[0] += 1
        a[1] += r["solved"]
        ok = r["score"] is not None and verdict(r["score"]) == tb[r["id"]]
        a[2] += ok
        b = bycls[r["limit"]][cls[r["id"]]]
        b[0] += 1
        b[1] += ok
        if not ok:
            wrong[r["limit"]].append((r["id"], tb[r["id"]], r["score"], cls[r["id"]]))
    print(f"## {path}")
    print("| limit | positions | best move wins | eval matches tablebase |")
    print("|---|---|---|---|")
    for lim, (n, s, e) in agg.items():
        print(f"| {lim} | {n} | {s} ({100*s/n:.0f}%) | {e} ({100*e/n:.0f}%) |")
    last = list(agg)[-1]
    print(f"\nEval mismatches at {last}, by CGT value class:",
          {k: f"{v[0]-v[1]}/{v[0]}" for k, v in bycls[last].items()})
    for w in wrong[last][:25]:
        print("   ", w)
