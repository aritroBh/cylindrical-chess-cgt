"""Independent re-implementation (verifier, not the worker) of two games on pawn
positions, written from the stated conventions without importing cylcgt or
crosscheck:

  W-game : whole-board convention game. First position in which exactly one
           side has a passed pawn ends the game (that side wins). A move that
           gives both sides passers is a race scored by RULE. E.p. rights are
           global and last exactly one move. No-move = loss.
  F-game : the sum model S = cylcgt.pawns.value, re-played as an explicit
           game form: live components (split at empty files, cylinder seam
           merged) plus one combined integer k (frozen +-BIG scores). A pawn
           move in component Z that makes Z terminal (one side passed, or a
           race) removes Z and adds +-BIG to k; otherwise Z is replaced by the
           components of its child. E.p. rights are LOCAL to the component
           (a stale right survives moves elsewhere), as in pawns._value.
           Integer part: Left may move k -> k-1 if k > 0, Right k -> k+1 if k < 0
           (canonical integer moves; outcome of a sum depends only on values).

Outcome of each game is found by plain alternating minimax (no CGT).
Squares are (file, rank), file 0 = a, rank 1..m.
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

BIG = 256
FILES = "abcdefghijklmnopqrstuvwxyz"


class Bd:
    __slots__ = ("n", "m", "wrap", "ep")

    def __init__(self, n, m, wrap, ep):
        self.n, self.m, self.wrap, self.ep = n, m, wrap, ep

    def key(self):
        return (self.n, self.m, self.wrap, self.ep)

    def adj(self, f):
        out = []
        for g in (f - 1, f + 1):
            if self.wrap:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return out


def parse(text):
    w, b = text.split("/")
    sq = lambda t: (FILES.index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()), None)


def fmt(p):
    nm = lambda s: f"{FILES[s[0]]}{s[1]}"
    return f"W: {' '.join(sorted(map(nm, p[0])))} / B: {' '.join(sorted(map(nm, p[1])))}" + (
        f" (ep {nm(p[2][0])} for {p[2][2]})" if p[2] else "")


def pawn_passed(bd, p, side, pawn):
    f, r = pawn
    enemy = p[1] if side == "W" else p[0]
    files = {f, *bd.adj(f)}
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
    """Moves of `side` from p. A right for `side` in p is usable; any other
    right is ignored. Children carry a right only after a double step."""
    W, B, ep = p
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else bd.m - 1
    other = "B" if side == "W" else "W"
    myep = ep if (ep is not None and ep[2] == side) else None
    out = []

    def put(nm, nt, e=None):
        q = (frozenset(nm), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm), e)
        if q not in out:
            out.append(q)

    for (f, r) in sorted(mine):
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
            elif myep is not None and myep[0] == t and myep[1] in theirs and t not in occ:
                put(rest | {t}, theirs - {myep[1]})
    return out


def term(bd, p):
    wp, bp = has_passer(bd, p, "W"), has_passer(bd, p, "B")
    if wp and bp:
        return 0
    if wp:
        return 1
    if bp:
        return -1
    return None


# ---------------------------------------------------------------- W-game

_wmemo = {}


def w_winner(bd, p, tm, rule):
    key = (bd.key(), p, tm, rule)
    if key in _wmemo:
        return _wmemo[key]
    t = term(bd, p)
    assert t is None, "terminal position passed to w_winner"
    other = "B" if tm == "W" else "W"
    res = other
    for c in gen(bd, p, tm):
        tc = term(bd, c)
        if tc == 0:
            r = race_winner(bd, c, tm, rule)
        elif tc == 1:
            r = "W"
        elif tc == -1:
            r = "B"
        else:
            r = w_winner(bd, c, other, rule)
        if r == tm:
            res = tm
            break
    _wmemo[key] = res
    return res


def outcome_from(fw, fb):
    """fw: winner when W moves first, fb: winner when B moves first."""
    if fw == "W" and fb == "W":
        return "L"
    if fw == "B" and fb == "B":
        return "R"
    return "N" if fw == "W" else "P"


def w_outcome(bd, p, rule):
    return outcome_from(w_winner(bd, p, "W", rule), w_winner(bd, p, "B", rule))


# ---------------------------------------------------------------- components

def comps(bd, p):
    W, B, ep = p
    files = sorted({f for f, _ in W | B})
    if not files:
        return []
    groups = []
    for f in files:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.n - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        s = set(g)
        e = ep if (ep is not None and ep[0][0] in s) else None
        out.append((frozenset(q for q in W if q[0] in s), frozenset(q for q in B if q[0] in s), e))
    return out


def ckey(c):
    return (tuple(sorted(c[0])), tuple(sorted(c[1])), c[2])


# ---------------------------------------------------------------- F-game

_tmemo = {}


def tau(bd, z):
    """Signs of passers reachable inside component z by moves of either side
    in any order (local e.p. rule: a right for s is usable by s; the other
    side's move in z strips it), stopping at terminal positions. Over-
    approximates what can happen to z inside the F-game."""
    key = (bd.key(), z)
    if key in _tmemo:
        return _tmemo[key]
    s = set()
    if has_passer(bd, z, "W"):
        s.add(1)
    if has_passer(bd, z, "B"):
        s.add(-1)
    if not s:
        for side in ("W", "B"):
            src = z if (z[2] is None or z[2][2] == side) else (z[0], z[1], None)
            for c in gen(bd, src, side):
                s |= tau(bd, c)
    r = frozenset(s)
    _tmemo[key] = r
    return r


def mpot(bd, live, side):
    if side == "W":
        return sum(bd.m - r for z in live for _, r in z[0])
    return sum(r - 1 for z in live for _, r in z[1])


_fmemo = {}


def f_winner(bd, live, k, tm, rule):
    """live: tuple of components (sorted by ckey), k: integer, tm: side to move."""
    key = (bd.key(), live, k, tm, rule)
    if key in _fmemo:
        return _fmemo[key]
    other = "B" if tm == "W" else "W"
    # sound shortcut (tempo argument): k > 0, no '-' threat anywhere live, and
    # k exceeds the number of moves Black can ever make -> Left wins; symmetric.
    th = set()
    for z in live:
        th |= tau(bd, z)
    if k > 0 and -1 not in th and k > mpot(bd, live, "B"):
        _fmemo[key] = "W"
        return "W"
    if k < 0 and 1 not in th and -k > mpot(bd, live, "W"):
        _fmemo[key] = "B"
        return "B"
    res = other
    opts = []
    if tm == "W" and k > 0:
        opts.append((live, k - 1))
    if tm == "B" and k < 0:
        opts.append((live, k + 1))
    for i, z in enumerate(live):
        rest = live[:i] + live[i + 1:]
        src = z if (z[2] is None or z[2][2] == tm) else (z[0], z[1], None)
        for c in gen(bd, src, tm):
            tc = term(bd, c)
            if tc == 0:
                opts.append((rest, k + (BIG if race_winner(bd, c, tm, rule) == "W" else -BIG)))
            elif tc is not None:
                opts.append((rest, k + tc * BIG))
            else:
                nl = tuple(sorted(rest + tuple(comps(bd, c)), key=ckey))
                opts.append((nl, k))
    for nl, nk in opts:
        if f_winner(bd, nl, nk, other, rule) == tm:
            res = tm
            break
    _fmemo[key] = res
    return res


def s_outcome(bd, p, rule):
    t = term(bd, p)
    assert t is None
    live = tuple(sorted(comps(bd, p), key=ckey))
    return outcome_from(f_winner(bd, live, 0, "W", rule), f_winner(bd, live, 0, "B", rule))


def clear():
    _wmemo.clear()
    _fmemo.clear()
    _tmemo.clear()


# ---------------------------------------------------------------- F-game, global e.p.
# Same as f_winner, but every move (pawn move anywhere, or integer move) deletes
# all e.p. rights except one created by that very move. Used only to test
# whether an e.p.-on disagreement S != W survives when stale rights are removed,
# i.e. whether it is caused by +-BIG cancellation rather than by stale rights.

_gmemo = {}


def _strip(z):
    return z if z[2] is None else (z[0], z[1], None)


def g_winner(bd, live, k, tm, rule):
    key = (bd.key(), live, k, tm, rule)
    if key in _gmemo:
        return _gmemo[key]
    other = "B" if tm == "W" else "W"
    th = set()
    for z in live:
        th |= tau(bd, z)
    if k > 0 and -1 not in th and k > mpot(bd, live, "B"):
        _gmemo[key] = "W"
        return "W"
    if k < 0 and 1 not in th and -k > mpot(bd, live, "W"):
        _gmemo[key] = "B"
        return "B"
    res = other
    opts = []
    stripped_all = tuple(sorted((_strip(z) for z in live), key=ckey))
    if tm == "W" and k > 0:
        opts.append((stripped_all, k - 1))
    if tm == "B" and k < 0:
        opts.append((stripped_all, k + 1))
    for i, z in enumerate(live):
        rest = tuple(_strip(y) for y in live[:i] + live[i + 1:])
        src = z if (z[2] is None or z[2][2] == tm) else _strip(z)
        for c in gen(bd, src, tm):
            tc = term(bd, c)
            if tc == 0:
                opts.append((tuple(sorted(rest, key=ckey)), k + (BIG if race_winner(bd, c, tm, rule) == "W" else -BIG)))
            elif tc is not None:
                opts.append((tuple(sorted(rest, key=ckey)), k + tc * BIG))
            else:
                nl = tuple(sorted(rest + tuple(comps(bd, c)), key=ckey))
                opts.append((nl, k))
    for nl, nk in opts:
        if g_winner(bd, nl, nk, other, rule) == tm:
            res = tm
            break
    _gmemo[key] = res
    return res


def s_outcome_global_ep(bd, p, rule):
    live = tuple(sorted(comps(bd, p), key=ckey))
    return outcome_from(g_winner(bd, live, 0, "W", rule), g_winner(bd, live, 0, "B", rule))
