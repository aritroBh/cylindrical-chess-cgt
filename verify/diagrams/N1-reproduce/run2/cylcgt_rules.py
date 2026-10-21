"""cylcgt value of the 7.3 {c,d} sub-game under every race rule / board / e.p. setting, cache cleared each time,
with race-hit counts and the exact (undisplayed) number inside the c3-c4 option.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/N1-reproduce/run2/cylcgt_rules.py
"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, value
T = cgt.make([cgt.integer(0)], [cgt.make([cgt.integer(0)], [cgt.integer(-1)])])  # {0||0|-1}
for wrap in (True, False):
    for ep in (True, False):
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule; pawns._value.cache_clear(); pawns.race_hits.clear()
            b = Board(8, 8, wrap, ep)
            g = value(b, Pos.parse("W: c1 c3 d3 / B: c2 d4 d5 d6"))
            c4 = value(b, Pos.parse("W: c1 c4 d3 / B: c2 d4 d5 d6"))
            exact = [(str(x.num) if x.num is not None else cgt.show(x)) for x in c4.R]
            inner = [[str(y.num) for y in x.L] for x in c4.R]
            print(f"wrap={wrap!s:5} ep={ep!s:5} rule={rule:8s} value {cgt.show(g):8s} is-{{0||0|-1}} {g is T}  "
                  f"race_hits {len(pawns.race_hits)}  c3-c4 option {cgt.show(c4)} : R-options {exact}, their L-options {inner}")
pawns.RACE_RULE = "count"; pawns._value.cache_clear()
