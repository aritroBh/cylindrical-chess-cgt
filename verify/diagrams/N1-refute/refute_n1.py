"""Adversarial (REFUTE-lens) check of claim N1: the 7.3 {c,d} sub-game
W c1 c3 d3 / B c2 d4 d5 d6 has value tiny(1) = {0 || 0 | -1}.

Written from scratch for this check. Imports NOTHING from cylcgt/ or crosscheck/.
Contains:
  * an own pawn move generator (8x8, flat or cylinder, e.p. on/off, double step only from 2nd rank),
  * an own canonical-form CGT (interned games, dominated/reversible simplification, Conway <=),
  * a raw-tree sum minimax (no canonical forms at all) that decides G + X for test games X,
    with the REAL e.p. semantics in sums (the right expires after ANY move, in any component),
  * three terminal conventions:
      "passed"   : project convention: exactly one side has a passed pawn (no enemy pawn strictly
                   ahead on own/adjacent file) => +-BIG; both => race rule;
      "promote"  : no passed-pawn shortcut at all; only an actual promotion (W on rank 8, B on rank 1)
                   is terminal (+-BIG). This removes the race rule and the 'passed' heuristic entirely.
  * BIG in {16, 256} to test sensitivity to the size of the win value.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/N1-refute/refute_n1.py
"""
import sys
import itertools
from functools import lru_cache

sys.setrecursionlimit(1_000_000)
FILES = "abcdefgh"

# ============================================================ own CGT (canonical forms)
_ids = itertools.count()
_intern = {}
_names = {}


class G:
    __slots__ = ("L", "R", "id")

    def __init__(self, L, R):
        self.L, self.R, self.id = tuple(L), tuple(R), next(_ids)


def _key(L, R):
    return (frozenset(x.id for x in L), frozenset(x.id for x in R))


_le_memo = {}


def le(a, b):
    """Conway: a <= b iff no a^L with b <= a^L and no b^R with b^R <= a."""
    k = (a.id, b.id)
    r = _le_memo.get(k)
    if r is None:
        r = not any(le(b, al) for al in a.L) and not any(le(br, a) for br in b.R)
        _le_memo[k] = r
    return r


def eq(a, b):
    return le(a, b) and le(b, a)


def make(L, R):
    """Canonical form of {L | R}, L and R canonical."""
    L, R = list(dict.fromkeys(L)), list(dict.fromkeys(R))
    while True:
        changed = False
        # dominated options (canonical forms interned => equal means identical)
        L2 = [x for x in L if not any(y is not x and le(x, y) for y in L)]
        R2 = [x for x in R if not any(y is not x and le(y, x) for y in R)]
        if len(L2) != len(L) or len(R2) != len(R):
            changed = True
        L, R = L2, R2
        T = G(L, R)  # temporary, never interned
        newL = []
        for x in L:
            rev = next((xr for xr in x.R if le(xr, T)), None)
            if rev is not None:
                newL.extend(rev.L); changed = True
            else:
                newL.append(x)
        newR = []
        for y in R:
            rev = next((yl for yl in y.L if le(T, yl)), None)
            if rev is not None:
                newR.extend(rev.R); changed = True
            else:
                newR.append(y)
        L, R = list(dict.fromkeys(newL)), list(dict.fromkeys(newR))
        if not changed:
            break
    k = _key(L, R)
    g = _intern.get(k)
    if g is None:
        g = G(L, R)
        _intern[k] = g
    return g


ZERO = make([], [])
_int_cache = {0: ZERO}


def integer(n):
    if n not in _int_cache:
        _int_cache[n] = make([integer(n - 1)], []) if n > 0 else make([], [integer(n + 1)])
    return _int_cache[n]


STAR = make([ZERO], [ZERO])
ONE, MONE = integer(1), integer(-1)
SW_0_M1 = make([ZERO], [MONE])           # {0 | -1}
TINY1 = make([ZERO], [SW_0_M1])          # {0 || 0 | -1}
MINY1 = make([make([ONE], [ZERO])], [ZERO])   # {1 | 0 || 0} = -tiny(1)
UP = make([ZERO], [STAR])


def neg(g):
    return make([neg(x) for x in g.R], [neg(x) for x in g.L])


def show(g, depth=0):
    for n, h in _int_cache.items():
        if h is g:
            return str(n)
    for nm_, h in (("*", STAR), ("tiny(1)", TINY1), ("miny(1)", MINY1), ("up", UP)):
        if h is g:
            return nm_
    if depth > 6:
        return "..."
    return "{" + ", ".join(show(x, depth + 1) for x in g.L) + " | " + ", ".join(show(x, depth + 1) for x in g.R) + "}"


# ============================================================ own pawn rules
def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def nm(s):
    return f"{FILES[s[0]]}{s[1]}"


def parse(text):
    w, b = text.split("/")
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()), None)


