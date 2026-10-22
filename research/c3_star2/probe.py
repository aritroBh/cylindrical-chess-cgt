from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B3 = pawns.Board(3, 8, True, True)
P3 = pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7")
G = pawns.value(B3, P3)
def show(p): return str(p)
# Reversal replacement sets at depth 2
for label, pos_str in [("W03 a3-a4", "W: a2 a4 b2 / B: b7 c6 c7"), ("B03 c6-c5", "W: a2 a3 b2 / B: b7 c5 c7")]:
    P = pawns.Pos.parse(pos_str)
    mover = "W" if label.startswith("W") else "B"
    other = "B" if mover == "W" else "W"
    print("==", label, val(B3, P, mover) and cgt.show(val(B3, P, mover)))
    for d in pawns.moves(B3, P, other):
        w = val(B3, d, other)
        rel = "<=G" if cgt.le(w, G) else (">=G" if cgt.le(G, w) else "incomparable")
        print("  reply", other, d, cgt.show(w), rel)
        if mover=="W" and cgt.le(w,G) or mover=="B" and cgt.le(G,w):
            for z in pawns.moves(B3, d, mover):
                zv = val(B3, z, mover)
                print("     ", mover, z, cgt.show(zv), cgt.outcome(zv))
