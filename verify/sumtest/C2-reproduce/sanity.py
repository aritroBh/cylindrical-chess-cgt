"""Sanity checks of indep_nim.py on known one-file values."""
import sys
sys.path.insert(0, sys.argv[1])
from indep_nim import make_solver, parse, outcome

cases = [("W: a4 / B: a6", "* -> G+* must be P"),
         ("W: a4 / B: a5", "0 -> G must be P"),
         ("W: a2 / B: a5", "up -> G is L, G+* is N"),
         ("W: a3 / B: a6", "?")]
win = make_solver(1, False, True, "plain", "local", "count")
for pos, note in cases:
    W, B = parse(pos)
    print(pos, note, [outcome(win, W, B, h) for h in range(4)])
