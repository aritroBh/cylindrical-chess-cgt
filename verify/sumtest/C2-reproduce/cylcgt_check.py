"""C2 verifier: cylcgt value of W a2 c2 / B b7 d7 on 4-file flat board, per race rule and e.p."""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

POS = "W: a2 c2 / B: b7 d7"
pos = Pos.parse(POS)
star = cgt.nimber(1); star2 = cgt.nimber(2); zero = cgt.integer(0)
for rule in ("count", "mover", "opponent"):
    for ep in (False, True):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        pawns.race_hits.clear()
        b = Board(4, 8, False, ep)
        g = pawns.value(b, pos)
        out = {n: cgt.outcome(cgt.add(g, x)) for n, x in (("0", zero), ("*", star), ("*2", star2), ("*3", cgt.nimber(3)))}
        print(rule, "ep" if ep else "noep", "value=", cgt.show(g), "eq*2:", cgt.le(g, star2) and cgt.le(star2, g),
              "eq0:", cgt.le(g, zero) and cgt.le(zero, g), out, "race_hits=", len(pawns.race_hits),
              "distinct", len(set(pawns.race_hits)))
# also with 8-file flat, 8-file cylinder embedding (files e-h empty) and 5-file cyl
for (F, wrap) in ((8, False), (8, True), (5, True)):
    for rule in ("count", "mover", "opponent"):
        for ep in (False, True):
            pawns.RACE_RULE = rule; pawns._value.cache_clear()
            g = pawns.value(Board(F, 8, wrap, ep), pos)
            print(F, "cyl" if wrap else "flat", rule, ep, cgt.show(g))
