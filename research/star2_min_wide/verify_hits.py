#!/usr/bin/env python3
"""Verify the *2 hits of the scans with (1) cylcgt (default setting), on a 4-file and on an 8-file flat board, with the
component split and as a whole-board game (pawns.components = lambda b,p:[p]); (2) the independent Codex whole-board solver
verify_ext/codex/solver.py (PawnGame(width,'count',True,'aware')); (3) the colour-reversal and mirror twins.
Run from the project root:  PYTHONPATH=. .venv/bin/python research/star2_min_wide/verify_hits.py"""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
sys.path.insert(0, os.path.dirname(__file__))
import solver as cx
from common import *

HITS = ["W: a4 b3 d2 d3 / B: a7 b7 c5", "W: b4 c2 d2 / B: a6 a7 c6 d5"]

def colour_reverse(text, width):
    W, B = parse_pos(text)
    return pos_text([(f, 9 - r) for f, r in B], [(f, 9 - r) for f, r in W])
def mirror(text, width):
    W, B = parse_pos(text)
    return pos_text([(width - 1 - f, r) for f, r in W], [(width - 1 - f, r) for f, r in B])

def cyl(text, files, whole):
    saved = pawns.components
    if whole: pawns.components = lambda b, p: [p]
    pawns._value.cache_clear()
    try:
        return pawns.value(pawns.Board(files, 8, False, True), pawns.Pos.parse(text))
    finally:
        pawns.components = saved; pawns._value.cache_clear()

for h in HITS:
    print(h, "   colour-reversal:", colour_reverse(h, 4), "   mirror:", mirror(h, 4))
    for files in (4, 8):
        for whole in (False, True):
            g = cyl(h, files, whole)
            print(f"  cylcgt files={files} {'whole-board' if whole else 'components '}: {cgt.show(g)}  nim={g.nim}  outcome={cgt.outcome(g)}")
    cg = cx.PawnGame(4, "count", True, "aware").value(*cx.parse_position(h.replace(":", ""), 4))
    print(f"  codex  width=4 count/e.p./aware: {cx.show(cg)}  nimber={cx.as_nimber(cg)}")
    pg = cx.PawnGame(4, "count", True, "aware"); st = cx.parse_position(h.replace(":", ""), 4); lm, rm = pg._outcome_masks(*st)
    print("  codex bitmask test (no canonicalisation): G+*k is a second-player win exactly for k =", [k for k in range(293) if not (lm >> k) & 1 and not (rm >> k) & 1])
    for twin in (colour_reverse(h, 4), mirror(h, 4), mirror(colour_reverse(h, 4), 4)):
        g = cyl(twin, 4, False)
        cg = cx.PawnGame(4, "count", True, "aware").value(*cx.parse_position(twin.replace(":", ""), 4))
        print(f"  twin {twin}: cylcgt {cgt.show(g)} / codex {cx.show(cg)} nimber={cx.as_nimber(cg)}")
