"""C4 verifier (reproduce lens), second independent implementation.

Everything about the pawn game is written here from scratch: board geometry,
move generation (single/double steps, wrapped captures, en passant), the
passed-pawn test (textbook or e.p.-aware), race resolution and the recursion.
It imports neither sumtest/ nor cylcgt.pawns.  Only cylcgt.cgt (canonical forms)
is used, to name the values.

Conventions:
  * White = Left, Black = Right, normal play, 8 ranks.
  * After every move: exactly one side has a passer -> +-BIG; both -> race rule.
  * e.p. right: created by a double step when an enemy pawn stands beside the
    arrival square; usable only as the opponent's very next move in this game
    (if the double-stepper moves again here, the right lapses).
  * aware=True: the pawn that can be captured e.p. right now is not counted as
    passed (it is still an obstacle for the other side's passer test).

Usage: python c4_indep_v2.py
"""
import sys
from functools import lru_cache

sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from cylcgt import cgt  # noqa: E402

BIG = 256
NR = 8
FILES = "abcdefgh"


class Game:
    def __init__(self, nfiles, wrap, ep=True, aware=True, rule="count", race_double=True):
        self.F, self.wrap, self.ep, self.aware, self.rule = nfiles, wrap, ep, aware, rule
        self.race_double = race_double
        self.val = lru_cache(maxsize=None)(self._val)

    def adj(self, f):
        out = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    @staticmethod
    def parse(text):
        w, b = text.split("/")
        conv = lambda part: frozenset((FILES.index(t[0]), int(t[1:])) for t in part.split(":")[1].split())
        return conv(w), conv(b)

    @staticmethod
    def show(W, B, ep=None):
        n = lambda s: f"{FILES[s[0]]}{s[1]}"
        txt = f"W: {' '.join(sorted(map(n, W)))} / B: {' '.join(sorted(map(n, B)))}"
        return txt + (f" [ep {n(ep[0])} for {ep[2]}]" if ep else "")

    # ---- moves -------------------------------------------------------------
    def moves(self, W, B, ep, side):
        """children (W', B', ep') for one move of side; ep = (target, victim, capturer)."""
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        home = 2 if side == "W" else NR - 1
        other = "B" if side == "W" else "W"
        out = []

        def emit(m, t, e=None):
            out.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))

        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            if not 1 <= r1 <= NR:
                continue
            if (f, r1) not in occ:
                emit(rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == home and (f, r2) not in occ:
                    e = None
                    if self.ep and any((g, r2) in theirs for g in self.adj(f)):
                        e = ((f, r1), (f, r2), other)
                    emit(rest | {(f, r2)}, theirs, e)
            for g in self.adj(f):
                if (g, r1) in theirs:
                    emit(rest | {(g, r1)}, theirs - {(g, r1)})
        if ep and ep[2] == side:
            target, victim, _ = ep
            for (f, r) in mine:
                if r == victim[1] and target[0] in self.adj(f):
                    emit((mine - {(f, r)}) | {target}, theirs - {victim})
        return list(dict.fromkeys(out))

    # ---- passers -------------------------------------------------------------
    def passers(self, W, B, ep, side):
        mine, theirs = (W, B) if side == "W" else (B, W)
        if self.aware and ep and ep[2] != side and ep[1] in mine:
            mine = mine - {ep[1]}
        res = []
        for (f, r) in mine:
            span = {f} | self.adj(f)
            if side == "W":
                blocked = any(g in span and s > r for (g, s) in theirs)
            else:
                blocked = any(g in span and s < r for (g, s) in theirs)
            if not blocked:
                res.append((f, r))
        return res

    def dist(self, sqs, side):
        if side == "W":
            return min(NR - r - (1 if self.race_double and r == 2 else 0) for _, r in sqs)
        return min(r - 1 - (1 if self.race_double and r == NR - 1 else 0) for _, r in sqs)

    def after(self, W, B, ep, mover):
        wp, bp = self.passers(W, B, ep, "W"), self.passers(W, B, ep, "B")
        if wp and not bp:
            return cgt.integer(BIG)
        if bp and not wp:
            return cgt.integer(-BIG)
        if wp and bp:
            other = "B" if mover == "W" else "W"
            if self.rule == "mover":
                win = mover
            elif self.rule == "opponent":
                win = other
            else:
                dm = self.dist(wp if mover == "W" else bp, mover)
                do = self.dist(bp if mover == "W" else wp, other)
                win = other if do <= dm else mover
            return cgt.integer(BIG if win == "W" else -BIG)
        return self.val(W, B, ep)

    def _val(self, W, B, ep):
        # the e.p. right is only for the capturer's immediate move: when the
        # other side moves again here it lapses (moves() ignores it then)
        L = [self.after(*c, "W") for c in self.moves(W, B, ep, "W")]
        R = [self.after(*c, "B") for c in self.moves(W, B, ep, "B")]
        return cgt.make(L, R)

    def value(self, text):
        W, B = self.parse(text)
        return self.val(W, B, None)


def opts(g, text):
    W, B = g.parse(text)
    for side in "WB":
        for c in g.moves(W, B, None, side):
            v = g.after(*c, side)
            print(f"      {side} -> {g.show(*c)} : {cgt.show(v)}")


if __name__ == "__main__":
    X = "W: a2 c2 / B: b4 d7"
    Y = "W: a2 c2 / B: b5 d7"
    G = "W: a2 c2 / B: b7 d7"
    for wrap in (False, True):
        for rule in ("count", "mover", "opponent"):
            for aware in (False, True):
                g = Game(4, wrap, ep=True, aware=aware, rule=rule)
                tag = f"{'cyl4' if wrap else 'flat4'} {rule:8s} {'aware' if aware else 'plain'}"
                vals = [cgt.show(g.value(t)) for t in (X, Y, G)]
                print(f"{tag}: X={vals[0]:14s} Y(b5)={vals[1]:10s} G={vals[2]}")
    for aware in (False, True):
        g = Game(4, False, ep=True, aware=aware, rule="count")
        print(f"\noptions of X, flat4 count {'aware' if aware else 'plain'}:")
        opts(g, X)
        W, B = g.parse(X)
        a4 = [c for c in g.moves(W, B, None, "W") if (0, 4) in c[0]][0]
        print("   after a2-a4:", g.show(*a4), "W passers", g.passers(*a4, "W"), "B passers", g.passers(*a4, "B"))
        if aware:
            print("   value of the a2-a4 node:", cgt.show(g.val(*a4)))
            for c in g.moves(*a4, "B"):
                print("     B reply", g.show(*c), ":", cgt.show(g.after(*c, "B")))
        print(f"  options of G, flat4 count {'aware' if aware else 'plain'}:")
        opts(g, G)
    # no e.p. at all, for reference
    for rule in ("count", "opponent"):
        g = Game(4, False, ep=False, aware=False, rule=rule)
        print(f"\nflat4 {rule} NO e.p.: X={cgt.show(g.value(X))} Y={cgt.show(g.value(Y))} G={cgt.show(g.value(G))}")
