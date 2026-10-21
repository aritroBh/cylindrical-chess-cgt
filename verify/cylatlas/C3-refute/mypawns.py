"""Independent pawn-game model for the C3 check (does not import cylcgt).

Model (re-implemented from the stated conventions):
  * 8 ranks; White moves up, Black down; double step from rank 2 / 7; e.p. on.
  * a pawn is passed if no enemy pawn stands on its own or an adjacent file
    strictly ahead of it; a position where exactly one side has a passer is
    worth +BIG / -BIG; a move that leaves both sides a passer is a race,
    scored by the "count" rule (opponent of the mover moves first; each side's
    distance is the min over its passed front-of-file pawns of
    ranks-to-go, minus 1 if a double step is still available; opponent wins ties).
  * Components (maximal runs of occupied files; on a ring all files) are
    disjunctive summands.  An e.p. right lives in its component and is usable
    only by the side named in it.
Geometry: ('flat',) = unbounded strip (no pawns outside the component) or
('ring', n) = n-file cylinder with every file occupied.
"""
from __future__ import annotations

import os

import mycgt as C

BIG = int(os.environ.get("MYBIG", "256"))
# WHOLE=1: no decomposition; a passer anywhere ends the whole position and an
# e.p. right dies after any move anywhere (exact for the position played alone).
WHOLE = os.environ.get("WHOLE", "0") == "1"
RACE = os.environ.get("RACE", "count")  # count | mover | opponent
EP = os.environ.get("EP", "1") == "1"
RANKS = 8
WIN = None
LOSS = None


def init():
    global WIN, LOSS
    WIN = C.num(BIG)
    LOSS = C.num(-BIG)


init()


def nbrs(geom, f):
    if geom[0] == "ring":
        n = geom[1]
        return ((f - 1) % n, (f + 1) % n)
    return (f - 1, f + 1)


def has_passer(geom, mine, theirs, side):
    for f, r in mine:
        a, b = nbrs(geom, f)
        if side == "W":
            if not any((g == f or g == a or g == b) and s > r for g, s in theirs):
                return True
        else:
            if not any((g == f or g == a or g == b) and s < r for g, s in theirs):
                return True
    return False


def passers(geom, W, B):
    return has_passer(geom, W, B, "W"), has_passer(geom, B, W, "B")


