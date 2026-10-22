"""Prop. 11: X = W b2 d4 g3 h5 / B a7 c7 f7 g4 on cyl(8), e.p. off, count rule.
Checks with the repo engine: single component at the root, sum_safe() True (top-level test passes), HSS False,
o(S)=R, o(W)=N; and with the independent module: HSS False (Definition 9 recomputed).
Run: PYTHONPATH=. .venv/bin/python notes/proof_audit2/checks/prop11_hss_check.py
"""
import sys
sys.path.insert(0, "notes/proof_audit2/checks")
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common as C
import indep_sum_model as M, hss_search as H
b = Board(8, 8, True, False)
x = Pos.parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
print("components at root:", len(pawns.components(b, x)))
print("sum_safe (top-level test):", pawns.sum_safe(b, x))
print("HSS (repo):", C.hereditarily_safe(b, x))
print("o(S) repo:", cgt.outcome(C.S(b, x, "count")), " o(W) repo:", C.alt_outcome(b, x, "count"))
M.configure(8, 8, True, False, "count", True, big=24)
W, B = M.parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
print("HSS, (E) (independent):", H.analyse(W, B))
