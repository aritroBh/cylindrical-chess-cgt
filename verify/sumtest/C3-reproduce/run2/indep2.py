"""Second independent check (verifier C3-reproduce, run2) of claim C3.

Written from scratch for this verification; it does not import sumtest/ or
crosscheck/.  It imports cylcgt.cgt ONLY to name canonical values (display and
an equality test); every outcome is computed by plain minimax over explicit
sums with a game-tree class defined here.

Model (as stated in the task / claim):
  * White = Left, Black = Right, normal play, 8 ranks.
  * single step, double step from rank 2 / rank 7, diagonal captures (wrapping on
    a cylinder), en passant (also across the seam) when enabled.
  * After a move: exactly one side has a passed pawn -> that side wins G (+-BIG,
    which dominates every test game X used here, so the whole sum is won);
    both sides -> race rule ("count": the opponent of the mover moves first,
    fewer moves to promote wins, ties to the opponent, home-rank pawn gets the
    double-step credit; "mover"; "opponent").
  * passer conventions:
      textbook : the usual test, ignoring any pending e.p. right;
      aware    : a pawn that may be captured e.p. on the very next move is not
                 passed (the claim's convention);
      defer    : (extra, NOT the claim's convention) while an e.p. right is
                 pending no adjudication at all is made; it happens after the
                 next move in G (or, in global scope, after any move).
  * e.p. scope: local (the right lives in G until the next move in G, which is
    what a single CGT value of G can represent) or global (any move anywhere,
    including in X, cancels the right; on cancellation G is re-adjudicated with
    the X-mover as "mover").

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C3-reproduce/run2/indep2.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(200000)
NR = 8
FN = "abcdefgh"


class Tree:
    """Explicit game: frozensets of Tree options (hash-consed by id)."""
    _intern = {}

    def __new__(cls, L=(), R=()):
        key = (frozenset(L), frozenset(R))
        t = cls._intern.get(key)
        if t is None:
            t = object.__new__(cls)
            t.L, t.R = key
            cls._intern[key] = t
        return t


def tneg(t, memo={}):
    if t in memo:
        return memo[t]
    r = Tree([tneg(x) for x in t.R], [tneg(x) for x in t.L])
    memo[t] = r
    return r


def tsum(a, b, memo={}):
    k = (a, b)
    if k in memo:
        return memo[k]
    r = Tree([tsum(x, b) for x in a.L] + [tsum(a, y) for y in b.L],
             [tsum(x, b) for x in a.R] + [tsum(a, y) for y in b.R])
    memo[k] = r
    return r


Z = Tree()
S = Tree([Z], [Z])
S2 = Tree([Z, S], [Z, S])
S3 = Tree([Z, S, S2], [Z, S, S2])
UP = Tree([Z], [S])
DN = tneg(UP)
ONE = Tree([Z], [])
MONE = tneg(ONE)
HALF = Tree([Z], [ONE])
MHALF = tneg(HALF)
SW10 = Tree([ONE], [Z])
PM1 = Tree([ONE], [MONE])
TINY1 = Tree([Z], [Tree([Z], [MONE])])
TWO = Tree([ONE], [])
THREE = Tree([TWO], [])
MTWO, MTHREE = tneg(TWO), tneg(THREE)
REF = [("0", Z), ("*", S), ("*2", S2), ("*3", S3), ("up", UP), ("down", DN),
       ("up*", tsum(UP, S)), ("dup*", tsum(tsum(UP, UP), S)), ("1/2", HALF), ("-1/2", MHALF),
       ("1", ONE), ("-1", MONE), ("{1|0}", SW10), ("+-1", PM1), ("tiny1", TINY1)]
# H = {2+-1 | -2+-1} = {{3|1} | {-1|-3}}
H = Tree([Tree([THREE], [ONE])], [Tree([MONE], [MTHREE])])


class Model:
    def __init__(self, files, wrap, ep=True, conv="aware", race="count", scope="local"):
        assert conv in ("textbook", "aware", "defer") and scope in ("local", "global")
        self.F, self.wrap, self.ep, self.conv, self.race, self.scope = files, wrap, ep, conv, race, scope
        self.races = 0

    def nbrs(self, f):
        s = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                s.add(g)
        return s

    def parse(self, txt):
        w, b = txt.split("/")
        sq = lambda part: frozenset((FN.index(t[0]), int(t[1:])) for t in part.split(":")[1].split())
        return (sq(w), sq(b), None)

    # pos = (white set, black set, ep) ; ep = None or (colour_entitled, target, victim)
    def moves(self, pos, col):
        W, B, ep = pos
        me, op = (W, B) if col == "W" else (B, W)
        d, home = (1, 2) if col == "W" else (-1, 7)
        occ = W | B
        out = []

        def emit(nme, nop, e=None):
            out.append((nme, nop, e) if col == "W" else (nop, nme, e))

        for p in me:
            f, r = p
            rest = me - {p}
            a = (f, r + d)
            if 1 <= a[1] <= NR and a not in occ:
                emit(rest | {a}, op)
                b2 = (f, r + 2 * d)
                if r == home and b2 not in occ:
                    e = None
                    if self.ep and any((g, r + 2 * d) in op for g in self.nbrs(f)):
                        e = ("B" if col == "W" else "W", a, b2)
                    emit(rest | {b2}, op, e)
            for g in self.nbrs(f):
                t = (g, r + d)
                if t in op:
                    emit(rest | {t}, op - {t})
                if ep is not None and ep[0] == col and ep[1] == t:
                    emit(rest | {t}, op - {ep[2]})
        return out

    def is_passed(self, p, col, pos):
        W, B, ep = pos
        op = B if col == "W" else W
        f, r = p
        files = {f} | self.nbrs(f)
        ahead = range(r + 1, NR + 1) if col == "W" else range(1, r)
        return not any((g, t) in op for g in files for t in ahead)

    def passers(self, pos, col):
        W, B, ep = pos
        me = W if col == "W" else B
        out = []
        for p in me:
            if self.conv == "aware" and ep is not None and ep[2] == p:
                continue
            if self.is_passed(p, col, pos):
                out.append(p)
        return out

    def togo(self, ps, col):
        best = 99
        for (f, r) in ps:
            n = (NR - r - (r == 2)) if col == "W" else (r - 1 - (r == 7))
            best = min(best, n)
        return best

    def adjudicate(self, pos, mover):
        """None (game goes on) or 'L'/'R' (winner of G)."""
        if self.conv == "defer" and pos[2] is not None:
            return None
        wp, bp = self.passers(pos, "W"), self.passers(pos, "B")
        if not wp and not bp:
            return None
        if wp and not bp:
            return "L"
        if bp and not wp:
            return "R"
        self.races += 1
        mv = "L" if mover == "W" else "R"
        opp = "R" if mover == "W" else "L"
        if self.race == "mover":
            return mv
        if self.race == "opponent":
            return opp
        nw, nb = self.togo(wp, "W"), self.togo(bp, "B")
        nm, no = (nw, nb) if mover == "W" else (nb, nw)
        return opp if no <= nm else mv

    def child(self, pos, col):
        res = []
        for c in self.moves(pos, col):
            a = self.adjudicate(c, col)
            res.append(a if a else c)
        return res

    def cancel_ep(self, pos, mover):
        """Global scope: a move made outside G cancels a pending e.p. right."""
        if self.scope == "local" or pos in ("L", "R") or pos[2] is None:
            return pos
        p = (pos[0], pos[1], None)
        a = self.adjudicate(p, mover)
        return a if a else p


def outcome_of_sum(m, g0, X):
    """Outcome class of G + X by minimax; G given by state g0."""

    @lru_cache(maxsize=None)
    def win(g, x, col):
        # does `col` moving first in (g, x) win?
        if g == "L" or g == "R":
            return (g == "L") == (col == "W")       # BIG dominates every X used
        other = "B" if col == "W" else "W"
        for c in m.child(g, col):
            if not win(c, x, other):
                return True
        for xo in (x.L if col == "W" else x.R):
            if not win(m.cancel_ep(g, col), xo, other):
                return True
        return False

    lw, rw = win(g0, X, "W"), win(g0, X, "B")
    return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lw, rw)]


def canonical(m, g0):
    from cylcgt import cgt
    BIG = 256

    @lru_cache(maxsize=None)
    def v(g):
        if g == "L":
            return cgt.integer(BIG)
        if g == "R":
            return cgt.integer(-BIG)
        return cgt.make([v(c) for c in m.child(g, "W")], [v(c) for c in m.child(g, "B")])

    return v(g0)


def run(pos="W: a2 c2 / B: b7 d7", files=4, wrap=False, ep=True, conv="aware", race="count", scope="local",
        want_cgt=True):
    m = Model(files, wrap, ep, conv, race, scope)
    g0 = m.parse(pos)
    assert not m.passers(g0, "W") and not m.passers(g0, "B")
    vec = "".join(outcome_of_sum(m, g0, X) for _, X in REF)
    gmh = outcome_of_sum(m, g0, tneg(H))
    gms2 = outcome_of_sum(m, g0, S2)        # *2 = -*2
    cg = ""
    if want_cgt and scope == "local":
        from cylcgt import cgt
        v = canonical(m, g0)
        cg = f"cgt={cgt.show(v)} mean={cgt.mean(v)} temp={cgt.temperature(v)}"
    return vec, gmh, gms2, m.races, cg


if __name__ == "__main__":
    print("reference order:", " ".join(n for n, _ in REF))
    print("*2's own vector :", "".join(outcome_of_sum(Model(1, False), (frozenset(), frozenset(), None), tsum(S2, X))
                                     for _, X in REF))
    print("H's own vector  :", "".join(outcome_of_sum(Model(1, False), (frozenset(), frozenset(), None), tsum(H, X))
                                     for _, X in REF))
    boards = [(4, False, "4flat"), (8, False, "8flat"), (8, True, "8cyl"), (5, True, "5cyl")]
    for files, wrap, bn in boards:
        for race in ("count", "mover", "opponent"):
            for ep, conv in ((False, "textbook"), (True, "textbook"), (True, "aware"), (True, "defer")):
                for scope in ("local", "global"):
                    if not ep and scope == "global":
                        continue
                    vec, gmh, gms2, races, cg = run(files=files, wrap=wrap, ep=ep, conv=conv, race=race,
                                                    scope=scope, want_cgt=(files <= 5 or True))
                    print(f"{bn:5s} {race:8s} ep={'on ' if ep else 'off'} {conv:8s} {scope:6s} vec={vec} "
                          f"G+*2={vec[2]} G-H={gmh} G-*2={gms2} races={races} {cg}", flush=True)
