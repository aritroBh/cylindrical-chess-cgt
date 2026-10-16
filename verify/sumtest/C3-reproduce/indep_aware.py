"""Independent re-implementation (verifier C3-reproduce) of the e.p.-aware
passed-pawn = BIG model, written without reading sumtest's move generator into it.

Representation: white/black = frozenset of (file, rank), file 0-based, rank 1..8;
ep = None or (skipped_square, victim_square, capturing_colour).

Checks, all by plain minimax on explicit sums (no canonical forms):
  * G + X outcome for the 15 reference X;
  * G - H is P, where H = {{3|1} | {-1|-3}}   (claim: G = {2+-1 | -2+-1});
  * G - *2 is P or not.
Also builds the canonical value with cylcgt.cgt for display only.
Scopes: 'local' (e.p. right lives in G until the next move in G) and
'global' (any move anywhere, including in X, kills the right).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C3-reproduce/indep_aware.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

NR = 8


class Model:
    def __init__(self, files, wrap, ep=True, aware=True, race="count"):
        self.F, self.wrap, self.ep, self.aware, self.race = files, wrap, ep, aware, race

    def nb(self, f):
        out = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    # ---------------- moves ----------------
    def moves(self, pos, colour):
        W, B, ep = pos
        mine, theirs = (W, B) if colour == "W" else (B, W)
        d = 1 if colour == "W" else -1
        home = 2 if colour == "W" else NR - 1
        occ = W | B
        res = []

        def put(newmine, newtheirs, e=None):
            if colour == "W":
                res.append((frozenset(newmine), frozenset(newtheirs), e))
            else:
                res.append((frozenset(newtheirs), frozenset(newmine), e))

        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            if 1 <= r1 <= NR and (f, r1) not in occ:
                put(rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == home and (f, r2) not in occ:
                    e = None
                    if self.ep and any((g, r2) in theirs for g in self.nb(f)):
                        e = ((f, r1), (f, r2), "B" if colour == "W" else "W")
                    put(rest | {(f, r2)}, theirs, e)
            for g in self.nb(f):
                t = (g, r1)
                if 1 <= r1 <= NR and t in theirs:
                    put(rest | {t}, theirs - {t})
                if ep is not None and ep[2] == colour and ep[0] == t:
                    assert ep[1] in theirs
                    put(rest | {t}, theirs - {ep[1]})
        return res

    # ---------------- passers ----------------
    def passers(self, pos, colour):
        W, B, ep = pos
        mine, theirs = (W, B) if colour == "W" else (B, W)
        out = []
        for (f, r) in mine:
            if self.aware and ep is not None and ep[1] == (f, r):
                continue  # capturable en passant right now: not yet passed
            span = {f} | self.nb(f)
            if colour == "W":
                blocked = any(g in span and s > r for (g, s) in theirs)
            else:
                blocked = any(g in span and s < r for (g, s) in theirs)
            if not blocked:
                out.append((f, r))
        return out

    def steps(self, sqs, colour):
        best = 99
        for (f, r) in sqs:
            if colour == "W":
                n = NR - r - (1 if r == 2 else 0)
            else:
                n = r - 1 - (1 if r == NR - 1 else 0)
            best = min(best, n)
        return best

    def resolve(self, pos, mover):
        wp, bp = self.passers(pos, "W"), self.passers(pos, "B")
        if not wp and not bp:
            return None
        if wp and not bp:
            return "L"
        if bp and not wp:
            return "R"
        me = "L" if mover == "W" else "R"
        opp = "R" if mover == "W" else "L"
        if self.race == "mover":
            return me
        if self.race == "opponent":
            return opp
        sw, sb = self.steps(wp, "W"), self.steps(bp, "B")
        s_me, s_opp = (sw, sb) if mover == "W" else (sb, sw)
        return opp if s_opp <= s_me else me

    def child(self, c, mover):
        r = self.resolve(c, mover)
        return r if r else c


# ---------------- explicit abstract games ----------------
# game = (tuple_of_left_options, tuple_of_right_options), hashable
Z = ((), ())


def g(L, R):
    return (tuple(L), tuple(R))


def integer(n):
    x = Z
    for _ in range(abs(n)):
        x = g([x], []) if n > 0 else g([], [x])
    return x


def gneg(x):
    return g([gneg(r) for r in x[1]], [gneg(l) for l in x[0]])


def gadd(a, b):
    return g([gadd(l, b) for l in a[0]] + [gadd(a, l) for l in b[0]],
             [gadd(r, b) for r in a[1]] + [gadd(a, r) for r in b[1]])


STAR = g([Z], [Z])
STAR2 = g([Z, STAR], [Z, STAR])
STAR3 = g([Z, STAR, STAR2], [Z, STAR, STAR2])
UP = g([Z], [STAR])
DOWN = gneg(UP)
ONE, MONE = integer(1), integer(-1)
REF = {
    "0": Z, "*": STAR, "*2": STAR2, "*3": STAR3, "up": UP, "down": DOWN,
    "up*": gadd(UP, STAR), "dup*": gadd(gadd(UP, UP), STAR),
    "1/2": g([Z], [ONE]), "-1/2": g([MONE], [Z]), "1": ONE, "-1": MONE,
    "{1|0}": g([ONE], [Z]), "+-1": g([ONE], [MONE]), "tiny1": g([Z], [g([Z], [MONE])]),
}
NAMES = list(REF)
H = g([g([integer(3)], [integer(1)])], [g([integer(-1)], [integer(-3)])])   # {2+-1 | -2+-1}


def solver(model, scope):
    """wins(gstate, x, colour): does `colour`, moving first in G + x, win?"""

    @lru_cache(maxsize=None)
    def wins(gs, x, colour):
        if gs == "L":
            return colour == "W"       # BIG dominates every x used here
        if gs == "R":
            return colour == "B"
        opp = "B" if colour == "W" else "W"
        # move in G
        for c in model.moves(gs, colour):
            if not wins(model.child(c, colour), x, opp):
                return True
        # move in x
        xo = x[0] if colour == "W" else x[1]
        if xo:
            gs2 = gs
            if scope == "global" and gs[2] is not None:
                gs2 = model.child((gs[0], gs[1], None), colour)
            for y in xo:
                if not wins(gs2, y, opp):
                    return True
        return False

    def outcome(start, x):
        l, r = wins(start, x, "W"), wins(start, x, "B")
        return {(1, 0): "L", (0, 1): "R", (1, 1): "N", (0, 0): "P"}[(l, r)]

    return outcome


def parse(text):
    W, B = set(), set()
    for part in text.split("/"):
        side, _, sqs = part.strip().partition(":")
        for t in sqs.split():
            (W if side.strip() == "W" else B).add(("abcdefgh".index(t[0]), int(t[1:])))
    return frozenset(W), frozenset(B), None


def cgt_value(model, start):
    from cylcgt import cgt

    @lru_cache(maxsize=None)
    def val(s):
        if s == "L":
            return cgt.integer(256)
        if s == "R":
            return cgt.integer(-256)
        return cgt.make([val(model.child(c, "W")) for c in model.moves(s, "W")],
                        [val(model.child(c, "B")) for c in model.moves(s, "B")])
    v = val(start)
    return cgt.show(v), cgt.mean(v), cgt.temperature(v)


def main():
    pos = "W: a2 c2 / B: b7 d7"
    for files, wrap in ((4, False), (8, False), (8, True), (5, True)):
        for race in ("count", "mover", "opponent"):
            for label, ep, aware in (("ep off", False, False), ("ep textbook", True, False), ("ep aware", True, True)):
                for scope in ("local", "global"):
                    if not ep and scope == "global":
                        continue
                    m = Model(files, wrap, ep=ep, aware=aware, race=race)
                    st = parse(pos)
                    out = solver(m, scope)
                    vec = "".join(out(st, REF[n]) for n in NAMES)
                    eqH = out(st, gneg(H))
                    eqS2 = out(st, STAR2)      # -*2 = *2
                    val = cgt_value(m, st) if scope == "local" else ("-", "-", "-")
                    print(f"{files}{'cyl' if wrap else 'flat'} {race:8s} {label:11s} {scope:6s} vec={vec} "
                          f"G-H:{eqH} G-*2:{eqS2} cgt={val[0]} mean={val[1]} temp={val[2]}")
    # mechanism positions (4 flat, count)
    for race in ("count",):
        for aware in (False, True):
            m = Model(4, False, ep=True, aware=aware, race=race)
            for p in ("W: a2 c2 / B: b4 d7", "W: a2 c2 / B: b5 d7", "W: a2 c4 / B: b7 d7"):
                print("mech", race, "aware" if aware else "textbook", p, cgt_value(m, parse(p)))


if __name__ == "__main__":
    main()
