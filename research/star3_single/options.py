#!/usr/bin/env python3
"""options.py WIDTH "W: ... / B: ..." : value (cylcgt, default setting) of every option of a flat-board position."""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT); sys.setrecursionlimit(1000000)
from cylcgt import pawns, cgt
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
b = pawns.Board(int(sys.argv[1]), 8, False, True)
p = pawns.Pos.parse(sys.argv[2])
print("root", cgt.show(pawns.value(b, p)))
for side in "WB":
    for q in pawns.moves(b, p, side):
        v = pawns._child(b, q, side)
        print(f"{side} -> {q}\t{cgt.outcome(v)}\t{cgt.show(v)[:140]}")
