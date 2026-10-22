"""Checks of the Black-side claims in the C3 walk-through (exact, engine values)."""
from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B = pawns.Board(3, 8, True, True)
G = pawns.value(B, pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7"))
STAR = cgt.STAR; ZERO = cgt.ZERO
V = pawns.Pos.parse("W: a2 a3 b4 / B: b7 c5 c7")
Y2 = pawns.Pos.parse("W: a2 a3 / B: b4 b7 c7")
Z = pawns.Pos.parse("W: a2 b4 / B: b7 c7")
vV = pawns.value(B, V); print("V value", cgt.show(vV), "G<=V", cgt.le(G, vV))
Vb = {}
for d in pawns.moves(B, V, "B"):
    w = val(B, d, "B"); Vb[str(d)] = w
    print("  V B-option", d, cgt.show(w))
y2v = pawns.value(B, Y2)
print("Y2 value", cgt.show(y2v), "Y2 = c5xb4 result; Y2 Right-option check G<=Y2 ?", cgt.le(G, y2v))
zv = pawns.value(B, Z)
print("Z value", cgt.show(zv), "G<=Z", cgt.le(G, zv))
for d in pawns.moves(B, Z, "B"):
    w = val(B, d, "B")
    print("  Z B-option", d, cgt.show(w), "dominated by 0 (0<=w):", cgt.le(ZERO, w), " w<=0:", cgt.le(w, ZERO))
# Y2 white options reversal: a3xb4 is Z
for d in pawns.moves(B, Y2, "W"):
    w = val(B, d, "W"); print("  Y2 W-option", d, cgt.show(w), "G<=w:", cgt.le(G, w))
# V: which black options are dominated by * or Y2
star = STAR
y2val = y2v
for d in pawns.moves(B, V, "B"):
    w = val(B, d, "B")
    print("  V B-option", d, cgt.show(w), "w>=*:", cgt.le(star, w), "w>=Y2:", cgt.le(y2val, w))
