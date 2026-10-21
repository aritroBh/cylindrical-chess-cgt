"""C2-theory: is Stockfish's flip delta class-blind? Threshold-free N-vs-P separation (AUC) + permutation test,
and delta sign by N subgroup.  Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C2-theory/discrim.py
"""
import json, random, statistics
from pathlib import Path
R = Path("/Users/aritro/Downloads/Research/Chessendgames")
se = {r["id"]: r for r in json.loads((R/"engine/experiments/results/static_eval.json").read_text())["rows"]}
lc = {r["id"]: r for r in json.loads((R/"engine/experiments/results/lc0_value_n1.json").read_text())["rows"]}
def d(r, eng):
    sgn = 1 if r["stm"] == "W" else -1
    if eng == "sf": return (r["final"] - r["twin_final"]) * sgn
    l = lc[r["id"]]; return (l["lc0_orig_white_cp"] - l["lc0_twin_white_cp"]) * sgn
def auc(a, b):
    return sum((x > y) + 0.5 * (x == y) for x in a for y in b) / (len(a) * len(b))
for eng in ("sf", "lc0"):
    N = [d(r, eng) for r in se.values() if r["o"] == "N"]
    P = [d(r, eng) for r in se.values() if r["o"] == "P"]
    L = [d(r, eng) for r in se.values() if r["o"] == "L"]
    Rr = [d(r, eng) for r in se.values() if r["o"] == "R"]
    a = auc(N, P)
    pool = N + P; rng = random.Random(1); k = 0; T = 20000
    for _ in range(T):
        rng.shuffle(pool)
        if auc(pool[:len(N)], pool[len(N):]) >= a: k += 1
    print(f"{eng}: AUC(N delta > P delta) = {a:.3f}, one-sided permutation p ~ {(k+1)/(T+1):.4f}; "
          f"AUC(N>L) = {auc(N, L):.3f}; AUC(L>P) = {auc(L, P):.3f}; AUC(N>R) = {auc(N, Rr):.3f}")
    # best single threshold accuracy on N vs P
    best = max(((sum(x > t for x in N) + sum(x <= t for x in P)) / (len(N) + len(P)), t) for t in sorted(set(N + P)))
    print(f"   best-threshold N/P accuracy {best[0]:.3f} at delta > {best[1]:+.2f}")
def grp(r):
    v = r["value_count"]
    if v.startswith("*"): return "nimber"
    if "W" in v: return "hot-BIG"
    return "other"
from collections import defaultdict
g = defaultdict(list)
for r in se.values():
    if r["o"] == "N": g[grp(r)].append(r)
for k, rs in g.items():
    s = [d(r, "sf") for r in rs]; l = [d(r, "lc0") for r in rs]
    print(f"N/{k}: n={len(rs)} SF delta>0 {sum(x>0 for x in s)} (median {statistics.median(s):+.2f}); Lc0 delta>0 {sum(x>0 for x in l)} (median {statistics.median(l):+.0f})")
# both-sign test vs model
for o in "NP":
    rs = [r for r in se.values() if r["o"] == o]
    def ok(eW, eB): return (eW > 0 and eB < 0) if o == "N" else (eW < 0 and eB > 0)
    def ev(r, eng):
        if eng == "sf": a, b = r["final"], r["twin_final"]
        else: a, b = lc[r["id"]]["lc0_orig_white_cp"], lc[r["id"]]["lc0_twin_white_cp"]
        return (a, b) if r["stm"] == "W" else (b, a)
    print(f"{o}: both White-POV signs match the model: SF {sum(ok(*ev(r,'sf')) for r in rs)}/{len(rs)}, Lc0 {sum(ok(*ev(r,'lc0')) for r in rs)}/{len(rs)}")
# subgroup AUCs vs P
P_sf = [d(r, "sf") for r in se.values() if r["o"] == "P"]
P_lc = [d(r, "lc0") for r in se.values() if r["o"] == "P"]
for k, rs in g.items():
    print(f"AUC(N/{k} delta > P delta): SF {auc([d(r,'sf') for r in rs], P_sf):.3f}, Lc0 {auc([d(r,'lc0') for r in rs], P_lc):.3f}")
print("SF P median %+.2f, L median %+.2f" % (statistics.median(P_sf), statistics.median([d(r,'sf') for r in se.values() if r['o']=='L'])))
