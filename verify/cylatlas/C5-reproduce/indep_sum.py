"""Independent check (no cylcgt import) of the C5 headline values.

Method: G = H  iff  G + (-H) is a second-player win.  For a pawn component G
and an explicit short game X we search the sum G + X by plain win/loss minimax.
When the pawn part becomes decided (exactly one side has a passed pawn, or a
race resolved by RACE_RULE) it is worth +-256, which dominates every X used
here (all stops of X lie in [-3, 3]); so that move simply decides the sum.

En passant follows the cylcgt *model* convention: the right belongs to the pawn
component and survives moves made in X; it is used or lost at the next move made
inside the pawn component.  For the positions tested here (2 v 2 pawns) the pawn
component never splits without a passed pawn appearing, so whole-position
passer tests coincide with the per-component tests of the model.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_sum.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
RANKS = 8

# ---------- explicit short games as (Ltuple, Rtuple) ----------
ZERO = ((), ())


def opts(*xs):
    return tuple(xs)


def G(L, R):
    return (tuple(L), tuple(R))


STAR = G([ZERO], [ZERO])
STAR2 = G([ZERO, STAR], [ZERO, STAR])
STAR3 = G([ZERO, STAR, STAR2], [ZERO, STAR, STAR2])


def integer(n):
    g = ZERO
    for _ in range(abs(n)):
        g = G([g], []) if n > 0 else G([], [g])
    return g


ONE, TWO, M1, M2 = integer(1), integer(2), integer(-1), integer(-2)
HALF = G([ZERO], [ONE])
MHALF = G([M1], [ZERO])
UP = G([ZERO], [STAR])
DOWN = G([STAR], [ZERO])
PM_HALF = G([HALF], [MHALF])            # +-1/2
SW_2_1 = G([TWO], [ONE])               # 3/2 +- 1/2
SW_m1_m2 = G([M1], [M2])               # -3/2 +- 1/2
H_CYL4 = G([SW_2_1], [SW_m1_m2])       # {3/2+-1/2 | -3/2+-1/2}; equals its own negative


def neg(x):
    L, R = x
    return (tuple(neg(r) for r in R), tuple(neg(l) for l in L))


# ---------- pawn model ----------
class Cfg:
    def __init__(self, n, wrap, ep, rule):
        self.n, self.wrap, self.ep, self.rule = n, wrap, ep, rule

    def adj(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.wrap:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return out


def parse(text):
    w, b = text.split("/")
    sq = lambda t: ("abcdefgh".index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()))


def is_passed(cfg, side, f, r, W, B):
    files = {f, *cfg.adj(f)}
    if side == "W":
        return not any(g in files and s > r for g, s in B)
    return not any(g in files and s < r for g, s in W)


def has_passer(cfg, side, W, B):
    mine = W if side == "W" else B
    return any(is_passed(cfg, side, f, r, W, B) for f, r in mine)


def dist(cfg, side, W, B):
    """moves needed by `side`'s best passed pawn (frontmost on its file) to promote."""
    best = 10 ** 6
    mine = W if side == "W" else B
    for f, r in mine:
        if not is_passed(cfg, side, f, r, W, B):
            continue
        if side == "W":
            if any((f, s) in mine for s in range(r + 1, RANKS + 1)):
                continue
            d = (RANKS - r) - (1 if r == 2 else 0)
        else:
            if any((f, s) in mine for s in range(1, r)):
                continue
            d = (r - 1) - (1 if r == RANKS - 1 else 0)
        best = min(best, d)
    return best


