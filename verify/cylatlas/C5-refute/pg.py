"""Independent pawn-game model for the C5-refute check (does not import cylcgt).

A component is (kind, n, W, B, ep):
  kind 'F' = flat strip of n files (0..n-1), 'C' = ring of n files (wrap).
  W, B = sorted tuples of (file, rank); ranks 1..8, White moves up.
  ep = (target_sq, captured_sq, side_that_may_capture) or None; it is only
       recorded when an enemy pawn actually stands next to the double-stepped pawn.

Settings (module globals, call reset() after changing):
  RULE    'count' | 'mover' | 'opponent'   (race: both sides get a passer by one move)
  EP      True/False                        (double steps create e.p. rights)
  EPAWARE True/False                        (a pawn that may be taken e.p. is not passed)
  SPLIT   True  -> value of a split position = sum of its components (cylcgt's model)
          False -> whole-board game: first passer anywhere ends it (no splitting)
"""
from __future__ import annotations

import cg

BIG = 256
RANKS = 8
RULE = "count"
EP = True
EPAWARE = False
SPLIT = True

_memo: dict = {}
race_count = [0]


def reset():
    _memo.clear()
    race_count[0] = 0


def nbrs(kind, n, f):
    if kind == "C":
        return ((f - 1) % n, (f + 1) % n)
    return tuple(g for g in (f - 1, f + 1) if 0 <= g < n)


def ep_capturable(kind, n, W, B, ep, side, sq):
    if not (EPAWARE and ep is not None and ep[1] == sq and ep[2] != side):
        return False
    f, r = sq
    theirs = B if side == "W" else W
    return any((g, r) in theirs for g in nbrs(kind, n, f))


def pawn_passed(kind, n, W, B, ep, side, sq):
    f, r = sq
    files = (f,) + nbrs(kind, n, f)
    if side == "W":
        if any(g in files and s > r for (g, s) in B):
            return False
    else:
        if any(g in files and s < r for (g, s) in W):
            return False
    return not ep_capturable(kind, n, W, B, ep, side, sq)


def has_passer(kind, n, W, B, ep, side):
    mine = W if side == "W" else B
    return any(pawn_passed(kind, n, W, B, ep, side, p) for p in mine)


def dist(kind, n, W, B, ep, side):
    best = 10 ** 6
    mine = W if side == "W" else B
    for p in mine:
        if not pawn_passed(kind, n, W, B, ep, side, p):
            continue
        f, r = p
        if side == "W":
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        best = min(best, d)
    return best


def race_winner(kind, n, W, B, ep, mover):
    race_count[0] += 1
    other = "B" if mover == "W" else "W"
    if RULE == "mover":
        return mover
    if RULE == "opponent":
        return other
    # count: the opponent of the mover is first to move in the race and wins ties
    return other if dist(kind, n, W, B, ep, other) <= dist(kind, n, W, B, ep, mover) else mover


def gen(kind, n, W, B, ep, side):
    """Children (W', B', ep') after one move by side."""
    Ws, Bs = set(W), set(B)
    occ = Ws | Bs
    out = set()
    if side == "W":
        mine, theirs, d, start = Ws, Bs, 1, 2
    else:
        mine, theirs, d, start = Bs, Ws, -1, RANKS - 1
    my_ep = ep if (ep is not None and ep[2] == side) else None
    for (f, r) in mine:
        r1 = r + d
        if not (1 <= r1 <= RANKS):
            continue
        rest = mine - {(f, r)}
        if (f, r1) not in occ:
            out.add((frozenset(rest | {(f, r1)}), frozenset(theirs), None))
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                nep = None
                if EP and any((g, r2) in theirs for g in nbrs(kind, n, f)):
                    nep = ((f, r1), (f, r2), "B" if side == "W" else "W")
                out.add((frozenset(rest | {(f, r2)}), frozenset(theirs), nep))
        for g in nbrs(kind, n, f):
            t = (g, r1)
            if t in theirs:
                out.add((frozenset(rest | {t}), frozenset(theirs - {t}), None))
            elif my_ep is not None and my_ep[0] == t:
                out.add((frozenset(rest | {t}), frozenset(theirs - {my_ep[1]}), None))
    res = []
    for mn, th, nep in out:
        if side == "W":
            res.append((tuple(sorted(mn)), tuple(sorted(th)), nep))
        else:
            res.append((tuple(sorted(th)), tuple(sorted(mn)), nep))
    return res


