from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B3 = pawns.Board(3, 8, True, True)
G = pawns.value(B3, pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7"))
def dump(label, s, mover):
    P = pawns.Pos.parse(s)
    v = pawns.value(B3, P)
    print(f"== {label}: {P} value {cgt.show(v)} [{cgt.outcome(v)}]  L={[cgt.show(x) for x in v.L]} R={[cgt.show(x) for x in v.R]}")
    for d in pawns.moves(B3, P, mover):
        w = val(B3, d, mover)
        tag = ""
        if mover == "W" and cgt.le(w, G): tag = "  <=G"
        if mover == "B" and cgt.le(G, w): tag = "  >=G"
        print(f"   {mover} {d} -> {cgt.show(w)} [{cgt.outcome(w)}]{tag}")
dump("Y = c5xb4", "W: a2 a3 / B: b4 b7 c7", "W")
dump("V = b2-b4 ep after c6-c5", "W: a2 a3 b4 / B: b7 c5 c7", "B")
print("Y.L", cgt.show(val(B3, pawns.Pos.parse('W: a2 a3 / B: b4 b7 c7'), 'W')))
