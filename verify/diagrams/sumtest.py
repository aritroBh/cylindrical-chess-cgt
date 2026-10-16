"""Distinguish the paper's claimed sub-game values from the solver's values by sum tests,
using BOTH cylcgt (exact value -> outcome) and the independent crosscheck minimax (outcome only).
Test components on otherwise-empty files: MINUS1 = W y4 / B y5 y7 (value -1), STAR = W y4 / B y6 (value *).
Run: PYTHONPATH=. .venv/bin/python verify/diagrams/sumtest.py
"""
import sys
from dataclasses import replace
from cylcgt import cgt, pawns
from cylcgt.pawns import Pos, Board
from crosscheck.minimax import Board as XBoard, outcome_class, parse_position

sys.setrecursionlimit(100000)
CASES = [
    # label, position text, board(wrap), what each hypothesis predicts
    ("7.3{c,d} alone",          "W: c1 c3 d3 / B: c2 d4 d5 d6",              False, "1:L  tiny(1):L"),
    ("7.3{c,d} + (-1) [f-file]", "W: c1 c3 d3 f4 / B: c2 d4 d5 d6 f5 f7",    False, "1:P  tiny(1):R"),
    ("7.3{c,d} + * [f-file]",    "W: c1 c3 d3 f4 / B: c2 d4 d5 d6 f6",       False, "1:L  tiny(1):N"),
    ("(-1) alone [f-file]",      "W: f4 / B: f5 f7",                         False, "-1:R"),
    ("* alone [f-file]",         "W: f4 / B: f6",                            False, "*:N"),
    ("7.1{h,a} alone",           "W: a4 a5 h2 h3 / B: a7 h6",                True,  "1:L  {+W|*}:N (Right moves to *+*=0)"),
    ("7.1{h,a} + (-1) [d-file]", "W: a4 a5 h2 h3 d4 / B: a7 h6 d5 d7",       True,  "1:P  {+W|*}:N"),
    ("7.1{h,a} + * [d-file]",    "W: a4 a5 h2 h3 d4 / B: a7 h6 d6",          True,  "1:L  {+W|*}:N (Right moves to *+*=0)"),
]
for ep in (True, False):
    for label, text, wrap, pred in CASES:
        b = Board(8, 8, wrap, ep)
        pawns.RACE_RULE = "count"; pawns._value.cache_clear()
        p = Pos.parse(text)
        g = pawns.value(b, p)
        oc_cyl = cgt.outcome(g)
        safe = pawns.sum_safe(b, p)
        oc_x = outcome_class(XBoard(8, 8, wrap, ep), parse_position(text))
        print(f"ep={'on ' if ep else 'off'} {'cyl ' if wrap else 'flat'} {label:28s} cylcgt {oc_cyl} "
              f"(value {cgt.show(g)}, sum_safe {safe})  crosscheck {oc_x}   predictions: {pred}")
