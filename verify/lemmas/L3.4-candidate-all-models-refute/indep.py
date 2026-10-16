"""Independent re-computation of claim L3.4 (the *2 candidate W a2 c2 / B b7 d7).

Written from the rule text in notes/lemmas.md section 0 only. It imports NOTHING
from cylcgt/, lemmas/ or crosscheck/ (stdlib only).

Two independent methods:
  A. CGT-free: G = *2  <=>  G + *2 is a second-player win (P); G = 0 <=> G in P.
     The sum G + *h is searched by plain minimax over states (pawn position with
     its e.p. right, heap size, side to move). Terminal +-BIG + *k is decided
     (BIG + *k > 0), so a passer / scored race decides the sum.
  B. A small canonical-form CGT engine of my own (dominated-option removal and
     reversible-option bypass), giving the canonical value of S, W, WF.

Models (notes/lemmas.md section 0):
  W  : whole board; exactly one side passed -> +-BIG; a move creating passers
       for both sides scored by the race rule; e.p. rights global (a node's
       Left options are generated with a Black right deleted, and vice versa).
  WF : W plus, at every non-terminal node, a Left option -BIG and a Right option +BIG.
  S  : sum model: root passer check, then the sum of the component values;
       component C(Z) = { c(Z') | c(Z'') }, c = race score or S(child).

Run:  cd <root> && .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-refute/indep.py
"""
from __future__ import annotations

import sys
import time
from functools import lru_cache

sys.setrecursionlimit(100000)

RANKS = 8
FILES = "abcdefgh"


# ---------------------------------------------------------------------------
# pawn rules
# ---------------------------------------------------------------------------
class Bd:
    def __init__(self, nfiles, ep, wrap=False, big=256):
        self.n, self.ep, self.wrap, self.big = nfiles, ep, wrap, big

    def adj(self, f):
        out = []
        for g in (f - 1, f + 1):
            if self.wrap:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return out

    def key(self):
        return (self.n, self.ep, self.wrap, self.big)


def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def parse(w, b):
    return (frozenset(map(sq, w.split())), frozenset(map(sq, b.split())), None)


def show(p):
    w, b, e = p
    nm = lambda s: f"{FILES[s[0]]}{s[1]}"
    t = "W: " + " ".join(sorted(map(nm, w))) + " / B: " + " ".join(sorted(map(nm, b)))
    if e:
        t += f" (ep {nm(e[0])} for {e[2]})"
    return t


def has_passer(bd, p, side):
    w, b, _ = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    for (f, r) in mine:
        fs = {f, *bd.adj(f)}
        if side == "W":
            if not any(g in fs and s > r for (g, s) in theirs):
                return True
        else:
            if not any(g in fs and s < r for (g, s) in theirs):
                return True
    return False


