"""Sanity tests of my own CGT engine and pawn model (c4check.py).
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C4-refute/selftest.py
"""
import os, sys, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4check import *  # noqa

def main():
    I = integer
    s, s2 = star(), nim(2)
    up = canon([ZERO], [s]); down = neg(up)
    half = canon([ZERO], [I(1)])
    checks = {
        "*+*=0": add(s, s) == ZERO,
        "*2+*2=0": add(s2, s2) == ZERO,
        "*+*2=*3": add(s, s2) == nim(3),
        "up+down=0": add(up, down) == ZERO,
        "1/2+1/2=1": add(half, half) == I(1),
        "+-1 + +-1 = 0": add(sw(I(1), I(-1)), sw(I(1), I(-1))) == ZERO,
        "{0,*|0,*} canonical = *2": canon([ZERO, s], [ZERO, s]) == s2,
        "{1|0} not number": number_value(sw(I(1), ZERO)) is None,
        "3 + (-3) = 0": add(I(3), I(-3)) == ZERO,
        "256 + (-255) = 1": add(I(256), I(-255)) == I(1),
        "up* = {0,*|0}": add(up, s) == canon([ZERO, s], [ZERO]),
        "outcome(up)=L": outcome(up) == "L",
        "outcome(*2)=N": outcome(s2) == "N",
        "-2+-1 + 2+-1 = 0": add(sw(I(-1), I(-3)), sw(I(3), I(1))) == ZERO,
    }
    m = Model(1, 8, False, ep=True)
    W, B = parse("W: a4 / B: a6"); checks["1-file a4/a6 = *"] = m.value((W, B, None)) == s
    W, B = parse("W: a2 / B: a5"); checks["1-file a2/a5 = up"] = m.value((W, B, None)) == up
    m3 = Model(3, 8, False, ep=True)
    W, B = parse("W: a2 / B: b3"); checks["W a2/B b3 decided: a2xb3 or b3xa2"] = \
        m3.resolve((W, B, None), "W") is None
    for k, v in checks.items():
        print(("PASS " if v else "FAIL ") + k)

threading.stack_size(1 << 29)
t = threading.Thread(target=main); t.start(); t.join()
