"""Recompute, with a fresh cylcgt run (cache cleared per rule), the CGT value and the
race-sensitivity of every component used in results.json, and check the grouping that
defines the 94 (tame-A) and 54 (tame-B) positions of claim C2. Also split the B group's
king-move results by side to move.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-reproduce/regroup_c2.py
"""
import collections
import json
import sys

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
sys.path.insert(0, f"{ROOT}/engine/suite")
import cgtpos as C  # read-only import of the worker's helper (no writes)
from cylcgt import pawns

rows = json.load(open(f"{ROOT}/engine/suite/results.json"))
cands = {(r["pos"], r["stm"]): r for r in json.load(open(f"{ROOT}/engine/suite/candidates.json"))}


def rec_pos(rec):
    w = frozenset(pawns.sq(s) for s in rec["white"])
    b = frozenset(pawns.sq(s) for s in rec["black"])
    ep = None
    if rec["ep"]:
        t = pawns.sq(rec["ep"])
        ep = (t, (t[0], t[1] - 1), "W") if rec["stm"] == "W" else (t, (t[0], t[1] + 1), "B")
    return pawns.Pos(w, b, ep)


need = sorted({(r["component"], r["stm"]) for r in rows})
fresh = collections.defaultdict(dict)
for rule in ("count", "mover", "opponent"):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    for key in need:
        rec = cands[key]
        a = C.analyse(rec_pos(rec), key[1], rule)
        fresh[key][rule] = (a["value"], tuple(sorted(m["uci"] for m in a["moves"] if m["wins"])))
bad = 0
for key in need:
    for rule in ("count", "mover", "opponent"):
        old = cands[key]["rules"][rule]
        oldw = tuple(sorted(m[0] for m in old["moves"] if m[4]))
        if (old["value"], oldw) != fresh[key][rule]:
            bad += 1
            print("STALE", key, rule, old["value"], oldw, fresh[key][rule])
print("components re-evaluated:", len(need), "x 3 rules; mismatches vs candidates.json:", bad)

grp = collections.defaultdict(collections.Counter)
npos = collections.Counter()
for r in rows:
    key = (r["component"], r["stm"])
    tame = "W" not in fresh[key]["count"][0]
    rs = len({fresh[key][ru][1] for ru in ("count", "mover", "opponent")}) > 1
    if tame and not rs:
        g = f"tame-{r['treb'][0]}-stm{r['stm']}"
        npos[g] += 1
        grp[g].update(r["king_move_results"].values())
for g in sorted(grp):
    print(f"{g:14s} positions={npos[g]:3d} king moves={dict(grp[g])} total={sum(grp[g].values())}")
