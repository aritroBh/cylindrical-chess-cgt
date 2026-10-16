"""Independent, CGT-free re-implementation (theory-lens verifier, claim L2.2).

Written from the rules in notes/lemmas.md section 0 (M1-M4, passer test, race rules).
Imports nothing from cylcgt/, crosscheck/ or lemmas/.

Two games, both evaluated by plain alternating-play minimax:

  Wg  whole-board convention game: the first position in which exactly one side has a
      passer is terminal (that side wins); a move that gives both sides passers is a race,
      scored by the race rule; e.p. rights are global (they die after any other move).

  Sg  the sum model as a game FORM, played literally: state = (multiset of live components,
      integer n). A live component that acquires a passer (or a race) is removed and +-BIG
      (or the race score) is added to n. Otherwise the moved component is replaced by its
      own sub-components. n is a number game: Left may move n -> n-1 when n > 0, Right
      n -> n+1 when n < 0. E.p. rights live inside their component (the sum convention),
      so a right survives moves made in other components.

Positions: (frozenset white squares, frozenset black squares, ep) with squares (file, rank),
file 0 = a, ep = (target, captured_square, side_allowed) or None.
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

FILES = "abcdefgh"


class B:
    def __init__(self, n, m, cyl, ep):
        self.n, self.m, self.cyl, self.ep = n, m, cyl, ep

    def adj(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.cyl:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return out

    def key(self):
        return (self.n, self.m, self.cyl, self.ep)


def parse(text):
    w, b = text.split("/")
    sqs = lambda s: frozenset((FILES.index(t[0]), int(t[1:])) for t in s.split(":")[1].split())
    return (sqs(w), sqs(b), None)


def show(p):
    nm = lambda s: " ".join(sorted(f"{FILES[f]}{r}" for f, r in s))
    return f"W: {nm(p[0])} / B: {nm(p[1])}" + (f" (ep {p[2]})" if p[2] else "")


def pawn_passed(bd, p, side, sq):
    f, r = sq
    files = {f, *bd.adj(f)}
    enemy = p[1] if side == "W" else p[0]
    if side == "W":
        return not any(g in files and s > r for g, s in enemy)
    return not any(g in files and s < r for g, s in enemy)


def has_passer(bd, p, side):
    mine = p[0] if side == "W" else p[1]
    return any(pawn_passed(bd, p, side, q) for q in mine)


def dist(bd, p, side):
    mine = p[0] if side == "W" else p[1]
    best = 10 ** 6
    for f, r in mine:
        if not pawn_passed(bd, p, side, (f, r)):
            continue
        if side == "W":
            if any(g == f and s > r for g, s in mine):
                continue
            d = bd.m - r - (1 if r == 2 else 0)
        else:
            if any(g == f and s < r for g, s in mine):
                continue
            d = r - 1 - (1 if r == bd.m - 1 else 0)
        best = min(best, d)
    return best


def race_winner(bd, p, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if dist(bd, p, other) <= dist(bd, p, mover) else mover


def gen(bd, p, side):
    """All positions after one move of `side`. Only a right owned by `side` is usable."""
    W, Bk, ep = p
    mine, theirs = (W, Bk) if side == "W" else (Bk, W)
    occ = W | Bk
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else bd.m - 1
    other = "B" if side == "W" else "W"
    usable = ep if (ep and ep[2] == side) else None
    out = set()

    def put(nm, nt, e=None):
        out.add((frozenset(nm), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm), e))

    for (f, r) in mine:
        r1 = r + d
        if not 1 <= r1 <= bd.m:
            continue
        rest = mine - {(f, r)}
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= bd.m and (f, r2) not in occ:
                put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if bd.ep else None)
        for g in bd.adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif usable and usable[0] == t:
                put(rest | {t}, theirs - {usable[1]})
    return out


def comps(bd, p):
    W, Bk, ep = p
    occ = sorted({f for f, _ in W | Bk})
    if not occ:
        return []
    groups = []
    for f in occ:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if bd.cyl and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.n - 1:
        groups[0] = groups.pop() + groups[0]
    res = []
    for g in groups:
        fs = set(g)
        e = ep if (ep and ep[0][0] in fs) else None
        res.append((frozenset(q for q in W if q[0] in fs), frozenset(q for q in Bk if q[0] in fs), e))
    return res


def make_solvers(bd: B, rule: str, BIG: int):
    @lru_cache(maxsize=None)
    def Wg(p, tm):
        """winner ('W'/'B') of the whole-board game with `tm` to move; p non-terminal."""
        other = "B" if tm == "W" else "W"
        for c in gen(bd, p, tm):
            wp, bp = has_passer(bd, c, "W"), has_passer(bd, c, "B")
            if wp and bp:
                res = race_winner(bd, c, tm, rule)
            elif wp:
                res = "W"
            elif bp:
                res = "B"
            else:
                res = Wg(c, other)
            if res == tm:
                return tm
        return other

    def strip(p):
        return (p[0], p[1], None)

    @lru_cache(maxsize=None)
    def Sg(state, n, tm):
        """winner of the sum-model game form. state: sorted tuple of live components."""
        other = "B" if tm == "W" else "W"
        # integer move
        if tm == "W" and n > 0 and Sg(state, n - 1, other) == "W":
            return "W"
        if tm == "B" and n < 0 and Sg(state, n + 1, other) == "B":
            return "B"
        for i, c in enumerate(state):
            rest = state[:i] + state[i + 1:]
            # a right of the other side expires when tm moves in THIS component (local rights)
            src = c if (c[2] and c[2][2] == tm) else strip(c) if c[2] else c
            for ch in gen(bd, src, tm):
                wp, bp = has_passer(bd, ch, "W"), has_passer(bd, ch, "B")
                if wp and bp:
                    w = race_winner(bd, ch, tm, rule)
                    nn, ns = n + (BIG if w == "W" else -BIG), rest
                elif wp:
                    nn, ns = n + BIG, rest
                elif bp:
                    nn, ns = n - BIG, rest
                else:
                    nn, ns = n, rest + tuple(comps(bd, ch))
                ns = tuple(sorted(ns, key=repr))
                if Sg(ns, nn, other) == tm:
                    return tm
        return other

    def outcome(fn_first, fn_second):
        a, b = fn_first, fn_second
        if a == "W" and b == "W":
            return "L"
        if a == "B" and b == "B":
            return "R"
        return "N" if a == "W" else "P"

    def oW(p):
        return outcome(Wg(p, "W"), Wg(p, "B"))

    def oS(p):
        # top level of pawns.value: a global passer check first, then split
        wp, bp = has_passer(bd, p, "W"), has_passer(bd, p, "B")
        assert not (wp or bp)
        st = tuple(sorted(comps(bd, p), key=repr))
        return outcome(Sg(st, 0, "W"), Sg(st, 0, "B"))

    return oW, oS, Wg, Sg


def threats(bd, p, memo):
    if p in memo:
        return memo[p]
    s = set()
    if has_passer(bd, p, "W"):
        s.add(1)
    if has_passer(bd, p, "B"):
        s.add(-1)
    if not s:
        for side in ("W", "B"):
            src = p if (p[2] is None or p[2][2] == side) else (p[0], p[1], None)
            for c in gen(bd, src, side):
                s |= threats(bd, c, memo)
    memo[p] = frozenset(s)
    return memo[p]


def reach(bd, p):
    seen, st = {p}, [p]
    while st:
        x = st.pop()
        if has_passer(bd, x, "W") or has_passer(bd, x, "B"):
            continue
        for side in ("W", "B"):
            src = x if (x[2] is None or x[2][2] == side) else (x[0], x[1], None)
            for c in gen(bd, src, side):
                if c not in seen:
                    seen.add(c)
                    st.append(c)
    return seen
