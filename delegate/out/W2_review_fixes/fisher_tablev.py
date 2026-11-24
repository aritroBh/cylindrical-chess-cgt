"""Table V counts (from engine/runs/sf19_depth.json, scored as engine/runs/analyze_sf.py) and Fisher exact tests.
Run from repo root: python3 delegate/out/W2_review_fixes/fisher_tablev.py
Threshold: engine/runs/analyze_sf.py:22 (win if cp >= 150, loss if <= -150, else draw; mate = win/loss)."""
import json, re
from math import comb
from fractions import Fraction
tb, cls = {}, {}
for path in ["engine/suite/cgt_verified.epd", "engine/suite/cgt_disagree.epd"]:
    for line in open(path):
        if not line.strip(): continue
        i = re.search(r'id "([^"]+)"', line).group(1)
        tb[i] = re.search(r"tablebase root: (\w+)", line).group(1)
        cls[i] = re.search(r'c5 "class ([^;]+);', line).group(1)
def verdict(s):
    k, v = s.split()[0], int(s.split()[1])
    if k == "mate": return "win" if v > 0 else "loss"
    return "win" if v >= 150 else "loss" if v <= -150 else "draw"
d = json.load(open("engine/runs/sf19_depth.json"))
cnt = {}
for r in d["results"]:
    c = cls[r["id"]]
    if c == "decided": continue
    ok = r["score"] is not None and verdict(r["score"]) == tb[r["id"]]
    a = cnt.setdefault((r["limit"], c), [0, 0]); a[0] += 1; a[1] += ok
def fisher(a, n1, b, n2):
    K = a + b; N = n1 + n2
    pr = lambda x: Fraction(comb(n1, x) * comb(n2, K - x), comb(N, K))
    lo, hi = max(0, K - n2), min(n1, K)
    p0 = pr(a)
    return float(sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0))
def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z*z/n
    c = (p + z*z/(2*n)) / den; h = z*((p*(1-p)/n + z*z/(4*n*n))**.5) / den
    return c - h, c + h
classes = ["hot-BIG", "number", "switch", "other-tame", "nimber", "infinitesimal"]
for lim in ["depth 1", "depth 2", "depth 4", "depth 6", "depth 8", "depth 12"]:
    print(f"== {lim}")
    for c in classes:
        n, k = cnt[(lim, c)]
        print(f"  {c:14s} n={n:3d} match={k:3d} {100*k/n:5.1f}%")
    ni, ki = cnt[(lim, "infinitesimal")]
    lo, hi = wilson(ki, ni)
    print(f"  infinitesimal Wilson 95%: {100*lo:.0f}-{100*hi:.0f}%")
    for c in classes[:-1]:
        n, k = cnt[(lim, c)]
        print(f"  Fisher two-sided infinitesimal vs {c:11s}: p = {fisher(ki, ni, k, n):.5f}")
