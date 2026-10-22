#!/usr/bin/env python3
"""check_SR_rows.py : rows where variant S and variant R of the scanner differ -- who agrees with the whole-board cylcgt game
(pawns.components = lambda b,p:[p], real-chess e.p. expiry) and with the Codex whole-board solver?"""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex")); sys.path.insert(0, os.path.dirname(__file__))
import solver as cx
from common import *
rows = [("W: a5 d2 e2 / B: a7 b6 d4", "S=R,-1  R=N,-1"), ("W: a5 d2 e2 / B: a7 b6 e4", "S=R,-1  R=N,-1"), ("W: a5 d2 e3 / B: a7 b7 d4", "S=L,-1  R=N,-1"),
        ("W: a5 d3 e2 / B: a7 b7 e4", "S=L,-1  R=N,-1"), ("W: b5 d2 e2 / B: a6 b7 d4", "S=R,-1  R=N,-1")]
for text, note in rows:
    W, B = parse_pos(text); width = max(f for f, _ in W + B) + 1
    saved = pawns.components; pawns.components = lambda b, p: [p]; pawns._value.cache_clear()
    gw = pawns.value(pawns.Board(width, 8, False, True), pawns.Pos(frozenset(W), frozenset(B)))
    pawns.components = saved; pawns._value.cache_clear()
    gs = pawns.value(pawns.Board(width, 8, False, True), pawns.Pos(frozenset(W), frozenset(B)))
    pg = cx.PawnGame(width, "count", True, "aware"); st = cx.parse_position(text.replace(":", ""), width)
    lm, rm = pg._outcome_masks(st[0], st[1])
    lf, rf = bool(lm & 1), bool(rm & 1); oc = "N" if lf and rf else "L" if lf else "R" if rf else "P"
    print(f"{text}   scanner: {note}   cylcgt whole-board: {outcome_nim(gw)}   cylcgt sum model: {outcome_nim(gs)}   codex whole-board (bitmask): {oc}", flush=True)
