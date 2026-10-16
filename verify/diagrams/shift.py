"""Rank-1 white pawns are illegal in chess. Shift each such diagram up one rank (all pawns +1)
to get a legal placement, and see whether the value survives. Cylinder 8x8, race rule 'count', e.p. on/off.
Run: PYTHONPATH=. .venv/bin/python verify/diagrams/shift.py
"""
from dataclasses import replace
from cylcgt import cgt, pawns
from cylcgt.pawns import CYL8, Pos, value

def up(p, k=1):
    return Pos(frozenset((f, r + k) for f, r in p.white), frozenset((f, r + k) for f, r in p.black))

for label, text, claim in [
    ("2.2", "W: a2 h1 / B: a3 h4", "0"),
    ("2.3", "W: c1 d2 / B: c4 d3", "0"),
    ("3.1", "W: a3 h1 / B: a4 h5", "1"),
    ("3.2", "W: a4 h1 / B: a5 h6", "2"),
    ("7.3{c,d}", "W: c1 c3 d3 / B: c2 d4 d5 d6", "1"),
]:
    p = Pos.parse(text)
    for b in (CYL8, replace(CYL8, ep=False)):
        pawns.RACE_RULE = "count"; pawns._value.cache_clear()
        v0 = cgt.show(value(b, p)); v1 = cgt.show(value(b, up(p)))
        print(f"{label:9s} ep={'on ' if b.ep else 'off'} claim {claim}: as drawn {v0:10s} shifted up one rank ({up(p)}) -> {v1}")
