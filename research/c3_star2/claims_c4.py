"""Checks of the C4 walk-through claims (engine values, default setting)."""
from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B = pawns.Board(4, 8, True, True)
P = pawns.Pos.parse("W: a4 b2 c2 / B: b6 c5 d6 d7")
G = pawns.value(B, P)
star, zero = cgt.STAR, cgt.ZERO
print("G =", cgt.show(G), "G==*2:", G is cgt.make([zero, star], [zero, star]))
print("== W a5 (a4-a5) reversal through b6-b5: White replies of W a5 b2 c2 / B b5 c5 d6 d7")
Ya = pawns.Pos.parse("W: a5 b2 c2 / B: b5 c5 d6 d7")
for z in pawns.moves(B, Ya, "W"):
    zv = val(B, z, "W")
    print(f"  {z} value {cgt.show(zv)[:70]}  <=0:{cgt.le(zv, zero)}  <=*:{cgt.le(zv, star)}  G<=z:{cgt.le(G, zv)}")
print("== B b6-b5 reversal through a4xb5: Black replies of W b2 b5 c2 / B c5 d6 d7")
Yb = pawns.Pos.parse("W: b2 b5 c2 / B: c5 d6 d7")
for d in pawns.moves(B, Yb, "B"):
    dv = val(B, d, "B")
    print(f"  {d} value {cgt.show(dv)[:70]}  *<=w:{cgt.le(star, dv)}  0<=w:{cgt.le(zero, dv)}")
print("== B d6-d5 reversal through a4xd5: Black replies of W b2 c2 d5 / B b6 c5 d7")
Yd = pawns.Pos.parse("W: b2 c2 d5 / B: b6 c5 d7")
for d in pawns.moves(B, Yd, "B"):
    dv = val(B, d, "B")
    print(f"  {d} value {cgt.show(dv)[:70]}  *:{cgt.le(dv, star) and cgt.le(star, dv)}  <=*:{cgt.le(dv, star)}  >=*:{cgt.le(star, dv)}")
