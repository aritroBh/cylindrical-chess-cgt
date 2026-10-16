"""Exact short-game combinatorial game theory (Conway / Berlekamp-Conway-Guy).

Every game is stored in canonical form and hash-consed, so two games are equal
iff they are the same Python object. Supports comparison, negation, sums,
recognition of numbers / nimbers / ups / tinies / switches, and thermographs
(mean value and temperature).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import count

sys.setrecursionlimit(1_000_000)

_ids = count()
_table: dict[tuple, "Game"] = {}
_le_memo: dict[tuple[int, int], bool] = {}
_add_memo: dict[tuple[int, int], "Game"] = {}
_neg_memo: dict[int, "Game"] = {}


class Game:
    __slots__ = ("L", "R", "id", "num", "nim", "_thermo")

    def __init__(self, L, R):
        self.L = tuple(L)
        self.R = tuple(R)
        self.id = next(_ids)
        self.num = None  # Fraction if this canonical game is a number
        self.nim = None  # n if this canonical game is *n
        self._thermo = None

    # ordering -------------------------------------------------------------
    def __le__(self, other):
        return le(self, other)

    def __ge__(self, other):
        return le(other, self)

    def __lt__(self, other):
        return le(self, other) and not le(other, self)

    def __gt__(self, other):
        return le(other, self) and not le(self, other)

    def fuzzy(self, other):
        return not le(self, other) and not le(other, self)

    def __add__(self, other):
        return add(self, other)

    def __neg__(self):
        return neg(self)

    def __sub__(self, other):
        return add(self, neg(other))

    def __repr__(self):
        return show(self)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self is other


def le(a: Game, b: Game) -> bool:
    """a <= b  iff  no a^L >= b  and  no b^R <= a."""
    if a is b:
        return True
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    key = (a.id, b.id)
    r = _le_memo.get(key)
    if r is None:
        r = not any(le(b, al) for al in a.L) and not any(le(br, a) for br in b.R)
        _le_memo[key] = r
    return r


def _dedupe(xs):
    seen, out = set(), []
    for x in xs:
        if x.id not in seen:
            seen.add(x.id)
            out.append(x)
    return out


def _maximal(xs):
    xs = _dedupe(xs)
    return [x for x in xs if not any(y is not x and le(x, y) for y in xs)]


def _minimal(xs):
    xs = _dedupe(xs)
    return [x for x in xs if not any(y is not x and le(y, x) for y in xs)]


def _simplest_between(lo, hi):
    """Simplest number strictly between lo and hi (None = unbounded)."""
    if lo is None and hi is None:
        return Fraction(0)
    if lo is None:  # simplest x < hi
        return Fraction(0) if hi > 0 else Fraction(hi.__ceil__() - 1)
    if hi is None:  # simplest x > lo
        return Fraction(0) if lo < 0 else Fraction(lo.__floor__() + 1)
    if lo < 0 < hi:
        return Fraction(0)
    # integers strictly between, closest to zero
    if hi > 0:
        n = lo.__floor__() + 1
        if n < hi:
            return Fraction(n)
    else:
        n = hi.__ceil__() - 1
        if n > lo:
            return Fraction(n)
    d = 2
    while True:
        k = (lo * d).__floor__() + 1
        if Fraction(k, d) < hi:
            return Fraction(k, d)
        d *= 2


def _intern(L, R) -> Game:
    L = sorted(L, key=lambda g: g.id)
    R = sorted(R, key=lambda g: g.id)
    key = (tuple(g.id for g in L), tuple(g.id for g in R))
    g = _table.get(key)
    if g is not None:
        return g
    g = Game(L, R)
    # number recognition (valid because the form is canonical)
    if len(L) <= 1 and len(R) <= 1 and all(x.num is not None for x in L + R):
        lo = L[0].num if L else None
        hi = R[0].num if R else None
        if lo is None or hi is None or lo < hi:
            g.num = _simplest_between(lo, hi)
    # nimber recognition
    if key[0] == key[1] and all(x.nim is not None for x in L):
        if sorted(x.nim for x in L) == list(range(len(L))):
            g.nim = len(L)
    _table[key] = g
    return g


def make(L, R) -> Game:
    """Canonical form of {L | R} where L, R are iterables of canonical games."""
    L, R = list(L), list(R)
    while True:
        L, R = _maximal(L), _minimal(R)
        raw = Game(L, R)  # same value as the game being built; not interned
        changed = False
        newL = []
        for gl in L:
            rev = next((glr for glr in gl.R if le(glr, raw)), None)
            if rev is None:
                newL.append(gl)
            else:
                newL.extend(rev.L)
                changed = True
        newR = []
        for gr in R:
            rev = next((grl for grl in gr.L if le(raw, grl)), None)
            if rev is None:
                newR.append(gr)
            else:
                newR.extend(rev.R)
                changed = True
        if not changed:
            return _intern(L, R)
        L, R = newL, newR


ZERO = make([], [])
STAR = make([ZERO], [ZERO])
UP = make([ZERO], [STAR])
DOWN = make([STAR], [ZERO])


def integer(n: int) -> Game:
    g = ZERO
    for _ in range(abs(n)):
        g = make([g], []) if n > 0 else make([], [g])
    return g


def number(x) -> Game:
    """Canonical form of a dyadic rational."""
    x = Fraction(x)
    if x.denominator == 1:
        return integer(int(x))
    d = x.denominator
    assert d & (d - 1) == 0, "only dyadic rationals are short games"
    return make([number(x - Fraction(1, d))], [number(x + Fraction(1, d))])


def nimber(n: int) -> Game:
    opts = [nimber(k) for k in range(n)]
    return make(opts, opts)


def neg(g: Game) -> Game:
    r = _neg_memo.get(g.id)
    if r is None:
        r = make([neg(x) for x in g.R], [neg(x) for x in g.L])
        _neg_memo[g.id] = r
    return r


def add(a: Game, b: Game) -> Game:
    if a is ZERO:
        return b
    if b is ZERO:
        return a
    if a.num is not None and b.num is not None:
        return number(a.num + b.num)
    key = (a.id, b.id) if a.id <= b.id else (b.id, a.id)
    r = _add_memo.get(key)
    if r is None:
        L = [add(x, b) for x in a.L] + [add(a, x) for x in b.L]
        R = [add(x, b) for x in a.R] + [add(a, x) for x in b.R]
        r = make(L, R)
        _add_memo[key] = r
    return r


def total(games) -> Game:
    g = ZERO
    for x in games:
        g = add(g, x)
    return g


def outcome(g: Game) -> str:
    """'L' Left wins, 'R' Right wins, 'P' second player wins, 'N' first player wins."""
    ge0, le0 = le(ZERO, g), le(g, ZERO)
    if ge0 and le0:
        return "P"
    if ge0:
        return "L"
    if le0:
        return "R"
    return "N"


# ---------------------------------------------------------------------------
# thermographs: walls are piecewise-linear functions of temperature t >= 0
# represented as (points, tail_slope) with points = [(t0, v0), (t1, v1), ...]
# ---------------------------------------------------------------------------

def _pl_eval(f, t):
    pts, slope = f
    if t >= pts[-1][0]:
        return pts[-1][1] + slope * (t - pts[-1][0])
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    raise ValueError(t)


def _pl_shift(f, s):
    """f(t) + s*t"""
    pts, slope = f
    return ([(t, v + s * t) for t, v in pts], slope + s)


def _pl_combine(fs, pick):
    """Pointwise max/min of PL functions on [0, inf)."""
    ts = sorted({t for f in fs for t, _ in f[0]})
    # add pairwise crossing points
    cand = set(ts)
    bounds = ts + [ts[-1] + 1]
    for a, b in zip(bounds, bounds[1:]):
        for i in range(len(fs)):
            for j in range(i + 1, len(fs)):
                da = _pl_eval(fs[i], a) - _pl_eval(fs[j], a)
                db = _pl_eval(fs[i], b) - _pl_eval(fs[j], b)
                if da * db < 0:
                    cand.add(a + (b - a) * da / (da - db))
    last = max(cand)
    # beyond `last` every function is linear; pick by value then by slope
    tail = pick(fs, key=lambda f: (_pl_eval(f, last), f[1]))[1]
    # crossings beyond `last`
    for i in range(len(fs)):
        for j in range(i + 1, len(fs)):
            d0 = _pl_eval(fs[i], last) - _pl_eval(fs[j], last)
            ds = fs[i][1] - fs[j][1]
            if ds != 0:
                tc = last - d0 / ds
                if tc > last:
                    cand.add(tc)
    pts = []
    for t in sorted(cand):
        v = pick(_pl_eval(f, t) for f in fs)
        pts.append((t, v))
    last = pts[-1][0]
    tail = pick(fs, key=lambda f: (_pl_eval(f, last), f[1]))[1]
    return (_pl_simplify(pts), tail)


def _pl_simplify(pts):
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        (t0, v0), (t1, v1), (t2, v2) = out[-1], pts[i], pts[i + 1]
        if (v1 - v0) * (t2 - t0) != (v2 - v0) * (t1 - t0):
            out.append(pts[i])
    if len(pts) > 1:
        out.append(pts[-1])
    return out


def thermograph(g: Game):
    """Returns (left_wall, right_wall, mean, temperature).

    Numbers get a mast from t=0 and temperature reported as -1 (integers) or
    -1/2^k style per Berlekamp is not needed here, so we report 0-masts with
    temperature `None` for numbers.
    """
    if g._thermo is not None:
        return g._thermo
    if g.num is not None:
        mast = ([(Fraction(0), g.num)], 0)
        g._thermo = (mast, mast, g.num, None)
        return g._thermo
    Ls = _pl_combine([_pl_shift(thermograph(x)[1], -1) for x in g.L], max) if g.L else None
    Rs = _pl_combine([_pl_shift(thermograph(x)[0], +1) for x in g.R], min) if g.R else None
    assert Ls is not None and Rs is not None, "non-number canonical game must have both options"
    # find first t >= 0 with Ls(t) <= Rs(t)
    def gap(t):
        return _pl_eval(Ls, t) - _pl_eval(Rs, t)
    ts = sorted({t for t, _ in Ls[0]} | {t for t, _ in Rs[0]})
    T = None
    if gap(ts[0]) <= 0:
        T = ts[0]
    else:
        probe = ts + [ts[-1] + 10**6]
        for a, b in zip(probe, probe[1:]):
            ga, gb = gap(a), gap(b)
            if gb <= 0:
                T = a + (b - a) * ga / (ga - gb)
                break
    assert T is not None, "scaffolds never meet"
    M = _pl_eval(Ls, T)
    lw = ([(t, v) for t, v in Ls[0] if t < T] + [(T, M)], 0)
    rw = ([(t, v) for t, v in Rs[0] if t < T] + [(T, M)], 0)
    g._thermo = (lw, rw, M, T)
    return g._thermo


def mean(g: Game):
    return thermograph(g)[2]


def temperature(g: Game):
    return thermograph(g)[3]


def stops(g: Game):
    lw, rw, _, _ = thermograph(g)
    return _pl_eval(lw, 0), _pl_eval(rw, 0)


# ---------------------------------------------------------------------------
# display
# ---------------------------------------------------------------------------

BIG_DISPLAY = None  # set by callers: numbers with |x| >= this print as +W / -W


def _fmt_num(x: Fraction) -> str:
    if BIG_DISPLAY is not None and abs(x) >= BIG_DISPLAY:
        return "+W" if x > 0 else "-W"
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def show(g: Game) -> str:
    if g.num is not None:
        return _fmt_num(g.num)
    if g.nim is not None:
        return "*" if g.nim == 1 else f"*{g.nim}"
    named = _named()
    if g.id in named:
        return named[g.id]
    L, R = g.L, g.R
    # x ± y  (switch between numbers)
    if len(L) == 1 and len(R) == 1 and L[0].num is not None and R[0].num is not None:
        a, b = L[0].num, R[0].num
        if a == b:
            return f"{_fmt_num(a)}*"
        m, d = (a + b) / 2, (a - b) / 2
        return (f"±{_fmt_num(d)}" if m == 0 else f"{_fmt_num(m)}±{_fmt_num(d)}")
    # tiny / miny
    if L == (ZERO,) and len(R) == 1 and R[0].L == (ZERO,) and len(R[0].R) == 1 and R[0].R[0].num is not None:
        return f"tiny({_fmt_num(-R[0].R[0].num)})"
    if R == (ZERO,) and len(L) == 1 and L[0].R == (ZERO,) and len(L[0].L) == 1 and L[0].L[0].num is not None:
        return f"miny({_fmt_num(L[0].L[0].num)})"
    return "{" + ", ".join(show(x) for x in L) + " | " + ", ".join(show(x) for x in R) + "}"


_named_cache: dict[int, str] = {}


def _named():
    if not _named_cache:
        up_star = make([ZERO, STAR], [ZERO])
        down_star = neg(up_star)
        dup = add(UP, UP)
        for g, name in [
            (UP, "↑"), (DOWN, "↓"), (up_star, "↑*"), (down_star, "↓*"),
            (dup, "⇑"), (neg(dup), "⇓"), (add(dup, STAR), "⇑*"), (neg(add(dup, STAR)), "⇓*"),
            (add(dup, UP), "3↑"), (neg(add(dup, UP)), "3↓"),
        ]:
            _named_cache.setdefault(g.id, name)
    return _named_cache
