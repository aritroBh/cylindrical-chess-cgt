"""Verifier: check the stated mechanism of the headline counterexample.
  (a) W: b5 d4 g3 / B: c6 f6 g4 h6 is reachable from X, splits into {b,c,d} and
      {f,g,h}, each with both threat signs, o(S)=R and o(W)=L.
  (b) "Three of White's four moves and one of Black's six lead to children where
      S and W already disagree in outcome."
Both cylcgt-based and indep-based numbers are printed.

Run from project root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python \
      verify/lemmas/L2.2-sum_safe-counterexample-reproduce/check_mechanism.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402
from lemmas.common import S, W, reachable, terminal, threats  # noqa: E402

b = Board(8, 8, True, False)
bd = indep.Bd(8, 8, True, False)
X = Pos.parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
Y = Pos.parse("W: b5 d4 g3 / B: c6 f6 g4 h6")

R = reachable(b, X)
print("(a) Y reachable from X:", Y in R, "| #reachable:", len(R))
cs = pawns.components(b, Y)
print("    components of Y:", [str(c) for c in cs])
print("    threats per component (common.threats):", [sorted(threats(b, c)) for c in cs])
print("    threats per component (indep.tau):", [sorted(indep.tau(bd, (c.white, c.black, None))) for c in cs])
print("    o(S(Y)) pawns:", cgt.outcome(S(b, Y, "count")), " indep:", indep.s_outcome(bd, (Y.white, Y.black, None), "count"))
print("    o(W(Y)) common:", cgt.outcome(W(b, Y, "count")), " indep:", indep.w_outcome(bd, (Y.white, Y.black, None), "count"))


def child_outcomes(side):
    out = []
    for c in pawns.moves(b, X, side):
        t = terminal(b, c)
        if t is not None:
            out.append((str(c), "terminal", t))
            continue
        so = cgt.outcome(S(b, c, "count"))
        wo = cgt.outcome(W(b, c, "count"))
        p = (c.white, c.black, None)
        iso = indep.s_outcome(bd, p, "count")
        iwo = indep.w_outcome(bd, p, "count")
        out.append((str(c), so, wo, iso, iwo, "DIFF" if so != wo else "same"))
    return out


for side in ("W", "B"):
    ch = child_outcomes(side)
    nd = sum(1 for r in ch if r[-1] == "DIFF")
    print(f"(b) {side} has {len(ch)} moves; children with o(S)!=o(W): {nd}")
    for r in ch:
        print("      ", r)
