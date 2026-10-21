"""Independent re-implementation (verifier C2-theory) of the ChessSums component model.

Written from the stated rules only: it imports nothing from cylcgt or bench.
  * own short-game CGT engine (canonical forms by removing dominated options and
    bypassing reversible ones; hash-consed, so equal values are the same object);
  * own pawn move generator (single/double steps, captures, en passant);
  * own "textbook" and "e.p.-aware" passed tests, own race rules (count/mover/opponent);
  * cylcgt's modelling semantics re-implemented from its documented behaviour:
      - value(pos): exactly one side passed -> +-BIG; else split on empty files and sum;
      - inside a component: both passed -> RaceError, one passed -> +-BIG;
      - a child with both sides passed is a race resolved by the race rule;
      - an e.p. right survives only for the capturing side's next move in that component.
Also records, at every position where a passed-test judgement is made under the textbook
test, whether the e.p.-aware test would judge it differently (passed flags or race distances).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import count

sys.setrecursionlimit(200000)

# ----------------------------------------------------------------------------- CGT
_ids = count()
_table: dict = {}
_le: dict = {}
_add: dict = {}
_neg: dict = {}
_int: dict = {}


class Gm:
    __slots__ = ("L", "R", "id", "num")

    def __init__(self, L, R):
        self.L, self.R, self.id, self.num = tuple(L), tuple(R), next(_ids), None


def le(a, b):
    if a is b:
        return True
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    k = (a.id, b.id)
    r = _le.get(k)
    if r is None:
        r = not any(le(b, x) for x in a.L) and not any(le(x, a) for x in b.R)
        _le[k] = r
    return r


def _dedupe(xs):
    seen, out = set(), []
    for x in xs:
        if x.id not in seen:
            seen.add(x.id)
            out.append(x)
    return out


def _simplest(lo, hi):
    """simplest number strictly between lo and hi (None = unbounded)."""
    import math
    if (lo is None or lo < 0) and (hi is None or hi > 0):
        return Fraction(0)
    if lo is not None and lo >= 0:
        n = math.floor(lo) + 1          # smallest integer > lo
        if hi is None or n < hi:
            return Fraction(n)
    elif hi is not None and hi <= 0:
        n = math.ceil(hi) - 1           # largest integer < hi
        if lo is None or n > lo:
            return Fraction(n)
    k = 1                               # lo, hi finite: smallest-denominator dyadic
    while True:
        d = Fraction(1, 2 ** k)
        m = math.floor(lo / d) + 1
        if m * d < hi:
            return m * d
        k += 1


def make(L, R):
    L, R = _dedupe(L), _dedupe(R)
    while True:
        changed = False
        L2 = [x for x in L if not any(y is not x and le(x, y) for y in L)]
        R2 = [x for x in R if not any(y is not x and le(y, x) for y in R)]
        if len(L2) != len(L) or len(R2) != len(R):
            changed = True
        L, R = L2, R2
        cur = Gm(L, R)  # temporary form, used only for comparisons
        newL = []
        for x in L:
            rev = next((xr for xr in x.R if le(xr, cur)), None)
            if rev is None:
                newL.append(x)
            else:
                newL.extend(rev.L)
                changed = True
        newR = []
        for x in R:
            rev = next((xl for xl in x.L if le(cur, xl)), None)
            if rev is None:
                newR.append(x)
            else:
                newR.extend(rev.R)
                changed = True
        L, R = _dedupe(newL), _dedupe(newR)
        if not changed:
            break
    key = (tuple(sorted(x.id for x in L)), tuple(sorted(x.id for x in R)))
    g = _table.get(key)
    if g is None:
        g = Gm(sorted(L, key=lambda x: x.id), sorted(R, key=lambda x: x.id))
        if all(x.num is not None for x in L + R):
            lo = max((x.num for x in L), default=None)
            hi = min((x.num for x in R), default=None)
            if lo is None or hi is None or lo < hi:
                g.num = _simplest(lo, hi)
        _table[key] = g
    return g


def integer(n):
    g = _int.get(n)
    if g is None:
        g = make([], []) if n == 0 else make([integer(n - 1)], []) if n > 0 else make([], [integer(n + 1)])
        _int[n] = g
    return g


def number(q):
    q = Fraction(q)
    if q.denominator == 1:
        return integer(int(q))
    e = Fraction(1, q.denominator)
    return make([number(q - e)], [number(q + e)])


def neg(g):
    r = _neg.get(g.id)
    if r is None:
        r = make([neg(x) for x in g.R], [neg(x) for x in g.L])
        _neg[g.id] = r
    return r


def add(a, b):
    if a.id > b.id:
        a, b = b, a
    k = (a.id, b.id)
    r = _add.get(k)
    if r is None:
        if a.num is not None and b.num is not None:
            r = number(a.num + b.num)
        elif a.num is not None and a.num == 0:
            r = b
        elif b.num is not None and b.num == 0:
            r = a
        else:
            r = make([add(x, b) for x in a.L] + [add(a, x) for x in b.L],
                     [add(x, b) for x in a.R] + [add(a, x) for x in b.R])
        _add[k] = r
    return r


def outcome(g):
    zero = integer(0)
    lw = not le(g, zero)   # Left moving first wins iff not G <= 0
    rw = not le(zero, g)   # Right moving first wins iff not G >= 0
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


def show(g, depth=0):
    if g.num is not None:
        return str(g.num)
    if depth > 6:
        return "..."
    return "{" + ",".join(show(x, depth + 1) for x in g.L) + "|" + ",".join(show(x, depth + 1) for x in g.R) + "}"


# ----------------------------------------------------------------------------- pawns
RANKS = 8
BIG = 256
FILES = "abcdefgh"


class RaceError(Exception):
    pass


def parse(text):
    wp, bp = text.split("/")
    sq = lambda t: (FILES.index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in wp.split(":")[1].split()),
            frozenset(sq(t) for t in bp.split(":")[1].split()), None)


def ptext(p):
    nm = lambda s: f"{FILES[s[0]]}{s[1]}"
    return "W: " + " ".join(sorted(map(nm, p[0]))) + " / B: " + " ".join(sorted(map(nm, p[1])))


class Model:
    """One setting: width w (flat strip), e.p. on/off, passed test, race rule."""

    def __init__(self, w, ep_on, aware, rule, audit=False):
        self.w, self.ep_on, self.aware, self.rule, self.audit = w, ep_on, aware, rule, audit
        self.memo = {}
        self.mismatch = []   # positions judged differently by the two tests (audit mode)
        self.visited = set()

    # ---- e.p. helpers: ep = (captured_square, capturing_side)
    def ep_capturable(self, p, side, s):
        """side's pawn on s is the double-stepped pawn and the opponent can take it e.p."""
        ep = p[2]
        if ep is None or ep[0] != s or ep[1] == side:
            return False
        theirs = p[1] if side == "W" else p[0]
        f, r = s
        return (f - 1, r) in theirs or (f + 1, r) in theirs

    def pawn_free(self, p, side, s):
        """textbook: no enemy pawn ahead on this or an adjacent file."""
        theirs = p[1] if side == "W" else p[0]
        f, r = s
        for g, t in theirs:
            if abs(g - f) <= 1 and ((t > r) if side == "W" else (t < r)):
                return False
        return True

    def passed(self, p, side, aware):
        mine = p[0] if side == "W" else p[1]
        return any(self.pawn_free(p, side, s) and not (aware and self.ep_capturable(p, side, s)) for s in mine)

    def dist(self, p, side, aware):
        mine = p[0] if side == "W" else p[1]
        occ = p[0] | p[1]
        best = None
        for s in mine:
            if not self.pawn_free(p, side, s) or (aware and self.ep_capturable(p, side, s)):
                continue
            f, r = s
            if side == "W":
                if any((f, t) in occ for t in range(r + 1, RANKS + 1)):
                    continue
                d = RANKS - r - (1 if r == 2 else 0)
            else:
                if any((f, t) in occ for t in range(1, r)):
                    continue
                d = r - 1 - (1 if r == RANKS - 1 else 0)
            best = d if best is None else min(best, d)
        return 10 ** 6 if best is None else best

    def judge(self, p, aware):
        wp, bp = self.passed(p, "W", aware), self.passed(p, "B", aware)
        d = (self.dist(p, "W", aware), self.dist(p, "B", aware)) if (wp and bp) else None
        return wp, bp, d

    def J(self, p):
        """judgement under the active test; in audit mode also compare with the other test."""
        j = self.judge(p, self.aware)
        if self.audit:
            self.visited.add(p)
            o = self.judge(p, not self.aware)
            if o != j:
                self.mismatch.append(p)
        return j

    # ---- moves
    def moves(self, p, side):
        Wp, Bp, ep = p
        mine, theirs = (Wp, Bp) if side == "W" else (Bp, Wp)
        occ = Wp | Bp
        dr = 1 if side == "W" else -1
        start = 2 if side == "W" else RANKS - 1
        other = "B" if side == "W" else "W"
        out = []

        def emit(nm, nt, nep=None):
            out.append((frozenset(nm), frozenset(nt), nep) if side == "W" else (frozenset(nt), frozenset(nm), nep))

        for s in mine:
            f, r = s
            rest = mine - {s}
            r1 = r + dr
            if not 1 <= r1 <= RANKS:
                continue
            if (f, r1) not in occ:
                emit(rest | {(f, r1)}, theirs)
                r2 = r + 2 * dr
                if r == start and (f, r2) not in occ:
                    emit(rest | {(f, r2)}, theirs, ((f, r2), other) if self.ep_on else None)
            for g in (f - 1, f + 1):
                if not 0 <= g < self.w:
                    continue
                t = (g, r1)
                if t in theirs:
                    emit(rest | {t}, theirs - {t})
                elif ep is not None and ep[1] == side and ep[0] == (g, r) and t not in occ:
                    emit(rest | {t}, theirs - {(g, r)})
        return list(dict.fromkeys(out))

    def split(self, p):
        files = sorted({f for f, _ in p[0] | p[1]})
        groups = []
        for f in files:
            if groups and f == groups[-1][-1] + 1:
                groups[-1].append(f)
            else:
                groups.append([f])
        out = []
        for g in groups:
            fs = set(g)
            ep = p[2] if (p[2] is not None and p[2][0][0] in fs) else None
            out.append((frozenset(s for s in p[0] if s[0] in fs), frozenset(s for s in p[1] if s[0] in fs), ep))
        return out

    # ---- values (cylcgt semantics)
    def value(self, p):
        wp, bp, _ = self.J(p)
        if wp != bp:
            return integer(BIG if wp else -BIG)
        comps = self.split(p)
        if len(comps) > 1:
            g = integer(0)
            for c in comps:
                g = add(g, self.cvalue(c))
            return g
        return self.cvalue(p)

    def cvalue(self, p):
        g = self.memo.get(p)
        if g is not None:
            return g
        wp, bp, _ = self.J(p)
        if wp and bp:
            raise RaceError(ptext(p))
        if wp or bp:
            g = integer(BIG if wp else -BIG)
        else:
            plain = (p[0], p[1], None)
            lp = p if (p[2] is not None and p[2][1] == "W") else plain
            rp = p if (p[2] is not None and p[2][1] == "B") else plain
            g = make([self.child(q, "W") for q in self.moves(lp, "W")],
                     [self.child(q, "B") for q in self.moves(rp, "B")])
        self.memo[p] = g
        return g

    def child(self, q, mover):
        wp, bp, d = self.J(q)
        if wp and bp:
            other = "B" if mover == "W" else "W"
            if self.rule == "mover":
                win = mover
            elif self.rule == "opponent":
                win = other
            else:
                dW, dB = d
                dm, do = (dW, dB) if mover == "W" else (dB, dW)
                win = other if do <= dm else mover
            return integer(BIG if win == "W" else -BIG)
        return self.value(q)

    def ep_capture_available(self, p):
        """non-terminal e.p. capture check (filter 5 analogue)."""
        if p[2] is None:
            return False
        side = p[2][1]
        return set(self.moves(p, side)) != set(self.moves((p[0], p[1], None), side))


def root_and_children(w, p, ep_on, aware, rule, audit=False):
    m = Model(w, ep_on, aware, rule, audit)
    try:
        root = m.value(p)
    except RaceError:
        root = None
    kids = []
    for side in "WB":
        for q in m.moves(p, side):
            try:
                kids.append((side, q, m.child(q, side)))
            except RaceError:
                kids.append((side, q, None))
    return m, root, kids
