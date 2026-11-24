"""Check one flat five-file headline witness; pass index 1, 2, or 3."""
import sys
from cylcgt import pawns, cgt

POSITIONS = (
    "W: a3 b3 c2 e2 / B: a6 c5 d5 e3",
    "W: a4 b3 c2 d2 / B: a7 b6 c7 e4",
    "W: a6 b4 c4 e3 / B: a7 c7 d6 e6",
)

index = int(sys.argv[1]) - 1
assert 0 <= index < len(POSITIONS), "pass 1, 2, or 3"
text = POSITIONS[index]
pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
pawns._value.cache_clear()
board = pawns.Board(5, 8, False, True)
pos = pawns.Pos.parse(text)
assert not pawns.passed(board, pos, "W") and not pawns.passed(board, pos, "B")
game = pawns.value(board, pos)
assert game.nim == 2, (text, cgt.show(game), game.nim)
print(f"*2: {text}")
