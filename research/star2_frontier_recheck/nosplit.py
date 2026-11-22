"""cylcgt with component splitting switched off (one component = whole board)."""
from cylcgt import pawns, cgt
orig = pawns.components
for split in (True, False):
    pawns.components = orig if split else (lambda b, p: [p])
    for race in ("opponent", "count", "mover"):
        pawns.RACE_RULE = race; pawns.PASSED_RESPECTS_EP = True; pawns._value.cache_clear()
        b = pawns.Board(5, 8, False, True)
        out = []
        for t in ("W: a3 b3 c2 e2 / B: a6 c5 d5 e3", "W: a6 b4 c4 e3 / B: a7 c7 d6 e6", "W: a4 b3 c2 d2 / B: a7 b6 c7 e4"):
            g = pawns.value(b, pawns.Pos.parse(t))
            out.append(f"{cgt.show(g)}(nim={g.nim})")
        print(f"split={split!s:5} race={race:8} aware: " + "  ".join(out))
