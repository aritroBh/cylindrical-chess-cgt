"""Independent check of claim C4 (adversarial verifier, workstream sumtest).

Written from scratch: imports NOTHING from sumtest/, cylcgt/ or crosscheck/.
Two methods, both mine:
  (A) canonical forms with my own small CGT kernel (numbers as atoms);
  (B) brute-force outcome of  X + (-V)  played out as an explicit sum,
      with V given as an explicit tree, to confirm X == V (P-position).

Model (pawn-only, Elkies 1996 style):
  * board: F files (flat unless --wrap), ranks 1..8; White = Left moves up.
  * single step, double step from home rank, diagonal captures, en passant.
  * after every move: passers tested for both sides;
      exactly one side has a passer  -> +BIG / -BIG
      both                           -> race rule (count / mover / opponent)
  * passer test:
      textbook: no enemy pawn ahead on own or adjacent file;
      aware   : textbook AND not a pawn that the opponent can capture e.p.
                with the very next move (just double-stepped next to an
                enemy pawn).
  * an e.p. right lives in the component and dies with the next move made
    in it (component scope: the only scope a CGT component value can have).

Usage:
  PYTHONPATH= .venv/bin/python verify/sumtest/C4-refute/c4_indep.py
"""
import sys
from fractions import Fraction as Fr
from functools import lru_cache
import argparse

sys.setrecursionlimit(200000)

# ----------------------------------------------------------------------------
# Minimal CGT kernel
# ----------------------------------------------------------------------------
_intern = {}


class G:
    __slots__ = ("key", "num", "L", "R", "uid")

    def __repr__(self):
        return show(self)


def num(x):
    x = Fr(x)
    k = ("n", x)
    g = _intern.get(k)
    if g is None:
        g = G(); g.key = k; g.num = x; g.L = None; g.R = None; g.uid = len(_intern)
        _intern[k] = g
    return g


def raw(L, R):
    L = tuple(sorted(set(L), key=lambda g: g.uid))
    R = tuple(sorted(set(R), key=lambda g: g.uid))
    k = ("g", tuple(g.uid for g in L), tuple(g.uid for g in R))
    g = _intern.get(k)
    if g is None:
        g = G(); g.key = k; g.num = None; g.L = L; g.R = R; g.uid = len(_intern)
        _intern[k] = g
    return g


def opts(g):
    if g.num is None:
        return g.L, g.R
    x = g.num
    if x == 0:
        return (), ()
    if x.denominator == 1:
        return ((num(x - 1),), ()) if x > 0 else ((), (num(x + 1),))
    d = Fr(1, x.denominator)
    return (num(x - d),), (num(x + d),)


_le = {}


def le(a, b):
    """a <= b (Conway)."""
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    k = (a.uid, b.uid)
    r = _le.get(k)
    if r is not None:
        return r
    aL, _ = opts(a)
    _, bR = opts(b)
    r = not any(le(b, x) for x in aL) and not any(le(y, a) for y in bR)
    _le[k] = r
    return r


def eq(a, b):
    return le(a, b) and le(b, a)


