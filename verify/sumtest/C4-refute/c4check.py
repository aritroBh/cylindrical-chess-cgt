"""Independent check of claim C4 (refute lens).  Imports nothing from cylcgt/,
crosscheck/ or sumtest/.  Own canonical-form CGT + own pawn model.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C4-refute/c4check.py
"""
import sys
import threading
from fractions import Fraction

sys.setrecursionlimit(2_000_000)

# --------------------------------------------------------------------------
# minimal CGT: games are ints (ids) into GAMES; GAMES[i] = (Ltuple, Rtuple)
# --------------------------------------------------------------------------
GAMES = []
INTERN = {}
LE = {}


def raw(L, R):
    key = (tuple(sorted(set(L))), tuple(sorted(set(R))))
    g = INTERN.get(key)
    if g is None:
        g = len(GAMES)
        GAMES.append(key)
        INTERN[key] = g
    return g


def le(g, h):
    """g <= h"""
    k = (g, h)
    v = LE.get(k)
    if v is None:
        gl, _ = GAMES[g]
        _, hr = GAMES[h]
        v = (not any(le(h, x) for x in gl)) and (not any(le(y, g) for y in hr))
        LE[k] = v
    return v


def eq(g, h):
    return le(g, h) and le(h, g)


def canon(L, R):
    """canonical form of {L | R}, where L, R are canonical ids"""
    L, R = set(L), set(R)
    while True:
        changed = False
        g = raw(L, R)
        nL = set()
        for a in L:
            rev = next((ar for ar in GAMES[a][1] if le(ar, g)), None)
            if rev is None:
                nL.add(a)
            else:
                nL |= set(GAMES[rev][0])
                changed = True
        nR = set()
        for b in R:
            rev = next((bl for bl in GAMES[b][0] if le(g, bl)), None)
            if rev is None:
                nR.add(b)
            else:
                nR |= set(GAMES[rev][1])
                changed = True
        L = {a for a in nL if not any(b != a and le(a, b) for b in nL)}
        R = {b for b in nR if not any(c != b and le(c, b) for c in nR)}
        if not changed:
            return raw(L, R)


def neg(g, memo={}):
    if g in memo:
        return memo[g]
    L, R = GAMES[g]
    r = canon([neg(x) for x in R], [neg(x) for x in L])
    memo[g] = r
    return r


ADD = {}


def add(g, h):
    k = (min(g, h), max(g, h))
    if k in ADD:
        return ADD[k]
    gL, gR = GAMES[g]
    hL, hR = GAMES[h]
    r = canon([add(x, h) for x in gL] + [add(g, y) for y in hL],
              [add(x, h) for x in gR] + [add(g, y) for y in hR])
    ADD[k] = r
    return r


ZERO = canon([], [])
_INT = {0: ZERO}


def integer(n):
    if n in _INT:
        return _INT[n]
    for k in range(1, abs(n) + 1):
        if k not in _INT:
            _INT[k] = canon([_INT[k - 1]], [])
        if -k not in _INT:
            _INT[-k] = canon([], [_INT[-(k - 1)]])
    return _INT[n]


def sw(a, b):
    return canon([a], [b])


def star():
    return canon([ZERO], [ZERO])


def nim(n):
    opts = [nim(k) for k in range(n)]
    return canon(opts, opts)


def number_value(g, memo={}):
    """value if canonical form g is a number, else None"""
    if g in memo:
        return memo[g]
    L, R = GAMES[g]
    lv = [number_value(x) for x in L]
    rv = [number_value(x) for x in R]
    res = None
    if all(v is not None for v in lv + rv) and len(L) <= 1 and len(R) <= 1:
        lo = lv[0] if lv else None
        hi = rv[0] if rv else None
        if lo is None and hi is None:
            res = Fraction(0)
        elif hi is None:
            res = lo + 1
        elif lo is None:
            res = hi - 1
        elif lo < hi:
            res = (lo + hi) / 2
    memo[g] = res
    return res


def outcome(g):
    L, R = GAMES[g]
    # Left moving first wins iff exists GL >= 0 ; Right moving first wins iff exists GR <= 0
    lw = any(le(ZERO, x) for x in L)
    rw = any(le(x, ZERO) for x in R)
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


