"""Independent check of claim C3 (verifier, REFUTE lens).

Written from scratch: imports neither sumtest/ nor cylcgt/ nor crosscheck/.
Only the stdlib.  Positions are sets of (file, rank) tuples, not bitmasks.

Model (task spec, Elkies 1996):
  * White = Left, Black = Right, normal play.
  * Pawn moves: single step, double step from home rank (2 / 7) through an empty
    square, diagonal captures (wrapping on a cylinder), en passant (optional;
    across the seam on a cylinder).
  * After every move in G: if exactly one side has a passed pawn, G := +BIG/-BIG
    (absorbing: that side wins the whole sum, since |X| <= 3 here).
    Both sides -> race rule (count / mover / opponent).
  * e.p.-aware passer test ("aware"): a pawn that has just double-stepped and can
    be captured en passant right now is not (yet) counted as passed.
    "plain": textbook test, ignores any pending e.p. capture.
  * e.p. scope: "local"  = the e.p. right survives moves made in X and dies only at
                           the next move made in G;
                "global" = any move anywhere (in G or X) kills it (chess).  When it
                           dies through a move in X the position is re-tested for
                           passers, with the X-mover as "mover".
Outcome of G + X is computed by plain minimax over the explicit sum.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(200000)

NR = 8


# ---------------------------------------------------------------- abstract games
class G_:
    """Interned explicit short game {L | R}; options are G_ objects."""
    _tab = {}

    def __new__(cls, L=(), R=()):
        key = (tuple(sorted(id(x) for x in L)), tuple(sorted(id(x) for x in R)))
        if key in cls._tab:
            return cls._tab[key]
        o = super().__new__(cls)
        o.L, o.R = tuple(L), tuple(R)
        o._key = key
        cls._tab[key] = o
        return o


ZERO = G_()


def integer(n):
    g = ZERO
    for _ in range(abs(n)):
        g = G_([g], []) if n > 0 else G_([], [g])
    return g


_sum_cache = {}


def gsum(a, b):
    k = (id(a), id(b))
    if k in _sum_cache:
        return _sum_cache[k]
    L = [gsum(x, b) for x in a.L] + [gsum(a, y) for y in b.L]
    R = [gsum(x, b) for x in a.R] + [gsum(a, y) for y in b.R]
    r = G_(L, R)
    _sum_cache[k] = r
    return r


def gneg(a):
    return G_([gneg(x) for x in a.R], [gneg(x) for x in a.L])


STAR = G_([ZERO], [ZERO])
STAR2 = G_([ZERO, STAR], [ZERO, STAR])
STAR3 = G_([ZERO, STAR, STAR2], [ZERO, STAR, STAR2])
UP = G_([ZERO], [STAR])
DOWN = gneg(UP)
ONE, MONE = integer(1), integer(-1)
REF = [
    ("0", ZERO), ("*", STAR), ("*2", STAR2), ("*3", STAR3), ("up", UP), ("down", DOWN),
    ("up*", gsum(UP, STAR)), ("dup*", gsum(gsum(UP, UP), STAR)),
    ("1/2", G_([ZERO], [ONE])), ("-1/2", G_([MONE], [ZERO])), ("1", ONE), ("-1", MONE),
    ("{1|0}", G_([ONE], [ZERO])), ("+-1", G_([ONE], [MONE])),
    ("tiny1", G_([ZERO], [G_([ZERO], [MONE])])),
]


def sw(a, b):
    """{a | b} for integers a, b."""
    return G_([integer(a)], [integer(b)])


# H = {2+-1 | -2+-1} = {{3|1} | {-1|-3}}
H = G_([sw(3, 1)], [sw(-1, -3)])


# ---------------------------------------------------------------- pawn model
class Model:
    def __init__(self, files, wrap, ep=True, aware=True, race="count", scope="local",
                 race_double=True):
        self.F, self.wrap, self.ep, self.aware = files, wrap, ep, aware
        self.race, self.scope, self.race_double = race, scope, race_double
        self.race_hits = 0
        self.ep_captures = 0

    def adj(self, f):
        out = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    # ep = None or (owner, skipped_square, victim_square); stored only when the
    # opponent actually has a pawn able to take en passant.
    def moves(self, pos, white):
        W, B, ep = pos
        occ = W | B
        out = []
        mine, theirs = (W, B) if white else (B, W)
        d = 1 if white else -1
        home = 2 if white else NR - 1
        for (f, r) in mine:
            t = (f, r + d)
            if 1 <= r + d <= NR and t not in occ:
                out.append(self._mk(white, mine - {(f, r)} | {t}, theirs, None))
                t2 = (f, r + 2 * d)
                if r == home and t2 not in occ:
                    nep = None
                    if self.ep and any((g, r + 2 * d) in theirs for g in self.adj(f)):
                        nep = ("W" if white else "B", t, t2)
                    out.append(self._mk(white, mine - {(f, r)} | {t2}, theirs, nep))
            for g in self.adj(f):
                c = (g, r + d)
                if c in theirs:
                    out.append(self._mk(white, mine - {(f, r)} | {c}, theirs - {c}, None))
        if ep is not None and ep[0] == ("B" if white else "W"):
            _, skip, victim = ep
            for g in self.adj(skip[0]):
                s = (g, victim[1])
                if s in mine:
                    out.append(self._mk(white, mine - {s} | {skip}, theirs - {victim}, None))
        return out

    @staticmethod
    def _mk(white, mine, theirs, ep):
        mine, theirs = frozenset(mine), frozenset(theirs)
        return (mine, theirs, ep) if white else (theirs, mine, ep)

    def passers(self, pos, white):
        W, B, ep = pos
        mine, theirs = (W, B) if white else (B, W)
        out = []
        for (f, r) in mine:
            if self.aware and ep is not None and ep[0] == ("W" if white else "B") and ep[2] == (f, r):
                continue           # can be taken e.p. right now -> not yet passed
            span = {f} | self.adj(f)
            if white:
                blocked = any(g in span and s > r for (g, s) in theirs)
            else:
                blocked = any(g in span and s < r for (g, s) in theirs)
            if not blocked:
                out.append((f, r))
        return out

    def dist(self, sqs, white):
        best = 10 ** 6
        for (f, r) in sqs:
            if white:
                n = NR - r - (1 if (self.race_double and r == 2) else 0)
            else:
                n = r - 1 - (1 if (self.race_double and r == NR - 1) else 0)
            best = min(best, n)
        return best

    def resolve(self, pos, mover_white):
        wp, bp = self.passers(pos, True), self.passers(pos, False)
        if not wp and not bp:
            return pos
        if wp and not bp:
            return "L"
        if bp and not wp:
            return "R"
        self.race_hits += 1
        mover, opp = ("L", "R") if mover_white else ("R", "L")
        if self.race == "mover":
            return mover
        if self.race == "opponent":
            return opp
        dw, db = self.dist(wp, True), self.dist(bp, False)
        dm, do = (dw, db) if mover_white else (db, dw)
        return opp if do <= dm else mover

    def children(self, pos, white):
        return [self.resolve(c, white) for c in self.moves(pos, white)]

    def after_x_move(self, pos, mover_white):
        """State of G after a move made in X."""
        if self.scope == "local" or pos[2] is None:
            return pos
        return self.resolve((pos[0], pos[1], None), mover_white)

    # ------------------------------------------------ outcome of G + X
    def solver(self):
        @lru_cache(maxsize=None)
        def lw(g, x):            # Left moves first in g + x and wins
            if g == "L":
                return True
            if g == "R":
                return False
            for c in self.children(g, True):
                if not rw(c, x):
                    return True
            g2 = self.after_x_move(g, True)
            for xl in x.L:
                if not rw(g2, xl):
                    return True
            return False

        @lru_cache(maxsize=None)
        def rw(g, x):            # Right moves first in g + x and wins
            if g == "R":
                return True
            if g == "L":
                return False
            for c in self.children(g, False):
                if not lw(c, x):
                    return True
            g2 = self.after_x_move(g, False)
            for xr in x.R:
                if not lw(g2, xr):
                    return True
            return False

        def outcome(g, x):
            return {(True, False): "L", (False, True): "R", (True, True): "N",
                    (False, False): "P"}[(lw(g, x), rw(g, x))]
        return outcome

    def parse(self, text):
        W, B = set(), set()
        for part in text.split("/"):
            side, _, sqs = part.strip().partition(":")
            tgt = W if side.strip().upper() == "W" else B
            for t in sqs.split():
                tgt.add(("abcdefgh".index(t[0]), int(t[1:])))
        return (frozenset(W), frozenset(B), None)


def pure_outcome(x):
    @lru_cache(maxsize=None)
    def lw(a):
        return any(not rw(o) for o in a.L)

    @lru_cache(maxsize=None)
    def rw(a):
        return any(not lw(o) for o in a.R)
    return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lw(x), rw(x))]


def main():
    pos_txt = "W: a2 c2 / B: b7 d7"
    star2_vec = "".join(pure_outcome(gsum(STAR2, x)) for _, x in REF)
    h_vec = "".join(pure_outcome(gsum(H, x)) for _, x in REF)
    print("reference order :", " ".join(n for n, _ in REF))
    print("*2 + X vector   :", star2_vec)
    print("H  + X vector   :", h_vec, " (H = {{3|1}|{-1|-3}} = {2+-1 | -2+-1})")
    print("H == -H (same interned tree):", gneg(H) is H)
    # H canonical-form side conditions, by outcome tests (no CGT library):
    #   Left option {3|1} reversible iff its Right option 1 <= H, i.e. H - 1 >= 0
    #   i.e. Right moving first in H + (-1) loses.
    print("H-1 outcome (need not L/P for non-reversibility):", pure_outcome(gsum(H, MONE)))
    print()
    configs = []
    for files, wrap in ((4, False), (8, False), (8, True), (5, True)):
        for race in ("count", "mover", "opponent"):
            for ep, aware, scope in ((False, False, "local"), (True, False, "local"),
                                     (True, False, "global"), (True, True, "local"),
                                     (True, True, "global")):
                configs.append((files, wrap, race, ep, aware, scope))
    print("| board | race | e.p. | passer test | scope | vector | =*2 vec | =H vec | G+*2 | G+H | G+*2 (equality *2) | races | ep-caps |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for files, wrap, race, ep, aware, scope in configs:
        m = Model(files, wrap, ep=ep, aware=aware, race=race, scope=scope)
        out = m.solver()
        g = m.parse(pos_txt)
        assert not m.passers(g, True) and not m.passers(g, False)
        vec = "".join(out(g, x) for _, x in REF)
        gh = out(g, H)               # G + H is P  <=>  G = -H = H
        b = f"{files}{'cyl' if wrap else 'flat'}"
        print(f"| {b} | {race} | {'on' if ep else 'off'} | {'aware' if aware else 'plain'} | {scope} | {vec} | "
              f"{'yes' if vec == star2_vec else 'no'} | {'yes' if vec == h_vec else 'no'} | "
              f"{out(g, STAR2)} | {gh} | {'G=*2' if out(g, STAR2) == 'P' else 'G!=*2'}"
              f"{'; G=H' if gh == 'P' else ''} | {m.race_hits} | - |")
    print()
    # mechanism checks on the 4-file flat board, count rule
    print("Mechanism checks (4-file flat, count, e.p. on, local scope):")
    for aware in (False, True):
        m = Model(4, False, ep=True, aware=aware, race="count", scope="local")
        out = m.solver()
        tag = "aware" if aware else "plain"
        b5 = m.parse("W: a2 c2 / B: b5 d7")
        c4 = m.parse("W: a2 c4 / B: b7 d7")
        x = m.parse("W: a2 c2 / B: b4 d7")
        print(f"  [{tag}] after 1...b7-b5:  P? alone={out(b5, ZERO)}  +(2+-1)={out(b5, sw(3, 1))}"
              f"   (P alone => 0; P with +(2+-1) => -2+-1)")
        print(f"  [{tag}] after 1.c2-c4:    P? alone={out(c4, ZERO)}  +(-2+-1)={out(c4, sw(-1, -3))}"
              f"   (P alone => 0; P with +(-2+-1) => 2+-1)")
        print(f"  [{tag}] X=W a2 c2/B b4 d7: +3={out(x, integer(3))}   (P => X = -3)")
        # children of X after a2-a4
        for c in m.moves(x, True):
            if (0, 4) in c[0]:
                r = m.resolve(c, True)
                print(f"  [{tag}] X then a2-a4 resolves to: {r if isinstance(r, str) else 'unresolved, ep=' + str(r[2])}")


if __name__ == "__main__":
    main()
