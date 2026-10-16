"""Verifier's own brute-force outcome solver for G + X (claim C1, REFUTE lens).

Written from scratch by the C1-refute verifier.  Imports neither sumtest/,
cylcgt/ nor crosscheck/.  No canonical forms: it plays the disjunctive sum
G + X out by exhaustive minimax and returns outcome classes.

G: pawn-only position, 8 ranks, F files, flat or cylinder.
X: explicit abstract game tree (textbook definitions; up* and dup* are built
   as explicit sums up+* and up+up+*).

Model (the passed-pawn = BIG model under test):
  * White = Left, Black = Right, normal play.
  * single step, double step from rank 2 / 7 through an empty square,
    diagonal captures (wrapping on a cylinder), optional en passant
    (also across the seam).
  * after any move in G: exactly one side owns a textbook passed pawn
    (no enemy pawn strictly ahead on the same or an adjacent file) ->
    that side wins the whole sum; both sides -> race rule:
      count:    mover's opponent moves first; fewer moves to promote wins,
                ties to the opponent; a passed pawn on its home rank gets
                one move of credit for the double step.
      mover / opponent: that side wins.
  * e.p. right scope: "P"      = survives moves in X, cleared by the next
                                 move in G (by either side);
                      "global" = cleared by any move anywhere.
"""
import itertools
import sys

sys.setrecursionlimit(100000)
LET = "abcdefghijklmnop"
RANKS = 8


class XU:
    """Universe of explicit abstract game nodes; children have smaller ids."""

    def __init__(self):
        self.L, self.R, self.idx = [], [], {}
        self._sum = {}

    def node(self, L, R):
        k = (tuple(sorted(set(L))), tuple(sorted(set(R))))
        if k not in self.idx:
            self.idx[k] = len(self.L)
            self.L.append(k[0])
            self.R.append(k[1])
        return self.idx[k]

    def add(self, a, b):
        k = (a, b)
        if k in self._sum:
            return self._sum[k]
        L = [self.add(x, b) for x in self.L[a]] + [self.add(a, y) for y in self.L[b]]
        R = [self.add(x, b) for x in self.R[a]] + [self.add(a, y) for y in self.R[b]]
        n = self.node(L, R)
        self._sum[k] = n
        return n


NAMES = ["0", "*", "*2", "*3", "up", "down", "up*", "dup*", "1/2", "-1/2", "1", "-1",
         "{1|0}", "+-1", "tiny1"]
TEXTBOOK = "PNNNLRNLLRLRNNL"


def build_refs():
    U = XU()
    z = U.node([], [])
    one = U.node([z], [])
    mone = U.node([], [z])
    s1 = U.node([z], [z])
    s2 = U.node([z, s1], [z, s1])
    s3 = U.node([z, s1, s2], [z, s1, s2])
    up = U.node([z], [s1])
    down = U.node([s1], [z])
    upstar = U.add(up, s1)
    dupstar = U.add(U.add(up, up), s1)
    half = U.node([z], [one])
    mhalf = U.node([mone], [z])
    sw = U.node([one], [z])
    pm1 = U.node([one], [mone])
    tiny = U.node([z], [U.node([z], [mone])])
    refs = [z, s1, s2, s3, up, down, upstar, dupstar, half, mhalf, one, mone, sw, pm1, tiny]
    return U, refs


