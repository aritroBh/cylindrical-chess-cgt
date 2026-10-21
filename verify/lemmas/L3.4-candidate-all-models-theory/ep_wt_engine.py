"""Canonical value of the candidate with the project's e.p.-aware cylcgt (branch ep-aware-passed,
checked out read-only at $EPWT). Run:
  EPWT=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$EPWT ../../../.venv/bin/python ep_wt_engine.py"""
import sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
print("engine:", pawns.__file__)
X = Pos.parse("W: a2 c2 / B: b7 d7")
for aware in (False, True):
    pawns.PASSED_RESPECTS_EP = aware
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        for ep in (True, False):
            pawns._value.cache_clear()
            g = pawns.value(Board(4, 8, False, ep), X)
            print(f"aware={aware!s:5} rule={rule:8} ep={ep!s:5} S = {cgt.show(g)}")
