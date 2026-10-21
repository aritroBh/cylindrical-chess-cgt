"""Independent re-implementation (C1-theory verifier): pawn game generator with
textbook / e.p.-aware passed tests, race rules, per-component e.p. model, and a
plain CGT comparison (<=) on unsimplified game DAGs. Imports nothing from
cylcgt or bench. Written from the conventions stated in the task, not from
cylcgt's code (only the per-component e.p. rule mirrors cylcgt's docstring).
"""
import sys, threading
from functools import lru_cache
sys.setrecursionlimit(1_000_000)
threading.stack_size(512 * 1024 * 1024)

BIG = 256
RANKS = 8

_ALIVE = []  # keep every node alive so id()-keyed memo entries stay valid
class G:
    __slots__ = ("L", "R", "n", "__weakref__")
    def __init__(self, L, R, n=None):
        self.L, self.R, self.n = tuple(L), tuple(R), n
        _ALIVE.append(self)

_ints = {}
def integer(n):
    if n not in _ints:
        if n == 0: _ints[n] = G((), (), 0)
        elif n > 0: _ints[n] = G((integer(n - 1),), (), n)
        else: _ints[n] = G((), (integer(n + 1),), n)
    return _ints[n]

_le = {}
def le(a, b):
    if a is b: return True
    if a.n is not None and b.n is not None: return a.n <= b.n
    k = (id(a), id(b))
    r = _le.get(k)
    if r is None:
        r = not any(le(b, x) for x in a.L) and not any(le(x, a) for x in b.R)
        _le[k] = r
    return r

def eq(a, b): return le(a, b) and le(b, a)
def neg(a):
    if a.n is not None: return integer(-a.n)
    return G([neg(x) for x in a.R], [neg(x) for x in a.L])
def add(a, b):
    if a.n is not None and b.n is not None: return integer(a.n + b.n)
    return G([add(x, b) for x in a.L] + [add(a, y) for y in b.L],
             [add(x, b) for x in a.R] + [add(a, y) for y in b.R])
def outcome(a):
    zero = integer(0)
    ge0, le0 = le(zero, a), le(a, zero)
    return {(True, True): "P", (True, False): "L", (False, True): "R", (False, False): "N"}[(ge0, le0)]

ZERO = integer(0); ONE = integer(1)
STAR = G([ZERO], [ZERO])
UP = G([ZERO], [STAR]); DOWN = neg(UP)
HALF = G([ZERO], [ONE])
def nim(k): return G([nim(i) for i in range(k)], [nim(i) for i in range(k)])

# ---------- pawns ----------
# pos = (frozenset white, frozenset black, ep) ; ep = (target, captured, capturer) or None
def sq(s): return ("abcdefgh".index(s[0]), int(s[1:]))
def parse(t):
    w, b = t.split("/")
    return (frozenset(sq(x) for x in w.split(":")[1].split()),
            frozenset(sq(x) for x in b.split(":")[1].split()), None)

class Rules:
    def __init__(self, files, ep_on, aware, race):
        self.files, self.ep_on, self.aware, self.race = files, ep_on, aware, race
        self.memo = {}

    def nbrs(self, f):
        return [g for g in (f - 1, f + 1) if 0 <= g < self.files]

    def ep_takeable(self, pos, side, s):
        W, B, ep = pos
        if not (self.aware and ep and ep[1] == s and ep[2] != side): return False
        theirs = B if side == "W" else W
        return any((g, s[1]) in theirs for g in self.nbrs(s[0]))

    def pawn_passed_tb(self, theirs, side, s):
        f, r = s
        fs = {f, *self.nbrs(f)}
        if side == "W": return not any(g in fs and q > r for g, q in theirs)
        return not any(g in fs and q < r for g, q in theirs)

    def passed(self, pos, side):
        W, B, _ = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        return any(self.pawn_passed_tb(theirs, side, s) and not self.ep_takeable(pos, side, s) for s in mine)

    def dist(self, pos, side):
        W, B, _ = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        best = 10**6
        for s in mine:
            f, r = s
            if not self.pawn_passed_tb(theirs, side, s) or self.ep_takeable(pos, side, s): continue
            if side == "W":
                if any((f, q) in mine for q in range(r + 1, RANKS + 1)): continue
                d = (RANKS - r) - (1 if r == 2 else 0)
            else:
                if any((f, q) in mine for q in range(1, r)): continue
                d = (r - 1) - (1 if r == RANKS - 1 else 0)
            best = min(best, d)
        return best

    def moves(self, pos, side):
        W, B, ep = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        start = 2 if side == "W" else RANKS - 1
        other = "B" if side == "W" else "W"
        out = []
        def emit(m, t, e=None):
            out.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))
        for s in mine:
            f, r = s
            rest = mine - {s}
            one = (f, r + d)
            if 1 <= one[1] <= RANKS and one not in occ:
                emit(rest | {one}, theirs)
                two = (f, r + 2 * d)
                if r == start and two not in occ:
                    emit(rest | {two}, theirs, (one, two, other) if self.ep_on else None)
            for g in self.nbrs(f):
                t = (g, r + d)
                if t in theirs: emit(rest | {t}, theirs - {t})
                elif ep and ep[2] == side and ep[0] == t: emit(rest | {t}, theirs - {ep[1]})
        return list(dict.fromkeys(out))

    def child(self, pos, mover):
        wp, bp = self.passed(pos, "W"), self.passed(pos, "B")
        if wp and bp:
            other = "B" if mover == "W" else "W"
            if self.race == "mover": win = mover
            elif self.race == "opponent": win = other
            else: win = other if self.dist(pos, other) <= self.dist(pos, mover) else mover
            return integer(BIG if win == "W" else -BIG)
        return self.value(pos)

    def value(self, pos):
        if pos in self.memo: return self.memo[pos]
        wp, bp = self.passed(pos, "W"), self.passed(pos, "B")
        assert not (wp and bp), pos
        if wp: g = integer(BIG)
        elif bp: g = integer(-BIG)
        else:
            W, B, ep = pos
            plain = (W, B, None)
            lpos = plain if (ep and ep[2] != "W") else pos
            rpos = plain if (ep and ep[2] != "B") else pos
            g = G([self.child(c, "W") for c in self.moves(lpos, "W")],
                  [self.child(c, "B") for c in self.moves(rpos, "B")])
        self.memo[pos] = g
        return g

    def children(self, pos):
        return [("W", c, self.child(c, "W")) for c in self.moves(pos, "W")] + \
               [("B", c, self.child(c, "B")) for c in self.moves(pos, "B")]

def run(fn):
    res = []
    t = threading.Thread(target=lambda: res.append(fn()))
    t.start(); t.join()
    return res[0]
