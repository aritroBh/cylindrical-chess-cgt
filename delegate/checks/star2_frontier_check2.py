"""Completes star2_frontier_check.py, which hit its 3000 s timeout after two witnesses.
Only the headline setting (count / e.p. on / e.p.-aware), for the witnesses it did not reach.

    PYTHONPATH=. .venv/bin/python delegate/checks/star2_frontier_check2.py
"""
import sys
import time

from cylcgt import cgt, pawns

sys.path.insert(0, "verify_ext/codex")
import solver as cx  # noqa: E402

POSITIONS = (
    "W: a6 b4 c4 e3 / B: a7 c7 d6 e6",
    "W: a4 b3 c3 e2 / B: a7 c5 d5 d6",
)
pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
for text in POSITIONS:
    t0 = time.time()
    a5 = cgt.show(pawns.value(pawns.Board(5, 8, False, True), pawns.Pos.parse(text)))
    g = cx.PawnGame(5, "count", True, "aware")
    w, b = cx.parse_position(text.replace(":", ""), 5)
    c5 = cx.show(g.value(w, b))
    print(f"{text:36s} count/aware  cylcgt F5 {a5:10s} codex F5 {c5:10s} ({time.time() - t0:.0f}s)", flush=True)