def _remap(W, B, ep, fmap):
    W2 = tuple(sorted((fmap[f], r) for f, r in W))
    B2 = tuple(sorted((fmap[f], r) for f, r in B))
    ep2 = None
    if ep is not None and ep[0][0] in fmap:
        ep2 = ((fmap[ep[0][0]], ep[0][1]), (fmap[ep[1][0]], ep[1][1]), ep[2])
    return W2, B2, ep2


def components(kind, n, W, B, ep):
    occ = sorted({f for f, _ in W} | {f for f, _ in B})
    if not occ:
        return []
    if kind == "C" and len(occ) == n:
        return [("C", n, W, B, ep)]
    occs = set(occ)
    # runs of consecutive occupied files
    if kind == "C":
        e = next(f for f in range(n) if f not in occs)
        order = [(e + 1 + i) % n for i in range(n - 1)]
    else:
        order = list(range(n))
    runs, cur = [], []
    for f in order:
        if f in occs:
            cur.append(f)
        else:
            if cur:
                runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    comps = []
    for run in runs:
        fmap = {f: i for i, f in enumerate(run)}
        Wc = [(f, r) for f, r in W if f in fmap]
        Bc = [(f, r) for f, r in B if f in fmap]
        W2, B2, ep2 = _remap(Wc, Bc, ep, fmap)
        comps.append(("F", len(run), W2, B2, ep2))
    return comps


def whole(kind, n, W, B, ep):
    """Normalise a whole-board position (no splitting) to a key."""
    occ = {f for f, _ in W} | {f for f, _ in B}
    if kind == "C" and len(occ) < n:
        e = next(f for f in range(n) if f not in occ)
        order = [(e + 1 + i) % n for i in range(n - 1)]
    elif kind == "C":
        return ("C", n, W, B, ep)
    else:
        order = list(range(n))
    idx = [i for i, f in enumerate(order) if f in occ]
    lo, hi = idx[0], idx[-1]
    order = order[lo:hi + 1]
    fmap = {f: i for i, f in enumerate(order)}
    W2, B2, ep2 = _remap(W, B, ep, fmap)
    return ("F", len(order), W2, B2, ep2)


def child_value(kind, n, W, B, ep, mover):
    wp = has_passer(kind, n, W, B, ep, "W")
    bp = has_passer(kind, n, W, B, ep, "B")
    if wp and bp:
        w = race_winner(kind, n, W, B, ep, mover)
        return cg.integer(BIG if w == "W" else -BIG)
    if wp:
        return cg.integer(BIG)
    if bp:
        return cg.integer(-BIG)
    return position_value(kind, n, W, B, ep)


def position_value(kind, n, W, B, ep):
    """Value of a position with no passer for either side."""
    if SPLIT:
        g = cg.ZERO
        for c in components(kind, n, W, B, ep):
            g = cg.add(g, cval(*c))
        return g
    return cval(*whole(kind, n, W, B, ep))


def cval(kind, n, W, B, ep):
    key = (SPLIT, RULE, EP, EPAWARE, kind, n, W, B, ep)
    v = _memo.get(key)
    if v is not None:
        return v
    Ls = [child_value(kind, n, w, b, e, "W") for (w, b, e) in gen(kind, n, W, B, ep, "W")]
    Rs = [child_value(kind, n, w, b, e, "B") for (w, b, e) in gen(kind, n, W, B, ep, "B")]
    v = cg.make(Ls, Rs)
    _memo[key] = v
    return v


def root_value(kind, n, W, B):
    """Value of a root (no e.p. right); None if a passer stands at the start."""
    W = tuple(sorted(W)); B = tuple(sorted(B))
    if has_passer(kind, n, W, B, None, "W") or has_passer(kind, n, W, B, None, "B"):
        return None
    return position_value(kind, n, W, B, None)


FILES = "abcdefghijklmnop"


def parse(text):
    w, b = text.split("/")
    W = tuple(sorted((FILES.index(t[0]), int(t[1:])) for t in w.split(":")[1].split()))
    B = tuple(sorted((FILES.index(t[0]), int(t[1:])) for t in b.split(":")[1].split()))
    return W, B


def fmt(W, B):
    return ("W: " + " ".join(f"{FILES[f]}{r}" for f, r in sorted(W)) + " / B: "
            + " ".join(f"{FILES[f]}{r}" for f, r in sorted(B)))
