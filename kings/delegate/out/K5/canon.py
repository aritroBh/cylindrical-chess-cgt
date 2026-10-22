"""Independent short-game CGT engine for K5 (stand-in for CGSuite).

Written from textbook definitions (Siegel; Berlekamp-Conway-Guy). Does NOT
import cylcgt.cgt. Imports cylcgt.pawns only for pawn rules.
"""
from __future__ import annotations
import sys
from fractions import Fraction
import itertools

sys.setrecursionlimit(1_000_000)

_id_counter = itertools.count()
_table = {}
_le_memo = {}
_add_memo = {}
_neg_memo = {}
_NAMED = {}

BIG_DISPLAY = None


class Game:
    __slots__ = ("L", "R", "gid", "num", "nim")

    def __init__(self, L, R):
        self.L = tuple(L)
        self.R = tuple(R)
        self.gid = next(_id_counter)
        self.num = None
        self.nim = None

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
        return self.gid

    def __eq__(self, other):
        return self is other


def _dedupe(xs):
    seen = set()
    out = []
    for x in xs:
        if x.gid not in seen:
            seen.add(x.gid)
            out.append(x)
    return out


def _maximal(xs):
    xs = _dedupe(xs)
    return [x for x in xs if not any(y is not x and le(x, y) for y in xs)]


def _minimal(xs):
    xs = _dedupe(xs)
    return [x for x in xs if not any(y is not x and le(y, x) for y in xs)]


def _simplest_between(lo, hi):
    if lo is None and hi is None:
        return Fraction(0)
    if lo is None:
        if hi > 0:
            return Fraction(0)
        return Fraction(int(hi.__ceil__()) - 1)
    if hi is None:
        if lo < 0:
            return Fraction(0)
        return Fraction(int(lo.__floor__()) + 1)
    if lo < 0 < hi:
        return Fraction(0)
    if hi > 0:
        n = int(lo.__floor__()) + 1
        if n < hi:
            return Fraction(n)
    else:
        n = int(hi.__ceil__()) - 1
        if n > lo:
            return Fraction(n)
    d = 2
    while True:
        k = int((lo * d).__floor__()) + 1
        val = Fraction(k, d)
        if val < hi:
            return val
        d *= 2


def _intern(L, R):
    L = sorted(L, key=lambda g: g.gid)
    R = sorted(R, key=lambda g: g.gid)
    key = (tuple(g.gid for g in L), tuple(g.gid for g in R))
    g = _table.get(key)
    if g is not None:
        return g
    g = Game(L, R)
    if len(L) <= 1 and len(R) <= 1 and all(x.num is not None for x in L + R):
        lo = L[0].num if L else None
        hi = R[0].num if R else None
        if lo is None or hi is None or lo < hi:
            g.num = _simplest_between(lo, hi)
    if len(L) == len(R) and all(x.nim is not None for x in L + R):
        ls = sorted(x.nim for x in L)
        rs = sorted(x.nim for x in R)
        if ls == rs and ls == list(range(len(L))):
            g.nim = len(L)
    _table[key] = g
    return g


def le(a, b):
    if a is b:
        return True
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    key = (a.gid, b.gid)
    r = _le_memo.get(key)
    if r is None:
        r = not any(le(b, al) for al in a.L) and not any(le(br, a) for br in b.R)
        _le_memo[key] = r
    return r


def make(L, R):
    L, R = list(L), list(R)
    while True:
        L = _maximal(L)
        R = _minimal(R)
        raw = Game(L, R)
        changed = False
        newL = []
        for gl in L:
            rev = None
            for glr in gl.R:
                if le(glr, raw):
                    rev = glr
                    break
            if rev is None:
                newL.append(gl)
            else:
                newL.extend(rev.L)
                changed = True
        newR = []
        for gr in R:
            rev = None
            for grl in gr.L:
                if le(raw, grl):
                    rev = grl
                    break
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


def integer(n):
    if n == 0:
        return ZERO
    if n > 0:
        g = ZERO
        for _ in range(n):
            g = make([g], [])
        return g
    else:
        g = ZERO
        for _ in range(-n):
            g = make([], [g])
        return g


def number(x):
    x = Fraction(x)
    if x.denominator == 1:
        return integer(int(x))
    d = x.denominator
    return make([number(x - Fraction(1, d))], [number(x + Fraction(1, d))])


def nimber(n):
    opts = [nimber(k) for k in range(n)]
    return make(opts, opts)


def neg(g):
    r = _neg_memo.get(g.gid)
    if r is None:
        r = make([neg(x) for x in g.R], [neg(x) for x in g.L])
        _neg_memo[g.gid] = r
    return r


def add(a, b):
    if a is ZERO:
        return b
    if b is ZERO:
        return a
    if a.num is not None and b.num is not None:
        return number(a.num + b.num)
    if a.num is not None and b.num is None:
        x = a.num
        L = [add(number(x), gl) for gl in b.L]
        R = [add(number(x), gr) for gr in b.R]
        return make(L, R)
    if b.num is not None and a.num is None:
        x = b.num
        L = [add(number(x), gl) for gl in a.L]
        R = [add(number(x), gr) for gr in a.R]
        return make(L, R)
    key = (a.gid, b.gid) if a.gid <= b.gid else (b.gid, a.gid)
    r = _add_memo.get(key)
    if r is None:
        L = [add(x, b) for x in a.L] + [add(a, x) for x in b.L]
        R = [add(x, b) for x in a.R] + [add(a, x) for x in b.R]
        r = make(L, R)
        _add_memo[key] = r
    return r


