"""Pawn-level exact-equality test of claim N1: G + M where M = colour-mirror of the paper's 4.3 tiny position
(W a4 h2 h4 / B a5 a6 a7 h3 mirrored -> W a2 a3 a4 h6 / B a5 h5 h7, expected miny(1)).
If G = tiny(1) and M = miny(1), the cylinder sum is a second-player win (P).
Checked with: my independent code (indep_tiny.py, explicit-tree <=), cylcgt, and crosscheck minimax (whole-board play).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/N1-reproduce/exact_sum_test.py
"""
import sys
sys.path.insert(0, "verify/diagrams/N1-reproduce")
sys.setrecursionlimit(100000)
import indep_tiny as T
from cylcgt import cgt, pawns
from crosscheck.minimax import Board as XB, outcome_class, parse_position

CD = "W: c1 c3 d3 / B: c2 d4 d5 d6"
M = "W: a2 a3 a4 h6 / B: a5 h5 h7"
SUM = "W: a2 a3 a4 c1 c3 d3 h6 / B: a5 c2 d4 d5 d6 h5 h7"
MINY1 = T.G([T.G([T.ONE], [T.ZERO])], [T.ZERO])
for ep in (True, False):
    T.CFG.update(wrap=True, ep=ep, race="count"); T.reset()
    m = T.pawnnode(T.parse(M)); g = T.pawnnode(T.parse(CD))
    print(f"ep={ep}: indep  M == miny(1): {T.eq(m, MINY1)}")
    # G + M = 0  <=>  G == -M ; with M == miny(1) this is G == tiny(1)
    print(f"        indep  G == tiny(1): {T.eq(g, T.TINY1)}")
    b = pawns.Board(8, 8, True, ep); pawns.RACE_RULE = "count"; pawns._value.cache_clear()
    gs = pawns.value(b, pawns.Pos.parse(SUM))
    print(f"        cylcgt value(M) = {cgt.show(pawns.value(b, pawns.Pos.parse(M)))}; value(G+M) = {cgt.show(gs)}, "
          f"outcome {cgt.outcome(gs)}, sum_safe {pawns.sum_safe(b, pawns.Pos.parse(SUM))}")
    print(f"        crosscheck whole-board outcome of G+M: {outcome_class(XB(8, 8, True, ep), parse_position(SUM))}")
