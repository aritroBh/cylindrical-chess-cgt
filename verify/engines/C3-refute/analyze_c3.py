#!/usr/bin/env python3
"""Verifier analysis for claim C3, on the verifier's own runs (out/*.json from drive.py).

Comparison per iteration d = the full list of `info depth d ...` lines (every aspiration/bound line, all
fields except time/nps/hashfull), which is stricter than (score, nodes, PV head) of the final exact line.
Counters from the instrumented build give, per iteration, cumulative npmnode/nmpexec/s15 etc.
"""
import collections
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
ROOT = Path(__file__).resolve().parents[3]


def load(name):
    return json.load(open(OUT / f"{name}.json"))["rows"]


def by_depth(lines):
    d = collections.defaultdict(list)
    for l in lines:
        t = l.split()
        if t[0] == "info" and t[1] == "depth":
            d[int(t[2])].append(l)
    return d


def counters(lines):
    c = {}
    for l in lines:
        if l.startswith("info string myc"):
            t = l.split()
            k = int(t[4])
            c[k] = {t[i]: int(t[i + 1]) for i in range(5, len(t), 2)}
    return c


def first_diff(a, b, D=16):
    A, B = by_depth(a), by_depth(b)
    for d in range(1, D + 1):
        if A.get(d) != B.get(d):
            return d
    return None


base, nonmp, nos15, cnt = load("base"), load("nonmp"), load("nos15"), load("count")

# 0. instrumented build must not perturb the search
pert = sum(by_depth(b["lines"]) != by_depth(c["lines"]) or b["bestmove"] != c["bestmove"] for b, c in zip(base, cnt))
print("0. positions where counter build differs from base (should be 0):", pert)

# 0b. compare verifier's base to the worker's base.json on (score, nodes, pv0) of last exact line
wb = json.load(open(ROOT / "engine/ablation/results/base.json"))["results"]
wn = json.load(open(ROOT / "engine/ablation/results/NMP.json"))["results"]
ws = json.load(open(ROOT / "engine/ablation/results/SHALLOW.json"))["results"]


def triple(lines):
    out = {}
    for l in lines:
        t = l.split()
        if t[1] != "depth" or "pv" not in t or "lowerbound" in t or "upperbound" in t:
            continue
        if "multipv" in t and t[t.index("multipv") + 1] != "1":
            continue
        i = t.index("score")
        out[t[2]] = {"score": f"{t[i+1]} {t[i+2]}", "nodes": int(t[t.index("nodes") + 1]), "pv0": t[t.index("pv") + 1]}
    return out


for nm, mine, theirs in (("base", base, wb), ("NMP", nonmp, wn), ("SHALLOW", nos15, ws)):
    mism = sum(triple(m["lines"]) != t["iters"] for m, t in zip(mine, theirs))
    ids = all(m["id"] == t["id"] for m, t in zip(mine, theirs))
    print(f"0b. verifier {nm} vs worker {nm}.json triples: mismatching positions {mism}/233 (ids aligned {ids})")


def first_pos(c, key, D=16):
    for d in range(1, D + 1):
        if c.get(d, {}).get(key, 0) > 0:
            return d
    return None


for label, var, key in (("NMP-off", nonmp, "nmpexec"), ("Step15-off", nos15, "s15")):
    dist = collections.Counter()
    viol = []
    lead = collections.Counter()
    for b, v, c in zip(base, var, cnt):
        fd = first_diff(b["lines"], v["lines"])
        dist[fd] += 1
        C = counters(c["lines"])
        fk = first_pos(C, key)
        # mechanism check: a difference at iteration d requires the guarded block to have been entered
        # at some iteration <= d in the base search (identical search up to that point).
        if fd is not None and (fk is None or fk > fd):
            viol.append((b["id"], fd, fk))
        lead[(fd - fk) if (fd is not None and fk is not None) else ("nd" if fd is None else "?")] += 1
    print(f"\n{label}: first differing iteration (full info lines): "
          + ", ".join(f"{k}:{dist[k]}" for k in sorted(k for k in dist if k is not None)) + f", never:{dist[None]}")
    print(f"  violations (diff before block ever entered): {viol}")
    print(f"  (first diff) - (first iteration block entered): {dict(sorted(lead.items(), key=str))}")

# when do nodes with NPM(side to move) first appear; is NMP / S15 ever entered with zero NPM nodes?
fn = collections.Counter()
early = []
for b, c in zip(base, cnt):
    C = counters(c["lines"])
    f = first_pos(C, "npmnode")
    fn[f] += 1
    for d, x in C.items():
        if x["npmnode"] == 0 and (x["nmpexec"] or x["s15"]):
            early.append((b["id"], d))
print("\nfirst iteration with a main-search node whose mover has non-pawn material:",
      dict(sorted(fn.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))))
print("guarded blocks entered with no NPM node (should be empty):", early)
print("nmpblk>0 at iteration 5 (NMP blocked only by the guard):",
      sum(counters(c["lines"]).get(5, {}).get("nmpblk", 0) > 0 for c in cnt), "positions")
fnmp = collections.Counter(first_pos(counters(c["lines"]), "nmpexec") for c in cnt)
fs15 = collections.Counter(first_pos(counters(c["lines"]), "s15") for c in cnt)
print("first iteration NMP entered:", dict(sorted(fnmp.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))))
print("first iteration Step15 entered:", dict(sorted(fs15.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))))

# the earliest Step-15 position
for b, v, c in zip(base, nos15, cnt):
    if first_diff(b["lines"], v["lines"]) == 3:
        print("\nStep15-off differs at iteration 3:", b["id"], b["fen"])
        for d in (1, 2, 3):
            print("  base ", by_depth(b["lines"])[d][-1])
            print("  nos15", by_depth(v["lines"])[d][-1])
        print("  counters:", {k: counters(c["lines"])[k] for k in (1, 2, 3)})