def total(games):
    g = ZERO
    for x in games:
        g = add(g, x)
    return g


def outcome(g):
    ge0 = le(ZERO, g)
    le0 = le(g, ZERO)
    if ge0 and le0:
        return "P"
    if ge0:
        return "L"
    if le0:
        return "R"
    return "N"


def up_star():
    return make([ZERO, STAR], [ZERO])


def down_star():
    return neg(up_star())


def _named():
    if not _NAMED:
        us = up_star()
        ds = down_star()
        dup = add(UP, UP)
        pairs = [
            (UP, "↑"), (DOWN, "↓"), (us, "↑*"), (ds, "↓*"),
            (dup, "⇑"), (neg(dup), "⇓"), (add(dup, STAR), "⇑*"), (neg(add(dup, STAR)), "⇓*"),
            (add(dup, UP), "3↑"), (neg(add(dup, UP)), "3↓"),
        ]
        for g, name in pairs:
            _NAMED.setdefault(g.gid, name)
    return _NAMED


def show(g):
    bd = BIG_DISPLAY
    def fmt_num(x):
        if bd is not None and abs(x) >= bd:
            return "+W" if x > 0 else "-W"
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if g.num is not None:
        return fmt_num(g.num)
    if g.nim is not None:
        return "*" if g.nim == 1 else f"*{g.nim}"
    named = _named()
    if g.gid in named:
        return named[g.gid]
    L, R = g.L, g.R
    if len(L) == 1 and len(R) == 1 and L[0].num is not None and R[0].num is not None:
        a, b = L[0].num, R[0].num
        if a == b:
            return f"{fmt_num(a)}*"
        m = (a + b) / 2
        d = (a - b) / 2
        ms = fmt_num(m) if m != 0 else ""
        return (f"{ms}±{fmt_num(d)}" if ms else f"±{fmt_num(d)}")
    if L == (ZERO,) and len(R) == 1 and R[0].L == (ZERO,) and len(R[0].R) == 1 and R[0].R[0].num is not None:
        return f"tiny({fmt_num(-R[0].R[0].num)})"
    if R == (ZERO,) and len(L) == 1 and L[0].R == (ZERO,) and len(L[0].L) == 1 and L[0].L[0].num is not None:
        return f"miny({fmt_num(L[0].L[0].num)})"
    return "{" + ", ".join(show(x) for x in L) + " | " + ", ".join(show(x) for x in R) + "}"


def clear_caches():
    _table.clear()
    _le_memo.clear()
    _add_memo.clear()
    _neg_memo.clear()
    _NAMED.clear()
    global ZERO, STAR, UP, DOWN
    ZERO = make([], [])
    STAR = make([ZERO], [ZERO])
    UP = make([ZERO], [STAR])
    DOWN = make([STAR], [ZERO])


try:
    import cylcgt.pawns as _pawns
    BIG_DISPLAY = _pawns.BIG // 2
except Exception:
    BIG_DISPLAY = 128


# ---------- pawn-game recursion (mirrors cylcgt.pawns.value/_value/_child) ----------

_pawn_value_cache = {}


def clear_pawn_caches():
    _pawn_value_cache.clear()


def _pawn_child(board, pos, mover):
    import cylcgt.pawns as P
    if P.passed(board, pos, "W") and P.passed(board, pos, "B"):
        P.race_hits.append(f"{pos} after {mover}")
        if P.RACE_RULE == "mover":
            winner = mover
        elif P.RACE_RULE == "opponent":
            winner = "B" if mover == "W" else "W"
        else:
            other = "B" if mover == "W" else "W"
            winner = other if P.promote_distance(board, pos, other) <= P.promote_distance(board, pos, mover) else mover
        return integer(P.BIG if winner == "W" else -P.BIG)
    return pawn_value(board, pos)


def _pawn_value(board, pos):
    import cylcgt.pawns as P
    key = (board, pos)
    r = _pawn_value_cache.get(key)
    if r is not None:
        return r
    wp = P.passed(board, pos, "W")
    bp = P.passed(board, pos, "B")
    if wp and bp:
        raise P.RaceError(str(pos))
    if wp:
        r = integer(P.BIG)
        _pawn_value_cache[key] = r
        return r
    if bp:
        r = integer(-P.BIG)
        _pawn_value_cache[key] = r
        return r
    plain = P.Pos(pos.white, pos.black, None)
    lpos = plain if (pos.ep and pos.ep[2] != "W") else pos
    rpos = plain if (pos.ep and pos.ep[2] != "B") else pos
    L = [_pawn_child(board, p, "W") for p in P.moves(board, lpos, "W")]
    R = [_pawn_child(board, p, "B") for p in P.moves(board, rpos, "B")]
    r = make(L, R)
    _pawn_value_cache[key] = r
    return r


def pawn_value(board, pos):
    import cylcgt.pawns as P
    wp = P.passed(board, pos, "W")
    bp = P.passed(board, pos, "B")
    if wp != bp:
        return integer(P.BIG if wp else -P.BIG)
    comps = P.components(board, pos)
    if len(comps) > 1:
        return total(_pawn_value(board, c) for c in comps)
    return _pawn_value(board, pos)
