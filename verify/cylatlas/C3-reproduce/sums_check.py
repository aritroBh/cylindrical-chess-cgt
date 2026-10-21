"""Are the C3 "cylinder-only" values flat values once more than 5 pawns are allowed?
Checks only two-component flat positions A + B (A, B flat atoms with <= MAXP pawns
each, span(A) + 1 + span(B) <= 8), i.e. a lower bound on what more pawns give.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/cylatlas/C3-reproduce/sums_check.py --root . --impl main --maxp 4
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--impl", required=True)
ap.add_argument("--maxp", type=int, default=4)
a = ap.parse_args()
sys.path.insert(0, os.path.abspath(a.root))
from cylcgt import cgt, pawns  # noqa: E402
from enum_atoms import atoms  # noqa: E402

# target values: non-W cylinder-only set for this impl, recomputed from ring witnesses
recs = []
for f in glob.glob(os.path.join(HERE, f"out_{a.impl}", "*.jsonl")):
    L = [json.loads(l) for l in open(f)]
    if L[0]["meta"]["task"] != "sums":
        recs += L[1:-1]
flat = {r["vid"] for r in recs if r["kind"] == "flat"}
for f in glob.glob(os.path.join(HERE, f"out_{a.impl}", "sums.jsonl")):
    flat |= {json.loads(l)["vid"] for l in open(f) if '"vid"' in l}
targets = {}
for r in sorted(recs, key=lambda r: (r["p"], r["n"])):
    if r["kind"] == "ring" and not r["big"] and r["vid"] not in flat and r["vid"] not in targets:
        targets[r["vid"]] = r
print("targets (non-W cylinder-only):", len(targets))

def P(t):
    w, b = t.split("/")
    W = frozenset(("abcdefgh".index(x[0]), int(x[1])) for x in w.split(":")[1].split())
    B = frozenset(("abcdefgh".index(x[0]), int(x[1])) for x in b.split(":")[1].split())
    return pawns.Pos(W, B)

tg = {}
for v, r in targets.items():
    g = pawns.value(pawns.Board(r["n"], 8, True, True), P(r["pos"]))
    tg[g.id] = (g, r)

atomv = {}  # game id -> (game, (pawns, span, text))
for p in range(2, a.maxp + 1):
    for k in range(1, p + 1):
        b = pawns.Board(k, 8, False, True)
        for W, B in atoms(k, False, p):
            g = pawns.value(b, pawns.Pos(frozenset(W), frozenset(B)))
            cur = atomv.get(g.id)
            cand = (p, k, f"flat{k} W {sorted(W)} B {sorted(B)}")
            if cur is None or cand[:2] < cur[1][:2]:
                atomv[g.id] = (g, cand)
print("distinct flat atom values with <=", a.maxp, "pawns:", len(atomv))
hits = 0
for gid, (g, r) in tg.items():
    best = None
    for aid, (ga, (pa, ka, ta)) in atomv.items():
        d = cgt.add(g, cgt.neg(ga))
        hit = atomv.get(d.id)
        if hit is None:
            continue
        gb, (pb, kb, tb) = hit
        if ka + 1 + kb <= 8:
            c = (pa + pb, ka + 1 + kb, ta, tb)
            if best is None or c < best:
                best = c
    if best:
        hits += 1
        print(f"  {cgt.show(g)}  (C{r['n']} {r['pos']})  = flat sum, {best[0]} pawns, width {best[1]}: {best[2]}  +  {best[3]}")
print(f"{hits} of {len(tg)} cylinder-only values are two-component flat values with more pawns")
