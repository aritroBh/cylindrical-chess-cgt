"""cylcgt vs the Codex whole-board solver: value equality (as games, not display strings) on random
flat positions, all nine settings. Prints every disagreement.

    PYTHONPATH=. .venv/bin/python delegate/checks/cylcgt_vs_codex.py [N] [extra positions...]
"""
import random
import sys

sys.path.insert(0, "verify_ext/codex")
import solver as cx  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402

SETTINGS = [(race, ep, test) for race in ("count", "mover", "opponent")
            for ep, test in ((False, "textbook"), (True, "textbook"), (True, "aware"))]
memo = {}


def conv(g):
    """Codex Game -> cylcgt Game."""
    if g not in memo:
        memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return memo[g]


def compare(text, width):
    bad = []
    for race, ep, test in SETTINGS:
        pawns.RACE_RULE, pawns.PASSED_RESPECTS_EP = race, test == "aware"
        pawns._value.cache_clear()
        board = pawns.Board(width, 8, False, ep)
        pos = pawns.Pos.parse(text)
        try:
            a = pawns.value(board, pos)
        except pawns.RaceError:
            continue
        b = conv(cx.PawnGame(width, race, ep, test).value(*cx.parse_position(text.replace(":", ""), width)))
        if not (cgt.le(a, b) and cgt.le(b, a)):
            bad.append(f"{race}/{'off' if not ep else test}: cylcgt {cgt.show(a)}  codex {cgt.show(b)}")
    return bad


n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
random.seed(7)
cases = [(t, 5) for t in sys.argv[2:]]
for _ in range(n):
    width = random.choice((2, 3, 4))
    sqs = [f"{'abcd'[f]}{r}" for f in range(width) for r in range(2, 8)]
    k = random.randint(2, 6)
    pick = random.sample(sqs, k)
    j = random.randint(1, k - 1)
    cases.append((f"W: {' '.join(pick[:j])} / B: {' '.join(pick[j:])}", width))
ndiff = 0
for text, width in cases:
    pos = pawns.Pos.parse(text)
    board = pawns.Board(width, 8, False, True)
    if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"):
        continue
    for line in compare(text, width):
        ndiff += 1
        print(f"F{width} {text}: {line}", flush=True)
print(f"done: {len(cases)} cases, {ndiff} disagreements")