def pstr(p):
    w, b, ep = p
    s = "W: " + " ".join(sorted(map(nm, w))) + " / B: " + " ".join(sorted(map(nm, b)))
    return s + (f" (ep {nm(ep[0])} for {ep[2]})" if ep else "")


class Rules:
    def __init__(self, wrap=False, ep=True, race="count", term="passed", big=256):
        self.wrap, self.ep, self.race, self.term, self.big = wrap, ep, race, term, big
        self.stats = {"race": set(), "double": set(), "epcap": set(), "positions": set()}

    def adj(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.wrap:
                out.append(g % 8)
            elif 0 <= g < 8:
                out.append(g)
        return out

    def is_passed(self, p, side):
        w, b, _ = p
        mine, theirs = (w, b) if side == "W" else (b, w)
        for (f, r) in mine:
            fs = {f, *self.adj(f)}
            if side == "W":
                stop = any(g in fs and s > r for (g, s) in theirs)
            else:
                stop = any(g in fs and s < r for (g, s) in theirs)
            if not stop:
                return True
        return False

    def promoted(self, p, side):
        w, b, _ = p
        return any(r == 8 for _, r in w) if side == "W" else any(r == 1 for _, r in b)

    def gen(self, p, side):
        """Positions after one move of `side`. Only an e.p. right owned by `side` is usable."""
        w, b, ep = p
        mine, theirs = (w, b) if side == "W" else (b, w)
        occ = w | b
        d = 1 if side == "W" else -1
        start = 2 if side == "W" else 7
        other = "B" if side == "W" else "W"
        my_ep = ep if (ep is not None and ep[2] == side) else None
        res = []

        def put(m, t, e=None):
            res.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))

        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            if not 1 <= r1 <= 8:
                continue
            if (f, r1) not in occ:
                put(rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == start and 1 <= r2 <= 8 and (f, r2) not in occ:
                    self.stats["double"].add(pstr(p))
                    put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if self.ep else None)
            for g in self.adj(f):
                t = (g, r1)
                if t in theirs:
                    put(rest | {t}, theirs - {t})
                elif my_ep is not None and my_ep[0] == t:
                    self.stats["epcap"].add(pstr(p))
                    put(rest | {t}, theirs - {my_ep[1]})
        return list(dict.fromkeys(res))

    # ---------- terminal test of a position just reached by `mover`: returns +BIG, -BIG or None
    def terminal(self, p, mover):
        if self.term == "promote":
            if self.promoted(p, "W"):
                return self.big
            if self.promoted(p, "B"):
                return -self.big
            return None
        wp, bp = self.is_passed(p, "W"), self.is_passed(p, "B")
        if wp and bp:
            self.stats["race"].add(pstr(p))
            if self.race == "mover":
                win = mover
            elif self.race == "opponent":
                win = "B" if mover == "W" else "W"
            else:  # count: opponent of mover moves first, opponent wins ties
                opp = "B" if mover == "W" else "W"
                win = opp if self.dist(p, opp) <= self.dist(p, mover) else mover
            return self.big if win == "W" else -self.big
        if wp:
            return self.big
        if bp:
            return -self.big
        return None

    def dist(self, p, side):
        w, b, _ = p
        mine, theirs = (w, b) if side == "W" else (b, w)
        occ = w | b
        best = 10 ** 6
        for (f, r) in mine:
            single = (frozenset([(f, r)]), b, None) if side == "W" else (w, frozenset([(f, r)]), None)
            if not self.is_passed(single, side):
                continue
            ahead = range(r + 1, 9) if side == "W" else range(1, r)
            if any((f, s) in occ for s in ahead):
                continue
            n = (8 - r - (1 if r == 2 else 0)) if side == "W" else (r - 1 - (1 if r == 7 else 0))
            best = min(best, n)
        return best

    # ---------- canonical value of a (non-terminal) component, project e.p. approximation
    def value(self, p):
        return self._value(p)

    @lru_cache(maxsize=None)
    def _value(self, p):
        self.stats["positions"].add(pstr(p))
        w, b, ep = p
        plain = (w, b, None)
        lp = p if (ep is None or ep[2] == "W") else plain
        rp = p if (ep is None or ep[2] == "B") else plain
        L = [self.child(q, "W") for q in self.gen(lp, "W")]
        R = [self.child(q, "B") for q in self.gen(rp, "B")]
        return make(L, R)

    def child(self, q, mover):
        t = self.terminal(q, mover)
        return integer(t) if t is not None else self._value(q)

    # ---------- raw sum minimax: pawn component + raw test game X + integer counter
    # X is a raw tree: ("i", n) or ("g", (Xl...), (Xr...)).
    def sum_wins(self, p0, X, mover):
        @lru_cache(maxsize=None)
        def win(p, x, n, who):
            # does `who`, to move, win?
            other = "B" if who == "W" else "W"
            for nxt in succ(p, x, n, who):
                if not win(*nxt, other):
                    return True
            return False

        def norm(p, x, n):
            if x is not None and x[0] == "i":
                n += x[1]; x = None
            return p, x, n

        def succ(p, x, n, who):
            out = []
            if p is not None:
                w, b, ep = p
                src = p if (ep is None or ep[2] == who) else (w, b, None)
                for q in self.gen(src, who):
                    t = self.terminal(q, who)
                    out.append(norm(None, x, n + t) if t is not None else norm(q, x, n))
            p_noep = None if p is None else (p[0], p[1], None)  # e.p. right expires on a move elsewhere
            if x is not None:
                for xo in (x[1] if who == "W" else x[2]):
                    out.append(norm(p_noep, xo, n))
            if who == "W" and n > 0:
                out.append((p_noep, x, n - 1))
            if who == "B" and n < 0:
                out.append((p_noep, x, n + 1))
            return out

        p, x, n = norm(p0, X, 0)
        return win(p, x, n, mover)

    def sum_outcome(self, p0, X):
        lw, rw = self.sum_wins(p0, X, "W"), self.sum_wins(p0, X, "B")
        return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


