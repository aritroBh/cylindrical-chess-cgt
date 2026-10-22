from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val
setup("count", True)
B3 = pawns.Board(3, 8, True, True)
G = pawns.value(B3, pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7"))
def dump(label, s, mover):
    P = pawns.Pos.parse(s)
    v = pawns.value(B3, P)
    print(f"== {label}: {P} value {cgt.show(v)} [{cgt.outcome(v)}]  L={[cgt.show(x) for x in v.L]} R={[cgt.show(x) for x in v.R]}")
    other = "B" if mover == "W" else "W"
    for d in pawns.moves(B3, P, mover):
        w = val(B3, d, mover)
        tag = ""
        if mover == "W" and cgt.le(w, G): tag = "  <=G (reverses?)"
        if mover == "B" and cgt.le(G, w): tag = "  >=G"
        print(f"   {mover} {d} -> {cgt.show(w)} [{cgt.outcome(w)}]{tag}")
    return P
dump("X after a4xb5", "W: a2 b2 b5 / B: c6 c7", "B")
dump("Black c6xb5", "W: a2 b2 / B: b5 c7", "W")
dump("Black c6-c5", "W: a2 b2 b5 / B: c5 c7", "W")
dump("Q after b7-b5", "W: a2 a4 b2 / B: b5 c6 c7", "W")
dump("W a2 b2 b3 ... root b2-b3 then", "W: a2 a3 b3 / B: b7 c6 c7", "B")
print("G =", cgt.show(G), " G.L", [cgt.show(x) for x in G.L], "G.R", [cgt.show(x) for x in G.R])
