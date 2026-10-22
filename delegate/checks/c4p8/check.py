"""cylcgt check of the C4 eight-pawn (4+4) *3 hits of the C scanner (research/star26_rings/fixed_rerun/
research/star26_rings/cyl_w4_p8_4_4.hits.tsv). For each hit row and each of the nine settings where the scanner reports a
nimber >= 2, recompute the value with cylcgt, in the sum model and with component splitting off.
Usage: .venv/bin/python delegate/checks/c4p8/check.py ROW SETTING MODE   (MODE = sum | nosplit)
Output: delegate/checks/c4p8/r{ROW}_s{SETTING}_{MODE}.txt"""
import sys, time
sys.path.insert(0, '.'); sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
SETTINGS = [("count", True, False), ("count", False, False), ("count", True, True),
            ("mover", True, False), ("mover", False, False), ("mover", True, True),
            ("opponent", True, False), ("opponent", False, False), ("opponent", True, True)]
NAMES = ["count/epon", "count/epoff", "count/epon/aware", "mover/epon", "mover/epoff", "mover/epon/aware",
         "opponent/epon", "opponent/epoff", "opponent/epon/aware"]
row, s, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rows = [l.rstrip("\n").split("\t") for l in open("research/star26_rings/cyl_w4_p8_4_4.hits.tsv")]
pos, scanner = rows[row][0], rows[row][3 + s]
race, ep, aware = SETTINGS[s]
pawns.RACE_RULE = race; pawns.PASSED_RESPECTS_EP = aware
if mode == "nosplit":
    pawns.components = lambda board, p: [p]
t = time.time()
v = cgt.show(pawns.value(pawns.Board(4, 8, True, ep), pawns.Pos.parse(pos)))
open(f"delegate/checks/c4p8/r{row}_s{s}_{mode}.txt", "w").write(
    f"{pos}\t{NAMES[s]}\tscanner={scanner}\tcylcgt_{mode}={v}\t{time.time()-t:.0f}s\n")
