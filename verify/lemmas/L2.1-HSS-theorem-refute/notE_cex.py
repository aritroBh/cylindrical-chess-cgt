"""(E) is a necessary hypothesis of Theorem 2.1: an HSS position violating (E)
whose S and W outcome classes differ, checked with BOTH implementations.
6x6 flat board, e.p. on; Black has just played a5-a3, so White may take b3xa4 e.p.
Run from the project root: PYTHONPATH=. .venv/bin/python verify/lemmas/L2.1-HSS-theorem-refute/notE_cex.py
"""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/verify/lemmas/L2.1-HSS-theorem-refute')
import indep as I
from cylcgt import cgt
from cylcgt.pawns import Board, Pos, sq
from lemmas.common import S, W, alt_outcome, hereditarily_safe

b = Board(6, 6, False, True)
x0 = Pos.parse("W: a2 b3 d2 / B: a3 b4 d4")
x = Pos(x0.white, x0.black, (sq("a4"), sq("a3"), "W"))
bd = I.Board(6, 6, False, True)
y = I.mkpos(x.white, x.black, ((0, 4), (0, 3), "W"))
a = I.analyse(bd, y)
print("mine: HSS", a["HSS"], "(E)", a["E"], "move bound", I.move_bound(bd, y))
for rule in ("count", "mover", "opponent"):
    s, w = S(b, x, rule), W(b, x, rule)
    print(rule, "| worker: o(S)", cgt.outcome(s), "S =", cgt.show(s), " o(W)", cgt.outcome(w), "W =", cgt.show(w),
          "alt", alt_outcome(b, x, rule), "HSS", hereditarily_safe(b, x),
          "| mine: oS", I.oS(bd, y, rule), "oW", I.oW(bd, y, rule))
