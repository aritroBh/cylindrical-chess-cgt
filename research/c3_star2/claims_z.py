"""Check the reversal of Z's Black option c7-c5 (W a2 b4 / B b7 c5 ep c6) and the White options of V's c5xb4 chain."""
from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B = pawns.Board(3, 8, True, True)
Z = pawns.Pos.parse("W: a2 b4 / B: b7 c7")
zv = pawns.value(B, Z)
child = pawns.Pos.parse("W: a2 b4 / B: b7 c5")
child = pawns.Pos(child.white, child.black, ((0 + 1, 6 - 0) and (2, 6), (2, 5), "W"))  # ep target c6 for W; captured pawn on c5
print("child", child, cgt.show(pawns.value(B, child)))
for d in pawns.moves(B, child, "W"):
    w = val(B, d, "W")
    print("  W reply", d, cgt.show(w), "Z<=w:", cgt.le(zv, w), "w<=Z:", cgt.le(w, zv))
print("--- replacement for c7-c5: Black replies from the reversing position W a2 c5 / B b7")
rev = pawns.Pos.parse("W: a2 c5 / B: b7")
for d in pawns.moves(B, rev, "B"):
    w = val(B, d, "B")
    print("  B reply", d, cgt.show(w), " 0<=w:", cgt.le(cgt.ZERO, w))
