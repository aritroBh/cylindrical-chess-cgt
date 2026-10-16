"""Independent re-check of L3.4 (theory lens). Uses NO project code
(no cylcgt, no lemmas, no crosscheck): own pawn move generator, own passer /
race rules, and a CGT-free proof of equalities via the identity

    G = H  <=>  G - H is a second-player win (P),   and  -*k = *k,

so  W(X) = *2  <=>  W(X) + *2 is P.  The sum W(X) + H is played out by plain
alternating minimax, H being a small explicit game form (nim heaps etc.).
Terminal +-BIG positions are decided outright: with H small (fewer than BIG
moves for either side) +BIG + H' is a Left win whoever starts, -BIG + H' a
Right win. Hence the result does not depend on the size of BIG (any BIG larger
than the number of moves in H gives the same verdict).

E.p. semantics in a sum:
  'local'  = the CGT definition of W(X) as a game form: a move in H leaves the
             pawn node (and its right) unchanged (stale right survives);
  'global' = chess: any move anywhere expires the right.
"""
from __future__ import annotations
import sys
from functools import lru_cache
sys.setrecursionlimit(1_000_000)

FILES = "abcdefghijklmnop"

def sq(s): return (FILES.index(s[0]), int(s[1:]))
def parse(t):
    w, b = t.split("/")
    return (frozenset(sq(x) for x in w.split(":")[1].split()),
            frozenset(sq(x) for x in b.split(":")[1].split()), None)
def fmt(p):
    W, B, ep = p
    s = "W: " + " ".join(sorted(FILES[f]+str(r) for f, r in W)) + " / B: " + " ".join(sorted(FILES[f]+str(r) for f, r in B))
    return s + (f" (ep {FILES[ep[0][0]]}{ep[0][1]} for {ep[2]})" if ep else "")

class Bd:
    def __init__(self, files, ranks, wrap, ep):
        self.files, self.ranks, self.wrap, self.ep = files, ranks, wrap, ep
    def adj(self, f):
        out = []
        for g in (f-1, f+1):
            if self.wrap: out.append(g % self.files)
            elif 0 <= g < self.files: out.append(g)
        return out
    def key(self): return (self.files, self.ranks, self.wrap, self.ep)

def is_passed(bd, W, B, side, pawn):
    f, r = pawn
    files = {f, *bd.adj(f)}
    if side == "W":
        return not any(g in files and s > r for g, s in B)
    return not any(g in files and s < r for g, s in W)

def has_passer(bd, W, B, side):
    mine = W if side == "W" else B
    return any(is_passed(bd, W, B, side, p) for p in mine)

def term(bd, p):
    W, B, _ = p
    a, b = has_passer(bd, W, B, "W"), has_passer(bd, W, B, "B")
    if a and b: return "race"
    if a: return "W"
    if b: return "B"
    return None

def dist(bd, p, side):
    """smallest promotion distance of a passed pawn of `side` (double step from
    the start rank counts as one move)."""
    W, B, _ = p
    best = 10**6
    for (f, r) in (W if side == "W" else B):
        if not is_passed(bd, W, B, side, (f, r)):
            continue
        if side == "W":
            d = bd.ranks - r - (1 if (r == 2 and bd.ranks >= 4) else 0)
        else:
            d = r - 1 - (1 if (r == bd.ranks - 1 and bd.ranks >= 4) else 0)
        best = min(best, d)
    return best

def race_winner(bd, p, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover": return mover
    if rule == "opponent": return other
    return other if dist(bd, p, other) <= dist(bd, p, mover) else mover

def gen(bd, p, side):
    """all positions after one pawn move of `side`. Only a right entitled to
    `side` can be used; children carry a right only after a double step."""
    W, B, ep = p
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else bd.ranks - 1
    other = "B" if side == "W" else "W"
    out = set()
    def put(m, t, e=None):
        out.add((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= bd.ranks:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2*d
            if r == start and 1 <= r2 <= bd.ranks and (f, r2) not in occ:
                put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if bd.ep else None)
        for g in bd.adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[0] == t and ep[1] in theirs:
                put(rest | {t}, theirs - {ep[1]})
    return list(out)

# ---------------------------------------------------------------------------
# small explicit game forms H = (tuple of Left options, tuple of Right options)
ZERO = ((), ())
def nim(k):
    return (tuple(nim(j) for j in range(k)), tuple(nim(j) for j in range(k)))
STAR = nim(1)
UP = ((ZERO,), (STAR,))
DOWN = ((STAR,), (ZERO,))
ONE = ((ZERO,), ())
MONE = ((), (ZERO,))
HALF = ((ZERO,), (ONE,))
PM1 = ((ONE,), (MONE,))
def add(a, b):
    """formal sum of two explicit forms (only used for tiny forms)."""
    return (tuple(add(x, b) for x in a[0]) + tuple(add(a, y) for y in b[0]),
            tuple(add(x, b) for x in a[1]) + tuple(add(a, y) for y in b[1]))

# ---------------------------------------------------------------------------
def make_solver(bd, rule, kings=False, epmode="local"):
    @lru_cache(maxsize=None)
    def wins(p, h, side):
        """True iff `side`, to move in pawn-node p (non-terminal) + H-node h, wins."""
        other = "B" if side == "W" else "W"
        for c in gen(bd, p, side):
            t = term(bd, c)
            if t == "race":
                if race_winner(bd, c, side, rule) == side: return True
                continue
            if t is not None:
                if t == side: return True
                continue
            if not wins(c, h, other): return True
        for h2 in (h[0] if side == "W" else h[1]):
            p2 = p if epmode == "local" else (p[0], p[1], None)
            if not wins(p2, h2, other): return True
        # king move (kings=True) loses at once: never a winning option.
        return False
    return wins

def _cls(white_first_wins, black_first_wins):
    if white_first_wins and black_first_wins: return "N"
    if white_first_wins and not black_first_wins: return "L"
    if not white_first_wins and black_first_wins: return "R"
    return "P"

def outcome(bd, p, h, rule, kings=False, epmode="local"):
    w = make_solver(bd, rule, kings, epmode)
    return _cls(w(p, h, "W"), w(p, h, "B"))

# ---------------------------------------------------------------------------
def reachable(bd, p0):
    seen = {p0}; st = [p0]
    while st:
        x = st.pop()
        if term(bd, x) is not None: continue
        for side in "WB":
            for c in gen(bd, x, side):
                if c not in seen:
                    seen.add(c); st.append(c)
    return seen

def n_components(bd, p):
    occ = sorted({f for f, _ in p[0] | p[1]})
    if not occ: return 0
    comps = 1
    for a, b in zip(occ, occ[1:]):
        if b != a + 1: comps += 1
    if bd.wrap and comps > 1 and occ[0] == 0 and occ[-1] == bd.files - 1: comps -= 1
    return comps

def whole_board_outcome(bd, p, rule):
    """Whole-board convention game (first passer ends the game, race rule on
    the whole board, global e.p.), no H."""
    return outcome(bd, p, ZERO, rule, False, "global")
