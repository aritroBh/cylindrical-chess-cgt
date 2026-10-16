"""Outcome class of selected positions under each race rule, e.p. on/off (8x8 cylinder).
Run: PYTHONPATH=. .venv/bin/python verify/diagrams/race72.py
"""
from dataclasses import replace
from cylcgt import cgt, pawns
from cylcgt.pawns import CYL8, Pos, value
for text in ("W: a2 b2 h3 / B: a6 b7 h7", "W: a3 h1 / B: a4 h5", "W: a4 h1 / B: a5 h6", "W: a4 a5 h2 h3 / B: a7 h6"):
    for b in (CYL8, replace(CYL8, ep=False)):
        row = []
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule; pawns._value.cache_clear(); pawns.race_hits.clear()
            g = value(b, Pos.parse(text))
            row.append(f"{rule}: {cgt.outcome(g)} (race nodes {len(pawns.race_hits)})")
        print(f"{text:28s} ep={'on ' if b.ep else 'off'}  " + " | ".join(row))
pawns.RACE_RULE = "count"; pawns._value.cache_clear()
