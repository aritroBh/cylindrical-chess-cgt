"""Explain the 6 five-file positions where cylcgt (sum model) is not *2 but the C scanner and the whole-board
solver are: rerun cylcgt with component splitting switched off (whole-board game), count rule, e.p.-aware.
Usage: .venv/bin/python delegate/checks/w5_arbiter/nosplit.py INDEX   -> w5_arbiter/nosplit_INDEX.txt"""
import sys, time
sys.path.insert(0, '.'); sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
pawns.components = lambda board, pos: [pos]          # whole-board game: no splitting
POS = ["W: a2 b2 c2 d2 / B: a5 b4 d7 e4", "W: a2 b2 c2 e2 / B: a6 b4 d5 e3", "W: a4 b2 c3 e2 / B: a7 c6 d7 e5",
       "W: a4 b3 c3 e2 / B: a7 c6 d6 e5", "W: a5 b2 d5 e4 / B: b7 c7 d7 e7", "W: a6 b4 d5 e3 / B: a7 c7 d7 e7"]
i = int(sys.argv[1]); t = time.time()
v = cgt.show(pawns.value(pawns.Board(5, 8, False, True), pawns.Pos.parse(POS[i])))
open(f"delegate/checks/w5_arbiter/nosplit_{i}.txt", "w").write(f"{POS[i]}\tcylcgt_nosplit(count,ep,aware)={v}\t{time.time()-t:.0f}s\n")
