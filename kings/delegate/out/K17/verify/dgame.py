"""Referee's own implementation of the pawn-only decisive-event game D (whole-board, global e.p. right that
lasts one move, passer ends the game, 'count' race rule, normal play).  Written from the description in
LOOPY / notes/lemmas.md, sharing no code with cylcgt/ or lemmas/.   Ranks are 1-indexed (1..H), files 0..W-1.
pos = (frozenset white, frozenset black, ep) with ep = (target, captured, side_that_may_capture) or None."""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


class Bd:
    def __init__(self, w, h, wrap):
        self.w, self.h, self.wrap = w, h, wrap

    def nb(self, f, d):
        g = f + d
        if self.wrap:
            return g % self.w
        return g if 0 <= g < self.w else None


def ep_cap(bd, pos, side, sq):
    wp, bp, ep = pos
    if ep is None or ep[1] != sq or ep[2] == side:
        return False
    f, r = sq
    theirs = bp if side == 'W' else wp
    for d in (-1, 1):
        g = bd.nb(f, d)
        if g is not None and (g, r) in theirs:
            return True
    return False


def passed_set(bd, pos, side):
    wp, bp, ep = pos
    mine, theirs = (wp, bp) if side == 'W' else (bp, wp)
    res = []
    for (f, r) in mine:
        fs = {f}
        for d in (-1, 1):
            g = bd.nb(f, d)
            if g is not None: fs.add(g)
        if side == 'W':
            blocked = any(g in fs and s > r for g, s in theirs)
        else:
            blocked = any(g in fs and s < r for g, s in theirs)
        if not blocked and not ep_cap(bd, pos, side, (f, r)):
            res.append((f, r))
    return res


def promote_distance(bd, pos, side):
    wp, bp, ep = pos
    mine = wp if side == 'W' else bp
    occ = wp | bp
    best = None
    for (f, r) in mine:
        # passed against all enemy pawns (single-pawn test)
        single = (frozenset([(f, r)]), bp, ep) if side == 'W' else (wp, frozenset([(f, r)]), ep)
        fs = {f}
        for d in (-1, 1):
            g = bd.nb(f, d)
            if g is not None: fs.add(g)
        theirs = bp if side == 'W' else wp
        if side == 'W':
            blocked = any(g in fs and s > r for g, s in theirs)
        else:
            blocked = any(g in fs and s < r for g, s in theirs)
        if blocked: continue
        if ep_cap(bd, pos, side, (f, r)): continue
        if side == 'W':
            if any((f, s) in occ for s in range(r + 1, bd.h + 1)): continue
            d_ = bd.h - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)): continue
            d_ = r - 1 - (1 if r == bd.h - 1 else 0)
        best = d_ if best is None else min(best, d_)
    return best if best is not None else 10 ** 6


def terminal(bd, pos):
    a = passed_set(bd, pos, 'W'); b = passed_set(bd, pos, 'B')
    if a and b: return 0
    if a: return 1
    if b: return -1
    return None


def gen(bd, pos, side):
    """pawn moves of `side`; the opponent's e.p. right is dropped, own right used"""
    wp, bp, ep = pos
    ept = ep if (ep and ep[2] == side) else None
    mine, theirs = (wp, bp) if side == 'W' else (bp, wp)
    occ = wp | bp
    d = 1 if side == 'W' else -1
    start = 2 if side == 'W' else bd.h - 1
    out = []

    def emit(nm, nt, nep=None):
        out.append((frozenset(nm), frozenset(nt), nep) if side == 'W' else (frozenset(nt), frozenset(nm), nep))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not (1 <= r1 <= bd.h): continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= bd.h and (f, r2) not in occ:
                emit(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), 'B' if side == 'W' else 'W'))
        for df in (-1, 1):
            g = bd.nb(f, df)
            if g is None: continue
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif ept and ept[0] == t:
                emit(rest | {t}, theirs - {ept[1]})
    return list(dict.fromkeys(out))


def race_winner(bd, pos, mover):
    other = 'B' if mover == 'W' else 'W'
    dm = promote_distance(bd, pos, mover); do = promote_distance(bd, pos, other)
    return other if do <= dm else mover


def make_alt(bd):
    @lru_cache(maxsize=None)
    def alt(pos, to_move):
        t = terminal(bd, pos)
        if t == 1: return 'W'
        if t == -1: return 'B'
        if t == 0: raise RuntimeError('race at root')
        other = 'B' if to_move == 'W' else 'W'
        for c in gen(bd, pos, to_move):
            tc = terminal(bd, c)
            if tc == 0: res = race_winner(bd, c, to_move)
            elif tc is not None: res = 'W' if tc == 1 else 'B'
            else: res = alt(c, other)
            if res == to_move: return to_move
        return other
    return alt
