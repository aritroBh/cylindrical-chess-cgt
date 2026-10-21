"""Independent minimal canonical-form CGT for the C3 refutation check.

Written from scratch (does not import cylcgt).  Numbers are leaf nodes that
carry an exact Fraction; their canonical options are produced lazily.
Non-number games are hash-consed canonical forms.  Equality == identity.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction

sys.setrecursionlimit(1_000_000)


class Node:
    __slots__ = ("id", "num", "L", "R", "nim", "_key", "_big")

    def __init__(self, nid, num, L, R):
        self.id = nid
        self.num = num
        self.L = L
        self.R = R
        self.nim = None
        self._key = None
        self._big = None


_next = [0]
_nums: dict = {}
_tab: dict = {}
_le: dict = {}
_add: dict = {}


def _new(num, L, R):
    _next[0] += 1
    return Node(_next[0], num, L, R)


def num(x) -> Node:
    x = Fraction(x)
    g = _nums.get(x)
    if g is None:
        g = _new(x, None, None)
        if x == 0:
            g.nim = 0
        _nums[x] = g
    return g


def _num_opts(x: Fraction):
    """canonical (left, right) options of the number x, as Fractions."""
    if x.denominator == 1:
        if x > 0:
            return [x - 1], []
        if x < 0:
            return [], [x + 1]
        return [], []
    d = x.denominator
    return [x - Fraction(1, d)], [x + Fraction(1, d)]


def Lo(g):
    if g.num is not None:
        return [num(y) for y in _num_opts(g.num)[0]]
    return g.L


def Ro(g):
    if g.num is not None:
        return [num(y) for y in _num_opts(g.num)[1]]
    return g.R


def le(a: Node, b: Node) -> bool:
    if a is b:
        return True
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    k = (a.id, b.id)
    r = _le.get(k)
    if r is None:
        r = (not any(le(b, x) for x in Lo(a))) and (not any(le(y, a) for y in Ro(b)))
        _le[k] = r
    return r


class _Temp:
    """A not-yet-canonical game {L | R} for reversibility tests (local memo)."""

    def __init__(self, L, R):
        self.L, self.R = L, R
        self.m1 = {}  # x.id -> x <= T
        self.m2 = {}  # x.id -> T <= x

    def x_le_T(self, x):
        r = self.m1.get(x.id)
        if r is None:
            # x <= T iff no T^R <= x and no x^L >= T
            r = (not any(le(tr, x) for tr in self.R)) and (not any(self.T_le_x(xl) for xl in Lo(x)))
            self.m1[x.id] = r
        return r

    def T_le_x(self, x):
        r = self.m2.get(x.id)
        if r is None:
            # T <= x iff no T^L >= x and no x^R <= T
            r = (not any(le(x, tl) for tl in self.L)) and (not any(self.x_le_T(xr) for xr in Ro(x)))
            self.m2[x.id] = r
        return r


def _dedupe(xs):
    seen = set()
    out = []
    for x in xs:
        if x.id not in seen:
            seen.add(x.id)
            out.append(x)
    return out


def _maxi(xs):
    xs = _dedupe(xs)
    return [x for x in xs if not any(y is not x and le(x, y) for y in xs)]


def _mini(xs):
    xs = _dedupe(xs)
    return [x for x in xs if not any(y is not x and le(y, x) for y in xs)]


def simplest(lo, hi):
    """simplest number strictly between lo and hi (None = unbounded)."""
    if lo is None and hi is None:
        return Fraction(0)
    if lo is None:
        return Fraction(0) if hi > 0 else Fraction(math.ceil(hi) - 1)
    if hi is None:
        return Fraction(0) if lo < 0 else Fraction(math.floor(lo) + 1)
    assert lo < hi
    if lo < 0 < hi:
        return Fraction(0)
    if lo >= 0:
        n = math.floor(lo) + 1
        if n < hi:
            return Fraction(n)
    else:  # hi <= 0
        n = math.ceil(hi) - 1
        if n > lo:
            return Fraction(n)
    d = 2
    while True:
        k = math.floor(lo * d) + 1
        if Fraction(k, d) < hi:
            return Fraction(k, d)
        d *= 2


def make(L, R) -> Node:
    L = list(L)
    R = list(R)
    while True:
        L = _maxi(L)
        R = _mini(R)
        T = _Temp(L, R)
        changed = False
        nL = []
        for a in L:
            rev = None
            for ar in Ro(a):
                if T.x_le_T(ar):
                    rev = ar
                    break
            if rev is None:
                nL.append(a)
            else:
                nL.extend(Lo(rev))
                changed = True
        nR = []
        for a in R:
            rev = None
            for al in Lo(a):
                if T.T_le_x(al):
                    rev = al
                    break
            if rev is None:
                nR.append(a)
            else:
                nR.extend(Ro(rev))
                changed = True
        if not changed:
            break
        L, R = nL, nR
    # number recognition (canonical form is unique)
    if all(x.num is not None for x in L) and all(x.num is not None for x in R):
        lo = max((x.num for x in L), default=None)
        hi = min((x.num for x in R), default=None)
        if lo is None or hi is None or lo < hi:
            return num(simplest(lo, hi))
    L = sorted(L, key=lambda g: g.id)
    R = sorted(R, key=lambda g: g.id)
    k = (tuple(g.id for g in L), tuple(g.id for g in R))
    g = _tab.get(k)
    if g is None:
        g = _new(None, tuple(L), tuple(R))
        if k[0] == k[1] and all(x.nim is not None for x in L):
            if sorted(x.nim for x in L) == list(range(len(L))):
                g.nim = len(L)
        _tab[k] = g
    return g


def add(a: Node, b: Node) -> Node:
    if a.num is not None and b.num is not None:
        return num(a.num + b.num)
    if a.num == 0:
        return b
    if b.num == 0:
        return a
    k = (a.id, b.id) if a.id < b.id else (b.id, a.id)
    r = _add.get(k)
    if r is not None:
        return r
    if a.num is not None:  # number translation
        r = make([add(a, x) for x in b.L], [add(a, x) for x in b.R])
    elif b.num is not None:
        r = make([add(x, b) for x in a.L], [add(x, b) for x in a.R])
    else:
        r = make([add(x, b) for x in a.L] + [add(a, x) for x in b.L],
                 [add(x, b) for x in a.R] + [add(a, x) for x in b.R])
    _add[k] = r
    return r


def neg(a: Node) -> Node:
    if a.num is not None:
        return num(-a.num)
    return make([neg(x) for x in a.R], [neg(x) for x in a.L])


def key(g: Node) -> str:
    """Same textual convention as the worker's vkey (numbers p or p/q, *k, {L|R} sorted)."""
    if g._key is not None:
        return g._key
    if g.num is not None:
        x = g.num
        r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
    g._key = r
    return r


def has_big(g: Node, big=256) -> bool:
    if g._big is not None:
        return g._big
    if g.num is not None:
        r = abs(g.num) >= big // 2
    else:
        r = any(has_big(x, big) for x in g.L + g.R)
    g._big = r
    return r
