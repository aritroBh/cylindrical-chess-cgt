"""How many of the 53 count/e.p.-on cylinder-only values survive other rules.
  ../../../.venv/bin/python -I sens_intersect.py
"""
import sys
sys.argv = ["x", "results.json"]
exec(open("analyze_var.py").read().split("base = load")[0])
base = load("results.json")[0]
inter = set(base)
for f in ["results_mover_ep1.json", "results_opponent_ep1.json", "results_count_ep0.json"]:
    g = load(f)[0]
    print(f, "cyl-only nonW:", len(g), " of the 53 still cyl-only:", len(base & g))
    inter &= g
print("cyl-only nonW under all four settings:", len(inter))
for k in sorted(inter):
    print("  ", k)
ex = {"3/4": "3/4", "-3/4": "-3/4", "1/4±1/4": "{1/2|0}", "{3/2±1/2|-3/2±1/2}": "{{2|1}|{-1|-2}}"}
for f in ["results.json", "results_mover_ep1.json", "results_opponent_ep1.json", "results_count_ep0.json"]:
    g = load(f)[0]
    print(f, {name: (k in g) for name, k in ex.items()})
