"""Comparison with the project's own implementation (cylcgt), run only AFTER ring.c counts were done."""
import sys, time
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, value
assert pawns.RACE_RULE == "count" and pawns.PASSED_RESPECTS_EP is True
for n, text in [(3, "W: a2 a3 b2 / B: b7 c6 c7"), (4, "W: a4 b2 c2 / B: b6 c5 d6 d7"),
                (4, "W: b2 c2 d4 / B: a6 a7 b5 c6"), (4, "W: a4 b3 d2 d3 / B: a7 b7 c5")]:
    t = time.time()
    g = value(Board(n, 8, True, True), Pos.parse(text))
    print(n, text, "->", cgt.show(g), "(%.1fs)" % (time.time() - t), flush=True)
