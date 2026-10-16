"""Score the Lc0 runs on the CGT suite the way engine/runs/analyze_sf.py scores Stockfish:
did it pick a winning move (solved), and does its evaluation agree with the tablebase
result at the root (eval_ok), overall and by CGT value class.

The verdict thresholds are analyze_sf.py's: mate scores by sign, otherwise
cp >= 150 win, cp <= -150 loss, else draw. Lc0 reports cp converted from its
expected score, so the same thresholds apply.

Run from the project root:
  .venv/bin/python engine/runs/lc0/analyze_lc0.py engine/runs/lc0/lc0_nodes_*.json
"""
import json
import re
import sys
from collections import defaultdict

tb, cls = {}, {}
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


results = []
for path in sys.argv[1:]:
    results += json.load(open(path))["results"]
limits = list(dict.fromkeys(r["limit"] for r in results))
agg = defaultdict(lambda: [0, 0, 0])
bycls = defaultdict(lambda: defaultdict(lambda: [0, 0]))
wrong = defaultdict(list)
for r in results:
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

print("| limit | positions | best move wins | eval matches tablebase |")
print("|---|---|---|---|")
for lim in limits:
    n, s, e = agg[lim]
    print(f"| {lim} | {n} | {s} ({100 * s / n:.0f}%) | {e} ({100 * e / n:.0f}%) |")
classes = sorted({c for lim in limits for c in bycls[lim]}, key=lambda c: -bycls[limits[0]][c][0])
print("\n| CGT class | n | " + " | ".join(limits) + " |")
print("|---|---|" + "---|" * len(limits))
for c in classes:
    n = bycls[limits[0]][c][0]
    cells = [f"{100 * bycls[lim][c][1] / bycls[lim][c][0]:.0f}%" if bycls[lim][c][0] else "-" for lim in limits]
    print(f"| {c} | {n} | " + " | ".join(cells) + " |")
last = limits[-1]
print(f"\nEval mismatches at {last} ({len(wrong[last])}):")
for w in wrong[last]:
    print("   ", w)