def gen(bd, p, side):
    """Children after a move of `side`. A right is usable only if it belongs to
    `side`; children never inherit a right, except the one a double step makes."""
    w, b, e = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    occ = w | b
    dr = 1 if side == "W" else -1
    start = 2 if side == "W" else RANKS - 1
    right = e if (e is not None and e[2] == side) else None
    res = []

    def put(m2, t2, ne=None):
        res.append((m2, t2, ne) if side == "W" else (t2, m2, ne))

    for (f, r) in mine:
        m0 = mine - {(f, r)}
        r1 = r + dr
        if 1 <= r1 <= RANKS and (f, r1) not in occ:
            put(m0 | {(f, r1)}, theirs)
            r2 = r + 2 * dr
            if r == start and (f, r2) not in occ:
                ne = ((f, r1), (f, r2), "B" if side == "W" else "W") if bd.ep else None
                put(m0 | {(f, r2)}, theirs, ne)
        if 1 <= r1 <= RANKS:
            for g in bd.adj(f):
                if (g, r1) in theirs:
                    put(m0 | {(g, r1)}, theirs - {(g, r1)})
                elif right is not None and right[0] == (g, r1):
                    put(m0 | {(g, r1)}, theirs - {right[1]})
    out = []
    seen = set()
    for c in res:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def dist(bd, p, side):
    """Smallest promotion distance of a passed front pawn of `side`
    (a double step from the start rank counts as one move)."""
    w, b, _ = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    best = None
    for (f, r) in mine:
        fs = {f, *bd.adj(f)}
        if side == "W":
            if any(g in fs and s > r for (g, s) in theirs):
                continue
            if any((f, s) in mine for s in range(r + 1, RANKS + 1)):
                continue
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            if any(g in fs and s < r for (g, s) in theirs):
                continue
            if any((f, s) in mine for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        best = d if best is None else min(best, d)
    return best


def race_winner(bd, child, mover, rule):
    nu = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return nu
    return nu if dist(bd, child, nu) <= dist(bd, child, mover) else mover


def term(bd, p):
    """None (no passer), 'W', 'B' or 'race'."""
    a, c = has_passer(bd, p, "W"), has_passer(bd, p, "B")
    if a and c:
        return "race"
    if a:
        return "W"
    if c:
        return "B"
    return None


def comps(bd, p):
    """Split into components separated by empty files (flat board only here)."""
    w, b, e = p
    occf = sorted({f for f, _ in w | b})
    groups = []
    for f in occf:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.n - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for gr in groups:
        s = set(gr)
        ee = e if (e is not None and e[0][0] in s) else None
        out.append((frozenset(x for x in w if x[0] in s), frozenset(x for x in b if x[0] in s), ee))
    return out


# ---------------------------------------------------------------------------
# Method A: CGT-free minimax of  W(X) + *h  (and WF(X) + *h)
# ---------------------------------------------------------------------------
def make_winA(bd, rule, kings):
    @lru_cache(maxsize=None)
    def win(p, h, tm):
        """True iff side `tm` to move wins W(p)+*h (p non-terminal)."""
        other = "B" if tm == "W" else "W"
        for c in gen(bd, p, tm):
            t = term(bd, c)
            if t == "race":
                if race_winner(bd, c, tm, rule) == tm:
                    return True
                continue
            if t is not None:
                if t == tm:
                    return True
                continue
            if not win(c, h, other):
                return True
        for j in range(h):
            if not win(p, j, other):
                return True
        # king move (WF): immediate loss for the mover -> never a winning move
        return False
    return win


def outcome_from(w_first, w_second):
    # w_first: Left wins moving first; w_second: Left wins moving second
    if w_first and w_second:
        return "L"
    if not w_first and not w_second:
        return "R"
    return "N" if w_first else "P"


def outcomeA(bd, root, rule, kings, h):
    win = make_winA(bd, rule, kings)
    lf = win(root, h, "W")
    ls = not win(root, h, "B")
    return outcome_from(lf, ls)


# ---------------------------------------------------------------------------
# Method B: tiny canonical-form CGT engine
# ---------------------------------------------------------------------------
class E:
    def __init__(self):
        self.forms = []          # id -> (L tuple, R tuple)
        self.index = {}
        self.le_memo = {}
        self.canon_memo = {}
        self.ints = {}
        self.ZERO = self.intern((), ())

    def intern(self, L, R):
        k = (tuple(sorted(set(L))), tuple(sorted(set(R))))
        i = self.index.get(k)
        if i is None:
            i = len(self.forms)
            self.forms.append(k)
            self.index[k] = i
        return i

    def le(self, g, h):
        k = (g, h)
        r = self.le_memo.get(k)
        if r is None:
            gl, _ = self.forms[g]
            _, hr = self.forms[h]
            r = not any(self.le(h, x) for x in gl) and not any(self.le(x, g) for x in hr)
            self.le_memo[k] = r
        return r

    def eq(self, g, h):
        return self.le(g, h) and self.le(h, g)

    def integer(self, n):
        if n in self.ints:
            return self.ints[n]
        if n == 0:
            g = self.ZERO
        elif n > 0:
            g = self.intern((self.integer(n - 1),), ())
        else:
            g = self.intern((), (self.integer(n + 1),))
        self.ints[n] = g
        return g

    def make(self, L, R):
        """Canonical form of {L | R}, L and R lists of canonical ids."""
        L, R = list(set(L)), list(set(R))
        while True:
            changed = False
            # dominated
            L2 = [x for x in L if not any(y != x and self.le(x, y) for y in L)]
            R2 = [x for x in R if not any(y != x and self.le(y, x) for y in R)]
            if len(L2) != len(L) or len(R2) != len(R):
                changed = True
            L, R = L2, R2
            g = self.intern(L, R)
            # reversible Left options
            newL = []
            for x in L:
                xr = self.forms[x][1]
                rev = next((y for y in xr if self.le(y, g)), None)
                if rev is not None:
                    newL.extend(self.forms[rev][0])
                    changed = True
                else:
                    newL.append(x)
            newL = list(set(newL))
            g = self.intern(newL, R)
            newR = []
            for x in R:
                xl = self.forms[x][0]
                rev = next((y for y in xl if self.le(g, y)), None)
                if rev is not None:
                    newR.extend(self.forms[rev][1])
                    changed = True
                else:
                    newR.append(x)
            newR = list(set(newR))
            L, R = newL, newR
            if not changed:
                return self.intern(L, R)

    def add(self, g, h):
        if g == self.ZERO:
            return h
        if h == self.ZERO:
            return g
        k = (min(g, h), max(g, h))
        r = self.canon_memo.get(("add",) + k)
        if r is None:
            gl, gr = self.forms[g]
            hl, hr = self.forms[h]
            L = [self.add(x, h) for x in gl] + [self.add(g, x) for x in hl]
            R = [self.add(x, h) for x in gr] + [self.add(g, x) for x in hr]
            r = self.make(L, R)
            self.canon_memo[("add",) + k] = r
        return r

    def nim(self, k):
        if k == 0:
            return self.ZERO
        opts = [self.nim(j) for j in range(k)]
        return self.make(opts, opts)

    def name(self, g):
        for k in range(5):
            if self.eq(g, self.nim(k)):
                return "0" if k == 0 else ("*" if k == 1 else f"*{k}")
        L, R = self.forms[g]
        return "{" + ",".join(self.name(x) for x in L) + "|" + ",".join(self.name(x) for x in R) + "}"


def make_W(eng, bd, rule, kings):
    PB, NB = eng.integer(bd.big), eng.integer(-bd.big)
    memo = {}

    def W(p):
        r = memo.get(p)
        if r is not None:
            return r
        t = term(bd, p)
        assert t != "race"
        if t == "W":
            r = PB
        elif t == "B":
            r = NB
        else:
            L = [child(c, "W") for c in gen(bd, p, "W")]
            R = [child(c, "B") for c in gen(bd, p, "B")]
            if kings:
                L.append(NB)
                R.append(PB)
            r = eng.make(L, R)
        memo[p] = r
        return r

    def child(c, mover):
        if term(bd, c) == "race":
            return PB if race_winner(bd, c, mover, rule) == "W" else NB
        return W(c)
    return W


def make_S(eng, bd, rule):
    PB, NB = eng.integer(bd.big), eng.integer(-bd.big)
    memo = {}
    splits = []

    def S(p):
        t = term(bd, p)
        if t == "W":
            return PB
        if t == "B":
            return NB
        assert t is None
        cs = comps(bd, p)
        g = eng.ZERO
        for c in cs:
            g = eng.add(g, C(c))
        return g

    def C(z):
        r = memo.get(z)
        if r is not None:
            return r
        t = term(bd, z)
        if t == "W":
            r = PB
        elif t == "B":
            r = NB
        else:
            L = [ch(c, "W") for c in gen(bd, z, "W")]
            R = [ch(c, "B") for c in gen(bd, z, "B")]
            r = eng.make(L, R)
        memo[z] = r
        return r

    def ch(c, mover):
        t = term(bd, c)
        if t == "race":
            return PB if race_winner(bd, c, mover, rule) == "W" else NB
        if t is None and len(comps(bd, c)) > 1:
            splits.append(c)
        return S(c)
    return S, splits


# ---------------------------------------------------------------------------
# tree statistics
# ---------------------------------------------------------------------------
def tree_stats(bd, root, gpair_files=frozenset()):
    seen = {root}
    st = [root]
    nonterm = 0
    multi = 0
    ep_caps = 0
    race_edges = 0
    race_children = set()
    while st:
        x = st.pop()
        if term(bd, x) is not None:
            continue
        nonterm += 1
        live = [c for c in comps(bd, x) if not ({f for f, _ in c[0] | c[1]} <= gpair_files)]
        if len(live) > 1:
            multi += 1
        for side in "WB":
            for c in gen(bd, x, side):
                if len(c[0]) + len(c[1]) < len(x[0]) + len(x[1]):
                    w0, b0, _ = x
                    # e.p. capture: capturer lands on an empty square
                    if side == "W" and not ((c[0] - w0) <= b0):
                        ep_caps += 1
                    if side == "B" and not ((c[1] - b0) <= w0):
                        ep_caps += 1
                if term(bd, c) == "race":
                    race_edges += 1
                    race_children.add((c, side))
                if c not in seen:
                    seen.add(c)
                    st.append(c)
    return dict(reachable=len(seen), nonterminal=nonterm, multi_live_component_nodes=multi,
                ep_capture_edges=ep_caps, race_edges=race_edges, race_children=len(race_children))


def main():
    t0 = time.time()
    x4 = parse("a2 c2", "b7 d7")
    x8 = parse("a2 c2 g4", "b7 d7 g5")
    print("candidate:", show(x4), " | 8x8:", show(x8))
    rows = []
    for ep in (True, False):
        b4, b8 = Bd(4, ep), Bd(8, ep)
        print(f"\n== e.p. {'on' if ep else 'off'} ==")
        print(" tree stats 4-file:", tree_stats(b4, x4))
        print(" tree stats 8x8   :", tree_stats(b8, x8, frozenset({6})))
        for rule in ("count", "mover", "opponent"):
            # Method A
            oa = {}
            for nm, bd, x in (("4", b4, x4), ("8", b8, x8)):
                for kings in (False, True):
                    oa[(nm, kings)] = (outcomeA(bd, x, rule, kings, 0), outcomeA(bd, x, rule, kings, 1),
                                       outcomeA(bd, x, rule, kings, 2), outcomeA(bd, x, rule, kings, 3))
            # Method B
            eng = E()
            vals = {}
            for nm, bd, x in (("4", b4, x4), ("8", b8, x8)):
                Sf, splits = make_S(eng, bd, rule)
                vals["S" + nm] = Sf(x)
                vals["W" + nm] = make_W(eng, bd, rule, False)(x)
                vals["WF" + nm] = make_W(eng, bd, rule, True)(x)
                vals["splits" + nm] = len(splits)
            names = {k: eng.name(v) for k, v in vals.items() if not k.startswith("splits")}
            print(f" rule={rule:8s} B-engine values: {names}  (split events in S: 4f={vals['splits4']}, 8f={vals['splits8']})")
            for k, v in oa.items():
                print(f"   A: board={k[0]}f kings={k[1]!s:5s} outcome of G+*0,G+*1,G+*2,G+*3 = {v}")
            rows.append((ep, rule, names, oa))
    # robustness: does the value depend on BIG?
    print("\n== BIG robustness (W, 4 files) ==")
    for big in (32, 64, 1000):
        for ep in (True, False):
            for rule in ("count", "mover", "opponent"):
                eng = E()
                bd = Bd(4, ep, big=big)
                print(f" BIG={big} ep={ep} {rule}: W={eng.name(make_W(eng, bd, rule, False)(x4))}"
                      f" WF={eng.name(make_W(eng, bd, rule, True)(x4))}")
    print(f"\ntime {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
