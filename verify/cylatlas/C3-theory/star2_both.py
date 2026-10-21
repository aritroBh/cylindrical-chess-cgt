"""W a2 c2 / B b7 d7 on 4 files, flat and cylinder, under both passed tests (needs the ep-aware-passed checkout first on PYTHONPATH).
  PYTHONPATH=<ep-wt>:. .venv/bin/python verify/cylatlas/C3-theory/star2_both.py"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
p = Pos.parse("W: a2 c2 / B: b7 d7")
print("cylcgt from", pawns.__file__)
for aware in (False, True):
    pawns.PASSED_RESPECTS_EP = aware; pawns._value.cache_clear()
    for wrap in (False, True):
        print("e.p.-aware" if aware else "textbook  ", "cyl " if wrap else "flat", cgt.show(pawns.value(Board(4, 8, wrap, True), p)))
