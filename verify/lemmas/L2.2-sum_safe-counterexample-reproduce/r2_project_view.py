"""Project-code view of the headline: components, sum_safe, o(pawns.value),
o(common.W), common.alt_outcome, crosscheck.minimax, HSS.
cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L2.2-sum_safe-counterexample-reproduce/r2_project_view.py"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from crosscheck import minimax as mm
from lemmas.common import S, W, alt_outcome, hereditarily_safe
b = Board(8, 8, True, False)
x = Pos.parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
print("RACE_RULE before:", pawns.RACE_RULE)
s = S(b, x, "count")
print("components:", [str(c) for c in pawns.components(b, x)])
print("sum_safe:", pawns.sum_safe(b, x))
print("value S:", cgt.show(s), " o(S):", cgt.outcome(s))
print("o(W):", cgt.outcome(W(b, x, "count")), " alt:", alt_outcome(b, x, "count"))
print("crosscheck:", mm.outcome_class(mm.Board(8, 8, True, False), mm.Position(x.white, x.black, None)))
print("HSS:", hereditarily_safe(b, x))
# cache-staleness probe: switch rules and come back
for r in ("mover", "opponent", "count"):
    print(f"  rule {r}: o(S)={cgt.outcome(S(b, x, r))} o(W)={cgt.outcome(W(b, x, r))} sum_safe={pawns.sum_safe(b, x)}")
pawns._value.cache_clear(); pawns.RACE_RULE = "count"
print("after explicit cache_clear, count: o(S)=", cgt.outcome(pawns.value(b, x)))
