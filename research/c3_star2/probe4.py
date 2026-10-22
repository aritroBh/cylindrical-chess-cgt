from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B3 = pawns.Board(3, 8, True, True)
G = pawns.value(B3, pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7"))
Z = pawns.Pos.parse("W: a2 b4 / B: b7 c7")
zv = pawns.value(B3, Z)
print("Z", Z, cgt.show(zv), "G<=Z", cgt.le(G, zv), "Z<=G", cgt.le(zv, G))
for d in pawns.moves(B3, Z, "B"):
    w = val(B3, d, "B")
    print("  B", d, cgt.show(w), cgt.outcome(w), "G<=w" , cgt.le(G, w), "w<=G", cgt.le(w, G))
