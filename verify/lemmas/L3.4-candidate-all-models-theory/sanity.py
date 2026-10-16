"""Sanity checks of indep.py against values in notes/audit.md (8x8 cylinder, e.p. on)."""
import sys; sys.path.insert(0, ".")
from indep import *
bd = Bd(8, 8, True, True)
print("4.1 e4/e6 (audit: *):  o(G+*) =", outcome(bd, parse("W: e4 / B: e6"), STAR, "count"), " o(G) =", outcome(bd, parse("W: e4 / B: e6"), ZERO, "count"))
print("4.2' e2/e5 (audit: up): o(G+down) =", outcome(bd, parse("W: e2 / B: e5"), DOWN, "count"), " o(G+*) =", outcome(bd, parse("W: e2 / B: e5"), STAR, "count"))
print("2.1 e4/e5 (audit: 0):  o(G) =", outcome(bd, parse("W: e4 / B: e5"), ZERO, "count"))
