from cylcgt import pawns, cgt
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True; pawns._value.cache_clear()
B3 = pawns.Board(3, 8, True, True)
B4 = pawns.Board(4, 8, True, True)
P3 = pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7")
P4 = pawns.Pos.parse("W: a4 b2 c2 / B: b6 c5 d6 d7")
for B, P in [(B3, P3), (B4, P4)]:
    v = pawns.value(B, P)
    print(P, cgt.show(v), cgt.outcome(v), pawns.components(B, P))
    print(pawns.describe(B, P))