def pawn_moves(cfg, side, W, B, ep):
    """list of (W', B', ep') for `side`; ep is (target, captured, owner) or None."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    fwd = 1 if side == "W" else -1
    home = 2 if side == "W" else RANKS - 1
    other = "B" if side == "W" else "W"
    res = set()

    def put(m2, t2, e2=None):
        res.add((m2, t2, e2) if side == "W" else (t2, m2, e2))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + fwd
        if not 1 <= r1 <= RANKS:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * fwd
            if r == home and (f, r2) not in occ:
                put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if cfg.ep else None)
        for g in cfg.adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[0] == t:
                put(rest | {t}, theirs - {ep[1]})
    return list(res)


def decided(cfg, mover, W, B):
    """+1 / -1 if the pawn part is now decided for White / Black, else 0."""
    wp, bp = has_passer(cfg, "W", W, B), has_passer(cfg, "B", W, B)
    if wp and bp:
        if cfg.rule == "mover":
            win = mover
        elif cfg.rule == "opponent":
            win = "B" if mover == "W" else "W"
        else:
            opp = "B" if mover == "W" else "W"
            win = opp if dist(cfg, opp, W, B) <= dist(cfg, mover, W, B) else mover
        return 1 if win == "W" else -1
    if wp:
        return 1
    if bp:
        return -1
    return 0


def make_solver(cfg):
    @lru_cache(maxsize=None)
    def wins(W, B, ep, X, side):
        """Does `side` to move win the sum pawns(W,B,ep) + X?"""
        sgn = 1 if side == "W" else -1
        other = "B" if side == "W" else "W"
        for (W2, B2, e2) in pawn_moves(cfg, side, W, B, ep):
            d = decided(cfg, side, W2, B2)
            if d == sgn:
                return True
            if d == -sgn:
                continue
            if not wins(W2, B2, e2, X, other):
                return True
        for X2 in (X[0] if side == "W" else X[1]):
            if not wins(W, B, ep, X2, other):
                return True
        return False
    return wins


def is_zero(cfg, text, X):
    """True iff pawns(text) + X == 0 (second-player win both ways)."""
    W, B = parse(text)
    assert not has_passer(cfg, "W", W, B) and not has_passer(cfg, "B", W, B)
    wins = make_solver(cfg)
    return (not wins(W, B, None, X, "W")) and (not wins(W, B, None, X, "B"))


def race_edges(cfg, text):
    """Emulate cylcgt's race_hits accounting: for every distinct reached state
    (W,B,ep), for each side, each distinct child that is a race counts 1.
    Also return the number of distinct race child positions."""
    W0, B0 = parse(text)
    seen = set()
    edges = 0
    distinct = set()
    stack = [(W0, B0, None)]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        W, B, ep = s
        for side in ("W", "B"):
            e_use = ep if (ep and ep[2] == side) else None
            for (W2, B2, e2) in pawn_moves(cfg, side, W, B, e_use):
                wp, bp = has_passer(cfg, "W", W2, B2), has_passer(cfg, "B", W2, B2)
                if wp and bp:
                    edges += 1
                    distinct.add((W2, B2, e2))
                elif not (wp or bp):
                    stack.append((W2, B2, e2))
    return edges, len(distinct), len({(a, b) for a, b, _ in distinct}), len(seen)


CASES = [
    # (board, n, ep, rule, position, label, game X that should make the sum 0)
    ("flat", 4, True, "count", "W: a2 c2 / B: b7 d7", "*2", STAR2),
    ("flat", 4, True, "mover", "W: a2 c2 / B: b7 d7", "*2", STAR2),
    ("flat", 4, True, "opponent", "W: a2 c2 / B: b7 d7", "0", ZERO),
    ("flat", 4, False, "count", "W: a2 c2 / B: b7 d7", "*2", STAR2),
    ("flat", 4, False, "mover", "W: a2 c2 / B: b7 d7", "*2", STAR2),
    ("flat", 4, False, "opponent", "W: a2 c2 / B: b7 d7", "0", ZERO),
    ("cyl", 4, True, "count", "W: a2 c2 / B: b7 d7", "{3/2+-1/2|-3/2+-1/2}", neg(H_CYL4)),
    ("cyl", 4, True, "mover", "W: a2 c2 / B: b7 d7", "{3/2+-1/2|-3/2+-1/2}", neg(H_CYL4)),
    ("cyl", 4, True, "opponent", "W: a2 c2 / B: b7 d7", "{3/2+-1/2|-3/2+-1/2}", neg(H_CYL4)),
    ("cyl", 4, False, "count", "W: a2 c2 / B: b7 d7", "+-1/2", neg(PM_HALF)),
    ("cyl", 3, True, "opponent", "W: a2 b3 / B: a5 c5", "*2", STAR2),
    ("cyl", 3, False, "opponent", "W: a2 b3 / B: a5 c5", "*2", STAR2),
    ("cyl", 3, True, "count", "W: a2 b3 / B: a5 c5", "-1/2", HALF),
    ("cyl", 3, True, "mover", "W: a2 b3 / B: a5 c5", "up", DOWN),
    ("cyl", 3, True, "opponent", "W: a4 b4 / B: a7 c6", "*2", STAR2),
    # negative controls: these must NOT be zero
    ("flat", 4, True, "count", "W: a2 c2 / B: b7 d7", "(control: not *)", STAR),
    ("flat", 4, True, "count", "W: a2 c2 / B: b7 d7", "(control: not *3)", STAR3),
    ("flat", 4, True, "count", "W: a2 c2 / B: b7 d7", "(control: not 0)", ZERO),
    ("cyl", 4, True, "count", "W: a2 c2 / B: b7 d7", "(control: not *2)", STAR2),
]

if __name__ == "__main__":
    for board, n, ep, rule, text, label, X in CASES:
        cfg = Cfg(n, board == "cyl", ep, rule)
        z = is_zero(cfg, text, X)
        print(f"{board}{n} ep={'on' if ep else 'off'} {rule:8s} {text:22s} == {label:24s}: {z}", flush=True)
    for board, n, ep, text in [("flat", 4, True, "W: a2 c2 / B: b7 d7"),
                               ("flat", 4, False, "W: a2 c2 / B: b7 d7"),
                               ("cyl", 3, True, "W: a2 b3 / B: a5 c5"),
                               ("cyl", 4, True, "W: a2 c2 / B: b7 d7")]:
        cfg = Cfg(n, board == "cyl", ep, "count")
        e, d, dpos, states = race_edges(cfg, text)
        print(f"race accounting {board}{n} ep={'on' if ep else 'off'} {text}: race edges={e}, "
              f"distinct race children (with ep flag)={d}, distinct race placements={dpos}, "
              f"non-terminal states reached={states}")
