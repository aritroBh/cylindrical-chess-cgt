"""Repository LOOPY Prop. 2.10(a) says: T=1, H>=5 => (L2) holds in every non-terminal context.
Under the project's default e.p.-aware passed test that is false for H=5.  Position (flat, 4 files, 5 ranks, e.p. on):
W a2 / B a3 b2 with Black's e.p. right (target b3, pawn b2): Black has just played b4-b2.
Nothing is passed (b2 is capturable e.p. by a2, a-pawns face each other), yet Black promotes b2-b1 in ONE move.
The paper's Proposition 6 (>= 6 ranks) is not affected.
Run: PYTHONPATH=. .venv/bin/python notes/proof_audit2/checks/h5_counterexample.py
"""
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
b = Board(4, 5, False, True)
x = Pos(frozenset({(0, 2)}), frozenset({(0, 3), (1, 2)}), ((1, 3), (1, 2), "W"))
print("passed W:", pawns.passed(b, x, "W"), " passed B:", pawns.passed(b, x, "B"))
pawns.PASSED_RESPECTS_EP = False
print("textbook test, passed B:", pawns.passed(b, x, "B"), "(so the textbook test hides the problem)")
y = Pos(x.white, x.black, None)      # after any White move the right is gone; b2-b1 is then available
print("black pawn b2 is on its penultimate rank (rank 2 of 5): promotes in one move; legal moves of Black:",
      [str(p) for p in pawns.moves(b, y, "B")])
