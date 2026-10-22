"""The two 7-pawn *2 positions under count/e.p.-aware: all nine settings, cylcgt (F4, F8) and the Codex
whole-board solver (F4), compared as games.

    PYTHONPATH=. .venv/bin/python delegate/checks/star2_seven.py
"""
import sys

sys.path.insert(0, "verify_ext/codex")
import solver as cx  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402

memo = {}


def conv(g):
    if g not in memo:
        memo[g] = cgt.make([conv(x) for x in g.left], [conv(x) for x in g.right])
    return memo[g]


for text in ("W: a4 b3 d2 d3 / B: a7 b7 c5", "W: b4 c2 d2 / B: a6 a7 c6 d5"):
    print(text, flush=True)
    for race in ("count", "mover", "opponent"):
        for ep, test in ((False, "textbook"), (True, "textbook"), (True, "aware")):
            pawns.RACE_RULE, pawns.PASSED_RESPECTS_EP = race, test == "aware"
            vals = []
            for files in (4, 8):
                pawns._value.cache_clear()
                vals.append(pawns.value(pawns.Board(files, 8, False, ep), pawns.Pos.parse(text)))
            c = conv(cx.PawnGame(4, race, ep, test).value(*cx.parse_position(text.replace(":", ""), 4)))
            same = all(cgt.le(v, c) and cgt.le(c, v) for v in vals)
            print(f"  {race}/{'off' if not ep else test:9s} cylcgt {cgt.show(vals[0]):22s} codex {cgt.show(c):22s}"
                  f" {'agree' if same else 'DIFFER'}", flush=True)
