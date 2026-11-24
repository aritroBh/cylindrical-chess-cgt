"""Reproduce the two opponent/e.p.-aware C-versus-cylcgt differences."""
from cylcgt import pawns, cgt

CASES = (
    ("W: a3 b3 c2 e2 / B: a6 c5 d5 e3", "⇑"),
    ("W: a6 b4 c4 e3 / B: a7 c7 d6 e6", "⇓"),
)

for text, expected in CASES:
    pawns.RACE_RULE = "opponent"
    pawns.PASSED_RESPECTS_EP = True
    pawns._value.cache_clear()
    game = pawns.value(pawns.Board(5, 8, False, True), pawns.Pos.parse(text))
    assert game.nim is None and cgt.show(game) == expected, (text, cgt.show(game), game.nim)
    print(f"{cgt.show(game)}: {text}")
