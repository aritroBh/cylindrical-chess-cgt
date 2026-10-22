import pytest
from fractions import Fraction
import canon
from canon import (ZERO, STAR, UP, DOWN, make, add, neg, le, number, nimber,
                   clear_caches, show)


def test_star_star_zero():
    assert add(STAR, STAR) is ZERO


def test_up_down_zero():
    assert add(UP, DOWN) is ZERO


def test_half_half_one():
    h = number(Fraction(1, 2))
    assert add(h, h) is number(1)


def test_star2():
    s2 = make([ZERO, STAR], [ZERO, STAR])
    assert show(s2) == "*2"
    assert add(s2, s2) is ZERO


def test_up_star_fuzzy_zero():
    g = add(UP, STAR)
    assert not le(g, ZERO) and not le(ZERO, g)


def test_up2():
    ds = canon.down_star()
    up2 = make([ZERO], [ds])
    assert le(ZERO, up2) and not le(up2, ZERO)
    assert le(up2, UP) and not le(UP, up2)


def test_up2_plus_star():
    ds = canon.down_star()
    up2 = make([ZERO], [ds])
    g = add(up2, STAR)
    assert show(g) == "{0, * | ↓}"


def test_tiny1():
    tiny = make([ZERO], [make([ZERO], [canon.integer(-1)])])
    assert le(ZERO, tiny) and not le(tiny, ZERO)
    up2 = make([ZERO], [canon.down_star()])
    print("tiny vs UP: le(tiny,UP)=", le(tiny, UP), "le(UP,tiny)=", le(UP, tiny))
    print("tiny vs up2: le(tiny,up2)=", le(tiny, up2), "le(up2,tiny)=", le(up2, tiny))


def test_one_eighth():
    a = number(Fraction(1, 8))
    b = make([ZERO], [number(Fraction(1, 4))])
    assert a is b


def test_G_self_neg():
    inner = make([canon.number(1)], [canon.number(-1)])
    G = make([canon.number(2) + inner], [canon.number(-2) + inner])
    assert le(G, neg(G)) and le(neg(G), G)
    assert add(G, G) is ZERO
