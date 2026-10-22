"""Reproduce every computational claim used by the K1a edits.

    cd /Users/aritro/Downloads/Research/Chessendgames
    PYTHONPATH=. .venv/bin/python kings/delegate/out/K1a/verify.py

Labels: every line below is COMPUTED-1 (one implementation) unless the note says otherwise.
"""
from __future__ import annotations

from cylcgt import cgt
from cylcgt.pawns import Board, Pos
import lemmas.common as C

print("1) Proposition 1.13 with A' = { | -B}, B = 4, n = 0..7  (expect R R R R R P L L)")
print("   ", [cgt.outcome(cgt.total([cgt.make([], [cgt.integer(-4)]), cgt.integer(n)])) for n in range(8)])

print("2) the same with A' = {0 | -B} (the dead-position reading)  (expect N N N N N L L L)")
print("   ", [cgt.outcome(cgt.total([cgt.make([cgt.integer(0)], [cgt.integer(-4)]), cgt.integer(n)])) for n in range(8)])

print("3) frontier of the R1/R2 counterexample: B + { | -B}  (expect -1 and R for every B)")
for B in (2, 3, 4, 10, 100):
    p = cgt.add(cgt.integer(B), cgt.make([], [cgt.integer(-B)]))
    print(f"    B={B:4d} {cgt.show(p):>4s} {cgt.outcome(p)}")

print("4) Proposition 1.12 BIG part: {B|0} + {0|-B}  (expect 0, i.e. 0, for every B)")
for B in (1, 2, 4, 8):
    p = cgt.add(cgt.make([cgt.integer(B)], [cgt.integer(0)]), cgt.make([cgt.integer(0)], [cgt.integer(-B)]))
    print(f"    B={B} {cgt.show(p)}  is 0: {p == cgt.integer(0)}  outcome {cgt.outcome(p)}")

print("5) canonical forms: integer B = {B-1 | }, integer -B = { | -B+1}")
for B in (1, 2, 4, 256):
    print(f"    B={B:4d} {cgt.make([cgt.integer(B-1)], []) == cgt.integer(B)} "
          f"{cgt.make([], [cgt.integer(1-B)]) == cgt.integer(-B)}")

print("6) R2 item 2: flat 7x6, e.p. on, count rule, W: b2 d3 f2 / B: c4 c5 e5 g5")
b = Board(7, 6, False, True)
p = Pos.parse("W: b2 d3 f2 / B: c4 c5 e5 g5")
print("    components at the root:", len(__import__("cylcgt.pawns", fromlist=["x"]).components(b, p)))
print("    o(S) =", cgt.outcome(C.S(b, p, "count")), " o(W) =", cgt.outcome(C.W(b, p, "count")),
      " HSS:", C.hereditarily_safe(b, p))
