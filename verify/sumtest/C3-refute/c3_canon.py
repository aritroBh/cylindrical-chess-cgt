"""C3 refute-lens check, second independent path (verifier re-run, 2026-10-16).

Computes the canonical CGT value of the pawn position directly, with a tiny
canonical-form engine written here (dominated-option removal + reversible-option
bypass, comparisons by the recursive definition of <=).  Imports nothing from
sumtest/, cylcgt/, crosscheck/ or the earlier c3_indep.py.

Model: White = Left, Black = Right, normal play.  Pawn single/double steps,
diagonal captures (wrap on a cylinder), en passant (also across the seam).
After every move: exactly one side with a passed pawn -> +-BIG (BIG = 256);
both -> race rule.  e.p. right is "local": it lives in this component until
the next move made in it (the only reading under which the position has a
CGT value at all).

Passer tests:
  plain : textbook (no enemy pawn ahead on own or adjacent files)
  aware : as plain, but a pawn that has just double-stepped and can be taken
          en passant right now is not (yet) passed.

Usage:  .venv/bin/python -I verify/sumtest/C3-refute/c3_canon.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
NR = 8
BIG = 256

# ------------------------------------------------------------ CGT engine
_key2id = {}
GL, GR = [], []


def mk(L, R):
    k = (frozenset(L), frozenset(R))
    i = _key2id.get(k)
    if i is None:
        i = len(GL)
        _key2id[k] = i
        GL.append(k[0])
        GR.append(k[1])
    return i


@lru_cache(maxsize=None)
def le(a, b):
    """a <= b  iff  no a^L with b <= a^L  and  no b^R with b^R <= a."""
    return not any(le(b, x) for x in GL[a]) and not any(le(y, a) for y in GR[b])


def canon(L, R):
    L, R = set(L), set(R)
    while True:
        changed = False
        L = {a for a in L if not any(b != a and le(a, b) for b in L)}
        R = {a for a in R if not any(b != a and le(b, a) for b in R)}
        g = mk(L, R)
        for a in list(L):
            for aR in GR[a]:
                if le(aR, g):                       # Left option a reverses through aR
                    L.discard(a)
                    L |= set(GL[aR])
                    changed = True
                    break
            if changed:
                break
        if not changed:
            for b in list(R):
                for bL in GL[b]:
                    if le(g, bL):                   # Right option b reverses through bL
                        R.discard(b)
                        R |= set(GR[bL])
                        changed = True
                        break
                if changed:
                    break
        if not changed:
            return g


ZERO = mk((), ())
_int = {0: ZERO}


def integer(n):
    if n not in _int:
        _int[n] = mk([integer(n - 1)], []) if n > 0 else mk([], [integer(n + 1)])
    return _int[n]


@lru_cache(maxsize=None)
def add(a, b):
    L = [add(x, b) for x in GL[a]] + [add(a, y) for y in GL[b]]
    R = [add(x, b) for x in GR[a]] + [add(a, y) for y in GR[b]]
    return canon(L, R)


def neg(a):
    return canon([neg(x) for x in GR[a]], [neg(x) for x in GL[a]])


def outcome(g):
    ge0, le0 = le(ZERO, g), le(g, ZERO)
    return {(True, True): "P", (True, False): "L", (False, True): "R", (False, False): "N"}[(ge0, le0)]


def show(g):
    for n, v in _int.items():
        if v == g:
            return str(n)
    for name, v in NAMED.items():
        if v == g:
            return name
    Ls = ",".join(sorted(show(x) for x in GL[g]))
    Rs = ",".join(sorted(show(x) for x in GR[g]))
    return "{" + Ls + "|" + Rs + "}"


STAR = canon([ZERO], [ZERO])
STAR2 = canon([ZERO, STAR], [ZERO, STAR])
STAR3 = canon([ZERO, STAR, STAR2], [ZERO, STAR, STAR2])
UP = canon([ZERO], [STAR])
DOWN = neg(UP)
UPSTAR = add(UP, STAR)
DUPSTAR = add(add(UP, UP), STAR)
ONE, MONE = integer(1), integer(-1)
HALF = canon([ZERO], [ONE])
MHALF = neg(HALF)
SW10 = canon([ONE], [ZERO])
PM1 = canon([ONE], [MONE])
TINY1 = canon([ZERO], [canon([ZERO], [MONE])])
PM_2_1 = canon([integer(3)], [integer(1)])      # 2 +- 1 = {3|1}
PM_m2_1 = canon([integer(-1)], [integer(-3)])   # -2 +- 1 = {-1|-3}
H = canon([PM_2_1], [PM_m2_1])                   # {2+-1 | -2+-1}
NAMED = {"*": STAR, "*2": STAR2, "*3": STAR3, "up": UP, "down": DOWN, "up*": UPSTAR,
         "dup*": DUPSTAR, "1/2": HALF, "-1/2": MHALF, "{1|0}": SW10, "+-1": PM1,
         "tiny1": TINY1, "2+-1": PM_2_1, "-2+-1": PM_m2_1, "H={2+-1|-2+-1}": H}
REF = [("0", ZERO), ("*", STAR), ("*2", STAR2), ("*3", STAR3), ("up", UP), ("down", DOWN),
       ("up*", UPSTAR), ("dup*", DUPSTAR), ("1/2", HALF), ("-1/2", MHALF), ("1", ONE),
       ("-1", MONE), ("{1|0}", SW10), ("+-1", PM1), ("tiny1", TINY1)]


# ------------------------------------------------------------ pawn model
class Pawns:
    def __init__(self, files, wrap, ep=True, aware=True, race="count"):
        self.F, self.wrap, self.ep, self.aware, self.race = files, wrap, ep, aware, race
        self.stats = {"races": 0, "ep_pending_states": 0, "ep_pending_capturer_has_passer": 0,
                      "ep_pending_victim_plain_passed": 0}
        self._seen = set()

    def nbrs(self, f):
        s = set()
        for g in (f - 1, f + 1):
            if self.wrap:
                g %= self.F
            if 0 <= g < self.F and g != f:
                s.add(g)
        return s

    def is_passed(self, p, white, enemy):
        f, r = p
        span = {f} | self.nbrs(f)
        if white:
            return not any(g in span and s > r for g, s in enemy)
        return not any(g in span and s < r for g, s in enemy)

    def passers(self, st, white, aware=None):
        aware = self.aware if aware is None else aware
        W, B, ep = st
        mine, enemy = (W, B) if white else (B, W)
        out = []
        for p in mine:
            # ep = (skipped square, victim square, side allowed to capture)
            if aware and ep and ep[1] == p and ep[2] == ("B" if white else "W"):
                continue
            if self.is_passed(p, white, enemy):
                out.append(p)
        return out

    def gen(self, st, white):
        W, B, ep = st
        mine, enemy = (set(W), set(B)) if white else (set(B), set(W))
        occ = mine | enemy
        d, home, me = (1, 2, "W") if white else (-1, NR - 1, "B")
        other = "B" if white else "W"
        res = []

        def put(m, e, nep=None):
            m, e = frozenset(m), frozenset(e)
            res.append((m, e, nep) if white else (e, m, nep))

        for (f, r) in mine:
            one = (f, r + d)
            if 1 <= r + d <= NR and one not in occ:
                put(mine - {(f, r)} | {one}, enemy)
                two = (f, r + 2 * d)
                if r == home and two not in occ:
                    nep = None
                    if self.ep and any((g, r + 2 * d) in enemy for g in self.nbrs(f)):
                        nep = (one, two, other)
                    put(mine - {(f, r)} | {two}, enemy, nep)
            for g in self.nbrs(f):
                t = (g, r + d)
                if t in enemy:
                    put(mine - {(f, r)} | {t}, enemy - {t})
        if ep and ep[2] == me:
            skip, victim, _ = ep
            for g in self.nbrs(victim[0]):
                s = (g, victim[1])
                if s in mine:
                    put(mine - {s} | {skip}, enemy - {victim})
        return res

    def dist(self, ps, white):
        return min((NR - r - (r == 2)) if white else (r - 1 - (r == NR - 1)) for _, r in ps)

    def resolve(self, st, mover_white):
        wp, bp = self.passers(st, True), self.passers(st, False)
        if st not in self._seen:
            self._seen.add(st)
            if st[2]:
                self.stats["ep_pending_states"] += 1
                cap_white = st[2][2] == "W"
                if self.passers(st, cap_white, aware=False):
                    self.stats["ep_pending_capturer_has_passer"] += 1
                if self.is_passed(st[2][1], not cap_white, st[1] if not cap_white else st[0]):
                    self.stats["ep_pending_victim_plain_passed"] += 1
        if not wp and not bp:
            return st
        if wp and not bp:
            return "L"
        if bp and not wp:
            return "R"
        self.stats["races"] += 1
        mover, opp = ("L", "R") if mover_white else ("R", "L")
        if self.race == "mover":
            return mover
        if self.race == "opponent":
            return opp
        dm = self.dist(wp, True) if mover_white else self.dist(bp, False)
        do = self.dist(bp, False) if mover_white else self.dist(wp, True)
        return opp if do <= dm else mover

    def value(self, st):
        memo = {}

        def v(s):
            if s == "L":
                return integer(BIG)
            if s == "R":
                return integer(-BIG)
            if s in memo:
                return memo[s]
            L = [v(self.resolve(c, True)) for c in self.gen(s, True)]
            R = [v(self.resolve(c, False)) for c in self.gen(s, False)]
            memo[s] = canon(L, R)
            return memo[s]
        return v(st), memo

    def parse(self, text):
        W, B = set(), set()
        for part in text.split("/"):
            side, _, sqs = part.strip().partition(":")
            for t in sqs.split():
                (W if side.strip().upper() == "W" else B).add(("abcdefghij".index(t[0]), int(t[1:])))
        return (frozenset(W), frozenset(B), None)


def fmt(st):
    if isinstance(st, str):
        return "+BIG" if st == "L" else "-BIG"
    W, B, ep = st
    f = lambda s: " ".join(sorted("abcdefghij"[a] + str(b) for a, b in s))
    return f"W {f(W)} / B {f(B)}" + (f" [ep {'abcdefghij'[ep[0][0]]}{ep[0][1]} for {ep[2]}]" if ep else "")


def main():
    POS = "W: a2 c2 / B: b7 d7"
    print("H canonical:", show(H), " H == -H:", neg(H) == H)
    print("*2 + X:", "".join(outcome(add(STAR2, x)) for _, x in REF))
    print("H  + X:", "".join(outcome(add(H, x)) for _, x in REF))
    print()
    print("| board | race | e.p. | test | canonical value | = H | = *2 | G+*2 | vector | races | ep-pending states | ...capturer has plain passer | ...victim plain-passed |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for files, wrap in ((4, False), (8, False), (8, True), (5, True)):
        for race in ("count", "mover", "opponent"):
            for ep, aware in ((False, False), (True, False), (True, True)):
                m = Pawns(files, wrap, ep=ep, aware=aware, race=race)
                g = m.parse(POS)
                assert not m.passers(g, True) and not m.passers(g, False)
                val, _ = m.value(g)
                vec = "".join(outcome(add(val, x)) for _, x in REF)
                s = m.stats
                print(f"| {files}{'cyl' if wrap else 'flat'} | {race} | {'on' if ep else 'off'} | "
                      f"{'aware' if aware else 'plain'} | {show(val)} | {val == H} | {val == STAR2} | "
                      f"{outcome(add(val, STAR2))} | {vec} | {s['races']} | {s['ep_pending_states']} | "
                      f"{s['ep_pending_capturer_has_passer']} | {s['ep_pending_victim_plain_passed']} |")
    print()
    # options of the root and the mechanism line, 4-file flat, count, aware vs plain
    for aware in (False, True):
        m = Pawns(4, False, ep=True, aware=aware, race="count")
        g = m.parse(POS)
        val, memo = m.value(g)
        tag = "aware" if aware else "plain"
        print(f"[{tag}] root = {show(val)}")
        for white in (True, False):
            for c in m.gen(g, white):
                r = m.resolve(c, white)
                vv = integer(BIG) if r == "L" else integer(-BIG) if r == "R" else memo[r]
                print(f"   {'L' if white else 'R'}-option {fmt(c)} = {show(vv)}")
        x = m.parse("W: a2 c2 / B: b4 d7")
        xv, xm = m.value(x)
        print(f"   X = W a2 c2 / B b4 d7 = {show(xv)}")
        for c in m.gen(x, True):
            if (0, 4) in c[0]:
                r = m.resolve(c, True)
                print(f"     after a2-a4: {fmt(r)}" + ("" if isinstance(r, str) else f" = {show(xm[r])}"))
                if not isinstance(r, str):
                    for c2 in m.gen(r, False):
                        r2 = m.resolve(c2, False)
                        print(f"        Black reply {fmt(c2)} -> {fmt(r2) if isinstance(r2, str) else show(xm.get(r2) or m.value(r2)[0])}")


if __name__ == "__main__":
    main()
