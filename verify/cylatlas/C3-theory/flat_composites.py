"""Whole-board check that four of C3's 'cylinder-only' headline values occur on a FLAT 8-file strip
once more than 5 pawns are allowed (two components separated by an empty file).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C3-theory/flat_composites.py

(i)  cylcgt.pawns.value on the flat 8x8 board (sum of component values; textbook passed test)
(ii) sumtest whole-board tree (independent move generator, NO decomposition) + cylcgt.cgt canonical form,
     plus the brute-force outcome vector against 15 reference games (whole-board mode).
"""
import sys
sys.setrecursionlimit(100000)
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from sumtest import aware_value
sys.path.insert(0, "verify/cylatlas/C3-theory")
from cgtkey import key

cases = [
    ("3/4", "W: a2 b4 / B: b7 c6 (3-file cyl)", "W: a2 a3 c2 d4 / B: a6 c7 e6 e7"),
    ("-3/4", "W: a2 b3 / B: a5 c7 (3-file cyl)", "W: a2 c2 c3 e2 / B: a3 a5 d5 e7"),
    ("1/4±1/4", "W: a2 b2 / B: c5 c6 (3-file cyl)", "W: a2 a3 c3 f4 / B: a6 d7 e6 e7"),
    ("{3/2±1/2 | -3/2±1/2}", "W: a2 c2 / B: b7 d7 (4-file cyl)", "W: a2 c2 e3 / B: a4 a5 d6 d7"),
]
aware = "--aware" in sys.argv
for name, cylwit, flatpos in cases:
    b = Board(8, 8, False, True)
    g = pawns.value(b, Pos.parse(flatpos))
    v, brute, pred = aware_value.value(flatpos, 8, False, ep=True, aware=aware, race_rule="count")
    print(f"{name:24s} cyl witness {cylwit:34s} flat 8x8 {flatpos:36s} "
          f"sum-model={cgt.show(g):22s} whole-board={cgt.show(v):22s} same={key(g)==key(v)} brute==pred={brute==pred}", flush=True)
