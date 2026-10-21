"""Run cylcgt (as-is in this folder) on the candidate, for comparison only.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C2-refute/run2/cylcgt_values.py
"""
from cylcgt import pawns, cgt
print("PASSED_RESPECTS_EP present:", hasattr(pawns, "PASSED_RESPECTS_EP"))
pos = pawns.Pos.parse("W: a2 c2 / B: b7 d7")
for ep in (False, True):
    b = pawns.Board(4, 8, False, ep)
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        pawns.race_hits.clear()
        g = pawns.value(b, pos)
        print(f"ep={ep} rule={rule}: value={cgt.show(g)} G+*2 outcome={cgt.outcome(cgt.add(g, cgt.nimber(2)))} race_hits={len(pawns.race_hits)}")
