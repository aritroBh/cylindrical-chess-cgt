"""Cylinder-only / flat-only comparison (w+b <= 4) under every race rule and e.p. setting.

  cd /Users/aritro/Downloads/Research/Chessendgames/atlas/cylinder && \
  ../../.venv/bin/python sens_levels.py > logs/sens_levels.txt
Input: parts_sens_all/ (all canonical positions, w+b <= 4, widths 3..8, both boards).
"""
import glob
import json
import re
from collections import defaultdict

vals = {}
for vf in glob.glob("parts_sens_all/*.vals"):
    for line in open(vf):
        d = json.loads(line)
        vals.setdefault(d["vid"], d)

sets = defaultdict(lambda: defaultdict(dict))  # combo -> (board,n) -> vid -> witness pos
for pf in glob.glob("parts_sens_all/*.jsonl"):
    m = re.search(r"(cyl|flat)(\d)_w\db\d_(count|mover|opponent)_ep(\d)_", pf)
    board, n, rule, ep = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    combo = f"{rule}/ep{'on' if ep == '1' else 'off'}"
    for line in open(pf):
        r = json.loads(line)
        d = sets[combo][(board, n)]
        key = (r["w"] + r["b"], r["pos"])
        if r["vid"] not in d or key < d[r["vid"]]:
            d[r["vid"]] = key

combos = ["count/epon", "mover/epon", "opponent/epon", "count/epoff", "mover/epoff", "opponent/epoff"]
glob_only = {}
for c in combos:
    S = sets[c]
    print(f"\n## {c}")
    print("| n | cyl values | flat values | cyl-only non-W | flat-only non-W | nimbers on cyl | nimbers on flat |")
    for n in range(3, 9):
        C, F = S[("cyl", n)], S[("flat", n)]
        co = [v for v in set(C) - set(F) if not vals[v]["big"]]
        fo = [v for v in set(F) - set(C) if not vals[v]["big"]]
        nimc = sorted({vals[v]["show"] for v in C if vals[v]["cls"] == "nimber"})
        nimf = sorted({vals[v]["show"] for v in F if vals[v]["cls"] == "nimber"})
        print(f"| {n} | {len(C)} | {len(F)} | {len(co)} | {len(fo)} | {' '.join(nimc)} | {' '.join(nimf)} |")
    allC = set().union(*(set(S[("cyl", n)]) for n in range(3, 9)))
    allF = set().union(*(set(S[("flat", n)]) for n in range(3, 9)))
    g = {v for v in allC - allF if not vals[v]["big"]}
    glob_only[c] = {vals[v]["key"]: vals[v] for v in g}
    print(f"values on some cylinder, no flat strip (non-W): {len(g)}")
    for v in sorted(g, key=lambda v: vals[v]["show"]):
        n0 = min(n for n in range(3, 9) if v in S[("cyl", n)])
        print(f"   {vals[v].get('detail') or vals[v]['show']:40s} C{n0}: {S[('cyl', n0)][v][1]}")
    print(f"values on some flat strip, no cylinder (non-W): {sum(1 for v in allF - allC if not vals[v]['big'])}")
common = set.intersection(*(set(d) for d in glob_only.values()))
print(f"\n## cylinder-only (non-W, w+b<=4) under ALL six rule sets: {len(common)}")
for k in sorted(common):
    print("  ", glob_only['count/epon'][k]["show"])
