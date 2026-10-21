"""C4 verifier: textbook values straight from cylcgt (read-only import), with
cache_clear after each RACE_RULE change; also the a2-a4 child as cylcgt scores it."""
from cylcgt import pawns, cgt
for ep in (True, False):
    B4 = pawns.Board(4, 8, False, ep)
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        out = []
        for txt in ("W: a2 c2 / B: b4 d7", "W: a2 c2 / B: b5 d7", "W: a2 c2 / B: b7 d7"):
            out.append(cgt.show(pawns.value(B4, pawns.Pos.parse(txt))))
        X = pawns.Pos.parse("W: a2 c2 / B: b4 d7")
        a4 = [c for c in pawns.moves(B4, X, "W") if (0, 4) in c.white][0]
        print(f"flat4 ep={ep!s:5} {rule:8s}: X={out[0]:14s} Y(b5)={out[1]:6s} G={out[2]:4s} | a2-a4 child {a4} -> {cgt.show(pawns._child(B4, a4, 'W'))}")
