"""Re-check of T8's 8-pawn, 5-file *2 witnesses with two implementations:
cylcgt (component sums) and verify_ext/codex/solver.py (Codex, whole-board, written from the rules).
All nine settings, on the 5-file board and on the 8-file board with files f-h empty.

    PYTHONPATH=. .venv/bin/python delegate/checks/star2_frontier_check.py
"""
import sys
import time

from cylcgt import cgt, pawns

sys.path.insert(0, "verify_ext/codex")
import solver as cx  # noqa: E402

POSITIONS = (
    "W: a3 b3 c2 e2 / B: a6 c5 d5 e3",
    "W: a4 b3 c2 d2 / B: a7 b6 c7 e4",
    "W: a6 b4 c4 e3 / B: a7 c7 d6 e6",
    "W: a4 b3 c3 e2 / B: a7 c5 d5 d6",
)
SETTINGS = [(race, ep, test) for race in ("count", "mover", "opponent")
            for ep, test in ((False, "textbook"), (True, "textbook"), (True, "aware"))]


def cyl_value(text, files, race, ep, test):
    pawns.RACE_RULE = race
    pawns.PASSED_RESPECTS_EP = test == "aware"
    pawns._value.cache_clear()
    return cgt.show(pawns.value(pawns.Board(files, 8, False, ep), pawns.Pos.parse(text)))


def codex_value(text, files, race, ep, test):
    g = cx.PawnGame(files, race, ep, test)
    w, b = cx.parse_position(text.replace(":", ""), files)
    return cx.show(g.value(w, b))


for text in POSITIONS:
    print(text, flush=True)
    for s in SETTINGS:
        t0 = time.time()
        a5, a8 = cyl_value(text, 5, *s), cyl_value(text, 8, *s)
        c5 = codex_value(text, 5, *s)
        tag = f"{s[0]}/{'off' if not s[1] else s[2]}"
        flag = "" if a5 == a8 == c5 else "   <-- DIFFER"
        print(f"  {tag:18s} cylcgt F5 {a5:14s} cylcgt F8 {a8:14s} codex F5 {c5:14s} ({time.time() - t0:.0f}s){flag}",
              flush=True)
