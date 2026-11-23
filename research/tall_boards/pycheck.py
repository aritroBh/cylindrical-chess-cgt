#!/usr/bin/env python3
"""Validation 3: evaluate positions with cylcgt (whole-board).  usage (project root, PYTHONPATH=.): pycheck.py F wrap R "W: .. / B: .."  -> signature, value"""
import sys
from cylcgt import pawns, cgt
sys.setrecursionlimit(1000000)
pawns.components = lambda bd, p: [p]
F, wrap, R, text = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
b = pawns.Board(F, R, bool(wrap), True); g = pawns.value(b, pawns.Pos.parse(text))
print(text, "|", "".join(cgt.outcome(cgt.add(g, cgt.nimber(h))) for h in range(8)), "|", cgt.show(g)[:60])
