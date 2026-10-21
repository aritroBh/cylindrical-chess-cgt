"""Independent re-derivation of claim N1 (paper 7.3 {c,d} sub-game: W c1 c3 d3 / B c2 d4 d5 d6).

Imports NOTHING from cylcgt/ or crosscheck/. Two independent engines in this file:
  (A) a from-scratch short-game CGT library (interned games, <=, canonical form by
      dominated-option removal and reversible-option bypass) + a from-scratch pawn
      move generator -> exact canonical value of the sub-game and of each option;
  (B) a pure win/loss search over disjunctive sums (pawn component played by the move
      generator + explicit game trees), with NO canonicalisation, used for the decisive
      test "G + miny(1) is a second-player win  <=>  G = tiny(1)", plus G+(-1), G+*, G-1.
Variants swept: board (cylinder / flat), en passant on/off, race rule (count/mover/opponent),
termination ("passed": exactly-one-passer = +-BIG, Elkies convention; "promote": play on
until a pawn actually reaches the last rank), BIG in {16, 256}.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/N1-refute/v3/indep_n1.py
"""
import sys
import threading
from itertools import product

FILES = "abcdefgh"
NF, NR = 8, 8

# ---------------------------------------------------------------- (A) mini CGT
NODES = []          # id -> (sorted tuple of Left ids, sorted tuple of Right ids)
INTERN = {}
LE = {}


def node(L, R):
    key = (frozenset(L), frozenset(R))
    i = INTERN.get(key)
    if i is None:
        i = INTERN[key] = len(NODES)
        NODES.append((tuple(sorted(key[0])), tuple(sorted(key[1]))))
    return i


def le(a, b):
    """a <= b  iff  no a^L with b <= a^L  and no b^R with b^R <= a."""
    k = (a, b)
    r = LE.get(k)
    if r is None:
        aL, _ = NODES[a]
        _, bR = NODES[b]
        r = not any(le(b, x) for x in aL) and not any(le(y, a) for y in bR)
        LE[k] = r
    return r


def eq(a, b):
    return le(a, b) and le(b, a)


def canon(L, R):
    """Canonical form, assuming every option id is itself canonical."""
    L, R = set(L), set(R)
    while True:
        # dominated options
        L = {x for x in L if not any(y != x and le(x, y) for y in L)}
        R = {x for x in R if not any(y != x and le(y, x) for y in R)}
        G = node(L, R)
        changed = False
        for x in sorted(L):
            for xr in NODES[x][1]:
                if le(xr, G):                     # x reversible through xr
                    L.discard(x)
                    L |= set(NODES[xr][0])
                    changed = True
                    break
            if changed:
                break
        if not changed:
            for x in sorted(R):
                for xl in NODES[x][0]:
                    if le(G, xl):                 # x reversible through xl
                        R.discard(x)
                        R |= set(NODES[xl][1])
                        changed = True
                        break
                if changed:
                    break
        if not changed:
            return G


_INT = {}


def INT(n):
    if n not in _INT:
        if n == 0:
            _INT[n] = node([], [])
        elif n > 0:
            _INT[n] = node([INT(n - 1)], [])
        else:
            _INT[n] = node([], [INT(n + 1)])
    return _INT[n]


def neg(g, memo={}):
    if g not in memo:
        L, R = NODES[g]
        memo[g] = node([neg(y) for y in R], [neg(x) for x in L])
    return memo[g]


ZERO = INT(0)
STAR = node([ZERO], [ZERO])


def show(g, depth=0):
    for n, i in _INT.items():
        if i == g:
            return str(n)
    if g == STAR:
        return "*"
    L, R = NODES[g]
    if len(L) == 1 and len(R) == 1 and L[0] == R[0]:
        s = show(L[0])
        if s.lstrip("-").isdigit():
            return s + "*"
    if depth > 6:
        return "..."
    return "{" + ", ".join(show(x, depth + 1) for x in L) + " | " + ", ".join(show(x, depth + 1) for x in R) + "}"


# ---------------------------------------------------------------- pawn rules
def nb(f, d, wrap):
    g = f + d
    if wrap:
        return g % NF
    return g if 0 <= g < NF else None


def passed(W, B, side, wrap):
    mine, theirs = (W, B) if side == "W" else (B, W)
    for f, r in mine:
        fs = {f} | {g for g in (nb(f, -1, wrap), nb(f, 1, wrap)) if g is not None}
        if side == "W":
            stop = any(g in fs and s > r for g, s in theirs)
        else:
            stop = any(g in fs and s < r for g, s in theirs)
        if not stop:
            return True
    return False


STATS = {"double_steps": 0, "ep_captures": 0, "races": 0}


