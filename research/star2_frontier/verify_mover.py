"""Check the two independently evaluated mover-rule flat 5-file hits."""
from cylcgt import pawns, cgt

POSITION = "W: a4 b3 c3 e2 / B: a7 c5 d5 d6"
for name, ep, aware in (("M/T", True, False), ("M/off", False, False)):
    pawns.RACE_RULE = "mover"
    pawns.PASSED_RESPECTS_EP = aware
    pawns._value.cache_clear()
    game = pawns.value(pawns.Board(5, 8, False, ep), pawns.Pos.parse(POSITION))
    assert game.nim == 2, (name, cgt.show(game), game.nim)
    print(f"*2 under {name}: {POSITION}")
