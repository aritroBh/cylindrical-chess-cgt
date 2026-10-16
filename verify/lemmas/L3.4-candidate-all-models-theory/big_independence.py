"""Uses the project engine READ-ONLY (monkeypatches the module constant
pawns.BIG in this process only) to check that the candidate's value does not
depend on BIG.  Run: PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-theory/big_independence.py"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
X = Pos.parse("W: a2 c2 / B: b7 d7")
for big in (1, 2, 3, 4, 8, 64, 256):
    pawns.BIG = big
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        for ep in (True, False):
            pawns._value.cache_clear()
            g = pawns.value(Board(4, 8, False, ep), X)
            print(f"BIG={big:3d} rule={rule:8s} ep={ep!s:5s} S = {cgt.show(g)}  nim={g.nim}")
