"""Compare atom values across race rules and en passant (parts_sens/).

  cd /Users/aritro/Downloads/Research/Chessendgames/atlas/cylinder && \
  ../../.venv/bin/python sens_compare.py > logs/sens_compare.txt

Covers: full-width flat atoms of width 1..4 and rings of width 3..4 with
w+b <= 4, and rings of width 3..5 with w+b = 5 (see run_sensitivity.sh).
"""
import glob
import json
import re
from collections import Counter, defaultdict

vals = {}
for vf in glob.glob("parts_sens/*.vals") + glob.glob("parts/*.vals"):
    for line in open(vf):
        d = json.loads(line)
        vals.setdefault(d["vid"], d)

by = defaultdict(dict)  # (board, n, pos) -> combo -> vid
for pf in glob.glob("parts_sens/*.jsonl"):
    m = re.search(r"_(count|mover|opponent)_ep(\d)_", pf)
    combo = f"{m.group(1)}/ep{'on' if m.group(2) == '1' else 'off'}"
    for line in open(pf):
        r = json.loads(line)
        key = ("cyl" if r["wrap"] else "flat", r["n"], r["pos"], r["w"] + r["b"])
        by[key][combo] = r["vid"]

combos = ["count/epon", "mover/epon", "opponent/epon", "count/epoff", "mover/epoff", "opponent/epoff"]
groups = defaultdict(Counter)
for key, d in by.items():
    board, n, pos, p = key
    g = ("ring" if board == "cyl" else "flat-atom", n, p)
    groups[g]["positions"] += 1
    base = d.get("count/epon")
    for c in combos[1:]:
        if c in d and d[c] != base:
            groups[g][c] += 1
            if not vals[base]["big"] and not vals[d[c]]["big"]:
                groups[g][c + " (both non-W)"] += 1

print("## positions whose value differs from count/ep-on")
print("| atoms | positions | " + " | ".join(combos[1:]) + " |")
for g in sorted(groups):
    c = groups[g]
    print(f"| {g[0]} n={g[1]} pawns={g[2]} | {c['positions']} | " +
          " | ".join(f"{c[x]} ({c[x + ' (both non-W)']})" for x in combos[1:]) + " |")

# value-level: for each count/ep-on value (non-W), is it reproduced under every combo by the same position?
print("\n## non-W count/ep-on values of ring atoms whose witnesses change under another combo")
ring_vals = defaultdict(list)
for key, d in by.items():
    if key[0] == "cyl" and "count/epon" in d and not vals[d["count/epon"]]["big"]:
        ring_vals[d["count/epon"]].append((key, d))
for v, lst in sorted(ring_vals.items(), key=lambda kv: vals[kv[0]]["show"]):
    changed = [(k, d) for k, d in lst if any(d.get(c) != v for c in combos if c in d)]
    if changed:
        k, d = changed[0]
        alt = {c: vals[d[c]]["show"][:40] for c in combos if c in d and d[c] != v}
        print(f"  {vals[v]['show'][:50]:50s} {len(changed)}/{len(lst)} witnesses change; e.g. C{k[1]} {k[2]}: {alt}")
