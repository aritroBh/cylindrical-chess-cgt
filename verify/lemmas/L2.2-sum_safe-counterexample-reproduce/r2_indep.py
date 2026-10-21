"""Independent re-implementation (verifier, round 2) of the two game models
needed for claim L2.2.  Imports nothing from cylcgt/, lemmas/ or crosscheck/.

  Wwin(pos, side)   alternating-play winner of the whole-board convention game
                    (first passer ends the game; races by a rule).
  S outcome         outcome of the sum model, computed WITHOUT a CGT engine:
                    the sum model is the game  (sum of live components) + k,
                    k an integer (sum of frozen +-BIG scores). For a fixed live
                    multiset Y the set of k for which Left wins is upward closed,
                    so it is described by two thresholds
                       aL(Y) = least k s.t. Left wins Y + k moving first,
                       aR(Y) = least k s.t. Left wins Y + k moving second,
                    and (derived by induction on |k| using the canonical integer
                    forms {k-1|} and {|k+1}):
                       aL = min(A, max(1, B+1)),   aR = max(B, min(0, A-1)),
                    A = min over Left pawn moves (aR(Y') - d),
                    B = max over Right pawn moves (aL(Y'') - d),
                    d = +-BIG if the moved component froze, else 0.
                    E.p. rights live inside their component (as in the project's
                    sum model): a right survives moves in other components.
Squares are (file, rank), file 0 = a, rank 1..m.
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
INF = float("inf")
FILES = "abcdefghijklmnop"


def parse(text):
    w, b = text.split("/")
    sqs = lambda part: frozenset((FILES.index(t[0]), int(t[1:])) for t in part.split(":")[1].split())
    return (sqs(w), sqs(b), None)


def adj(n, wrap, f):
    out = set()
    for g in (f - 1, f + 1):
        if wrap:
            out.add(g % n)
        elif 0 <= g < n:
            out.add(g)
    out.discard(f)
    return out


def is_passed(n, m, wrap, pos, side, sq):
    W, B, _ = pos
    f, r = sq
    fs = {f} | adj(n, wrap, f)
    if side == "W":
        return not any(g in fs and s > r for (g, s) in B)
    return not any(g in fs and s < r for (g, s) in W)


def has_passer(n, m, wrap, pos, side):
    mine = pos[0] if side == "W" else pos[1]
    return any(is_passed(n, m, wrap, pos, side, p) for p in mine)


def dist(n, m, wrap, pos, side):
    """count-rule promotion distance: nearest passed FRONT pawn (no own pawn
    ahead on its file); a double step from the start rank counts as one move."""
    mine = pos[0] if side == "W" else pos[1]
    best = INF
    for (f, r) in mine:
        if not is_passed(n, m, wrap, pos, side, (f, r)):
            continue
        if side == "W":
            if any(g == f and s > r for (g, s) in mine):
                continue
            d = (m - r) - (1 if r == 2 else 0)
        else:
            if any(g == f and s < r for (g, s) in mine):
                continue
            d = (r - 1) - (1 if r == m - 1 else 0)
        best = min(best, d)
    return best


def race_winner(n, m, wrap, pos, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if dist(n, m, wrap, pos, other) <= dist(n, m, wrap, pos, mover) else mover


def gen(n, m, wrap, epflag, pos, side):
    """All child positions after one move of `side`. pos[2] = (target, victim, entitled side)."""
    W, B, ep = pos
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    dr = 1 if side == "W" else -1
    home = 2 if side == "W" else m - 1
    use_ep = ep if (ep is not None and ep[2] == side) else None
    kids = set()

    def put(nm, nt, e=None):
        kids.add((frozenset(nm), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm), e))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + dr
        if r1 < 1 or r1 > m:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * dr
            if r == home and 1 <= r2 <= m and (f, r2) not in occ:
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if epflag else None
                put(rest | {(f, r2)}, theirs, e)
        for g in adj(n, wrap, f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif use_ep is not None and use_ep[0] == t and use_ep[1] in theirs and t not in occ:
                put(rest | {t}, theirs - {use_ep[1]})
    return kids


def comps(n, m, wrap, pos):
    W, B, ep = pos
    files = {f for f, _ in W | B}
    seen, out = set(), []
    for f0 in sorted(files):
        if f0 in seen:
            continue
        stack, grp = [f0], set()
        while stack:
            f = stack.pop()
            if f in grp:
                continue
            grp.add(f)
            stack.extend(g for g in adj(n, wrap, f) if g in files and g not in grp)
        seen |= grp
        e = ep if (ep is not None and ep[0][0] in grp) else None
        out.append((frozenset(p for p in W if p[0] in grp), frozenset(p for p in B if p[0] in grp), e))
    return out


class Game:
    def __init__(self, n, m, wrap, epflag, rule="count", BIG=256):
        self.n, self.m, self.wrap, self.ep, self.rule, self.BIG = n, m, wrap, epflag, rule, BIG
        self.Wwin = lru_cache(maxsize=None)(self._Wwin)
        self.thr = lru_cache(maxsize=None)(self._thr)

    def term(self, pos):
        g = (self.n, self.m, self.wrap)
        wp, bp = has_passer(*g, pos, "W"), has_passer(*g, pos, "B")
        return wp, bp

    # ---- whole-board convention game, alternating minimax -----------------
    def _Wwin(self, pos, side):
        wp, bp = self.term(pos)
        assert not (wp and bp)
        if wp:
            return "W"
        if bp:
            return "B"
        other = "B" if side == "W" else "W"
        for c in gen(self.n, self.m, self.wrap, self.ep, pos, side):
            cw, cb = self.term(c)
            if cw and cb:
                res = race_winner(self.n, self.m, self.wrap, c, side, self.rule)
            elif cw:
                res = "W"
            elif cb:
                res = "B"
            else:
                res = self.Wwin(c, other)
            if res == side:
                return side
        return other

    def W_outcome(self, pos):
        a = self.Wwin(pos, "W") == "W"
        b = self.Wwin(pos, "B") == "W"
        return {(True, True): "L", (False, False): "R", (True, False): "N", (False, True): "P"}[(a, b)]

    # ---- sum model, CGT-free -----------------------------------------------
    def _component_moves(self, Z, side):
        """(delta, list_of_new_live_components) for each move of side in Z."""
        out = []
        g = (self.n, self.m, self.wrap)
        for c in gen(self.n, self.m, self.wrap, self.ep, Z, side):
            cw, cb = self.term(c)
            if cw and cb:
                win = race_winner(*g, c, side, self.rule)
                out.append((self.BIG if win == "W" else -self.BIG, []))
            elif cw:
                out.append((self.BIG, []))
            elif cb:
                out.append((-self.BIG, []))
            else:
                out.append((0, comps(*g, c)))
        return out

    def _thr(self, Y):
        """Y: frozenset of live components. Returns (aL, aR)."""
        A, B = INF, -INF
        for Z in Y:
            rest = Y - {Z}
            for d, new in self._component_moves(Z, "W"):
                Y2 = rest | frozenset(new)
                A = min(A, self.thr(Y2)[1] - d)
            for d, new in self._component_moves(Z, "B"):
                Y2 = rest | frozenset(new)
                B = max(B, self.thr(Y2)[0] - d)
        aL = min(A, max(1, B + 1))
        aR = max(B, min(0, A - 1))
        return aL, aR

    def S_outcome(self, pos):
        wp, bp = self.term(pos)
        if wp != bp:
            return "L" if wp else "R"
        aL, aR = self.thr(frozenset(comps(self.n, self.m, self.wrap, pos)))
        a, b = 0 >= aL, 0 >= aR
        return {(True, True): "L", (False, False): "R", (True, False): "N", (False, True): "P"}[(a, b)]

    # ---- threats (for the mechanism check) ----------------------------------
    def threats(self, pos, _memo=None):
        memo = self.__dict__.setdefault("_tm", {})
        if pos in memo:
            return memo[pos]
        wp, bp = self.term(pos)
        out = set()
        if wp:
            out.add(1)
        if bp:
            out.add(-1)
        if not out:
            W_, B_, ep = pos
            for side in ("W", "B"):
                src = pos if (ep is not None and ep[2] == side) else (W_, B_, None)
                for c in gen(self.n, self.m, self.wrap, self.ep, src, side):
                    out |= self.threats(c)
        memo[pos] = frozenset(out)
        return memo[pos]


def show(pos):
    nm = lambda s: " ".join(f"{FILES[f]}{r}" for f, r in sorted(s))
    return f"W: {nm(pos[0])} / B: {nm(pos[1])}"