def gen(W, B, ep, side, wrap, ep_on):
    """Child positions (W, B, ep) after one move by `side`. ep = (target, captured, owner) or None."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else NR - 1
    other = "B" if side == "W" else "W"
    my_ep = ep if (ep and ep[2] == side) else None
    out = []

    def emit(nm, nt, e=None):
        out.append((frozenset(nm), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm), e))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= NR:
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= NR and (f, r2) not in occ:
                STATS["double_steps"] += 1
                emit(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if ep_on else None)
        for df in (-1, 1):
            g = nb(f, df, wrap)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif my_ep and my_ep[0] == t:
                STATS["ep_captures"] += 1
                emit(rest | {t}, theirs - {my_ep[1]})
    return list(dict.fromkeys(out))


def dist(W, B, side, wrap):
    """Moves to promote for the best front-most passed pawn of `side` (double step counts as one)."""
    best = None
    occ = W | B
    for f, r in (W if side == "W" else B):
        if not passed(frozenset([(f, r)]) if side == "W" else W,
                      B if side == "W" else frozenset([(f, r)]), side, wrap):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, NR + 1)):
                continue
            dd = NR - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == NR - 1 else 0)
        best = dd if best is None else min(best, dd)
    return 10 ** 6 if best is None else best


class Rules:
    def __init__(self, wrap, ep_on, race, term, big):
        self.wrap, self.ep_on, self.race, self.term, self.big = wrap, ep_on, race, term, big

    def terminal(self, W, B, mover):
        """Integer value if (W,B) is decided, else None. `mover` = side that just moved (or None at root)."""
        if self.term == "promote":
            if any(r == NR for _, r in W):
                return self.big
            if any(r == 1 for _, r in B):
                return -self.big
            return None
        wp, bp = passed(W, B, "W", self.wrap), passed(W, B, "B", self.wrap)
        if wp and bp:
            if mover is None:
                raise RuntimeError("race at root")
            STATS["races"] += 1
            if self.race == "mover":
                win = mover
            elif self.race == "opponent":
                win = "B" if mover == "W" else "W"
            else:
                opp = "B" if mover == "W" else "W"
                win = opp if dist(W, B, opp, self.wrap) <= dist(W, B, mover, self.wrap) else mover
            return self.big if win == "W" else -self.big
        if wp:
            return self.big
        if bp:
            return -self.big
        return None


def cgt_value(rules, W, B, ep=None, mover=None, memo=None):
    if memo is None:
        memo = {}
    key = (W, B, ep, mover if rules.term == "passed" else None)
    if key in memo:
        return memo[key]
    t = rules.terminal(W, B, mover)
    if t is not None:
        v = INT(t)
    else:
        lep = ep if (ep and ep[2] == "W") else None
        rep = ep if (ep and ep[2] == "B") else None
        L = [cgt_value(rules, w, b, e, "W", memo) for (w, b, e) in gen(W, B, lep, "W", rules.wrap, rules.ep_on)]
        R = [cgt_value(rules, w, b, e, "B", memo) for (w, b, e) in gen(W, B, rep, "B", rules.wrap, rules.ep_on)]
        v = canon(L, R)
    memo[key] = v
    return v


# ---------------------------------------------------------------- (B) pure sum search (no CGT)
def T(L, R):
    return (tuple(L), tuple(R))


def TINT(n):
    if n == 0:
        return T([], [])
    return T([TINT(n - 1)], []) if n > 0 else T([], [TINT(n + 1)])


T0 = TINT(0)
TSTAR = T([T0], [T0])
TMINY1 = T([T([TINT(1)], [T0])], [T0])      # miny(1) = {1|0 || 0} = -tiny(1)
TTINY1 = T([T0], [T([T0], [TINT(-1)])])     # tiny(1) = {0 || 0|-1}
TUP = T([T0], [TSTAR])
TDOWN = T([TSTAR], [T0])


def sum_outcome(rules, W, B, tree):
    """Outcome class of (pawn component) + (explicit tree), by plain minimax over the sum."""
    memo = {}

    def pawn_moves(pc, side):
        kind = pc[0]
        if kind == "int":
            n = pc[1]
            if side == "W" and n > 0:
                return [("int", n - 1)]
            if side == "B" and n < 0:
                return [("int", n + 1)]
            return []
        _, w, b, ep = pc
        myep = ep if (ep and ep[2] == side) else None
        res = []
        for (w2, b2, e2) in gen(w, b, myep, side, rules.wrap, rules.ep_on):
            t = rules.terminal(w2, b2, side)
            res.append(("int", t) if t is not None else ("pawn", w2, b2, e2))
        return res

    def expire(pc, side):
        # `side` moved elsewhere: its own e.p. right (if any) lapses
        if pc[0] == "pawn" and pc[3] and pc[3][2] == side:
            return ("pawn", pc[1], pc[2], None)
        return pc

    def wins(pc, tr, side):
        k = (pc, tr, side)
        if k in memo:
            return memo[k]
        other = "B" if side == "W" else "W"
        res = False
        for pc2 in pawn_moves(pc, side):
            if not wins(pc2, tr, other):
                res = True
                break
        if not res:
            for tr2 in (tr[0] if side == "W" else tr[1]):
                if not wins(expire(pc, side), tr2, other):
                    res = True
                    break
        memo[k] = res
        return res

    t0 = rules.terminal(W, B, None)
    pc0 = ("int", t0) if t0 is not None else ("pawn", W, B, None)
    lw, rw = wins(pc0, tree, "W"), wins(pc0, tree, "B")
    return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lw, rw)]


# ---------------------------------------------------------------- driver
def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def parse(text):
    w, b = text.split("/")
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()))


def main():
    ROOT = "W: c1 c3 d3 / B: c2 d4 d5 d6"
    W, B = parse(ROOT)
    tiny1 = canon([ZERO], [canon([ZERO], [INT(-1)])])
    print("Position", ROOT)
    print("library sanity: tiny(1) =", show(tiny1), " >0:", le(ZERO, tiny1) and not le(tiny1, ZERO),
          " <up:", le(tiny1, canon([ZERO], [STAR])) and not le(canon([ZERO], [STAR]), tiny1))
    print()
    hdr = f"{'board':5s} {'ep':3s} {'race':8s} {'term':7s} {'BIG':>4s} | {'canonical value':22s} =tiny1 =1 | sum-search: G  G+miny1  G-1  G+*  G+down | 2step epcap races"
    print(hdr)
    print("-" * len(hdr))
    allok = True
    for wrap, ep_on, race, term, big in product((True, False), (True, False), ("count", "mover", "opponent"),
                                                ("passed", "promote"), (16, 256)):
        if term == "promote" and race != "count":
            continue  # race rule unused when play continues to promotion
        rules = Rules(wrap, ep_on, race, term, big)
        for k in STATS:
            STATS[k] = 0
        g = cgt_value(rules, W, B)
        is_t, is_1 = eq(g, tiny1), eq(g, INT(1))
        st = dict(STATS)
        oc = [sum_outcome(rules, W, B, t) for t in (T0, TMINY1, TINT(-1), TSTAR, TDOWN)]
        ok = is_t and not is_1 and oc == ["L", "P", "R", "N", "R"]
        allok &= ok
        print(f"{'cyl' if wrap else 'flat':5s} {'on' if ep_on else 'off':3s} {race:8s} {term:7s} {big:4d} | {show(g):22s} {str(is_t):6s} {str(is_1):5s}|"
              f"             {oc[0]}  {oc[1]:7s}  {oc[2]:3s}  {oc[3]:3s}  {oc[4]:6s} | {st['double_steps']:5d} {st['ep_captures']:5d} {st['races']:5d}  {'ok' if ok else 'MISMATCH'}")
    print()
    print("Expected if G = tiny(1): G alone L, G+miny(1) P, G-1 R, G+* N, G+down R.  If G = 1: G-1 would be P and G+* L.")
    print("ALL VARIANTS CONSISTENT WITH tiny(1):", allok)

    # literal options under the project convention
    rules = Rules(True, True, "count", "passed", 256)
    print("\nRoot options (cyl, ep on, count, passed, BIG=256), canonical values from engine (A):")
    for side in ("W", "B"):
        for (w, b, e) in gen(W, B, None, side, True, True):
            v = cgt_value(rules, w, b, e, side)
            mv = (sorted(FILES[f] + str(r) for f, r in (W - w)) + ["->"] + sorted(FILES[f] + str(r) for f, r in (w - W))) if side == "W" \
                else (sorted(FILES[f] + str(r) for f, r in (B - b)) + ["->"] + sorted(FILES[f] + str(r) for f, r in (b - B)))
            print(f"  {side}: {' '.join(mv):14s} value {show(v)}")
            for side2 in ("W", "B"):
                for (w2, b2, e2) in gen(w, b, None, side2, True, True):
                    v2 = cgt_value(rules, w2, b2, e2, side2)
                    print(f"       then {side2}: W {' '.join(sorted(FILES[f]+str(r) for f, r in w2))} / B {' '.join(sorted(FILES[f]+str(r) for f, r in b2))}  -> {show(v2)}")
    m257s = node([INT(-257)], [INT(-257)])
    after_c4 = cgt_value(rules, frozenset({sq('c1'), sq('c4'), sq('d3')}), B, None, "W")
    print("\n after c3-c4 equals {0 | -257*}:", eq(after_c4, canon([ZERO], [canon([INT(-257)], [INT(-257)])])),
          "  equals {0 | -256*}:", eq(after_c4, canon([ZERO], [canon([INT(-256)], [INT(-256)])])))
    print(" after d4xc3 equals {0|-1}:", eq(cgt_value(rules, frozenset({sq('c1'), sq('d3')}), frozenset({sq('c2'), sq('c3'), sq('d5'), sq('d6')}), None, "B"),
                                        canon([ZERO], [INT(-1)])))


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(1 << 29)
    t = threading.Thread(target=main)
    t.start()
    t.join()
