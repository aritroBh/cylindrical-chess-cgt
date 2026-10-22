"""cylcgt check of the C6 nine-pawn ring *2 hits from the C scanner (default setting: count, e.p. on, e.p.-aware).
Usage: .venv/bin/python delegate/checks/c6_star2_check.py INDEX -> delegate/checks/c6_star2_INDEX.txt"""
import sys, time
sys.path.insert(0, '.'); sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
POS = ["W: a4 c4 d2 e2 / B: b6 b7 d6 e5 f6", "W: a5 b3 d4 e2 / B: c6 d7 e6 e7 f7", "W: a5 c4 d4 e3 / B: b7 d7 e4 e6 f7"]
i = int(sys.argv[1]); t = time.time()
v = cgt.show(pawns.value(pawns.Board(6, 8, True, True), pawns.Pos.parse(POS[i])))
open(f"delegate/checks/c6_star2_{i}.txt", "w").write(f"{POS[i]}\tC6 cylcgt(count,ep,aware)={v}\t{time.time()-t:.0f}s\n")
