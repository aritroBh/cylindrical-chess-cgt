"""Referee (second round) -- my own pawn-only decisive-event game D, written from LOOPY Definition 1.5 / lemma L1.6 and
the verbal description of the count rule.  No import of cylcgt / lemmas / the investigator's or the first referee's code.
Position: (W, B, ep) with W, B frozensets of (file, rank) (rank 1..H), ep = None or (victim_square, capturer_side)
(the pawn on victim_square has just made a double step; capturer_side may capture it e.p. on the NEXT move only).
A pawn is "passed" if no enemy pawn stands strictly ahead on its own or an adjacent file, and it is not capturable e.p.
Terminal after a move: exactly one side has a passed pawn -> that side wins; both -> count race rule (fewer moves to
queen wins, ties go to the side that moves next, i.e. the non-mover); none -> play continues.  No move = loses."""
import sys
from functools import lru_cache
sys.setrecursionlimit(1000000)


class Bd:
    def __init__(s, w, h, wrap): s.w, s.h, s.wrap = w, h, wrap
    def f(s, x):
        if s.wrap: return x % s.w
        return x if 0 <= x < s.w else None


def epcap(bd, W, B, ep, side, sq):
    """can side `side` (owner of pawn at sq? no: the pawn at sq belongs to `side`) be captured e.p.?"""
    if ep is None: return False
    victim, capturer = ep
    if victim != sq or capturer == side: return False
    f, r = sq
    enemy = B if side == 'W' else W
    return any(bd.f(f + d) is not None and (bd.f(f + d), r) in enemy for d in (-1, 1))


def passed(bd, W, B, ep, side):
    mine, enemy = (W, B) if side == 'W' else (B, W)
    out = []
    for (f, r) in mine:
        fs = {f, bd.f(f - 1), bd.f(f + 1)} - {None}
        if side == 'W': blocked = any(g in fs and s > r for g, s in enemy)
        else: blocked = any(g in fs and s < r for g, s in enemy)
        if not blocked and not epcap(bd, W, B, ep, side, (f, r)): out.append((f, r))
    return out


def dist(bd, W, B, ep, side):
    """moves to queen of the best passed front pawn (count rule); big if none"""
    mine = W if side == 'W' else B
    occ = W | B
    best = 10 ** 6
    for (f, r) in passed(bd, W, B, ep, side):
        if side == 'W':
            if any((f, s) in occ for s in range(r + 1, bd.h + 1)): continue
            d = bd.h - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)): continue
            d = r - 1 - (1 if r == bd.h - 1 else 0)
        best = min(best, d)
    return best


def moves(bd, pos, side):
    """all pawn moves of `side` in pos = (W,B,ep); the opponent's ep right expires; returns list of new pos"""
    W, B, ep = pos
    mine, enemy = (W, B) if side == 'W' else (B, W)
    occ = W | B
    d = 1 if side == 'W' else -1
    start = 2 if side == 'W' else bd.h - 1
    myright = ep if (ep is not None and ep[1] == side) else None
    out = []

    def mk(nm, ne, nep):
        return (frozenset(nm), frozenset(ne), nep) if side == 'W' else (frozenset(ne), frozenset(nm), nep)

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not (1 <= r1 <= bd.h): continue
        if (f, r1) not in occ:
            out.append(mk(rest | {(f, r1)}, enemy, None))
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                out.append(mk(rest | {(f, r2)}, enemy, ((f, r2), 'B' if side == 'W' else 'W')))
        for df in (-1, 1):
            g = bd.f(f + df)
            if g is None: continue
            t = (g, r1)
            if t in enemy:
                out.append(mk(rest | {t}, enemy - {t}, None))
        if myright is not None:
            victim = myright[0]
            if victim[1] == r and victim[0] in (bd.f(f - 1), bd.f(f + 1)):
                out.append(mk(rest | {(victim[0], r1)}, enemy - {victim}, None))
    return list(dict.fromkeys(out))


def outcome_after(bd, pos, mover):
    """None if play continues, else 'W'/'B' = winner by the terminal"""
    W, B, ep = pos
    a = passed(bd, W, B, ep, 'W'); b = passed(bd, W, B, ep, 'B')
    if a and b:
        other = 'B' if mover == 'W' else 'W'
        dm, do = dist(bd, W, B, ep, mover), dist(bd, W, B, ep, other)
        return other if do <= dm else mover
    if a: return 'W'
    if b: return 'B'
    return None


def make(bd):
    @lru_cache(maxsize=None)
    def whole(pos, s):
        """winner ('W'/'B') of the whole-board D (chess e.p.), s to move, normal play"""
        o = 'B' if s == 'W' else 'W'
        for c in moves(bd, pos, s):
            t = outcome_after(bd, c, s)
            if t == s: return s
            if t is None and whole(c, o) == s: return s
        return o
    return whole
