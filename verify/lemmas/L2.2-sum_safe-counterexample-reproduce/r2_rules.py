"""Headline position under all three race rules, independent code.
cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-reproduce/r2_rules.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2_indep import Game, parse
x = parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
for ep in (False, True):
    for rule in ("count", "mover", "opponent"):
        g = Game(8, 8, True, ep, rule)
        print(f"8x8 cyl ep={'on' if ep else 'off'} {rule:8s}: o(S)={g.S_outcome(x)} o(W)={g.W_outcome(x)}", flush=True)
