"""Sanity checks of indep_tiny.py on single-file positions whose values are easy by hand.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/N1-reproduce/indep_sanity.py
"""
import sys
sys.path.insert(0, "verify/diagrams/N1-reproduce")
import indep_tiny as T
T.CFG.update(wrap=False, ep=True, race="count")
cases = [("W: e4 / B: e5", "0"), ("W: e4 / B: e6", "*"), ("W: e3 / B: e6", "0"), ("W: f4 / B: f5 f7", "-1"),
         ("W: f4 / B: f6", "*"), ("W: e4 / B: e7", "?")]
C = dict(T.CANDIDATES, **{"-1": T.MONE, "1": T.ONE})
for pos, hand in cases:
    T.reset()
    g = T.pawnnode(T.parse(pos))
    print(f"{pos:22s} hand {hand:3s} indep equals {[k for k, v in C.items() if T.eq(g, v)]}  outcome {T.outcome(g)}")
