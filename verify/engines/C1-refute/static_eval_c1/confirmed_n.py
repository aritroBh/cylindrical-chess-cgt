"""Re-score the N and nimber groups on positions whose twin the tablebase confirms (twin mover also wins).
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C1-refute/static_eval_c1/confirmed_n.py
"""
import json, math
from collections import Counter
D = "/Users/aritro/Downloads/Research/Chessendgames/verify/engines/C1-refute/static_eval_c1/"
me = {d["id"]: d for d in json.load(open(D + "indep_eval.json"))}
tw = json.load(open(D + "twin_results.json"))
def sf_ok(d):
    v = d["sf_final_white"] if d["stm"] == "w" else -d["sf_final_white"]
    return (v > 0) == (d["tb"] == "win")
def lc_ok(d):
    return (d["lc0_cp_stm"] > 0) == (d["tb"] == "win")
def wilson(k, n, z=1.96):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return f"[{100*(c-h):.0f}%, {100*(c+h):.0f}%]"
N = [me[i] for i in tw]
print("N positions:", len(N), "| twin TB categories:", Counter(tw.values()))
for name, sel in [("all model-N", lambda d: True), ("twin TB win (confirmed N)", lambda d: tw[d["id"]] == "win"),
                  ("twin TB draw/loss (not N in real chess)", lambda d: tw[d["id"]] != "win")]:
    for sub, f in [("", lambda d: True), (" / nimber", lambda d: bool(d["nim"])), (" / non-nimber", lambda d: not d["nim"])]:
        g = [d for d in N if sel(d) and f(d)]
        if not g:
            continue
        a, b = sum(map(sf_ok, g)), sum(map(lc_ok, g))
        print(f"  {name}{sub}: n={len(g)}  SF {a}/{len(g)} {wilson(a,len(g))}  Lc0 {b}/{len(g)} {wilson(b,len(g))}")
print("non-N twins:", sorted((i, tw[i], me[i]['show'], 'SF ok' if sf_ok(me[i]) else 'SF wrong') for i in tw if tw[i] != 'win'))