def show(g, depth=0):
    if g == ZERO:
        return "0"
    nv = number_value(g)
    if nv is not None:
        return str(nv)
    for n in range(1, 6):
        if g == nim(n):
            return "*" if n == 1 else f"*{n}"
    L, R = GAMES[g]
    # +-x: {x | -x}
    if len(L) == 1 and len(R) == 1:
        a, b = L[0], R[0]
        if b == neg(a) and number_value(a) is not None:
            return f"+-{show(a)}"
        na, nb = number_value(a), number_value(b)
        if na is not None and nb is not None and na > nb and (na + nb) % 2 == 0:
            c = (na + nb) / 2
            return f"{c}+-{(na - nb) / 2}"
    if depth > 6:
        return "{...}"
    return "{" + ", ".join(show(x, depth + 1) for x in L) + " | " + \
        ", ".join(show(x, depth + 1) for x in R) + "}"


# --------------------------------------------------------------------------
# pawn model
# --------------------------------------------------------------------------
BIG = 256


class Model:
    def __init__(self, files=4, ranks=8, wrap=False, ep=True, aware=False, race="count",
                 split=False, race_excl_epable=True):
        self.F, self.N, self.wrap, self.ep, self.aware, self.race = files, ranks, wrap, ep, aware, race
        self.split = split
        self.race_excl_epable = race_excl_epable
        self.memo = {}
        self.race_nodes = set()

    def adj(self, f):
        out = [f]
        for d in (-1, 1):
            g = f + d
            if self.wrap:
                out.append(g % self.F)
            elif 0 <= g < self.F:
                out.append(g)
        return out

    def nb(self, f):
        return [g for g in self.adj(f) if g != f]

    # ep = None or (target_sq, victim_sq, entitled_side)
    def epable_victim(self, W, B, ep, side):
        """victim pawn of `side` that the opponent can capture e.p. right now"""
        if not ep or not self.ep:
            return None
        tgt, vic, ent = ep
        if ent == side:
            return None
        enemy = B if side == "W" else W
        vf, vr = vic
        if any((g, vr) in enemy for g in self.nb(vf)):
            return vic
        return None

    def passed_pawns(self, W, B, ep, side):
        mine, theirs = (W, B) if side == "W" else (B, W)
        out = []
        for (f, r) in mine:
            fs = set(self.adj(f))
            if side == "W":
                blocked = any(g in fs and s > r for (g, s) in theirs)
            else:
                blocked = any(g in fs and s < r for (g, s) in theirs)
            if not blocked:
                out.append((f, r))
        if self.aware:
            v = self.epable_victim(W, B, ep, side)
            if v is not None and v in out:
                out.remove(v)
        return out

    def dist(self, sq, side):
        f, r = sq
        if side == "W":
            return self.N - r - (1 if r == 2 else 0)
        return r - 1 - (1 if r == self.N - 1 else 0)

    def moves(self, W, B, ep, side):
        """children states after `side` moves (ep right of the other side, if any, is dropped)"""
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        home = 2 if side == "W" else self.N - 1
        other = "B" if side == "W" else "W"
        my_ep = ep if (ep and self.ep and ep[2] == side) else None
        out = []

        def emit(nm, nt, nep=None):
            if side == "W":
                out.append((frozenset(nm), frozenset(nt), nep))
            else:
                out.append((frozenset(nt), frozenset(nm), nep))

        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            assert 1 <= r1 <= self.N, "promotion square reached in unresolved node"
            if (f, r1) not in occ:
                emit(rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == home and (f, r2) not in occ:
                    nep = ((f, r1), (f, r2), other) if self.ep else None
                    emit(rest | {(f, r2)}, theirs, nep)
            for g in self.nb(f):
                t = (g, r1)
                if t in theirs:
                    emit(rest | {t}, theirs - {t})
                elif my_ep and my_ep[0] == t:
                    emit(rest | {t}, theirs - {my_ep[1]})
        return list(dict.fromkeys(out))

    def resolve(self, st, mover):
        """None if unresolved, else +BIG / -BIG"""
        W, B, ep = st
        pw = self.passed_pawns(W, B, ep, "W")
        pb = self.passed_pawns(W, B, ep, "B")
        if pw and pb:
            self.race_nodes.add(st)
            other = "B" if mover == "W" else "W"
            if self.race == "mover":
                win = mover
            elif self.race == "opponent":
                win = other
            else:
                dm = min(self.dist(s, mover) for s in (pw if mover == "W" else pb))
                do = min(self.dist(s, other) for s in (pw if other == "W" else pb))
                win = other if do <= dm else mover
            return BIG if win == "W" else -BIG
        if pw:
            return BIG
        if pb:
            return -BIG
        return None

    def components(self, W, B, ep):
        files = sorted({f for f, _ in W | B})
        groups = []
        for f in files:
            if groups and f == groups[-1][-1] + 1:
                groups[-1].append(f)
            else:
                groups.append([f])
        if self.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == self.F - 1:
            groups[0] = groups.pop() + groups[0]
        out = []
        for gr in groups:
            s = set(gr)
            e = ep if (ep and ep[1][0] in s) else None
            out.append((frozenset(p for p in W if p[0] in s), frozenset(p for p in B if p[0] in s), e))
        return out

    def value(self, st):
        if st in self.memo:
            return self.memo[st]
        W, B, ep = st
        if self.split:
            comps = self.components(W, B, ep)
            if len(comps) > 1:
                v = ZERO
                for c in comps:
                    v = add(v, self.value(c))
                self.memo[st] = v
                return v
        L, R = [], []
        for side, lst in (("W", L), ("B", R)):
            for c in self.moves(W, B, ep, side):
                res = self.resolve(c, side)
                lst.append(integer(res) if res is not None else self.value(c))
        v = canon(L, R)
        self.memo[st] = v
        return v


def parse(text):
    w, b = text.split("/")
    def sqs(s):
        return frozenset((ord(t[0]) - 97, int(t[1:])) for t in s.split(":")[1].split())
    return sqs(w), sqs(b)


def main():
    I = integer
    pm256 = sw(I(256), I(-256))
    T_text = canon([I(256)], [pm256])          # {256 | +-256}
    m3 = I(-3)
    m2pm1 = sw(I(-1), I(-3))                    # -2 +- 1
    p2pm1 = sw(I(3), I(1))
    root_aware = canon([p2pm1], [m2pm1])        # {2+-1 | -2+-1}
    s2 = nim(2)
    targets = {"{256|+-256}": T_text, "-3": m3, "0": ZERO, "-2+-1": m2pm1,
               "*2": s2, "{2+-1|-2+-1}": root_aware}

    X = "W: a2 c2 / B: b4 d7"
    B5 = "W: a2 c2 / B: b5 d7"
    G = "W: a2 c2 / B: b7 d7"
    rows = []
    for race in ("count", "mover", "opponent"):
        for ep, aware in ((True, False), (True, True), (False, False)):
            for split in (False, True):
                m = Model(4, 8, False, ep=ep, aware=aware, race=race, split=split)
                res = {}
                for name, pos in (("X", X), ("B5", B5), ("G", G)):
                    W, Bp = parse(pos)
                    v = m.value((W, Bp, None))
                    match = [k for k, t in targets.items() if v == t]
                    res[name] = (show(v), match, outcome(v))
                tag = f"race={race:8s} ep={'on ' if ep else 'off'} test={'aware' if aware else 'textbook'} split={split}"
                print(tag)
                for k in ("X", "B5", "G"):
                    print(f"   {k:2s} = {res[k][0]:30s} equals {res[k][1]}  outcome {res[k][2]}")
                print(f"   race nodes visited: {len(m.race_nodes)}")
    # Two-ply detail of the mechanism (aware, count)
    print("\nMechanism detail (count rule, ep on):")
    for aware in (False, True):
        m = Model(4, 8, False, ep=True, aware=aware, race="count")
        W, Bp = parse(X)
        st = (W, Bp, None)
        for c in m.moves(*st, "W"):
            res = m.resolve(c, "W")
            desc = sorted(c[0]), sorted(c[1]), c[2]
            val = res if res is not None else show(m.value(c))
            print(f"  test={'aware' if aware else 'textbook'}  Left option {desc} -> {val}")
        y = ((W - {(0, 2)}) | {(0, 4)}, Bp, ((0, 3), (0, 4), "B"))
        if m.resolve(y, "W") is None:
            for c in m.moves(*y, "B"):
                res = m.resolve(c, "B")
                print(f"     after a2-a4, Right {sorted(c[0])} / {sorted(c[1])} -> "
                      f"{res if res is not None else show(m.value(c))}")


if __name__ == "__main__":
    threading.stack_size(1 << 29)
    t = threading.Thread(target=main)
    t.start()
    t.join()
