"""cylcgt check of C7 ten-pawn ring *2 hits from the C scanner (default setting: count, e.p. on, e.p.-aware).
Usage: .venv/bin/python delegate/checks/c7p10/check.py "POSITION" TAG MODE   (MODE = sum | nosplit)
Output: delegate/checks/c7p10/TAG_MODE.txt"""
import sys, time
sys.path.insert(0, '.'); sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
pos, tag, mode = sys.argv[1], sys.argv[2], sys.argv[3]
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
if mode == "nosplit":
    pawns.components = lambda board, p: [p]
t = time.time()
v = cgt.show(pawns.value(pawns.Board(7, 8, True, True), pawns.Pos.parse(pos)))
open(f"delegate/checks/c7p10/{tag}_{mode}.txt", "w").write(f"{pos}\tC7 cylcgt_{mode}(count,ep,aware)={v}\t{time.time()-t:.0f}s\n")
