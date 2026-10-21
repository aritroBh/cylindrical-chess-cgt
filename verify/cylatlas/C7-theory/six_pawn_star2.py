"""Values of the flat8 census's 6-pawn 3-file *2 (opponent rule) and of the 4-file *2,
on a 3-file flat strip and placed on files b-d of the 8-file cylinder (a and e empty),
under each race rule, e.p. on/off, with the main checkout's cylcgt (textbook passed test).
Also the 4-file *2 on a 9-file cylinder with two empty buffer files.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C7-theory/six_pawn_star2.py"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
print("cylcgt has PASSED_RESPECTS_EP:", hasattr(pawns, "PASSED_RESPECTS_EP"), getattr(pawns, "PASSED_RESPECTS_EP", None))
cases = [
    ("flat3", Board(3, 8, False, None), "W: a2 b3 c3 / B: a6 b5 b7"),
    ("cyl8 on b-d", Board(8, 8, True, None), "W: b2 c3 d3 / B: b6 c5 c7"),
    ("flat4", Board(4, 8, False, None), "W: a2 c2 / B: b7 d7"),
    ("cyl9, trebuchet a/b/i, component d-g, buffers c,h", Board(9, 8, True, None), "W: d2 f2 / B: e7 g7"),
    ("flat4 (mover/ep-off *2 of flat8 census)", Board(4, 8, False, None), "W: a3 b2 d3 / B: a6 c7 d6"),
]
for lab, b0, t in cases:
    for ep in (True, False):
        b = Board(b0.files, b0.ranks, b0.wrap, ep)
        row = []
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            g = pawns.value(b, Pos.parse(t))
            row.append(f"{rule}={cgt.show(g)[:40]}")
        print(f"{lab:48s} {t:28s} ep={'on ' if ep else 'off'} " + "  ".join(row))
pawns.RACE_RULE = "count"