# raw test games (own trees, no canonical simplification involved)
def RI(n):
    return ("i", n)


R0 = RI(0)
RSTAR = ("g", (R0,), (R0,))
RMINY1 = ("g", (("g", (RI(1),), (R0,)),), (R0,))     # {1|0 || 0} = -tiny(1)
RTINY1 = ("g", (R0,), (("g", (R0,), (RI(-1),)),))    # {0 || 0|-1}
RM1 = RI(-1)
RMUP = ("g", (RSTAR,), (R0,))                         # down = {* | 0}

POS = "W: c1 c3 d3 / B: c2 d4 d5 d6"


def main():
    p0 = parse(POS)
    print(f"Position {POS}")
    print("Hand check of the move list at the root (from own generator):")
    r = Rules()
    for side in "WB":
        for q in r.gen(p0, side):
            print(f"   {side}: -> {pstr(q)}")
    print()
    hdr = f"{'term':8s} {'race':9s} {'ep':4s} {'wrap':5s} {'BIG':>4s} | {'canonical value':22s} | ==tiny(1) ==1 | sum G+miny(1) G+(-1) G+* G+down | races doubles epcaps positions"
    print(hdr)
    print("-" * len(hdr))
    for term in ("passed", "promote"):
        races = ("count", "mover", "opponent") if term == "passed" else ("n/a",)
        for race in races:
            for ep in (True, False):
                for wrap in (False, True):
                    for big in (16, 256):
                        R_ = Rules(wrap=wrap, ep=ep, race=race if race != "n/a" else "count", term=term, big=big)
                        g = R_.value(p0)
                        s1 = R_.sum_outcome(p0, RMINY1)
                        s2 = R_.sum_outcome(p0, RM1)
                        s3 = R_.sum_outcome(p0, RSTAR)
                        s4 = R_.sum_outcome(p0, RMUP)
                        st = R_.stats
                        print(f"{term:8s} {race:9s} {str(ep):4s} {str(wrap):5s} {big:4d} | {show(g):22s} | "
                              f"{str(eq(g, TINY1)):5s}     {str(eq(g, ONE)):5s} | {s1:13s} {s2:6s} {s3:3s} {s4:6s} | "
                              f"{len(st['race']):5d} {len(st['double']):7d} {len(st['epcap']):6d} {len(st['positions']):9d}")
    print()
    print("Root options under the project convention (term=passed, race=count, ep on, flat, BIG=256):")
    R_ = Rules()
    for side in "WB":
        for q in R_.gen(p0, side):
            v = R_.child(q, side)
            print(f"   {side}: -> {pstr(q):40s} value {show(v)}")
    A = parse("W: c1 c4 d3 / B: c2 d4 d5 d6")
    print("Options of A = after c3-c4:")
    for side in "WB":
        for q in R_.gen(A, side):
            print(f"   {side}: -> {pstr(q):40s} value {show(R_.child(q, side))}")
    A3 = parse("W: c1 d3 / B: c2 c4 d4 d6")
    vA3 = R_.value(A3)
    print(f"A3 = after c3-c4 d5xc4: value {show(vA3)}; A3 == -BIG+*: {eq(vA3, make([integer(-256)], [integer(-256)]))};"
          f" A3 <= tiny(1): {le(vA3, TINY1)}")
    print(f"Value of A: {show(R_.value(A))}; reversibility check A^R=A3 <= G: {le(vA3, R_.value(p0))}")
    print()
    print("Interpretation: G == tiny(1) iff G + miny(1) is P (second-player win).")
    print("If G were 1: G+(-1) would be P and G+* would be L. If G = tiny(1): G+(-1) is R, G+* is N, G+down is N?"
          " (tiny(1) + down: computed above, not predicted here).")


if __name__ == "__main__":
    main()
