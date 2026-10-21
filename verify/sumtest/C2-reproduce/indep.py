"""Independent verifier solver for claim C2 (written by the C2-reproduce verifier).

Plays G + R by exhaustive minimax, where G is a pawn position (chess-like rules,
first passed pawn ends the whole game) and R is an explicit game tree given as
nested (lefts, rights) tuples.  No code shared with sumtest/ or cylcgt/.

Options:
  ep        : en passant allowed
  aware     : a pawn that can be taken e.p. on the very next move is not passed
  scope     : 'local'  - e.p. right survives moves made in R (CGT component view)
              'global' - any move anywhere kills the e.p. right (chess view)
  race      : 'count' | 'mover' | 'opponent'
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)

def G(l=(), r=()):
    return (tuple(l), tuple(r))
Z = G(); S = G([Z], [Z]); S2 = G([Z, S], [Z, S]); S3 = G([Z, S, S2], [Z, S, S2])
UP = G([Z], [S]); DN = G([S], [Z])
def add(a, b):
    return G([add(x, b) for x in a[0]] + [add(a, y) for y in b[0]],
             [add(x, b) for x in a[1]] + [add(a, y) for y in b[1]])
UPS = add(UP, S); DUPS = add(add(UP, UP), S)
ONE = G([Z], []); MONE = G([], [Z]); HALF = G([Z], [ONE]); MHALF = G([MONE], [Z])
SW = G([ONE], [Z]); PM1 = G([ONE], [MONE]); TINY = G([Z], [G([Z], [MONE])])
REF = [("0", Z), ("*", S), ("*2", S2), ("*3", S3), ("up", UP), ("down", DN), ("up*", UPS),
       ("dup*", DUPS), ("1/2", HALF), ("-1/2", MHALF), ("1", ONE), ("-1", MONE),
       ("{1|0}", SW), ("+-1", PM1), ("tiny1", TINY)]


class Solver:
    def __init__(self, nfiles, wrap, ep, aware, scope, race, nranks=8):
        self.F, self.wrap, self.ep, self.aware, self.scope, self.race = nfiles, wrap, ep, aware, scope, race
        self.NR = nranks
        self.races = 0
        self.win = lru_cache(maxsize=None)(self._win)

    def nbr(self, f):
        out = set()
        for d in (-1, 1):
            g = f + d
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    def is_passed(self, pawn, color, enemy):
        f, r = pawn
        cols = {f} | self.nbr(f)
        if color == 'W':
            return not any(g in cols and s > r for (g, s) in enemy)
        return not any(g in cols and s < r for (g, s) in enemy)

    def passers(self, W, B, ep, color):
        mine, enemy = (W, B) if color == 'W' else (B, W)
        out = []
        for p in mine:
            if self.aware and ep is not None and ep[2] == p:
                # ep = (skipped square, capturing colour, the pawn that double-stepped)
                continue
            if self.is_passed(p, color, enemy):
                out.append(p)
        return out

    def dist(self, ps, color):
        best = 10**9
        for (f, r) in ps:
            if color == 'W':
                d = self.NR - r - (1 if r == 2 else 0)
            else:
                d = r - 1 - (1 if r == self.NR - 1 else 0)
            best = min(best, d)
        return best

    def verdict(self, W, B, ep, mover):
        """None, or 'W'/'B' winner of the whole game after `mover` moved."""
        wp = self.passers(W, B, ep, 'W'); bp = self.passers(W, B, ep, 'B')
        if not wp and not bp:
            return None
        if wp and not bp:
            return 'W'
        if bp and not wp:
            return 'B'
        self.races += 1
        opp = 'B' if mover == 'W' else 'W'
        if self.race == 'mover':
            return mover
        if self.race == 'opponent':
            return opp
        dm = self.dist(wp if mover == 'W' else bp, mover)
        do = self.dist(bp if mover == 'W' else wp, opp)
        return opp if do <= dm else mover

    def pawn_moves(self, W, B, ep, color):
        """yield (W', B', ep')"""
        mine, enemy = (W, B) if color == 'W' else (B, W)
        occ = W | B
        fwd = 1 if color == 'W' else -1
        home = 2 if color == 'W' else self.NR - 1
        res = []
        for p in mine:
            f, r = p
            rest = mine - {p}
            r1 = r + fwd
            if not 1 <= r1 <= self.NR:
                continue
            if (f, r1) not in occ:
                res.append((rest | {(f, r1)}, enemy, None))
                r2 = r + 2 * fwd
                if r == home and (f, r2) not in occ:
                    nep = None
                    if self.ep:
                        # opponent pawn beside the landing square can take e.p.
                        if any((g, r2) in enemy for g in self.nbr(f)):
                            nep = ((f, r1), 'B' if color == 'W' else 'W', (f, r2))
                    res.append((rest | {(f, r2)}, enemy, nep))
            for g in self.nbr(f):
                t = (g, r1)
                if t in enemy:
                    res.append((rest | {t}, enemy - {t}, None))
                elif ep is not None and ep[1] == color and ep[0] == t:
                    res.append((rest | {t}, enemy - {ep[2]}, None))
        out = []
        for (m, e, nep) in res:
            m, e = frozenset(m), frozenset(e)
            out.append((m, e, nep) if color == 'W' else (e, m, nep))
        return out

    def _win(self, W, B, ep, R, tomove):
        """True iff `tomove` wins G+R with tomove to play."""
        other = 'B' if tomove == 'W' else 'W'
        # moves in G
        for (W2, B2, ep2) in self.pawn_moves(W, B, ep, tomove):
            v = self.verdict(W2, B2, ep2, tomove)
            if v is not None:
                if v == tomove:
                    return True
                continue
            if not self.win(W2, B2, ep2, R, other):
                return True
        # moves in R
        for R2 in (R[0] if tomove == 'W' else R[1]):
            if ep is not None and self.scope == 'global':
                v = self.verdict(W, B, None, tomove)
                if v is not None:
                    if v == tomove:
                        return True
                    continue
                if not self.win(W, B, None, R2, other):
                    return True
            else:
                if not self.win(W, B, ep, R2, other):
                    return True
        return False


def parse(text):
    w, b = text.split('/')
    f = lambda t: frozenset(('abcdefgh'.index(x[0]), int(x[1:])) for x in t.split(':')[1].split())
    return f(w), f(b)


def vector(text, files, wrap, **kw):
    s = Solver(files, wrap, **kw)
    W, B = parse(text)
    out = ''
    for name, R in REF:
        lw = s.win(W, B, None, R, 'W'); rw = s.win(W, B, None, R, 'B')
        out += {(True, False): 'L', (False, True): 'R', (True, True): 'N', (False, False): 'P'}[(lw, rw)]
    return out, s


if __name__ == '__main__':
    POS = "W: a2 c2 / B: b7 d7"
    print("*2 vector (G=0, 1-file empty):", vector("W: / B:", 1, False, ep=False, aware=False, scope='local', race='count')[0])
    for files, wrap in ((4, False), (8, False), (8, True), (5, True)):
        for race in ('count', 'mover', 'opponent'):
            for (lab, ep, aware, scope) in (("off", False, False, 'local'), ("plain-local", True, False, 'local'),
                                           ("plain-global", True, False, 'global'), ("aware-local", True, True, 'local'),
                                           ("aware-global", True, True, 'global')):
                v, s = vector(POS, files, wrap, ep=ep, aware=aware, scope=scope, race=race)
                print(files, 'cyl' if wrap else 'flat', race, lab, v)
