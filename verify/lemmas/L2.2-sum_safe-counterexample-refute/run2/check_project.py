"""What the code under test (cylcgt.pawns) and Codex's crosscheck say on the 9 rows.
Not the decisive check (that is run_checks.py / indep2.py); this only confirms
that sum_safe() really returns True and pawns.value really has the claimed outcome.

Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/lemmas/L2.2-sum_safe-counterexample-refute/run2/check_project.py
"""
from cylcgt import cgt, pawns
from crosscheck import minimax as mm

CASES = [
    ((8, 8, True, False), "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count"),
    ((8, 8, True, False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count"),
    ((8, 8, True, False), "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count"),
    ((8, 8, True, True), "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count"),
    ((8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7", "count"),
    ((8, 7, True, False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count"),
    ((7, 6, False, True), "W: b2 d3 f2 / B: c4 c5 e5 g5", "count"),
    ((8, 8, True, True), "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent"),
    ((6, 8, False, False), "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent"),
]
for bd, text, rule in CASES:
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    b = pawns.Board(*bd)
    x = pawns.Pos.parse(text)
    v = pawns.value(b, x)
    xc = None
    if bd[1] == 8 and rule == "count":  # crosscheck hard-codes count races and 8 ranks
        xc = mm.outcome_class(mm.Board(*bd), mm.Position(x.white, x.black, None))
    print(f"{bd} {text} {rule}: comps={len(pawns.components(b, x))} sum_safe={pawns.sum_safe(b, x)} "
          f"o(pawns.value)={cgt.outcome(v)} crosscheck={xc}")
pawns.RACE_RULE = "count"
