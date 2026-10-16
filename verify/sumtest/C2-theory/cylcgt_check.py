"""Theory-lens verifier: recompute G with cylcgt and check G+*2 (and G-*2) via cgt directly.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C2-theory/cylcgt_check.py
"""
from cylcgt import cgt, pawns

POS = "W: a2 c2 / B: b7 d7"
star2 = cgt.nimber(2)
for rule in ("count", "mover", "opponent"):
    for ep in (False, True):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        pawns.race_hits.clear()
        b = pawns.Board(4, 8, False, ep)
        p = pawns.Pos.parse(POS)
        g = pawns.value(b, p)
        print(rule, "ep" if ep else "noep", "value:", cgt.show(g),
              "| G+*2:", cgt.outcome(cgt.add(g, star2)),
              "| G==*2:", cgt.le(g, star2) and cgt.le(star2, g),
              "| G==0:", cgt.le(g, cgt.integer(0)) and cgt.le(cgt.integer(0), g),
              "| race hits:", len(pawns.race_hits),
              "| sum_safe:", pawns.sum_safe(b, p))
