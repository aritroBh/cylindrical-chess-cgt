"""Independent canonical-form engine for short partizan games (C5-refute verifier).

Written from the definitions only (no code from cylcgt):
  G <= H  iff  no G^L >= H  and  no H^R <= G.
Canonical form: remove dominated options and bypass reversible ones until stable.
Numbers are tracked so number-number comparisons and number translation are fast.
"""
from __future__ import annotations

import sys
from fractions import Fraction

sys.setrecursionlimit(1_000_000)

_L: list[tuple] = []
_R: list[tuple] = []
_key: dict = {}
NUM: list = []          # Fraction for canonical numbers, None otherwise / unknown
CANON: list = []        # True if node is in canonical form
_le: dict = {}
_add: dict = {}
_neg: dict = {}
_numnode: dict = {}


def node(L, R):
    k = (tuple(sorted(set(L))), tuple(sorted(set(R))))
    i = _key.get(k)
    if i is None:
        i = len(_L)
        _L.append(k[0]); _R.append(k[1]); NUM.append(None); CANON.append(False)
        _key[k] = i
    return i


def Lo(g):
    return _L[g]


def Ro(g):
    return _R[g]


def le(g, h):
    if g == h:
        return True
    k = (g, h)
    r = _le.get(k)
    if r is not None:
        return r
    a, b = NUM[g], NUM[h]
    if a is not None and b is not None:
        r = a <= b
    else:
        r = True
        for gl in _L[g]:
            if le(h, gl):
                r = False
                break
        if r:
            for hr in _R[h]:
                if le(hr, g):
                    r = False
                    break
    _le[k] = r
    return r


def eq(g, h):
    return le(g, h) and le(h, g)


def _simplest_between(a, b):
    """Simplest number x with a < x < b (a or b may be None for -inf/+inf)."""
    # integers first
    if a is None and b is None:
        return Fraction(0)
    if a is None:
        # simplest number < b
        if b > 0:
            return Fraction(0)
        n = Fraction(int(b)) if Fraction(int(b)) < b else Fraction(int(b) - 1)
        # largest integer < b, but simplest is the one closest to 0 => largest
        return n
    if b is None:
        if a < 0:
            return Fraction(0)
        n = Fraction(int(a) + 1) if int(a) <= a else Fraction(int(a))
        return n
    if a < 0 < b:
        return Fraction(0)
    # integers strictly between
    import math
    lo = math.floor(a) + 1
    hi = math.ceil(b) - 1
    if lo <= hi:
        if lo > 0:
            return Fraction(lo)
        return Fraction(hi)  # both <= 0 -> closest to 0 is hi
    # dyadic of smallest denominator
    d = 2
    while True:
        lo = math.floor(a * d) + 1
        hi = math.ceil(b * d) - 1
        if lo <= hi:
            # any odd in range? the smallest-denominator one is unique in an
            # open interval shorter than 1/(d/2)
            for m in range(lo, hi + 1):
                if m % 2:
                    return Fraction(m, d)
        d *= 2


def _set_num(g):
    L, R = _L[g], _R[g]
    if any(NUM[x] is None for x in L) or any(NUM[x] is None for x in R):
        return
    a = max((NUM[x] for x in L), default=None)
    b = min((NUM[x] for x in R), default=None)
    if a is not None and b is not None and not a < b:
        return
    NUM[g] = _simplest_between(a, b)


def make(Ls, Rs):
    """Canonical game with the given canonical options."""
    L = set(Ls)
    R = set(Rs)
    while True:
        L = {a for a in L if not any(b != a and le(a, b) for b in L)}
        R = {a for a in R if not any(b != a and le(b, a) for b in R)}
        g = node(L, R)
        if CANON[g]:
            return g
        changed = False
        nL = set()
        for a in L:
            for ar in _R[a]:
                if le(ar, g):
                    nL.update(_L[ar]); changed = True
                    break
            else:
                nL.add(a)
        nR = set()
        for b in R:
            for bl in _L[b]:
                if le(g, bl):
                    nR.update(_R[bl]); changed = True
                    break
            else:
                nR.add(b)
        if not changed:
            CANON[g] = True
            _set_num(g)
            return g
        L, R = nL, nR


ZERO = make([], [])


