"""C1 verifier: split the static-eval sign test by queenside material balance and side to move.
Reads only engine/experiments/results/*.json. Run from the project root:
    .venv/bin/python verify/engines/C1-theory/material_split.py
"""
import json
from collections import Counter, defaultdict
se = {r["id"]: r for r in json.load(open("engine/experiments/results/static_eval.json"))["rows"]}
lc = {r["id"]: r for r in json.load(open("engine/experiments/results/lc0_value_n1.json"))["rows"]}
def sgn(r): return 1 if r["stm"] == "W" else -1
def sf(r): return sgn(r) * r["final"]
def l0(r): return sgn(r) * lc[r["id"]]["lc0_orig_white_cp"]
def ok(v, r): return (v > 0) == (r["tb_root"] == "win")
def mat(r):
    w, b = r["component"].split("/")
    nw = len(w.replace("W:", "").split()); nb = len(b.replace("B:", "").split())
    return nw - nb
def group(r):
    if r["o"] == "N" and r["value_count"].startswith("*"): return "N nimber"
    if r["class"] == "number" and not r["race_sensitive"]: return "number (tame, race-insens.)"
    if r["class"] == "number": return "number (race-sensitive)"
    return None
rows = [r for r in se.values() if r["tb_root"] in ("win", "loss")]
tab = defaultdict(lambda: [0, 0, 0])
for r in rows:
    g = group(r)
    if g is None: continue
    # material from the mover's view
    m = mat(r) * sgn(r)
    key = (g, f"mover material {m:+d}")
    for k in (key, (g, "all")):
        tab[k][0] += 1; tab[k][1] += ok(sf(r), r); tab[k][2] += ok(l0(r), r)
print("| group | split | n | SF sign right | Lc0 sign right |")
print("|---|---|---|---|---|")
for k in sorted(tab):
    n, a, b = tab[k]
    print(f"| {k[0]} | {k[1]} | {n} | {a} | {b} |")
# equal-material subset across all classes, by CGT outcome
print()
eq = defaultdict(lambda: [0, 0, 0])
for r in rows:
    if mat(r) == 0:
        for k in (r["o"], "all equal-material"):
            eq[k][0] += 1; eq[k][1] += ok(sf(r), r); eq[k][2] += ok(l0(r), r)
print("equal queenside material, by CGT outcome: n, SF right, Lc0 right")
for k in sorted(eq): print(k, eq[k])
# number values in the tame number group
nums = [r for r in rows if group(r) == "number (tame, race-insens.)"]
print("tame number values x material:", Counter((r["value_count"], mat(r)) for r in nums))
print("stm over all 275:", Counter(r["stm"] for r in se.values()))