class Board:
    def __init__(self, files, wrap, ep, rule, scope="P"):
        self.F, self.wrap, self.ep, self.rule, self.scope = files, wrap, ep, rule, scope
        self.races = 0
        n = files * RANKS
        self.sq = lambda f, r: f * RANKS + (r - 1)
        # forward spans for the passed test
        self.spanW = [0] * n
        self.spanB = [0] * n
        for f in range(files):
            fs = {f}
            for d in (-1, 1):
                g = self.nb(f, d)
                if g is not None:
                    fs.add(g)
            for r in range(1, RANKS + 1):
                mw = mb = 0
                for g in fs:
                    for s in range(1, RANKS + 1):
                        if s > r:
                            mw |= 1 << self.sq(g, s)
                        if s < r:
                            mb |= 1 << self.sq(g, s)
                self.spanW[self.sq(f, r)] = mw
                self.spanB[self.sq(f, r)] = mb

    def nb(self, f, d):
        g = f + d
        if self.wrap:
            return g % self.F
        return g if 0 <= g < self.F else None

    @staticmethod
    def bits(m):
        while m:
            low = m & -m
            yield low.bit_length() - 1
            m ^= low

    def passed_pawns(self, W, B, side):
        """list of squares of `side`'s passed pawns"""
        if side == "W":
            return [s for s in self.bits(W) if not (B & self.spanW[s])]
        return [s for s in self.bits(B) if not (W & self.spanB[s])]

    def dist(self, s, side):
        r = s % RANKS + 1
        if side == "W":
            return (RANKS - r) - (1 if r == 2 else 0)
        return (r - 1) - (1 if r == RANKS - 1 else 0)

    def resolve(self, W, B, mover):
        """None if undecided, else 'W' or 'B' = winner of the whole sum."""
        pw = self.passed_pawns(W, B, "W")
        pb = self.passed_pawns(W, B, "B")
        if pw and not pb:
            return "W"
        if pb and not pw:
            return "B"
        if not pw and not pb:
            return None
        self.races += 1
        other = "B" if mover == "W" else "W"
        if self.rule == "mover":
            return mover
        if self.rule == "opponent":
            return other
        dm = min(self.dist(s, mover) for s in (pw if mover == "W" else pb))
        do = min(self.dist(s, other) for s in (pw if other == "W" else pb))
        return other if do <= dm else mover

    def gen(self, state, side):
        """children of a G-move by `side`: list of ('W'|'B' decided winner) or new state"""
        W, B, ep = state  # ep: None or (target_sq, captured_sq, capturer_side)
        occ = W | B
        mine, theirs = (W, B) if side == "W" else (B, W)
        d = 1 if side == "W" else -1
        home = 2 if side == "W" else RANKS - 1
        epr = ep if (ep is not None and ep[2] == side) else None
        out = []

        def emit(nm, nt, nep=None):
            nW, nB = (nm, nt) if side == "W" else (nt, nm)
            res = self.resolve(nW, nB, side)
            out.append(res if res is not None else (nW, nB, nep))

        for s in self.bits(mine):
            f, r = divmod(s, RANKS)
            r += 1
            r1 = r + d
            if not (1 <= r1 <= RANKS):
                continue
            rest = mine & ~(1 << s)
            t1 = self.sq(f, r1)
            if not (occ >> t1) & 1:
                emit(rest | (1 << t1), theirs)
                if r == home:
                    t2 = self.sq(f, r + 2 * d)
                    if not (occ >> t2) & 1:
                        nep = None
                        if self.ep:
                            # e.p. right only if an enemy pawn stands beside t2
                            for dd in (-1, 1):
                                g = self.nb(f, dd)
                                if g is not None and (theirs >> self.sq(g, r + 2 * d)) & 1:
                                    nep = (t1, t2, "B" if side == "W" else "W")
                        emit(rest | (1 << t2), theirs, nep)
            for dd in (-1, 1):
                g = self.nb(f, dd)
                if g is None:
                    continue
                t = self.sq(g, r1)
                if (theirs >> t) & 1:
                    emit(rest | (1 << t), theirs & ~(1 << t))
                elif epr is not None and epr[0] == t:
                    emit(rest | (1 << t), theirs & ~(1 << epr[1]))
        return out


class Solver:
    def __init__(self, board, U):
        self.b, self.U = board, U
        self.N = len(U.L)
        self.ALL = (1 << self.N) - 1
        self.memo = {}

    def solve(self, state):
        """(LF, RF) bitmasks over X nodes: bit x of LF = Left moving first wins state+x."""
        m = self.memo.get(state)
        if m is not None:
            return m
        b, ALL = self.b, self.ALL
        PL = 0
        for c in b.gen(state, "W"):
            if c == "W":
                PL = ALL
                break
            if c == "B":
                continue
            PL |= ALL & ~self.solve(c)[1]
        PR = 0
        for c in b.gen(state, "B"):
            if c == "B":
                PR = ALL
                break
            if c == "W":
                continue
            PR |= ALL & ~self.solve(c)[0]
        # X moves
        if b.scope == "global" and state[2] is not None:
            XLF, XRF = self.solve((state[0], state[1], None))
            own = False
        else:
            own = True
        LF = RF = 0
        UL, UR = self.U.L, self.U.R
        for x in range(self.N):
            lf = (PL >> x) & 1
            if not lf:
                src = RF if own else XRF
                for y in UL[x]:
                    if not (src >> y) & 1:
                        lf = 1
                        break
            rf = (PR >> x) & 1
            if not rf:
                src = LF if own else XLF
                for y in UR[x]:
                    if not (src >> y) & 1:
                        rf = 1
                        break
            LF |= lf << x
            RF |= rf << x
        res = (LF, RF)
        self.memo[state] = res
        return res


def outcome_letter(LF, RF, x):
    l, r = (LF >> x) & 1, (RF >> x) & 1
    return "N" if l and r else "L" if l else "R" if r else "P"


def key(files, W, B):
    def nm(s):
        f, r = divmod(s, RANKS)
        return f"{LET[f]}{r + 1}"
    w = " ".join(sorted(nm(s) for s in Board.bits(W)))
    bb = " ".join(sorted(nm(s) for s in Board.bits(B)))
    return f"W: {w} / B: {bb}"


def family(files, wrap):
    """(1,1),(2,1),(1,2),(2,2) pawns on ranks 2..7, no passed pawn for either side."""
    b = Board(files, wrap, False, "count")
    sqs = [b.sq(f, r) for f in range(files) for r in range(2, 8)]
    out = []
    for nw, nb in ((1, 1), (2, 1), (1, 2), (2, 2)):
        for ws in itertools.combinations(sqs, nw):
            W = sum(1 << s for s in ws)
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                B = sum(1 << s for s in bs)
                if b.passed_pawns(W, B, "W") or b.passed_pawns(W, B, "B"):
                    continue
                out.append((W, B))
    return out


BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True),
          "cyl5": (5, True)}
