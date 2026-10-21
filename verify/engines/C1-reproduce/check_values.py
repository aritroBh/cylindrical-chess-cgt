"""Recompute the CGT value of each suite component under each race rule (cache cleared between rules)
and compare with results.json value strings and with static_eval.json's outcome class `o`.
Also lists positions whose FEN carries an e.p. square (the component string drops e.p. state)."""
import json
from cylcgt import cgt, pawns
B = pawns.Board(4, 8, False, True)
rows = json.load(open("engine/suite/results.json"))
se = {r["id"]: r for r in json.load(open("engine/experiments/results/static_eval.json"))["rows"]}
mism = []
outc = {}
for rule in ("count", "mover", "opponent"):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    for r in rows:
        v = pawns.value(B, pawns.Pos.parse(r["component"]))
        s = cgt.show(v)
        if rule == "count":
            outc[r["id"]] = cgt.outcome(v)
        if s != r["value"][rule]:
            mism.append((r["id"], rule, s, r["value"][rule]))
print("value-string mismatches (fresh cache, no ep state):", len(mism), mism[:8])
print("o mismatches:", sum(outc[i] != se[i]["o"] for i in outc))
ep = [(r["id"], r["fen"], r["component"], r["value"]["count"], se[r["id"]]["o"]) for r in rows if r["fen"].split()[3] != "-"]
print("positions with an ep square in FEN:", len(ep)); [print("  ", e) for e in ep]
