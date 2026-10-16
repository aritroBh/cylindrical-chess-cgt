"""Independent re-check of claim C3 (verifier C3-theory).

Written from scratch; imports neither cylcgt nor sumtest nor crosscheck.
Plays G + H out by plain minimax (no canonical forms) where
  G = a pawn position (W = Left, B = Right), 8 ranks, flat or cylinder,
  H = an explicit game tree given as nested (left_options, right_options).

Convention (the one C3 is about):
  * after any move in G, if exactly one side owns a passed pawn the whole sum
    is won by that side (BIG dominates every H used here, |H| <= 3);
  * both sides passed -> race rule ("count" / "mover" / "opponent", cylcgt's
    semantics: count = the mover's opponent moves first, fewer moves to promote
    wins, ties go to the opponent, a passer on its home rank is credited with
    the double step);
  * aware=True: a pawn that the opponent may capture en passant on his next move
    is not (yet) counted as passed;  aware=False: textbook test;
  * scope="component": the e.p. right survives moves made in H (only the next
    move *in G* can use it);  scope="global": any move anywhere ends it (chess).

Usage: PYTHONPATH=. .venv/bin/python verify/sumtest/C3-theory/indep_sum.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
NR = 8


def game(L=(), R=()):
    return (tuple(L), tuple(R))


ZERO = game()
STAR = game([ZERO], [ZERO])
STAR2 = game([ZERO, STAR], [ZERO, STAR])
STAR3 = game([ZERO, STAR, STAR2], [ZERO, STAR, STAR2])
UP = game([ZERO], [STAR])
DOWN = game([STAR], [ZERO])
ONE = game([ZERO], [])
MONE = game([], [ZERO])
TWO = game([ONE], [])
THREE = game([TWO], [])
MTWO = game([], [MONE])
MTHREE = game([], [MTWO])
HALF = game([ZERO], [ONE])
MHALF = game([MONE], [ZERO])
SW10 = game([ONE], [ZERO])
PM1 = game([ONE], [MONE])
TINY1 = game([ZERO], [game([ZERO], [MONE])])
PM_2_1 = game([THREE], [ONE])           # 2 +- 1 = {3 | 1}
PM_m2_1 = game([MONE], [MTHREE])        # -2 +- 1 = {-1 | -3}
H_CLAIM = game([PM_2_1], [PM_m2_1])     # {2+-1 | -2+-1}; note -H_CLAIM = H_CLAIM


def neg(g):
    L, R = g
    return game([neg(x) for x in R], [neg(x) for x in L])


def plus(a, b):
    """Explicit disjunctive sum of two trees."""
    return game([plus(x, b) for x in a[0]] + [plus(a, y) for y in b[0]],
                [plus(x, b) for x in a[1]] + [plus(a, y) for y in b[1]])


UPSTAR = plus(UP, STAR)
DUPSTAR = plus(plus(UP, UP), STAR)
REF = [("0", ZERO), ("*", STAR), ("*2", STAR2), ("*3", STAR3), ("up", UP), ("down", DOWN),
       ("up*", UPSTAR), ("dup*", DUPSTAR), ("1/2", HALF), ("-1/2", MHALF), ("1", ONE),
       ("-1", MONE), ("{1|0}", SW10), ("+-1", PM1), ("tiny1", TINY1)]


class Model:
    def __init__(self, files, wrap=False, ep=True, aware=True, rule="count", scope="component"):
        self.F, self.wrap, self.ep, self.aware, self.rule, self.scope = files, wrap, ep, aware, rule, scope
        self.cache = {}

    def nbrs(self, f):
        out = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                out.add(g)
        return out

    # position: (white frozenset{(f,r)}, black frozenset, ep) ; ep = (target, victim, capturer) or None
    def moves(self, pos, side):
        W, B, ep = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        home = 2 if side == "W" else NR - 1
        other = "B" if side == "W" else "W"
        out = []

        def emit(m, t, e=None):
            out.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))

        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            if not 1 <= r1 <= NR:
                continue
            if (f, r1) not in occ:
                emit(rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == home and (f, r2) not in occ:
                    e = None
                    # record an e.p. right only if an enemy pawn can actually use it
                    if self.ep and any((g, r2) in theirs for g in self.nbrs(f)):
                        e = ((f, r1), (f, r2), other)
                    emit(rest | {(f, r2)}, theirs, e)
            for g in self.nbrs(f):
                t = (g, r1)
                if t in theirs:
                    emit(rest | {t}, theirs - {t})
                elif ep and ep[2] == side and ep[0] == t:
                    emit(rest | {t}, theirs - {ep[1]})
        return list(dict.fromkeys(out))

    def passers(self, pos, side):
        W, B, ep = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        out = []
        for (f, r) in mine:
            if self.aware and ep and ep[1] == (f, r) and ep[2] != side:
                continue  # can be taken e.p. right now: not passed yet
            span = {f} | self.nbrs(f)
            if side == "W":
                blocked = any(g in span and s > r for (g, s) in theirs)
            else:
                blocked = any(g in span and s < r for (g, s) in theirs)
            if not blocked:
                out.append((f, r))
        return out

    def dist(self, pos, side, ps):
        W, B, _ = pos
        occ = W | B
        best = 10 ** 6
        for (f, r) in ps:
            if side == "W":
                if any((f, s) in occ for s in range(r + 1, NR + 1)):
                    continue
                dd = NR - r - (1 if r == 2 else 0)
            else:
                if any((f, s) in occ for s in range(1, r)):
                    continue
                dd = r - 1 - (1 if r == NR - 1 else 0)
            best = min(best, dd)
        return best

    def resolve(self, pos, mover):
        """None, or the winner 'W'/'B' of the whole sum."""
        wp, bp = self.passers(pos, "W"), self.passers(pos, "B")
        if wp and not bp:
            return "W"
        if bp and not wp:
            return "B"
        if not wp and not bp:
            return None
        other = "B" if mover == "W" else "W"
        if self.rule == "mover":
            return mover
        if self.rule == "opponent":
            return other
        dm = self.dist(pos, mover, wp if mover == "W" else bp)
        do = self.dist(pos, other, wp if other == "W" else bp)
        return other if do <= dm else mover

    def wins(self, pos, h, side):
        """True iff `side`, to move in G(pos) + h, wins."""
        key = (pos, h, side)
        c = self.cache.get(key)
        if c is not None:
            return c
        other = "B" if side == "W" else "W"
        res = False
        for child in self.moves(pos, side):
            w = self.resolve(child, side)
            if w is not None:
                if w == side:
                    res = True
                    break
                continue
            if not self.wins(child, h, other):
                res = True
                break
        if not res:
            for h2 in (h[0] if side == "W" else h[1]):
                p2 = pos
                if self.scope == "global" and pos[2] is not None:
                    p2 = (pos[0], pos[1], None)
                    w = self.resolve(p2, side)
                    if w is not None:
                        if w == side:
                            res = True
                            break
                        continue
                if not self.wins(p2, h2, other):
                    res = True
                    break
        self.cache[key] = res
        return res

    def outcome(self, pos, h):
        lf, rf = self.wins(pos, h, "W"), self.wins(pos, h, "B")
        return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lf, rf)]


def parse(text):
    w, b = text.split("/")
    sq = lambda t: ("abcdefghijklmnop".index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()), None)


def main():
    G = parse("W: a2 c2 / B: b7 d7")
    configs = []
    for rule in ("count", "mover", "opponent"):
        for (ep, aware, scope) in ((False, False, "component"), (True, False, "component"), (True, False, "global"),
                                   (True, True, "component"), (True, True, "global")):
            for (files, wrap) in ((4, False), (8, False), (8, True), (5, True)):
                configs.append((rule, ep, aware, scope, files, wrap))
    print("rule | ep | passer test | ep scope | board | 15-vector | G+*2 | G+H (H={2+-1|-2+-1}) | G alone")
    for rule, ep, aware, scope, files, wrap in configs:
        m = Model(files, wrap, ep, aware, rule, scope)
        vec = "".join(m.outcome(G, h) for _, h in REF)
        print(f"{rule} | {'on' if ep else 'off'} | {'aware' if aware else 'textbook'} | {scope} | "
              f"{files}{'cyl' if wrap else 'flat'} | {vec} | {m.outcome(G, STAR2)} | {m.outcome(G, H_CLAIM)} | {m.outcome(G, ZERO)}")
    # sub-positions named in the worker's mechanism (4-file flat, count)
    print()
    for aware in (True, False):
        m = Model(4, False, True, aware, "count", "component")
        X = parse("W: a2 c2 / B: b4 d7")
        Y = parse("W: a2 c2 / B: b5 d7")
        Yw = parse("W: a2 c4 / B: b7 d7")
        tag = "aware" if aware else "textbook"
        print(f"[{tag}] X=W a2 c2/B b4 d7: X+3 -> {m.outcome(X, THREE)} (P iff X=-3); X alone -> {m.outcome(X, ZERO)}")
        print(f"[{tag}] Y=W a2 c2/B b5 d7: Y+(2+-1) -> {m.outcome(Y, PM_2_1)} (P iff Y=-2+-1); Y alone -> {m.outcome(Y, ZERO)} (P iff Y=0)")
        print(f"[{tag}] Y'=W a2 c4/B b7 d7: Y'+(-2+-1) -> {m.outcome(Yw, PM_m2_1)} (P iff Y'=2+-1); Y' alone -> {m.outcome(Yw, ZERO)}")


if __name__ == "__main__":
    main()