def simplest_between(lo, hi):
    """Simplest number strictly between lo and hi (None = unbounded)."""
    if lo is not None and hi is not None:
        assert lo < hi
    if (lo is None or lo < 0) and (hi is None or hi > 0):
        return Fr(0)
    if hi is not None and hi <= 0:          # mirror into the positive side
        return -simplest_between(-hi, None if lo is None else -lo)
    # now lo >= 0 (not None)
    n = (lo // 1) + 1
    if hi is None or n < hi:
        return Fr(n)
    k = 1
    while True:
        step = Fr(1, 2 ** k)
        n = (lo // step) + 1
        if n * step < hi:
            return n * step
        k += 1


def make(L, R):
    L, R = list(set(L)), list(set(R))
    while True:
        changed = False
        # dominated
        L2 = [x for x in L if not any(y is not x and le(x, y) for y in L)]
        R2 = [x for x in R if not any(y is not x and le(y, x) for y in R)]
        if len(L2) != len(L) or len(R2) != len(R):
            L, R, changed = L2, R2, True
        cur = raw(L, R)
        # reversible
        newL = []
        for x in L:
            _, xR = opts(x)
            rev = next((y for y in xR if le(y, cur)), None)
            if rev is None:
                newL.append(x)
            else:
                newL.extend(opts(rev)[0]); changed = True
        newR = []
        for x in R:
            xL, _ = opts(x)
            rev = next((y for y in xL if le(cur, y)), None)
            if rev is None:
                newR.append(x)
            else:
                newR.extend(opts(rev)[1]); changed = True
        L, R = list(set(newL)), list(set(newR))
        if not changed:
            break
    if all(x.num is not None for x in L + R):
        lo = max((x.num for x in L), default=None)
        hi = min((x.num for x in R), default=None)
        if lo is None or hi is None or lo < hi:
            return num(simplest_between(lo, hi))
    return raw(L, R)


def neg(g):
    if g.num is not None:
        return num(-g.num)
    return make([neg(y) for y in g.R], [neg(x) for x in g.L])


def outcome(g):
    z = num(0)
    ge0, le0 = le(z, g), le(g, z)
    return {(True, True): "P", (True, False): "L", (False, True): "R", (False, False): "N"}[(ge0, le0)]


def show(g):
    if g.num is not None:
        x = g.num
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    L, R = g.L, g.R
    # +-x  form
    if len(L) == 1 and len(R) == 1 and L[0].num is not None and R[0].num is not None:
        a, b = L[0].num, R[0].num
        if a > b:
            m, t = (a + b) / 2, (a - b) / 2
            ms = "" if m == 0 else show(num(m))
            return f"{ms}±{show(num(t))}"
    if not L and not R:
        return "0"
    if L == (num(0),) and R == (num(0),):
        return "*"
    return "{" + ", ".join(show(x) for x in L) + " | " + ", ".join(show(x) for x in R) + "}"


# ----------------------------------------------------------------------------
# Pawn rules
# ----------------------------------------------------------------------------
NR = 8
FILES = "abcdefgh"


class Rules:
    def __init__(self, F, wrap=False, ep=True, aware=True, race="count", big=256, race_double=True):
        self.F, self.wrap, self.ep, self.aware, self.race = F, wrap, ep, aware, race
        self.big, self.race_double = big, race_double
        self.race_nodes = 0
        self.resolved_by_ep_exclusion = 0

    def adj(self, f):
        out = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    # state: (W frozenset of (f,r), B frozenset, ep) ; ep = None or (f, r, side)
    #   ep = (f, r_skipped, 'W') : White just double stepped to (f, r_skipped+1)
    def moves(self, st, white):
        W, B, ep = st
        occ = W | B
        out = []
        if white:
            for (f, r) in W:
                if (f, r + 1) not in occ:
                    assert r + 1 < NR, "promotion reached without passer test"
                    out.append((W - {(f, r)} | {(f, r + 1)}, B, None))
                    if r == 2 and (f, 4) not in occ:
                        nep = (f, 3, "W") if (self.ep and any((g, 4) in B for g in self.adj(f))) else None
                        out.append((W - {(f, r)} | {(f, 4)}, B, nep))
                for g in self.adj(f):
                    if (g, r + 1) in B:
                        out.append((W - {(f, r)} | {(g, r + 1)}, B - {(g, r + 1)}, None))
            if ep is not None and ep[2] == "B":
                ef, er, _ = ep           # black pawn skipped (ef, 6), stands on (ef, 5)
                for g in self.adj(ef):
                    if (g, 5) in W:
                        out.append((W - {(g, 5)} | {(ef, 6)}, B - {(ef, 5)}, None))
        else:
            for (f, r) in B:
                if (f, r - 1) not in occ:
                    assert r - 1 > 1, "promotion reached without passer test"
                    out.append((W, B - {(f, r)} | {(f, r - 1)}, None))
                    if r == 7 and (f, 5) not in occ:
                        nep = (f, 6, "B") if (self.ep and any((g, 5) in W for g in self.adj(f))) else None
                        out.append((W, B - {(f, r)} | {(f, 5)}, nep))
                for g in self.adj(f):
                    if (g, r - 1) in W:
                        out.append((W - {(g, r - 1)}, B - {(f, r)} | {(g, r - 1)}, None))
            if ep is not None and ep[2] == "W":
                ef, er, _ = ep           # white pawn skipped (ef, 3), stands on (ef, 4)
                for g in self.adj(ef):
                    if (g, 4) in B:
                        out.append((W - {(ef, 4)}, B - {(g, 4)} | {(ef, 3)}, None))
        return [(frozenset(a), frozenset(b), e) for a, b, e in out]

    def passers(self, st, white):
        W, B, ep = st
        mine, theirs = (W, B) if white else (B, W)
        res = []
        for (f, r) in mine:
            span = {f} | self.adj(f)
            if white:
                ahead = any(g in span and t > r for (g, t) in theirs)
            else:
                ahead = any(g in span and t < r for (g, t) in theirs)
            if ahead:
                continue
            if self.aware and ep is not None:
                ef, er, side = ep
                if white and side == "W" and (f, r) == (ef, 4):
                    continue
                if (not white) and side == "B" and (f, r) == (ef, 5):
                    continue
            res.append((f, r))
        return res

    def steps(self, sqs, white):
        best = 99
        for (f, r) in sqs:
            if white:
                n = NR - r - (1 if self.race_double and r == 2 else 0)
            else:
                n = r - 1 - (1 if self.race_double and r == NR - 1 else 0)
            best = min(best, n)
        return best

    def resolve(self, st, mover_white):
        """None, +1 (White wins component) or -1."""
        wp, bp = self.passers(st, True), self.passers(st, False)
        if not wp and not bp:
            return None
        if wp and not bp:
            return +1
        if bp and not wp:
            return -1
        self.race_nodes += 1
        m = +1 if mover_white else -1
        if self.race == "mover":
            return m
        if self.race == "opponent":
            return -m
        sw, sb = self.steps(wp, True), self.steps(bp, False)
        s_m, s_o = (sw, sb) if mover_white else (sb, sw)
        return -m if s_o <= s_m else m

    def parse(self, text):
        W, B = set(), set()
        for part in text.split("/"):
            side, _, sq = part.strip().partition(":")
            for t in sq.split():
                (W if side.strip() == "W" else B).add((FILES.index(t[0]), int(t[1:])))
        return (frozenset(W), frozenset(B), None)

    def children(self, st, white):
        """list of (child_state or None, resolved value or None)"""
        out = []
        for c in self.moves(st, white):
            r = self.resolve(c, white)
            out.append((c, r))
        return out


def sq(f, r):
    return FILES[f] + str(r)


def fmt(st):
    W, B, ep = st
    s = "W: " + " ".join(sorted(sq(*p) for p in W)) + " / B: " + " ".join(sorted(sq(*p) for p in B))
    if ep:
        s += f"  (ep {sq(ep[0], ep[1])})"
    return s


def value_fn(rules):
    @lru_cache(maxsize=None)
    def val(st):
        kids = {}
        for white in (True, False):
            vs = []
            for c, r in rules.children(st, white):
                vs.append(num(r * rules.big) if r is not None else val(c))
            kids[white] = vs
        return make(kids[True], kids[False])
    return val


# ----------------------------------------------------------------------------
# Method B: brute-force outcome of pawn position + explicit tree H (exact).
# H trees: tuples (Lopts, Ropts).  When the pawn component resolves it becomes
# the exact integer +-BIG, played out move by move (no "BIG dominates" shortcut).
# ----------------------------------------------------------------------------
def T(L=(), R=()):
    return (tuple(L), tuple(R))


ZERO = T()


def int_tree(n):
    t = ZERO
    for _ in range(abs(n)):
        t = T([t]) if n > 0 else T([], [t])
    return t


def neg_tree(t):
    return T([neg_tree(y) for y in t[1]], [neg_tree(x) for x in t[0]])


_add = {}


def add_tree(a, b):
    k = (a, b)
    if k not in _add:
        _add[k] = T([add_tree(x, b) for x in a[0]] + [add_tree(a, y) for y in b[0]],
                    [add_tree(x, b) for x in a[1]] + [add_tree(a, y) for y in b[1]])
    return _add[k]


def brute_wins(rules, st0, H):
    """(Left wins moving first, Right wins moving first) in pawnpos + H, exact."""

    @lru_cache(maxsize=None)
    def win(comp, h, left_to_move):
        kind, c = comp
        nxt = []
        if kind == "p":
            for ch, r in rules.children(c, left_to_move):
                nxt.append((("n", r * rules.big) if r is not None else ("p", ch), h))
        else:
            if left_to_move and c > 0:
                nxt.append((("n", c - 1), h))
            if not left_to_move and c < 0:
                nxt.append((("n", c + 1), h))
        for x in (h[0] if left_to_move else h[1]):
            nxt.append((comp, x))
        return any(not win(cc, hh, not left_to_move) for cc, hh in nxt)

    return win(("p", st0), H, True), win(("p", st0), H, False)


def outcome_from(wl, wr):
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(wl, wr)]


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--big", type=int, default=256)
    a = ap.parse_args()
    BIG = a.big
    STAR = T([ZERO], [ZERO])

    X = "W: a2 c2 / B: b4 d7"
    Y = "W: a2 c2 / B: b5 d7"
    ROOT = "W: a2 c2 / B: b7 d7"
    print(f"BIG = {BIG}; 4-file flat board, 8 ranks")
    for race in ("count", "mover", "opponent"):
        for label, ep, aware in (("e.p. off", False, False), ("e.p. on, textbook", True, False),
                                 ("e.p. on, aware", True, True)):
            ru = Rules(4, wrap=False, ep=ep, aware=aware, race=race, big=BIG)
            val = value_fn(ru)
            vals = {}
            for name, pos in (("X", X), ("Y(b5)", Y), ("root", ROOT)):
                st = ru.parse(pos)
                assert ru.resolve(st, True) is None
                vals[name] = val(st)
            print(f"[{race:8s} | {label:18s}] X = {show(vals['X']):14s} b5 = {show(vals['Y(b5)']):10s}"
                  f" root = {show(vals['root']):24s} race nodes = {ru.race_nodes}")

    # ---------------- detailed, count rule ----------------
    for aware in (False, True):
        ru = Rules(4, ep=True, aware=aware, race="count", big=BIG)
        val = value_fn(ru)
        st = ru.parse(X)
        print(f"\n== X = {X}, e.p. on, {'aware' if aware else 'textbook'} test, count rule ==")
        print("  value:", show(val(st)))
        for white in (True, False):
            for c, r in ru.children(st, white):
                v = num(r * BIG) if r is not None else val(c)
                tag = " (resolved)" if r is not None else ""
                print(f"   {'L' if white else 'R'}: -> {fmt(c):40s} = {show(v)}{tag}")
                # second ply for the a2-a4 line
                if white and c[2] is not None and r is None:
                    for c2, r2 in ru.children(c, False):
                        v2 = num(r2 * BIG) if r2 is not None else val(c2)
                        print(f"        R: -> {fmt(c2):36s} = {show(v2)}{' (resolved)' if r2 is not None else ''}")
                    for c2, r2 in ru.children(c, True):
                        v2 = num(r2 * BIG) if r2 is not None else val(c2)
                        print(f"        L: -> {fmt(c2):36s} = {show(v2)}{' (resolved)' if r2 is not None else ''}")
        sY = ru.parse(Y)
        print(f"  b5 position {Y}: {show(val(sY))}")
        sR = ru.parse(ROOT)
        print(f"  root {ROOT}: {show(val(sR))}")
        for c, r in ru.children(sR, False):
            v = num(r * BIG) if r is not None else val(c)
            print(f"   root R: -> {fmt(c):40s} = {show(v)}")
        for c, r in ru.children(sR, True):
            v = num(r * BIG) if r is not None else val(c)
            print(f"   root L: -> {fmt(c):40s} = {show(v)}")

    # ---------------- method B: explicit sum tests ----------------
    print("\n== Method B: exact brute-force outcome of position + (-V) [+ control] ==")
    print("   if position == V:  P for +0,  N for +*,  L for +1")
    STAR = T([ZERO], [ZERO])
    pmB = T([int_tree(BIG)], [int_tree(-BIG)])          # +-BIG
    tests = [
        ("X", X, False, T([int_tree(BIG)], [pmB]), "{BIG | ±BIG}"),
        ("X", X, True, int_tree(-3), "-3"),
        ("b5", Y, True, T([int_tree(-1)], [int_tree(-3)]), "-2±1"),
        ("b5", Y, False, ZERO, "0"),
        ("root", ROOT, False, T([ZERO, STAR], [ZERO, STAR]), "*2"),
        ("root", ROOT, True, T([ZERO, STAR], [ZERO, STAR]), "*2"),
    ]
    for name, pos, aware, V, vs in tests:
        ru = Rules(4, ep=True, aware=aware, race="count", big=BIG)
        st = ru.parse(pos)
        nv = neg_tree(V)
        res = [outcome_from(*brute_wins(ru, st, add_tree(nv, ctl))) for ctl in (ZERO, STAR, int_tree(1))]
        print(f"  {name:4s} {'aware   ' if aware else 'textbook'}: {name} - ({vs}) + [0, *, 1] -> {res}")

if __name__ == "__main__":
    main()