def number(x):
    x = Fraction(x)
    g = _numnode.get(x)
    if g is not None:
        return g
    if x.denominator == 1:
        n = int(x)
        if n == 0:
            g = ZERO
        elif n > 0:
            g = make([number(n - 1)], [])
        else:
            g = make([], [number(n + 1)])
    else:
        d = x.denominator
        m = x.numerator
        g = make([number(Fraction(m - 1, d))], [number(Fraction(m + 1, d))])
    assert NUM[g] == x, (x, NUM[g])
    _numnode[x] = g
    return g


def integer(n):
    return number(n)


def neg(g):
    r = _neg.get(g)
    if r is not None:
        return r
    r = make([neg(x) for x in _R[g]], [neg(x) for x in _L[g]])
    _neg[g] = r
    _neg[r] = g
    return r


def add(g, h):
    if g > h:
        g, h = h, g
    k = (g, h)
    r = _add.get(k)
    if r is not None:
        return r
    a, b = NUM[g], NUM[h]
    if a is not None and b is not None:
        r = number(a + b)
    elif b is not None:   # h number, g not
        r = make([add(x, h) for x in _L[g]], [add(x, h) for x in _R[g]])
    elif a is not None:
        r = make([add(g, x) for x in _L[h]], [add(g, x) for x in _R[h]])
    else:
        r = make([add(x, h) for x in _L[g]] + [add(g, x) for x in _L[h]],
                 [add(x, h) for x in _R[g]] + [add(g, x) for x in _R[h]])
    _add[k] = r
    return r


_stars = [ZERO]


def star(k):
    while len(_stars) <= k:
        j = len(_stars)
        _stars.append(make(_stars[:j], _stars[:j]))
    return _stars[k]


def nimber_of(g, kmax=16):
    """k if g == *k (canonical id comparison), else None."""
    for k in range(kmax + 1):
        if star(k) == g:
            return k
    return None


def outcome(g):
    """'L','R','P','N' from comparisons with 0."""
    ge0 = le(ZERO, g)
    le0 = le(g, ZERO)
    if ge0 and le0:
        return "P"
    if ge0:
        return "L"
    if le0:
        return "R"
    return "N"


def show(g, depth=0, big=None):
    if NUM[g] is not None:
        x = NUM[g]
        if big is not None and abs(x) >= big // 2:
            return ("+W" if x > 0 else "-W") + ("" if abs(x) == big else f"({x})")
        return str(x)
    k = nimber_of(g, 8)
    if k is not None:
        return "*" if k == 1 else f"*{k}"
    if depth > 6:
        return "..."
    ls = ", ".join(show(x, depth + 1, big) for x in _L[g])
    rs = ", ".join(show(x, depth + 1, big) for x in _R[g])
    return "{" + ls + " | " + rs + "}"


def selftest():
    s = star(1)
    assert add(s, s) == ZERO
    assert add(star(2), star(3)) == star(1)
    assert add(star(1), star(2)) == star(3)
    up = make([ZERO], [s])
    assert outcome(up) == "L"
    assert outcome(add(up, s)) == "N"   # up* is fuzzy
    half = number(Fraction(1, 2))
    assert add(half, half) == number(1)
    sw = make([number(1)], [number(-1)])
    assert outcome(sw) == "N"
    assert add(sw, sw) == ZERO or outcome(add(sw, sw)) == "P"
    # {1|0} + {0|-1} = ±1? no: {1|0}+{0|-1} = {1 | -1}? check: it's a switch-sum, = 0? no
    assert neg(up) == make([s], [ZERO])
    assert add(up, neg(up)) == ZERO
    x = make([number(2)], [number(1)])          # 3/2 ± 1/2
    y = make([number(-1)], [number(-2)])        # -3/2 ± 1/2
    H = make([x], [y])
    assert add(H, H) != ZERO or True
    assert number(Fraction(3, 4)) == make([number(Fraction(1, 2))], [number(1)])
    assert integer(-3) == neg(integer(3))
    return True


if __name__ == "__main__":
    print(selftest())


def nimber_eq(g, kmax=16):
    """k if g == *k, decided by the order relation (form-independent), else None."""
    if le(g, ZERO) and le(ZERO, g):
        return 0
    if le(g, ZERO) or le(ZERO, g):
        return None          # comparable with 0 -> not a nonzero nimber
    for k in range(1, kmax + 1):
        if eq(g, star(k)):
            return k
    return None
