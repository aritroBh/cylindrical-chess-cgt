"""Same positions under the ADOPTED e.p.-aware passed test (needs the ep-aware-passed
checkout of cylcgt first on PYTHONPATH).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=<scratchpad>/ep-wt:. .venv/bin/python verify/cylatlas/C7-theory/epaware_check.py"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
print(pawns.__file__, "PASSED_RESPECTS_EP =", pawns.PASSED_RESPECTS_EP)
for aware in (True, False):
    pawns.PASSED_RESPECTS_EP = aware
    for lab, b0, t in [("flat3", (3, False), "W: a2 b3 c3 / B: a6 b5 b7"),
                       ("cyl8 b-d", (8, True), "W: b2 c3 d3 / B: b6 c5 c7"),
                       ("flat4", (4, False), "W: a2 c2 / B: b7 d7"),
                       ("cyl9 buffered", (9, True), "W: d2 f2 / B: e7 g7")]:
        for ep in (True, False):
            row = []
            for rule in ("count", "mover", "opponent"):
                pawns.RACE_RULE = rule
                pawns._value.cache_clear()
                row.append(f"{rule}={cgt.show(pawns.value(Board(b0[0], 8, b0[1], ep), Pos.parse(t)))[:34]}")
            print(f"aware={aware!s:5} {lab:14s} {t:28s} ep={'on ' if ep else 'off'} " + "  ".join(row))
