"""Independent re-computation for claim C2 (verifier, REFUTE lens).

Written from scratch; imports neither cylcgt, crosscheck nor sumtest.
Whole-board outcome search of  G + X  where G is a pawn position and X an
explicit abstract game tree.  No canonical forms are used for the decisive
test: G = *2  <=>  G + *2 is a P-position (since -*2 = *2).

Model (passed pawn = +-BIG, Elkies 1996):
  * White = Left, Black = Right, normal play.
  * Pawns: single step, double step from home rank (2 / ranks-1), diagonal
    capture, optional en passant.
  * A state in which exactly one side owns a passed pawn is a win for that
    side (BIG dominates every X used here).  If both do, it is a race decided
    by the race rule, attributed to the player who made the last move.
  * passed test: textbook (no enemy pawn ahead on own/adjacent files) or
    e.p.-aware (a pawn that is the victim of a live e.p. right is not passed).
  * e.p. scope: "global" (any move anywhere kills the right, = chess),
    "local" (only the next move made in G kills it).
Race rules: count (opponent of last mover moves first; fewer moves wins; ties
to the opponent), mover (last mover wins), opponent (last mover loses).
Count variants: double-step credit on/off.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

LET = "abcdefghijklmnop"


class Cfg:
    def __init__(self, files=4, ranks=8, wrap=False, ep=True, aware=False,
                 scope="global", race="count", credit=True):
        self.files, self.ranks, self.wrap = files, ranks, wrap
        self.ep, self.aware, self.scope, self.race, self.credit = ep, aware, scope, race, credit

    def adj(self, f):
        out = []
        for g in (f - 1, f + 1):
            if self.wrap:
                out.append(g % self.files)
            elif 0 <= g < self.files:
                out.append(g)
        return out


def parse(s):
    w, b = s.split("/")
    sq = lambda t: (LET.index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()))


# ---------------------------------------------------------------- X trees
class Tree:
    """Explicit game tree node: (left options, right options)."""
    _intern = {}

    def __new__(cls, L=(), R=()):
        key = (tuple(sorted(id(x) for x in L)), tuple(sorted(id(x) for x in R)))
        if key in cls._intern:
            return cls._intern[key]
        t = super().__new__(cls)
        t.L, t.R = tuple(L), tuple(R)
        cls._intern[key] = t
        return t


ZERO = Tree()


def add(a, b, memo={}):
    k = (id(a), id(b))
    if k in memo:
        return memo[k]
    if a is ZERO:
        r = b
    elif b is ZERO:
        r = a
    else:
        r = Tree([add(x, b) for x in a.L] + [add(a, y) for y in b.L],
                 [add(x, b) for x in a.R] + [add(a, y) for y in b.R])
    memo[k] = r
    return r


def neg(a, memo={}):
    if id(a) in memo:
        return memo[id(a)]
    r = Tree([neg(x) for x in a.R], [neg(x) for x in a.L])
    memo[id(a)] = r
    return r


def refs():
    s1 = Tree([ZERO], [ZERO])
    s2 = Tree([ZERO, s1], [ZERO, s1])
    s3 = Tree([ZERO, s1, s2], [ZERO, s1, s2])
    one = Tree([ZERO], [])
    m1 = Tree([], [ZERO])
    up = Tree([ZERO], [s1])
    half = Tree([ZERO], [one])
    two = Tree([one], [])
    three = Tree([two], [])
    m2, m3 = neg(two), neg(three)
    pm1 = Tree([one], [m1])
    tiny1 = Tree([ZERO], [Tree([ZERO], [m1])])
    two_pm1 = Tree([three], [one])          # 2 +- 1 = {3|1}
    hyb = Tree([two_pm1], [neg(two_pm1)])   # {2+-1 | -2+-1}
    return {"0": ZERO, "*": s1, "*2": s2, "*3": s3, "up": up, "down": neg(up),
            "up*": add(up, s1), "dup*": add(add(up, up), s1), "1/2": half,
            "-1/2": neg(half), "1": one, "-1": m1, "{1|0}": Tree([one], [ZERO]),
            "+-1": pm1, "tiny1": tiny1, "hyb": hyb}


REF_ORDER = "0 * *2 *3 up down up* dup* 1/2 -1/2 1 -1 {1|0} +-1 tiny1".split()


# ---------------------------------------------------------------- pawn rules
def passers(cfg, W, B, ep):
    """Return (white_has_passer, black_has_passer, wset, bset)."""
    victim = ep[1] if (ep is not None and cfg.aware) else None
    wl, bl = [], []
    for (f, r) in W:
        if (f, r) == victim:
            continue
        fs = {f, *cfg.adj(f)}
        if not any(g in fs and s > r for (g, s) in B):
            wl.append((f, r))
    for (f, r) in B:
        if (f, r) == victim:
            continue
        fs = {f, *cfg.adj(f)}
        if not any(g in fs and s < r for (g, s) in W):
            bl.append((f, r))
    return wl, bl


def dist(cfg, side, pl, W, B):
    occ = W | B
    best = 10 ** 6
    for (f, r) in pl:
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, cfg.ranks + 1)):
                continue
            d = cfg.ranks - r - (1 if (cfg.credit and r == 2) else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if (cfg.credit and r == cfg.ranks - 1) else 0)
        best = min(best, d)
    return best


def resolve(cfg, W, B, ep, last_mover):
    wl, bl = passers(cfg, W, B, ep)
    if wl and not bl:
        return "W"
    if bl and not wl:
        return "B"
    if not wl and not bl:
        return None
    RACES.add((W, B, ep, last_mover))
    other = "B" if last_mover == "W" else "W"
    if cfg.race == "mover":
        return last_mover
    if cfg.race == "opponent":
        return other
    dw, db = dist(cfg, "W", wl, W, B), dist(cfg, "B", bl, W, B)
    d_other, d_mover = (dw, db) if other == "W" else (db, dw)
    return other if d_other <= d_mover else last_mover


RACES = set()


def pawn_moves(cfg, W, B, ep, side):
    """List of (W', B', ep') for `side`.  ep = (target, victim, capturer)."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    home = 2 if side == "W" else cfg.ranks - 1
    out = []
    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        assert 1 < r1 < cfg.ranks, "promotion reached: should have been resolved"
        def emit(nm, nt, nep=None):
            out.append((nm, nt, nep) if side == "W" else (nt, nm, nep))
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == home and (f, r2) not in occ:
                nep = None
                if cfg.ep:
                    cap = "B" if side == "W" else "W"
                    # store a right only if a capture is actually possible
                    if any((g, r2) in theirs for g in cfg.adj(f)):
                        nep = ((f, r1), (f, r2), cap)
                emit(rest | {(f, r2)}, theirs, nep)
        for g in cfg.adj(f):
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[0] == t:
                emit(rest | {t}, theirs - {ep[1]})
    return list(dict.fromkeys(out))


# ---------------------------------------------------------------- sum search
def make_solver(cfg):
    memo = {}

    def win(W, B, ep, X, to_move):
        """True iff `to_move` wins G+X, from a state that is NOT resolved."""
        key = (W, B, ep, id(X), to_move)
        if key in memo:
            return memo[key]
        memo[key] = None  # cycle guard (games are finite; should never trigger)
        other = "B" if to_move == "W" else "W"
        res = False
        # moves in G
        for (W2, B2, ep2) in pawn_moves(cfg, W, B, ep, to_move):
            r = resolve(cfg, W2, B2, ep2, to_move)
            if r is not None:
                if r == to_move:
                    res = True
                    break
                continue
            if not win(W2, B2, ep2, X, other):
                res = True
                break
        if not res:
            # moves in X
            for X2 in (X.L if to_move == "W" else X.R):
                if cfg.scope == "global":
                    ep2 = None
                else:
                    ep2 = ep
                W2, B2 = W, B
                if ep2 != ep:
                    # right expired: with an e.p.-aware test the victim may now be passed
                    r = resolve(cfg, W2, B2, ep2, to_move)
                    if r is not None:
                        if r == to_move:
                            res = True
                            break
                        continue
                if not win(W2, B2, ep2, X2, other):
                    res = True
                    break
        memo[key] = res
        return res

    return win, memo


def outcome(win, W, B, X):
    lw = win(W, B, None, X, "W")
    rw = win(W, B, None, X, "B")
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pos", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--files", type=int, default=4)
    ap.add_argument("--wrap", action="store_true")
    args = ap.parse_args()
    R = refs()
    W, B = parse(args.pos)
    # target: *2's own vector, computed on an empty board
    empty = make_solver(Cfg(files=1, ep=False))[0]
    target = "".join(outcome(empty, frozenset(), frozenset(), add(R["*2"], R[n])) for n in REF_ORDER)
    print(f"pos={args.pos} files={args.files} wrap={args.wrap}")
    print("ref order:", " ".join(REF_ORDER))
    print("*2 vector :", target)
    hdr = "race   credit ep  aware scope  | G G+* G+*2 G+*3 G+hyb | vector          | =*2vec | races | states"
    print(hdr)
    for race in ("count", "mover", "opponent"):
        for credit in ((True, False) if race == "count" else (True,)):
            for ep, aware, scope in ((False, False, "global"), (True, False, "global"), (True, False, "local"),
                                     (True, True, "global"), (True, True, "local")):
                RACES.clear()
                cfg = Cfg(files=args.files, wrap=args.wrap, ep=ep, aware=aware, scope=scope, race=race, credit=credit)
                win, memo = make_solver(cfg)
                o = {n: outcome(win, W, B, R[n]) for n in REF_ORDER + ["hyb"]}
                vec = "".join(o[n] for n in REF_ORDER)
                print(f"{race:8s} {str(credit):5s} {str(ep):5s} {str(aware):5s} {scope:6s} | "
                      f"{o['0']} {o['*']}   {o['*2']}    {o['*3']}    {o['hyb']}    | {vec} | "
                      f"{'yes' if vec == target else 'no ':3s}    | {len(RACES):5d} | {len(memo)}")


if __name__ == "__main__":
    main()
