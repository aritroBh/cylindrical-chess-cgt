"""Passer-certification tests used by the corrected convention CC, and the node census helpers.

S  (square rule): X's front passed pawn of promotion distance n beats every Y pawn's UNOBSTRUCTED distance d:
      X to move: n <= d      Y to move: n < d.        Sound in the frozen-king pawn game (proof in REPORT.md).
RP (run the passer): X only ever pushes that pawn; a search over all Y pawn moves shows Y cannot promote first.
      Exact for the strategy 'just run', sound, weaker than FG.
"""
import sys
sys.dont_write_bytecode = True
INF = 10 ** 6


def other(s): return "B" if s == "W" else "W"


def sdist(G, side, r):
    if side == "W":
        return G.H - r - (1 if r == 2 else 0)
    return r - 1 - (1 if r == G.H - 1 else 0)


def front(G, pos, side, s):
    W, B, _ = pos
    occ = W | B
    f, r = s
    rng = range(r + 1, G.H + 1) if side == "W" else range(1, r)
    return not any((f, t) in occ for t in rng)


def runners(G, pos, X, resp):
    """X's passed pawns that are the front pawn of their file"""
    return [s for s in G.passed_set(pos, X, resp) if front(G, pos, X, s)]


def S_cert(G, pos, mover, X, resp):
    rs = runners(G, pos, X, resp)
    if not rs:
        return False
    n = min(sdist(G, X, r) for f, r in rs)
    Y = other(X)
    ypawns = pos[1] if X == "W" else pos[0]
    d = min((sdist(G, Y, r) for f, r in ypawns), default=INF)
    return n <= d if mover == X else n < d


def _push(G, pos, X, s):
    """X's fastest push of the pawn on s: double step from the start rank if possible, else single. Returns (newpos, promoted)"""
    W, B, ep = pos
    f, r = s
    d = 1 if X == "W" else -1
    start = 2 if X == "W" else G.H - 1
    last = G.H if X == "W" else 1
    tgt = r + 2 * d if (r == start and (f, r + 2 * d) not in (W | B) and 1 <= r + 2 * d <= G.H) else r + d
    mine = (W if X == "W" else B) - {s} | {(f, tgt)}
    newpos = (frozenset(mine), B, None) if X == "W" else (W, frozenset(mine), None)
    return newpos, tgt == last, (f, tgt)


def RP_cert(G, pos, mover, X, resp):
    """True iff X wins by only pushing one of its front passed pawns, against every Y reply sequence"""
    for s in runners(G, pos, X, resp):
        if _rp(G, pos, mover, X, s):
            return True
    return False


def _rp(G, pos, side, X, s):
    # X wins from (pos, side to move) with X committed to pushing the pawn on s?
    Y = other(X)
    if side == X:
        newpos, promoted, s2 = _push(G, pos, X, s)
        if promoted:
            return True
        return _rp(G, newpos, Y, X, s2)
    mv = G.moves(pos, Y)
    if not mv:
        return True  # Y has no pawn move: a king move loses at once
    for lab, p, promo in mv:
        if promo:
            return False
        if s not in (p[0] if X == "W" else p[1]):
            return False  # the runner was captured (cannot happen for a passed pawn; kept as a guard)
        if not _rp(G, p, X, X, s):
            return False
    return True
