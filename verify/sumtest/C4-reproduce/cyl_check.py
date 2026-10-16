"""C4 verifier: textbook values from cylcgt itself (read-only import)."""
from cylcgt import pawns, cgt
B4 = pawns.Board(4, 8, False, True)
B4n = pawns.Board(4, 8, False, False)
for rule in ("count", "mover", "opponent"):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    for txt in ("W: a2 c2 / B: b4 d7", "W: a2 c2 / B: b5 d7", "W: a2 c2 / B: b7 d7",
                "W: a4 c2 / B: b4 d7", "W: c2 / B: a3 d7"):
        for bd, tag in ((B4, "ep"), (B4n, "noep")):
            p = pawns.Pos.parse(txt)
            print(rule, tag, txt, "->", cgt.show(pawns.value(bd, p)))
    # after a2-a4 with ep right stored, as cylcgt's _child sees it
    p = pawns.Pos.parse("W: a4 c2 / B: b4 d7")
    pe = pawns.Pos(p.white, p.black, (pawns.sq("a3"), pawns.sq("a4"), "B"))
    print(rule, "child a2-a4 with ep stored ->", cgt.show(pawns._child(B4, pe, "W")),
          "passedW", pawns.passed(B4, pe, "W"), "passedB", pawns.passed(B4, pe, "B"))
    # options of X under cylcgt
    X = pawns.Pos.parse("W: a2 c2 / B: b4 d7")
    for side in "WB":
        for c in pawns.moves(B4, X, side):
            print("   ", rule, side, "->", c, ":", cgt.show(pawns._child(B4, c, side)))
