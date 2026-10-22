#!/usr/bin/env python3
"""T27: split every hit into independent components (empty files) and print component values
under count/e.p. off, mover/e.p. off, mover/e.p. on-textbook and count/e.p. on-aware.
Run (project root): PYTHONPATH=. .venv/bin/python research/star27_textbook3/decompose.py
"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, components, value

SET = [("count/off", "count", False, False), ("mover/off", "mover", False, False),
       ("mover/T", "mover", True, False), ("count/aware", "count", True, True)]
for line in open("research/star27_textbook3/hit_positions.txt"):
    text = line.strip()
    pos = Pos.parse(text)
    print(text)
    for name, rule, ep, aware in SET:
        pawns.RACE_RULE, pawns.PASSED_RESPECTS_EP = rule, aware
        pawns._value.cache_clear()
        b = Board(6, 8, False, ep)
        comps = components(b, pos)
        parts = [f"[{c}] = {cgt.show(value(b, c))}" for c in comps]
        s = "  ;  ".join(p[:90] for p in parts)
        print(f"   {name:12s} total {cgt.show(value(b, pos))[:40]:40s} | {len(comps)} comp: {s}")
