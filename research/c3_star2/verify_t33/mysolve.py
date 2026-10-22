"""Verifier's own solver (written fresh from the rules, shares no code with cylcgt/ or frontier.c).

Game: pawn-only positions on an F-file x 8-rank cylinder.  A position is G; we decide the outcome of
G + H where H is an explicit short game (DAG of nodes), by exhaustive memoised search.

Model (as stated in cylcgt/pawns.py docstring and COMMON.md):
  - normal play, a side with no legal move loses;
  - after any move: if exactly one side has a passed pawn the game is over (that side wins, whatever the
    other summands); if both have, a race rule decides (mover moved last);
  - e.p. markers are kept per component (occupied-file connected region) until someone moves in it;
  - heap moves leave the pawn position (incl. e.p. markers) untouched.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

FILES = "abcdefgh"


def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def parse(text):
    w, b = text.split("/")
    W = tuple(sorted(sq(t) for t in w.split(":")[1].split()))
    B = tuple(sorted(sq(t) for t in b.split(":")[1].split()))
    return W, B


def name(s):
    return f"{FILES[s[0]]}{s[1]}"


class Solver:
    def __init__(self, F, race="count", ep_on=True, aware=True, ep_filter=None, R=8):
        self.F, self.R = F, R
        self.race, self.ep_on, self.aware = race, ep_on, aware
        self.ep_filter = ep_filter  # callable(side, from_sq, to_sq) -> bool; None = all e.p. captures allowed
        self.H = []  # nodes: (Lopts, Ropts)
        self.memo = {}
        self.nmoves = 0
        self._cache = {}

    # ---------------------------------------------------------------- explicit short games H
    def add_node(self, L, R):
        self.H.append((tuple(L), tuple(R)))
        return len(self.H) - 1

    def zero(self):
        return self._cached("zero", lambda: self.add_node([], []))

    def _cached(self, key, f):
        if key not in self._cache:
            self._cache[key] = f()
        return self._cache[key]

    def nimber(self, k):
        def mk():
            nodes = []
            for j in range(k + 1):
                nodes.append(self.add_node(nodes[:j], nodes[:j]))
            return nodes[k]
        return self._cached(("nim", k), mk)

    def integer(self, n):
        def mk():
            cur = self.zero()
            if n == 0:
                return cur
            for _ in range(abs(n)):
                cur = self.add_node([cur], []) if n > 0 else self.add_node([], [cur])
            return cur
        return self._cached(("int", n), mk)

    # ---------------------------------------------------------------- pawn mechanics
    def nbrs(self, f):
        return ((f - 1) % self.F, (f + 1) % self.F)

    def cone(self, f):
        return {f, (f - 1) % self.F, (f + 1) % self.F}

    def ep_capturable(self, EP, owner, s):
        # owner's pawn on s can be taken e.p. right now
        for tgt, vic, cap in EP:
            if vic == s and cap != owner:
                return True
        return False

    def passed_pawns(self, W, B, EP, side):
        mine, theirs = (W, B) if side == "W" else (B, W)
        out = []
        for (f, r) in mine:
            cf = self.cone(f)
            if side == "W":
                blocked = any(bf in cf and br > r for bf, br in theirs)
            else:
                blocked = any(bf in cf and br < r for bf, br in theirs)
            if blocked:
                continue
            if self.aware and self.ep_capturable(EP, side, (f, r)):
                continue
            out.append((f, r))
        return out

    def dist(self, W, B, EP, side):
        occ = set(W) | set(B)
        best = 10 ** 6
        for (f, r) in self.passed_pawns(W, B, EP, side):
            if side == "W":
                if any((f, s) in occ for s in range(r + 1, self.R + 1)):
                    continue
                d = self.R - r - (1 if r == 2 else 0)
            else:
                if any((f, s) in occ for s in range(1, r)):
                    continue
                d = r - 1 - (1 if r == self.R - 1 else 0)
            best = min(best, d)
        return best

    def verdict(self, W, B, EP, mover):
        """After `mover` moved. Returns 'W', 'B' if game decided for that colour, or None."""
        pw = self.passed_pawns(W, B, EP, "W")
        pb = self.passed_pawns(W, B, EP, "B")
        if pw and pb:
            opp = "B" if mover == "W" else "W"
            if self.race == "mover":
                return mover
            if self.race == "opponent":
                return opp
            dm, do = self.dist(W, B, EP, mover), self.dist(W, B, EP, opp)
            return opp if do <= dm else mover
        if pw:
            return "W"
        if pb:
            return "B"
        return None

    def comp_files(self, W, B, f):
        occf = {x for x, _ in W} | {x for x, _ in B}
        comp = {f}
        stack = [f]
        while stack:
            g = stack.pop()
            for h in self.nbrs(g):
                if h in occf and h not in comp:
                    comp.add(h)
                    stack.append(h)
        return comp

    def pawn_moves(self, W, B, EP, side):
        """List of (W', B', EP') reachable by `side`."""
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = set(W) | set(B)
        d = 1 if side == "W" else -1
        start = 2 if side == "W" else self.R - 1
        opp = "B" if side == "W" else "W"
        out = []
        seen = set()

        def emit(newmine, newtheirs, newEP):
            if side == "W":
                key = (tuple(sorted(newmine)), tuple(sorted(newtheirs)), newEP)
            else:
                key = (tuple(sorted(newtheirs)), tuple(sorted(newmine)), newEP)
            if key not in seen:
                seen.add(key)
                out.append(key)

        for (f, r) in mine:
            r1 = r + d
            if not (1 <= r1 <= self.R):
                continue
            comp = self.comp_files(W, B, f)
            baseEP = tuple(m for m in EP if m[0][0] not in comp)
            rest = [p for p in mine if p != (f, r)]
            if (f, r1) not in occ:
                emit(rest + [(f, r1)], list(theirs), baseEP)
                r2 = r + 2 * d
                if r == start and 1 <= r2 <= self.R and (f, r2) not in occ:
                    ep2 = baseEP
                    if self.ep_on and any((g, r2) in theirs for g in self.nbrs(f)):
                        ep2 = tuple(sorted(baseEP + (((f, r1), (f, r2), opp),)))
                    emit(rest + [(f, r2)], list(theirs), ep2)
            for g in self.nbrs(f):
                t = (g, r1)
                if t in theirs:
                    emit(rest + [t], [p for p in theirs if p != t], baseEP)
                else:
                    for tgt, vic, cap in EP:
                        if cap == side and tgt == t:
                            if self.ep_filter is not None and not self.ep_filter(side, (f, r), t):
                                continue
                            emit(rest + [t], [p for p in theirs if p != vic], baseEP)
        return out

    # ---------------------------------------------------------------- the search
    def wins(self, W, B, EP, h, side):
        """Does `side` (to move) win G + H[h]?"""
        key = (W, B, EP, h, side)
        v = self.memo.get(key)
        if v is not None:
            return v
        opp = "B" if side == "W" else "W"
        res = False
        for (nW, nB, nEP) in self.pawn_moves(W, B, EP, side):
            self.nmoves += 1
            vd = self.verdict(nW, nB, nEP, side)
            if vd == side:
                res = True
                break
            if vd == opp:
                continue
            if not self.wins(nW, nB, nEP, h, opp):
                res = True
                break
        if not res:
            Lopts, Ropts = self.H[h]
            for h2 in (Lopts if side == "W" else Ropts):
                if not self.wins(W, B, EP, h2, opp):
                    res = True
                    break
        self.memo[key] = res
        return res

    def outcome_with(self, W, B, EP, h):
        l = self.wins(W, B, EP, h, "W")
        r = self.wins(W, B, EP, h, "B")
        return "N" if l and r else "L" if l else "R" if r else "P"

    def nim_of(self, W, B, EP=(), kmax=8):
        """Return k such that G = *k (G + *k is a P-position), else None.  Also outcome of G alone."""
        for k in range(kmax):
            if self.outcome_with(W, B, EP, self.nimber(k)) == "P":
                return k
        return None


def solve_text(F, text, race="count", ep_on=True, aware=True, kmax=6, ep_filter=None):
    W, B = parse(text)
    s = Solver(F, race, ep_on, aware, ep_filter)
    oc = s.outcome_with(W, B, (), s.zero())
    k = s.nim_of(W, B, (), kmax)
    return oc, k, s


if __name__ == "__main__":
    import time
    t = time.time()
    oc, k, s = solve_text(3, "W: a2 a3 b2 / B: b7 c6 c7")
    print("C3 count/ep-on/aware: outcome", oc, "nimber", k, "states", len(s.memo), "t=%.1fs" % (time.time() - t))
