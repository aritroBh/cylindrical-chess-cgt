"""C5-theory: what does '398 race nodes' count? race_hits gets one entry per (parent, move) edge into a
race position among distinct cached parents. Report edges, distinct (position, mover) and distinct positions.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C5-theory/race_count.py
"""
from cylcgt import cgt, pawns
for ep in (True, False):
    pawns.RACE_RULE = "count"; pawns._value.cache_clear(); pawns.race_hits.clear()
    g = pawns.value(pawns.Board(4, 8, False, ep), pawns.Pos.parse("W: a2 c2 / B: b7 d7"))
    hits = pawns.race_hits
    print(f"flat4 a2c2/b7d7 ep={ep}: value {cgt.show(g)}; race edges {len(hits)}, distinct (pos,mover) {len(set(hits))}, "
          f"distinct positions {len({h.rsplit(' after ',1)[0] for h in hits})}")
