"""Literal options of 3.1 and 3.2 (cylinder 8x8, race rule 'count'). Run: PYTHONPATH=. .venv/bin/python verify/diagrams/options2.py"""
from dataclasses import replace
from cylcgt import cgt, pawns
from cylcgt.pawns import CYL8, Pos, moves, value
for text in ("W: a3 h1 / B: a4 h5", "W: a4 h1 / B: a5 h6"):
    for b in (CYL8, replace(CYL8, ep=False)):
        p = Pos.parse(text); pawns._value.cache_clear()
        L = [(str(q), cgt.show(pawns._child(b, q, "W"))) for q in moves(b, p, "W")]
        R = [(str(q), cgt.show(pawns._child(b, q, "B"))) for q in moves(b, p, "B")]
        print(f"{text} ep={'on ' if b.ep else 'off'} value {cgt.show(value(b, p))}\n   Left: {L}\n   Right: {R}")
