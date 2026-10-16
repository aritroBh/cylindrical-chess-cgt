from fractions import Fraction as F

from cylcgt import cgt
from cylcgt.cgt import ZERO, STAR, UP, DOWN, make, number, nimber, add, neg, show, outcome


def test_numbers():
    assert show(number(F(3, 4))) == "3/4"
    assert add(number(F(1, 2)), number(F(1, 2))) is number(1)
    assert make([number(0)], [number(1)]) is number(F(1, 2))
    assert make([number(-1)], []) is ZERO          # {-1|} = 0
    assert make([number(1)], [number(5)]) is number(2)


def test_nimbers_and_ups():
    assert add(STAR, STAR) is ZERO
    assert add(nimber(2), nimber(3)) is STAR
    assert show(make([ZERO, STAR], [STAR])) == "↑"        # * reversible
    assert show(add(UP, STAR)) == "↑*"
    assert show(add(add(UP, UP), STAR)) == "⇑*"
    assert UP > ZERO and outcome(UP) == "L"
    assert outcome(add(UP, STAR)) == "N"
    assert outcome(STAR) == "N" and outcome(ZERO) == "P"
    assert add(UP, DOWN) is ZERO


def test_switches_and_tiny():
    pm1 = make([number(1)], [number(-1)])
    assert show(pm1) == "±1"
    assert add(pm1, pm1) is ZERO
    tiny2 = make([ZERO], [make([ZERO], [number(-2)])])
    assert show(tiny2) == "tiny(2)"
    assert ZERO < tiny2 < UP


def test_thermographs():
    pm1 = make([number(1)], [number(-1)])
    assert cgt.mean(pm1) == 0 and cgt.temperature(pm1) == 1
    g = make([make([number(2)], [number(1)])], [ZERO])   # {{2|1}|0}
    assert cgt.mean(g) == F(3, 4) and cgt.temperature(g) == F(3, 4)
    assert cgt.temperature(UP) == 0 and cgt.mean(UP) == 0
    assert cgt.temperature(STAR) == 0
