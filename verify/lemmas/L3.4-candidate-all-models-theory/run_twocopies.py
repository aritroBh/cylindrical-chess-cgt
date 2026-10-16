"""Whole-board convention game (first passer anywhere ends the game; race rule
on the whole board; global e.p.) for TWO copies of the candidate, separated by
an empty file, on a flat 9-file 8-rank board.  The sum model predicts
*2 + *2 = 0, i.e. outcome P.  Also: one copy + a single dead file pair etc.
Run: python3 run_twocopies.py"""
import sys, time
sys.path.insert(0, ".")
from indep import *

cases = {
    "X + X (same colours, files a-d and f-i)": "W: a2 c2 f2 h2 / B: b7 d7 g7 i7",
    "X + X' (X' = colour-reversed copy on f-i)": "W: a2 c2 g2 i2 / B: b7 d7 f7 h7",
}
for name, txt in cases.items():
    for ep in (True, False):
        bd = Bd(9, 8, False, ep)
        p = parse(txt)
        for rule in ("count", "mover", "opponent"):
            t0 = time.time()
            o = whole_board_outcome(bd, p, rule)
            print(f"{name}; ep={ep}; rule={rule}: whole-board outcome {o}  (sum-model prediction: "
                  f"{'P' if rule != 'opponent' else 'P (0+0)'}) [{time.time()-t0:.1f}s]", flush=True)
