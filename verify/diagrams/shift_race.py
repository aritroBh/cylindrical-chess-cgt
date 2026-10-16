"""Race-rule sensitivity of the shifted (legal) versions. Run: PYTHONPATH=. .venv/bin/python verify/diagrams/shift_race.py"""
from dataclasses import replace
from cylcgt import cgt, pawns
from cylcgt.pawns import CYL8, Pos, value
for text in ("W: a3 h2 / B: a4 h5", "W: c2 d3 / B: c5 d4", "W: a4 h2 / B: a5 h6", "W: a5 h2 / B: a6 h7", "W: c2 c4 d4 / B: c3 d5 d6 d7"):
    for b in (CYL8, replace(CYL8, ep=False)):
        out = []
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule; pawns._value.cache_clear(); pawns.race_hits.clear()
            out.append(f"{rule}={cgt.show(value(b, Pos.parse(text)))}[{len(pawns.race_hits)}]")
        print(f"{text:30s} ep={'on ' if b.ep else 'off'} " + "  ".join(out))
pawns.RACE_RULE = "count"
