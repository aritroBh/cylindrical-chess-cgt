"""C1 verifier: (1) tb_root in static_eval.json vs the raw Lichess responses in engine/suite/tbcache
(found by scanning every cached file's 'fen' field, no hashing assumptions); (2) the CGT outcome class
'o' recomputed with cylcgt (count rule, 4-file flat board, ep on) and checked with cgt.outcome and,
for the nimber group, with cgt.le against * directly. No network.
    PYTHONPATH=. .venv/bin/python verify/engines/C1-theory/recheck_labels.py
"""
import json, glob
from cylcgt import cgt, pawns
from realchess import movegen
se = json.load(open("engine/experiments/results/static_eval.json"))["rows"]
cache = {}
for f in glob.glob("engine/suite/tbcache/*/*.json"):
    d = json.load(open(f))
    if d.get("status") == 200:
        cache[movegen.normal_fen(d["fen"])] = d["data"]
bad = missing = 0
for r in se:
    d = cache.get(movegen.normal_fen(r["fen"]))
    if d is None:
        missing += 1; continue
    if d["category"] != r["tb_root"]:
        bad += 1; print("MISMATCH", r["id"], d["category"], r["tb_root"])
print(f"tb_root check: {len(se)} rows, {missing} not in cache, {bad} mismatches")
pawns.RACE_RULE = "count"; pawns._value.cache_clear()
B = pawns.Board(4, 8, False, True)
star = cgt.nimber(1)
bad_o = 0; nim_ok = 0; nim_n = 0
for r in se:
    g = pawns.value(B, pawns.Pos.parse(r["component"]))
    if cgt.outcome(g) != r["o"]:
        bad_o += 1; print("O MISMATCH", r["id"])
    if r["o"] == "N" and r["value_count"].startswith("*"):
        nim_n += 1
        nim_ok += cgt.le(g, star) and cgt.le(star, g)
print(f"outcome-class check: {bad_o} mismatches; nimber group: {nim_ok}/{nim_n} components equal * exactly")
