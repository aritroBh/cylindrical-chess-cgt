"""Values of the claim's example components in all 12 settings, e.p.-aware cylcgt.
Run: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python verify/bench/C1-reproduce/examples.py <ep-wt>"""
import sys
sys.path.insert(0, sys.argv[1])
from cylcgt import pawns
from bench import cgtfmt
assert hasattr(pawns, "PASSED_RESPECTS_EP"), pawns.__file__
print(pawns.__file__)
for p, w in [("W: a2 c2 / B: a3 b6", 3), ("W: a2 c3 / B: b6 c4", 3), ("W: a6 b3 / B: a7 c7", 3), ("W: a2 c2 / B: a4 b6", 3), ("W: a2 c2 / B: a3 b5", 3), ("W: a2 c2 / B: b7 d7", 4)]:
    for aware in (False, True):
        pawns.PASSED_RESPECTS_EP = aware
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule; pawns._value.cache_clear()
            vs = [cgtfmt.fmt(pawns.value(pawns.Board(w, 8, False, ep), pawns.Pos.parse(p)), ascii=True) for ep in (True, False)]
            print(f"{p:22s} {'aware   ' if aware else 'textbook'} {rule:8s} ep-on: {vs[0]:40s} ep-off: {vs[1]}")
