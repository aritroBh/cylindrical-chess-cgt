"""V1 theory scratch: pawns.race_hits counts race-leaf EVALUATIONS (one per parent->child edge,
since _child is not cached), not distinct race positions.  Count both for 7.2{a,b,h}.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/V1-theory/race_count.py
"""
import sys
from dataclasses import replace
sys.setrecursionlimit(1_000_000)
from cylcgt import pawns
from cylcgt.pawns import CYL8, Pos
for b in (CYL8, replace(CYL8, ep=False)):
    pawns.RACE_RULE = "count"; pawns._value.cache_clear(); pawns.race_hits.clear()
    pawns.value(b, Pos.parse("W: a2 b2 h3 / B: a6 b7 h7"))
    pos_only = {h.rsplit(" after ", 1)[0] for h in pawns.race_hits}
    print(f"ep={'on ' if b.ep else 'off'} race_hits entries {len(pawns.race_hits)}, distinct (position, mover) "
          f"{len(set(pawns.race_hits))}, distinct positions {len(pos_only)}")