def dist(geom, W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = set(W) | set(B)
    best = 10 ** 6
    for f, r in mine:
        a, b = nbrs(geom, f)
        if side == "W":
            if any((g == f or g == a or g == b) and s > r for g, s in theirs):
                continue
            if any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                continue
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            if any((g == f or g == a or g == b) and s < r for g, s in theirs):
                continue
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        best = min(best, d)
    return best


def gen_moves(geom, W, B, ep, side):
    """list of (W', B', ep') after one move by side."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = set(W) | set(B)
    tset = set(theirs)
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else RANKS - 1
    other = "B" if side == "W" else "W"
    out = []
    seen = set()

    def emit(nm, nt, nep):
        nm = tuple(sorted(nm))
        nt = tuple(sorted(nt))
        k = (nm, nt, nep)
        if k in seen:
            return
        seen.add(k)
        if side == "W":
            out.append((nm, nt, nep))
        else:
            out.append((nt, nm, nep))

    for p in mine:
        f, r = p
        rest = [q for q in mine if q != p]
        r1 = r + d
        if not (1 <= r1 <= RANKS):
            continue
        if (f, r1) not in occ:
            emit(rest + [(f, r1)], list(theirs), None)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= RANKS and (f, r2) not in occ:
                emit(rest + [(f, r2)], list(theirs), (f, r1, r2, other) if EP else None)
        for g in set(nbrs(geom, f)):
            t = (g, r1)
            if t in tset:
                emit(rest + [t], [q for q in theirs if q != t], None)
            elif ep is not None and ep[3] == side and (ep[0], ep[1]) == t:
                cap = (ep[0], ep[2])
                emit(rest + [t], [q for q in theirs if q != cap], None)
    return out


def _useful_ep(geom, W, B, ep):
    if ep is None:
        return None
    f, rt, rc, side = ep
    mine = W if side == "W" else B
    a, b = nbrs(geom, f)
    if (a, rc) in mine or (b, rc) in mine:
        return ep
    return None


def _flat_norm(W, B, ep):
    fs = [f for f, _ in W] + [f for f, _ in B]
    lo, hi = min(fs), max(fs)
    W1 = tuple(sorted((f - lo, r) for f, r in W))
    B1 = tuple(sorted((f - lo, r) for f, r in B))
    e1 = None if ep is None else (ep[0] - lo, ep[1], ep[2], ep[3])
    W2 = tuple(sorted((hi - f, r) for f, r in W))
    B2 = tuple(sorted((hi - f, r) for f, r in B))
    e2 = None if ep is None else (hi - ep[0], ep[1], ep[2], ep[3])
    k1 = (W1, B1, e1 or ())
    k2 = (W2, B2, e2 or ())
    return min(k1, k2)


def _ring_norm(n, W, B, ep):
    best = None
    for s in (1, -1):
        for k in range(n):
            W1 = tuple(sorted(((s * f + k) % n, r) for f, r in W))
            B1 = tuple(sorted(((s * f + k) % n, r) for f, r in B))
            e1 = () if ep is None else (((s * ep[0] + k) % n), ep[1], ep[2], ep[3])
            kk = (W1, B1, e1)
            if best is None or kk < best:
                best = kk
    return best


def components(geom, W, B, ep):
    """list of (geom, W, B, ep) canonical component keys."""
    occ = sorted({f for f, _ in W} | {f for f, _ in B})
    if geom[0] == "ring":
        n = geom[1]
        if len(occ) == n:
            ep = _useful_ep(geom, W, B, ep)
            return [(geom, _ring_norm(n, W, B, ep))]
        e = next(f for f in range(n) if f not in set(occ))
        mp = lambda f: (f - e - 1) % n
        W = [(mp(f), r) for f, r in W]
        B = [(mp(f), r) for f, r in B]
        if ep is not None:
            ep = (mp(ep[0]), ep[1], ep[2], ep[3])
        occ = sorted({f for f, _ in W} | {f for f, _ in B})
    flat = ("flat",)
    runs = []
    for f in occ:
        if runs and f == runs[-1][-1] + 1:
            runs[-1].append(f)
        else:
            runs.append([f])
    out = []
    for run in runs:
        fs = set(run)
        cw = [p for p in W if p[0] in fs]
        cb = [p for p in B if p[0] in fs]
        cep = ep if (ep is not None and ep[0] in fs) else None
        cep = _useful_ep(flat, cw, cb, cep)
        out.append((flat, _flat_norm(cw, cb, cep)))
    return out


def whole_key(geom, W, B, ep):
    """normalised key of a whole position (no decomposition)."""
    occ = sorted({f for f, _ in W} | {f for f, _ in B})
    if geom[0] == "ring":
        n = geom[1]
        if len(occ) == n:
            ep = _useful_ep(geom, W, B, ep)
            return (geom, _ring_norm(n, W, B, ep))
        e = next(f for f in range(n) if f not in set(occ))
        mp = lambda f: (f - e - 1) % n
        W = [(mp(f), r) for f, r in W]
        B = [(mp(f), r) for f, r in B]
        if ep is not None:
            ep = (mp(ep[0]), ep[1], ep[2], ep[3])
        occ = sorted({f for f, _ in W} | {f for f, _ in B})
    # compress every gap of empty files to exactly one empty file
    newf = {}
    x = 0
    prev = None
    for f in occ:
        if prev is not None:
            x += 1 if f == prev + 1 else 2
        newf[f] = x
        prev = f
    W = [(newf[f], r) for f, r in W]
    B = [(newf[f], r) for f, r in B]
    if ep is not None:
        ep = (newf[ep[0]], ep[1], ep[2], ep[3]) if ep[0] in newf else None
    flat = ("flat",)
    ep = _useful_ep(flat, W, B, ep)
    return (flat, _flat_norm(W, B, ep))


MEMO: dict = {}
REACH: dict = {}   # comp key -> (can reach +BIG terminal, can reach -BIG terminal)
STATS = {"race": 0}


def pos_value(geom, W, B, ep):
    """value of a whole (sub)position with no race; returns (node, reach)."""
    wp, bp = passers(geom, W, B)
    if wp and bp:
        raise RuntimeError("race at pos_value")
    if wp:
        return WIN, (True, False)
    if bp:
        return LOSS, (False, True)
    if WHOLE:
        return comp_value(whole_key(geom, W, B, ep))
    tot = C.num(0)
    rw = rb = False
    for ck in components(geom, W, B, ep):
        v, re = comp_value(ck)
        tot = C.add(tot, v)
        rw |= re[0]
        rb |= re[1]
    return tot, (rw, rb)


def child_value(geom, W, B, ep, mover):
    wp, bp = passers(geom, W, B)
    if wp and bp:
        STATS["race"] += 1
        other = "B" if mover == "W" else "W"
        if RACE == "mover":
            winner = mover
        elif RACE == "opponent":
            winner = other
        else:
            winner = other if dist(geom, W, B, other) <= dist(geom, W, B, mover) else mover
        return (WIN, (True, False)) if winner == "W" else (LOSS, (False, True))
    return pos_value(geom, W, B, ep)


def comp_value(ck):
    r = MEMO.get(ck)
    if r is not None:
        return r
    geom, (W, B, ep) = ck
    ep = ep or None
    wp, bp = passers(geom, W, B)
    assert not wp and not bp, ck
    L = []
    R = []
    rw = rb = False
    for (W2, B2, e2) in gen_moves(geom, W, B, ep, "W"):
        v, re = child_value(geom, W2, B2, e2, "W")
        L.append(v)
        rw |= re[0]
        rb |= re[1]
    for (W2, B2, e2) in gen_moves(geom, W, B, ep, "B"):
        v, re = child_value(geom, W2, B2, e2, "B")
        R.append(v)
        rw |= re[0]
        rb |= re[1]
    g = C.make(L, R)
    r = (g, (rw, rb))
    MEMO[ck] = r
    return r


def parse(text):
    """'W: a2 c2 / B: b7 d7' -> (W, B) with 0-based files."""
    w, b = text.split("/")
    W = tuple(sorted(("abcdefghijklmnop".index(t[0]), int(t[1:])) for t in w.split(":")[1].split()))
    B = tuple(sorted(("abcdefghijklmnop".index(t[0]), int(t[1:])) for t in b.split(":")[1].split()))
    return W, B


def start_value(geom, W, B):
    """value of a root position (no e.p.); None if a passer exists at the root."""
    wp, bp = passers(geom, W, B)
    if wp or bp:
        return None
    return pos_value(geom, tuple(sorted(W)), tuple(sorted(B)), None)
