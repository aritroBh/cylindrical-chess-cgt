"""Values of the 4-file ring positions that the worker's own data flags as race-robust (e.p. on).
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C4-theory/key_positions.py            # textbook passed test
  PYTHONPATH=<scratchpad>/ep-wt:. .venv/bin/python verify/cylatlas/C4-theory/key_positions.py   # e.p.-aware
"""
from cylcgt import cgt, pawns
print("cylcgt:", pawns.__file__, "PASSED_RESPECTS_EP =", getattr(pawns, "PASSED_RESPECTS_EP", "absent (textbook)"))
POS = ["W: a2 c2 / B: b7 d7", "W: a2 c3 / B: b7 d7", "W: a2 c2 / B: b6 d7", "W: a2 c2 / B: b6 d6", "W: a3 c3 / B: b7 d7"]
for wrap in (True, False):
    for s in POS:
        row = []
        for ep in (True, False):
            for rule in ("count", "mover", "opponent"):
                pawns.RACE_RULE = rule; pawns._value.cache_clear(); pawns.race_hits.clear()
                g = pawns.value(pawns.Board(4, 8, wrap, ep), pawns.Pos.parse(s))
                row.append(f"{rule}/ep{'on' if ep else 'off'}={cgt.show(g)} [{cgt.outcome(g)}, races {len(pawns.race_hits)}]")
        print(("C4 " if wrap else "F4 ") + s)
        for r in row: print("     ", r)
