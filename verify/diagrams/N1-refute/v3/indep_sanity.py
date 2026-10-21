"""Sanity checks that engines (A) and (B) in indep_n1.py can tell the relevant values apart.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/N1-refute/v3/indep_sanity.py
"""
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_n1 as m  # noqa: E402  (my own file; nothing from cylcgt/crosscheck)


def run():
    R = m.Rules(True, True, "count", "passed", 256)
    tiny1 = m.canon([m.ZERO], [m.canon([m.ZERO], [m.INT(-1)])])
    tiny2 = m.canon([m.ZERO], [m.canon([m.ZERO], [m.INT(-2)])])
    up = m.canon([m.ZERO], [m.STAR])
    checks = []

    def chk(label, got, want):
        checks.append(got == want)
        print(f"{'ok ' if got == want else 'BAD'} {label}: got {got}, want {want}")

    W, B = m.parse("W: f4 / B: f5 f7")
    chk("A: W f4 / B f5 f7 = -1", m.eq(m.cgt_value(R, W, B), m.INT(-1)), True)
    chk("B: (W f4 / B f5 f7) + 1 is P", m.sum_outcome(R, W, B, m.TINT(1)), "P")
    W, B = m.parse("W: f4 / B: f6")
    chk("A: W f4 / B f6 = *", m.eq(m.cgt_value(R, W, B), m.STAR), True)
    chk("B: (W f4 / B f6) + * is P", m.sum_outcome(R, W, B, m.TSTAR), "P")
    W, B = m.parse("W: a4 h2 h4 / B: a5 a6 a7 h3")   # paper's Position 4.3 (cylinder), stated Tiny-1
    chk("A: Position 4.3 = tiny(1)", m.eq(m.cgt_value(R, W, B), tiny1), True)
    chk("B: Position 4.3 + miny(1) is P", m.sum_outcome(R, W, B, m.TMINY1), "P")
    E = frozenset()
    chk("B: 0 + miny(1) is R (test can fail)", m.sum_outcome(R, E, E, m.TMINY1), "R")
    chk("B: 0 + tiny(1) is L", m.sum_outcome(R, E, E, m.TTINY1), "L")
    chk("A: tiny(1) > tiny(2) > 0, tiny(1) < up",
        (m.le(tiny2, tiny1) and not m.le(tiny1, tiny2), m.le(m.ZERO, tiny2) and not m.le(tiny2, m.ZERO),
         m.le(tiny1, up) and not m.le(up, tiny1)), (True, True, True))
    W, B = m.parse("W: c1 c3 d3 / B: c2 d4 d5 d6")
    TMINY2 = m.T([m.T([m.TINT(2)], [m.T0])], [m.T0])
    chk("B: G + miny(2) is L (so the miny test separates tinies)", m.sum_outcome(R, W, B, TMINY2), "L")
    chk("B: G + down is R (G < up)", m.sum_outcome(R, W, B, m.TDOWN), "R")
    chk("B: G + (-1/2)... G + {-1|0}? skip; G + (-1) is R", m.sum_outcome(R, W, B, m.TINT(-1)), "R")
    print("all ok" if all(checks) else "SOME CHECK FAILED")


sys.setrecursionlimit(1_000_000)
threading.stack_size(1 << 29)
t = threading.Thread(target=run)
t.start()
t.join()
