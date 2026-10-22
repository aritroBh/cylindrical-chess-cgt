"""Third-program check of the 6 flat 5-file 8-pawn positions where T21's C scanner says *2 (count rule,
e.p. on, e.p.-aware test) but cylcgt does not.

Program: verify_ext/codex/solver.py (independent whole-board solver; game ends at the first passed pawn).
Usage: .venv/bin/python delegate/checks/w5_arbiter/arbiter.py INDEX  (0-5); output to w5_arbiter/out_INDEX.txt
"""
import sys, time
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'verify_ext/codex'); import solver as cx
POS = ["W: a2 b2 c2 d2 / B: a5 b4 d7 e4", "W: a2 b2 c2 e2 / B: a6 b4 d5 e3", "W: a4 b2 c3 e2 / B: a7 c6 d7 e5",
       "W: a4 b3 c3 e2 / B: a7 c6 d6 e5", "W: a5 b2 d5 e4 / B: b7 c7 d7 e7", "W: a6 b4 d5 e3 / B: a7 c7 d7 e7"]
i = int(sys.argv[1]); text = POS[i]; t = time.time()
g = cx.PawnGame(5, "count", True, "aware"); w, b = cx.parse_position(text.replace(":", ""), 5)
v = cx.show(g.value(w, b))
open(f"delegate/checks/w5_arbiter/out_{i}.txt", "w").write(f"{text}\tcodex(count,ep,aware)={v}\t{time.time()-t:.0f}s\n")
