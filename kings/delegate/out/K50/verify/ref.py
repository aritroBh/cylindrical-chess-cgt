"""K50 referee: an independent pawn-game reference (not importing embed_check).
Whole-board context game with chess e.p. (a right lasts one move), cylcgt's e.p.-aware passed test, the count rule
for races, a side with no move loses. Squares are (file, rank), files 0-based, ranks 1..H."""

FILES = "abcdefghijklmnopqrstuvwxyz"


class Geo:
    def __init__(self, W, H, wrap):
        self.W, self.H, self.wrap = W, H, wrap

    def nb(self, f, d):
        g = f + d
        if self.wrap:
            return g % self.W
        return g if 0 <= g < self.W else None


def sq(t):
    return (FILES.index(t[0]), int(t[1:]))


def name(s):
    return f"{FILES[s[0]]}{s[1]}"


def children(G, w, b, ep, side):
    """ep = (target, victim) usable by `side` or None. Returns list of (w, b, ep_for_next)."""
    mine, theirs = (w, b) if side == "W" else (b, w)
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else G.H - 1
    occ = w | b
    out = []
    for p in mine:
        f, r = p
        r1 = r + d
        if not 1 <= r1 <= G.H:
            continue
        rest = mine - {p}
        if (f, r1) not in occ:
            out.append((rest | {(f, r1)}, theirs, None))
            if r == start and 1 <= r1 + d <= G.H and (f, r1 + d) not in occ:
                out.append((rest | {(f, r1 + d)}, theirs, ((f, r1), (f, r1 + d))))
        for dd in (-1, 1):
            g = G.nb(f, dd)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                out.append((rest | {t}, theirs - {t}, None))
            elif ep and ep[0] == t:
                out.append((rest | {t}, theirs - {ep[1]}, None))
    res = []
    for nm_, nt, nep in out:
        nw, nb_ = (frozenset(nm_), frozenset(nt)) if side == "W" else (frozenset(nt), frozenset(nm_))
        res.append((nw, nb_, nep))
    return res


def is_passed(G, w, b, ep, side, p):
    mine, theirs = (w, b) if side == "W" else (b, w)
    f, r = p
    fs = {f, G.nb(f, -1), G.nb(f, 1)} - {None}
    for g, s in theirs:
        if g in fs and ((s > r) if side == "W" else (s < r)):
            return False
    # e.p.-capturable right now: ep right exists for the opponent and the victim is p, with an adjacent capturer
    if ep and ep[1] == p:
        for dd in (-1, 1):
            g = G.nb(f, dd)
            if g is not None and (g, r) in theirs:
                return False
    return True


def dist(G, w, b, ep, side):
    mine = w if side == "W" else b
    occ = w | b
    best = 10**6
    for p in mine:
        if not is_passed(G, w, b, ep, side, p):
            continue
        f, r = p
        ahead = range(r + 1, G.H + 1) if side == "W" else range(1, r)
        if any((f, s) in occ for s in ahead):
            continue
        d = (G.H - r - (1 if r == 2 else 0)) if side == "W" else (r - 1 - (1 if r == G.H - 1 else 0))
        best = min(best, d)
    return best


def credit(G, w, b, ep, mover):
    """ep: the right in force for the next mover (the opponent of mover)."""
    other = "B" if mover == "W" else "W"
    pm = any(is_passed(G, w, b, ep, mover, p) for p in (w if mover == "W" else b))
    po = any(is_passed(G, w, b, ep, other, p) for p in (w if other == "W" else b))
    if not (pm or po):
        return None
    if pm and po:
        return other if dist(G, w, b, ep, other) <= dist(G, w, b, ep, mover) else mover
    return mover if pm else other


def dgame(G, w, b, ep, side, memo=None, cap=2_000_000):
    """True iff `side` to move wins the whole-board D-game."""
    if memo is None:
        memo = {}
    key = (w, b, ep, side)
    if key in memo:
        return memo[key]
    if len(memo) > cap:
        raise RuntimeError("cap")
    o = "B" if side == "W" else "W"
    res = False
    for nw, nb_, nep in children(G, w, b, ep, side):
        c = credit(G, nw, nb_, nep, side)
        if c is not None:
            if c == side:
                res = True
                break
            continue
        if not dgame(G, nw, nb_, nep, o, memo, cap):
            res = True
            break
    memo[key] = res
    return res
