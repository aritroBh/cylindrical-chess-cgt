"""T20 step 1: build the CGT tree of the two new 7-pawn *2 positions and
count the terminals / sides by number of men, and report how many of the
embedded real-chess positions are already in the offline caches.

    PYTHONPATH=. .venv/bin/python research/star2_oracle/tree_stats.py
"""
import json
import os
import sys
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from realchess import movegen as mg
from realchess.certify import termdb
from realchess.certify.infra import kb
from realchess.oracle_value import Terminals

HERE = os.path.dirname(os.path.abspath(__file__))
COMPONENTS = {
    "A": "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "B": "W: b4 c2 d2 / B: a6 a7 c6 d5",
}

out = {}
db = termdb.load()
k = kb()
for name, comp in COMPONENTS.items():
    T = Terminals(Pos.parse(comp))
    sides = Counter()
    fens = set()
    per_men = Counter()
    for t in T.terms:
        m = T.men(t)
        per_men[m] += 1
        for s in "WB":
            pos = T.real_pos(t, s)
            sides[m] += 1
            fens.add(mg.normal_fen(pos))
    in_db = [f for f in fens if f in db]
    in_kb = []
    cats = Counter()
    for f in fens:
        rec = k.records.get(f)
        if rec is not None:
            cat = (rec.get("data") or {}).get("category")
            in_kb.append(f)
            cats[cat] += 1
    rec = {
        "component": comp,
        "internal_nodes": len(T.internal),
        "terminals": len(T.terms),
        "terminals_by_men": dict(sorted(per_men.items())),
        "sides_by_men": dict(sorted(sides.items())),
        "distinct_fens": len(fens),
        "sides_in_termdb": len(in_db),
        "sides_in_kb_cache": len(in_kb),
        "kb_categories": dict(cats),
        "model_value_count": None,
    }
    old = pawns.RACE_RULE
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        rec["model_value_" + rule] = cgt.show(pawns.value(T.board, Pos.parse(comp)))
    pawns.RACE_RULE = old
    pawns._value.cache_clear()
    out[name] = rec
    print(name, json.dumps(rec, indent=1), flush=True)

with open(os.path.join(HERE, "tree_stats.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote", os.path.join(HERE, "tree_stats.json"))
