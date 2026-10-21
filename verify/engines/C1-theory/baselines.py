"""C1 verifier: trivial material-count baselines on the same groups, plus exact tests.
    .venv/bin/python verify/engines/C1-theory/baselines.py
"""
import json
from math import comb
from collections import defaultdict
se = {r["id"]: r for r in json.load(open("engine/experiments/results/static_eval.json"))["rows"]}
lc = {r["id"]: r for r in json.load(open("engine/experiments/results/lc0_value_n1.json"))["rows"]}
def sgn(r): return 1 if r["stm"] == "W" else -1
def mat(r):
    w, b = r["component"].split("/")
    return len(w.replace("W:", "").split()) - len(b.replace("B:", "").split())
preds = {
    "SF19 static": lambda r: sgn(r) * r["final"] > 0,
    "Lc0 1 node": lambda r: sgn(r) * lc[r["id"]]["lc0_orig_white_cp"] > 0,
    "material, tie->mover loses": lambda r: sgn(r) * mat(r) > 0,
    "material, tie->mover wins": lambda r: sgn(r) * mat(r) >= 0,
}
def groups(r):
    g = ["all"]
    if r["class"] == "number" and not r["race_sensitive"]: g.append("tame race-insens. numbers (claim: 45)")
    if r["o"] == "N" and r["value_count"].startswith("*"): g.append("N nimber * (claim: 16)")
    if r["o"] == "N": g.append("N all (claim: 61)")
    if r["o"] == "P": g.append("P all")
    if mat(r) == 0: g.append(f"equal material, o={r['o']}")
    return g
tab = defaultdict(lambda: defaultdict(int)); n = defaultdict(int)
for r in se.values():
    if r["tb_root"] not in ("win", "loss"): continue
    want = r["tb_root"] == "win"
    for g in groups(r):
        n[g] += 1
        for k, p in preds.items(): tab[g][k] += p(r) == want
print("| group | n | " + " | ".join(preds) + " |")
print("|---|---|" + "---|" * len(preds))
for g in sorted(n):
    print(f"| {g} | {n[g]} | " + " | ".join(str(tab[g][k]) for k in preds) + " |")
def binom_le(k, n): return sum(comb(n, i) for i in range(k + 1)) / 2 ** n
print("\nP(X<=4 | n=16, p=1/2) one-sided =", round(binom_le(4, 16), 4), "two-sided =", round(2 * binom_le(4, 16), 4))
print("P(X<=18 | n=61, p=1/2) one-sided =", "%.2g" % binom_le(18, 61))
# McNemar exact on the 16 nimbers
nim = [r for r in se.values() if r["o"] == "N" and r["value_count"].startswith("*") and r["tb_root"] == "win"]
b = sum(preds["SF19 static"](r) and not preds["Lc0 1 node"](r) for r in nim)
c = sum((not preds["SF19 static"](r)) and preds["Lc0 1 node"](r) for r in nim)
print(f"nimber discordant pairs: SF-only right {b}, Lc0-only right {c}; exact McNemar two-sided p =",
      round(min(1, 2 * binom_le(min(b, c), b + c)), 4))
print("nimber SF |eval|<0.5 pawns:", sum(abs(r["final"]) < 0.5 for r in nim), "of", len(nim),
      "; SF eval < -1.0 for mover:", sum(sgn(r) * r["final"] < -1.0 for r in nim))
print("nimber stm:", sum(r["stm"] == "W" for r in nim), "White to move of", len(nim))
# agreement between each engine's sign and the 'material, tie->mover loses' rule on the 258 win/loss roots
rows = [r for r in se.values() if r["tb_root"] in ("win", "loss")]
for k in ("SF19 static", "Lc0 1 node"):
    agree = sum(preds[k](r) == preds["material, tie->mover loses"](r) for r in rows)
    print(f"{k}: sign agrees with 'material, tie->mover loses' on {agree}/{len(rows)}")
print("White to move among the 258:", sum(r["stm"] == "W" for r in rows))
