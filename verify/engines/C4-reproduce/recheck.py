#!/usr/bin/env python3
"""Independent recheck of claim C4 from engine/ablation/results/*.json (read-only).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C4-reproduce/recheck.py
"""
import json, math, re
from collections import defaultdict, Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
E = ROOT / "engine"
meta = {}
for p in [E/"suite"/"cgt_verified.epd", E/"suite"/"cgt_disagree.epd"]:
    for line in open(p):
        if not line.strip(): continue
        i = re.search(r'id "([^"]+)"', line).group(1)
        assert i not in meta, i
        meta[i] = dict(tb=re.search(r"tablebase root: ([a-z-]+)", line).group(1),
                       cls=re.search(r'c5 "class ([^;]+);', line).group(1),
                       stm=line.split()[1], file=p.name)
print("positions", len(meta), Counter(m["tb"] for m in meta.values()), Counter(m["stm"] for m in meta.values()))
print("classes", Counter(m["cls"] for m in meta.values()))
def load(v): return json.loads((E/"ablation"/"results"/f"{v}.json").read_text())
V = ["base","NMP","SHALLOW","RFP","RAZOR","SE","PROBCUT","LMR","CORR","IIR"]
R = {v: {r["id"]: r for r in load(v)["results"]} for v in V}
for v in V:
    rows = R[v]
    errs = sum(r["error"] is not None for r in rows.values())
    missing = sum(1 for r in rows.values() for d in range(1,17) if str(d) not in r["iters"])
    ids_ok = set(rows) == set(meta)
    print(f"{v}: n={len(rows)} errors={errs} missing-iterations={missing} ids-match={ids_ok} max_depth={load(v)['max_depth']}")
def cp(score):
    k, x = score.split(); x = int(x)
    if k == "mate": return 100000 if x > 0 else -100000
    return x
def verdict(score, thr=150):
    s = cp(score)
    return "win" if s >= thr else "loss" if s <= -thr else "draw"
def ok(v, d, thr=150, filt=lambda m: True):
    return sum(verdict(R[v][i]["iters"][str(d)]["score"], thr) == m["tb"] for i, m in meta.items() if filt(m))
print("\nEval-ok counts base vs RFP (thr 150):", {d: (ok("base", d), ok("RFP", d)) for d in (1,2,3,4,6,8)})
print("\nThreshold sensitivity, base -> RFP, at d3 and d4:")
for thr in (1, 50, 100, 150, 200, 300):
    print(f"  thr {thr:3d}: d3 {ok('base',3,thr)} -> {ok('RFP',3,thr)};  d4 {ok('base',4,thr)} -> {ok('RFP',4,thr)}")
print("\nBy tablebase root (wins vs draws), base -> RFP:")
for tb in ("win", "draw"):
    f = lambda m, tb=tb: m["tb"] == tb
    n = sum(f(m) for m in meta.values())
    print(f"  {tb} (n={n}): " + "; ".join(f"d{d} {ok('base',d,filt=f)}->{ok('RFP',d,filt=f)}" for d in (2,3,4,6)))
print("\nBy CGT class, absolute counts base -> RFP (gain):")
tot = Counter()
for c in sorted({m["cls"] for m in meta.values()}):
    f = lambda m, c=c: m["cls"] == c
    n = sum(f(m) for m in meta.values())
    parts = []
    for d in (3, 4):
        b, r = ok("base", d, filt=f), ok("RFP", d, filt=f)
        parts.append(f"d{d} {b}->{r} ({r-b:+d})")
        tot[d] += r - b
    print(f"  {c:14s} n={n:3d}: " + "; ".join(parts))
print("  total gain", dict(tot))
# per-position flips base vs RFP at d3, d4
for d in (3, 4):
    gain = [i for i, m in meta.items() if verdict(R["RFP"][i]["iters"][str(d)]["score"]) == m["tb"] != verdict(R["base"][i]["iters"][str(d)]["score"])]
    loss = [i for i, m in meta.items() if verdict(R["base"][i]["iters"][str(d)]["score"]) == m["tb"] != verdict(R["RFP"][i]["iters"][str(d)]["score"])]
    print(f"\nd{d}: RFP-off right & base wrong: {len(gain)}; base right & RFP-off wrong: {len(loss)}; net {len(gain)-len(loss)}")
    print("   gains by class", Counter(meta[i]["cls"] for i in gain), " losses by class", Counter(meta[i]["cls"] for i in loss))
    print("   gains by tb", Counter(meta[i]["tb"] for i in gain), " losses by tb", Counter(meta[i]["tb"] for i in loss))
# node cost
print("\nNodes at fixed depth, RFP / base:")
for d in (2, 3, 4, 6, 8, 16):
    sb = sum(R["base"][i]["iters"][str(d)]["nodes"] for i in meta)
    sr = sum(R["RFP"][i]["iters"][str(d)]["nodes"] for i in meta)
    gm = math.exp(sum(math.log(R["RFP"][i]["iters"][str(d)]["nodes"] / R["base"][i]["iters"][str(d)]["nodes"]) for i in meta) / len(meta))
    med = sorted(R["RFP"][i]["iters"][str(d)]["nodes"] / R["base"][i]["iters"][str(d)]["nodes"] for i in meta)[len(meta)//2]
    print(f"  d{d}: total-sum ratio {sr/sb:.3f}; per-position geo-mean {gm:.3f}; median {med:.3f}; base total {sb}")
# top contributors to d4 total
d4 = sorted(meta, key=lambda i: R["RFP"][i]["iters"]["4"]["nodes"] - R["base"][i]["iters"]["4"]["nodes"], reverse=True)[:5]
print("  top d4 extra-node contributors:", [(i, R["base"][i]["iters"]["4"]["nodes"], R["RFP"][i]["iters"]["4"]["nodes"]) for i in d4])
# equal-cost metric reimplemented
def eval_point(row, tb, thr=150):
    first = None
    for d in range(1, 17):
        x = row["iters"][str(d)]
        if verdict(x["score"], thr) == tb:
            if first is None: first = d
        else: first = None
    return None if first is None else (first, row["iters"][str(first)]["nodes"])
print("\nEqual-cost (nodes to stable right verdict), variant vs base:")
for v in V:
    for thr in (150,):
        logs = []; ch = de = sa = 0
        for i, m in meta.items():
            a, b = eval_point(R[v][i], m["tb"], thr), eval_point(R["base"][i], m["tb"], thr)
            if a and b:
                logs.append(math.log(a[1]/b[1])); ch += a[1] < b[1]; de += a[1] > b[1]; sa += a[1] == b[1]
        print(f"  {v:8s} thr {thr}: n={len(logs)} geo {math.exp(sum(logs)/len(logs)):.3f} cheaper/dearer/same {ch}/{de}/{sa}")
print("\nRFP equal-cost sensitivity to threshold:")
for thr in (50, 100, 150, 200, 300):
    logs = []; ch = de = 0
    for i, m in meta.items():
        a, b = eval_point(R["RFP"][i], m["tb"], thr), eval_point(R["base"][i], m["tb"], thr)
        if a and b:
            logs.append(math.log(a[1]/b[1])); ch += a[1] < b[1]; de += a[1] > b[1]
    print(f"  thr {thr}: n={len(logs)} geo {math.exp(sum(logs)/len(logs)):.3f} cheaper/dearer {ch}/{de}")
# per-variant: nodes by depth 4 and other cost measures range
print("\nCost ranges per variant: total nodes d4 ratio, per-position geo-mean d4, nodes-to-solve geo, equal-cost geo")
