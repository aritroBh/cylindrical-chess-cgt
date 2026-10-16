"""Independent re-implementation (adversarial verifier, claim L4.2-critical-races).

Imports NOTHING from cylcgt/ or lemmas/. Stdlib only.

Contents
  * pawn move generator on an F x 8 flat board (double step, e.p., captures),
    written from the rules, not copied;
  * the whole-board convention game W (exactly-one-passer = +-BIG terminal,
    both-passers = race leaf scored by a verdict table);
  * an own canonical-form CGT engine (hash-consed, dominated + reversible
    simplification, integers built as real game trees);
  * a CGT-FREE check: G = V  iff  G + (-V) is a second-player win, decided by
    plain alternating minimax over (pawn node, small game) pairs.

Run from the project root:
  .venv/bin/python verify/lemmas/L4.2-critical-races-refute/indep.py [section ...]
"""
from __future__ import annotations

import random
import sys
from itertools import count

sys.setrecursionlimit(100000)

BIG = 256
NRANKS = 8

# ---------------------------------------------------------------------------
# pawn positions
#   pos = (white: frozenset of (file, rank), black: frozenset, ep)
#   ep  = None or (target_square, captured_square, side_allowed_to_capture)
# ---------------------------------------------------------------------------


class Cfg:
    def __init__(self, files=4, ep=True):
        self.files = files
        self.ep = ep


def parse(text):
    w, b = text.split("/")
    sq = lambda t: ("abcdefgh".index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()), None)


def pstr(p):
    n = lambda s: "abcdefgh"[s[0]] + str(s[1])
    s = "W: " + " ".join(sorted(map(n, p[0]))) + " / B: " + " ".join(sorted(map(n, p[1])))
    if p[2]:
        s += " (ep %s for %s)" % (n(p[2][0]), p[2][2])
    return s


def has_passer(cfg, p, side):
    mine, theirs = (p[0], p[1]) if side == "W" else (p[1], p[0])
    for f, r in mine:
        ok = True
        for g, s in theirs:
            if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
                ok = False
                break
        if ok:
            return True
    return False


def status(cfg, p):
    """None (no passer), +1 / -1 (only W / only B has a passer), 0 (both)."""
    w, b = has_passer(cfg, p, "W"), has_passer(cfg, p, "B")
    if w and b:
        return 0
    if w:
        return 1
    if b:
        return -1
    return None


def children(cfg, p, side):
    white, black, ep = p
    mine, theirs = (white, black) if side == "W" else (black, white)
    occ = white | black
    d = 1 if side == "W" else -1
    home = 2 if side == "W" else NRANKS - 1
    other = "B" if side == "W" else "W"
    out = []

    def put(m, t, e=None):
        q = (frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e)
        if q not in out:
            out.append(q)

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= NRANKS:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == home and (f, r2) not in occ:
                e = ((f, r1), (f, r2), other) if cfg.ep else None
                put(rest | {(f, r2)}, theirs, e)
        for g in (f - 1, f + 1):
            if not 0 <= g < cfg.files:
                continue
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[0] == t:
                put(rest | {t}, theirs - {ep[1]})
    return out


def dist(cfg, p, side):
    """Moves the side needs to promote its best passer (front pawn of its file)."""
    mine = p[0] if side == "W" else p[1]
    occ = p[0] | p[1]
    best = None
    for f, r in mine:
        single = (frozenset([(f, r)]), p[1], None) if side == "W" else (p[0], frozenset([(f, r)]), None)
        if not has_passer(cfg, single, side):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, NRANKS + 1)):
                continue
            dd = NRANKS - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == NRANKS - 1 else 0)
        best = dd if best is None else min(best, dd)
    return 10 ** 6 if best is None else best


def count_winner(cfg, p, mover):
    opp = "B" if mover == "W" else "W"
    return opp if dist(cfg, p, opp) <= dist(cfg, p, mover) else mover


def explore(cfg, root):
    """All nodes reachable by moves of either side (any order), not expanding
    terminal ones; and all race leaves keyed (child, mover)."""
    seen = {root}
    stack = [root]
    races = set()
    while stack:
        x = stack.pop()
        if status(cfg, x) is not None:
            continue
        for side in "WB":
            for c in children(cfg, x, side):
                if status(cfg, c) == 0:
                    races.add((c, side))
                if c not in seen:
                    seen.add(c)
                    stack.append(c)
    return seen, races


# ---------------------------------------------------------------------------
# own CGT engine
# ---------------------------------------------------------------------------

_ids = count()
_tab = {}
_le = {}


class G:
    __slots__ = ("L", "R", "id")

    def __init__(self, L, R):
        self.L, self.R, self.id = L, R, next(_ids)


def node(L, R):
    key = (tuple(sorted(g.id for g in L)), tuple(sorted(g.id for g in R)))
    g = _tab.get(key)
    if g is None:
        g = G(tuple(sorted(set(L), key=lambda x: x.id)), tuple(sorted(set(R), key=lambda x: x.id)))
        _tab[key] = g
    return g


def le(a, b):
    """a <= b  iff  no a^L >= b and no b^R <= a."""
    k = (a.id, b.id)
    v = _le.get(k)
    if v is None:
        v = not any(le(b, x) for x in a.L) and not any(le(x, a) for x in b.R)
        _le[k] = v
    return v


def eq(a, b):
    return le(a, b) and le(b, a)


def canon(L, R):
    """Canonical form of {L | R} with canonical options."""
    L, R = list(set(L)), list(set(R))
    while True:
        changed = False
        # dominated options
        L2 = [x for x in L if not any(y is not x and le(x, y) and not (le(y, x) and y.id > x.id) for y in L)]
        R2 = [x for x in R if not any(y is not x and le(y, x) and not (le(x, y) and y.id > x.id) for y in R)]
        if len(L2) != len(L) or len(R2) != len(R):
            changed = True
        L, R = L2, R2
        g = node(L, R)
        # reversible options
        newL = []
        for x in L:
            rev = next((xr for xr in x.R if le(xr, g)), None)
            if rev is None:
                newL.append(x)
            else:
                newL.extend(rev.L)
                changed = True
        newR = []
        for x in R:
            rev = next((xl for xl in x.L if le(g, xl)), None)
            if rev is None:
                newR.append(x)
            else:
                newR.extend(rev.R)
                changed = True
        L, R = list(set(newL)), list(set(newR))
        if not changed:
            return node(L, R)


ZERO = node([], [])
_ints = {0: ZERO}


def integer(n):
    if n not in _ints:
        _ints[n] = node([integer(n - 1)], []) if n > 0 else node([], [integer(n + 1)])
    return _ints[n]


STAR = canon([ZERO], [ZERO])
STAR2 = canon([ZERO, STAR], [ZERO, STAR])
UP = canon([ZERO], [STAR])
DOWN = canon([STAR], [ZERO])
UPSTAR = canon([ZERO, STAR], [ZERO])
DOWNSTAR = canon([ZERO], [ZERO, STAR])
STAR3 = canon([ZERO, STAR, STAR2], [ZERO, STAR, STAR2])
NAMED = [("0", ZERO), ("*", STAR), ("*2", STAR2), ("*3", STAR3), ("^", UP), ("v", DOWN),
         ("^*", UPSTAR), ("v*", DOWNSTAR)]


def show(g):
    for n, h in NAMED:
        if g is h:
            return n
    return "other(L=%d,R=%d)" % (len(g.L), len(g.R))


PB, NB = None, None


def init_big():
    global PB, NB
    PB, NB = integer(BIG), integer(-BIG)


# ---------------------------------------------------------------------------
# W with verdict table: verdict(child, mover) -> 'W' or 'B'
#   frozen=True adds the frozen-king options (Left -> -BIG, Right -> +BIG)
# ---------------------------------------------------------------------------

def Wvalue(cfg, root, verdict, frozen=False):
    memo = {}

    def leaf_or_rec(c, mover):
        s = status(cfg, c)
        if s == 0:
            return PB if verdict(c, mover) == "W" else NB
        return rec(c)

    def rec(p):
        g = memo.get(p)
        if g is not None:
            return g
        s = status(cfg, p)
        if s == 1:
            g = PB
        elif s == -1:
            g = NB
        else:
            L = [leaf_or_rec(c, "W") for c in children(cfg, p, "W")]
            R = [leaf_or_rec(c, "B") for c in children(cfg, p, "B")]
            if frozen:
                L.append(NB)
                R.append(PB)
            g = canon(L, R)
        memo[p] = g
        return g

    return rec(root)


# ---------------------------------------------------------------------------
# CGT-free check: is G_W(root) - V == 0 ?  (second player wins G + (-V))
# small games given as explicit trees: tuples (Lopts, Ropts)
# ---------------------------------------------------------------------------

SG0 = ((), ())
SGS = ((SG0,), (SG0,))
SGS2 = ((SG0, SGS), (SG0, SGS))
SGUP = ((SG0,), (SGS,))
SGDOWN = ((SGS,), (SG0,))
NEG = {"0": SG0, "*2": SGS2, "^": SGDOWN, "v": SGUP, "*": SGS}  # -V as tree


def minimax_equal(cfg, root, verdict, vname, frozen=False):
    X = NEG[vname]
    memo = {}

    def outcome_leaf(c, mover):
        """result of moving into pawn node c: +1 W wins, -1 B wins, None continue"""
        s = status(cfg, c)
        if s == 0:
            return 1 if verdict(c, mover) == "W" else -1
        if s in (1, -1):
            return s
        return None

    def wins(p, x, tomove):
        k = (p, x, tomove)
        v = memo.get(k)
        if v is not None:
            return v
        res = False
        # moves in the pawn component
        for c in children(cfg, p, tomove):
            o = outcome_leaf(c, tomove)
            if o is not None:
                if (o == 1) == (tomove == "W"):
                    res = True
                    break
                continue
            if not wins(c, x, "B" if tomove == "W" else "W"):
                res = True
                break
        # (frozen king move always loses at once for the mover: never a winning try)
        if not res:
            opts = x[0] if tomove == "W" else x[1]
            for y in opts:
                if not wins(p, y, "B" if tomove == "W" else "W"):
                    res = True
                    break
        memo[k] = res
        return res

    # root itself must be non-terminal
    assert status(cfg, root) is None
    return (not wins(root, X, "W")) and (not wins(root, X, "B"))


ROOT = "W: a2 c2 / B: b7 d7"
CRIT_TXT = [("W: a2 b5 / B: d7", "W", "v"), ("W: a2 / B: c4 d7", "B", "^"),
            ("W: a3 b5 / B: d6", "W", "v"), ("W: a3 / B: c4 d6", "B", "^")]


def main(sections):
    init_big()
    for epflag in (True, False):
        cfg = Cfg(4, epflag)
        root = parse(ROOT)
        nodes, races = explore(cfg, root)
        print("=== e.p. %s: %d reachable nodes, %d race keys (child incl. ep field, mover)" %
              ("on" if epflag else "off", len(nodes), len(races)))
        # races grouped ignoring the ep field
        grp = {}
        for c, m in races:
            grp.setdefault(((c[0], c[1]), m), []).append((c, m))
        print("    race keys ignoring the ep field: %d; keys with >1 ep variant: %d" %
              (len(grp), sum(1 for v in grp.values() if len(v) > 1)))
        nmover = sum(1 for c, m in races if count_winner(cfg, c, m) == m)
        print("    count verdict = mover on %d keys" % nmover)
        cnt = lambda c, m: count_winner(cfg, c, m)
        base = Wvalue(cfg, root, cnt)
        print("    base W(count) =", show(base), "| minimax check base == *2:",
              minimax_equal(cfg, root, cnt, "*2"))
        for rule in ("mover", "opponent"):
            v = (lambda c, m: m) if rule == "mover" else (lambda c, m: "B" if m == "W" else "W")
            print("    W(%s) = %s" % (rule, show(Wvalue(cfg, root, v))))
        # single flips
        flips = []
        order = sorted(races, key=lambda cm: (pstr(cm[0]), cm[1]))
        for key in order:
            w0 = cnt(*key)
            flipped = "B" if w0 == "W" else "W"
            vt = (lambda c, m, key=key, flipped=flipped: flipped if (c, m) == key else cnt(c, m))
            g = Wvalue(cfg, root, vt)
            if g is not base:
                flips.append((pstr(key[0]), key[1], w0, show(g)))
        print("    single flips that change W:", len(flips))
        for t in flips:
            print("       ", t)
        crit = set()
        for txt, m, _ in CRIT_TXT:
            crit.add((parse(txt), m))
        assert crit <= races, "claimed critical races not all race keys"
        # CGT-free confirmation of the 4 flips' values, and that all other flips keep *2
        if "minimax" in sections:
            bad = []
            for key in order:
                w0 = cnt(*key)
                flipped = "B" if w0 == "W" else "W"
                vt = (lambda c, m, key=key, flipped=flipped: flipped if (c, m) == key else cnt(c, m))
                exp = {k: v for k, v in [((parse(t), m), vn) for t, m, vn in CRIT_TXT]}.get(key, "*2")
                if not minimax_equal(cfg, root, vt, exp):
                    bad.append((pstr(key[0]), key[1], exp))
            print("    minimax: single flips whose value is NOT the expected (*2, or ^/v for the 4):", bad)
        # group flips (all ep variants of one pawn configuration together)
        gflips = []
        for (wb, m), keys in sorted(grp.items(), key=lambda kv: (pstr(kv[0][0] + (None,)), kv[0][1])):
            if len(keys) < 2:
                continue
            ks = set(keys)
            vt = (lambda c, mm, ks=ks: ("B" if cnt(c, mm) == "W" else "W") if (c, mm) in ks else cnt(c, mm))
            g = Wvalue(cfg, root, vt)
            if g is not base:
                gflips.append((pstr(wb + (None,)), m, len(keys), show(g)))
        print("    group flips (all ep variants of one configuration, %d groups with >1 variant) that change W: %s"
              % (sum(1 for v in grp.values() if len(v) > 1), gflips))
        # the 4 won by mover, all others lost by mover
        other = lambda m: "B" if m == "W" else "W"
        v_mixed = lambda c, m: m if (c, m) in crit else other(m)
        g = Wvalue(cfg, root, v_mixed)
        print("    crit won by mover, others lost by mover:", show(g),
              "| minimax ==*2:", minimax_equal(cfg, root, v_mixed, "*2"))
        # the 4 lost by mover, rest count
        v_lost = lambda c, m: other(m) if (c, m) in crit else cnt(c, m)
        g = Wvalue(cfg, root, v_lost)
        print("    crit lost by mover, others count:", show(g),
              "| minimax ==0:", minimax_equal(cfg, root, v_lost, "0"))
        # frozen-king model WF: same sensitivity?
        if "frozen" in sections:
            bF = Wvalue(cfg, root, cnt, frozen=True)
            ff = []
            for key in order:
                w0 = cnt(*key)
                flipped = "B" if w0 == "W" else "W"
                vt = (lambda c, m, key=key, flipped=flipped: flipped if (c, m) == key else cnt(c, m))
                g = Wvalue(cfg, root, vt, frozen=True)
                if g is not bF:
                    ff.append((pstr(key[0]), key[1], w0, show(g)))
            print("    WF(count) =", show(bF), "; single flips that change WF:", ff)
            g = Wvalue(cfg, root, v_mixed, frozen=True)
            print("    WF crit won by mover, others lost by mover:", show(g))
        # random trials, deterministic order (sorted by string)
        if "random" in sections:
            for seed, trials in ((1, 200), (2, 200), (3, 200), (12345, 1000)):
                rng = random.Random(seed)
                hist = {}
                for _ in range(trials):
                    ov = {key: (key[1] if key in crit else rng.choice("WB")) for key in order}
                    g = Wvalue(cfg, root, lambda c, m, ov=ov: ov[(c, m)])
                    hist[show(g)] = hist.get(show(g), 0) + 1
                print("    random others (seed %d, %d trials, sorted order): %s" % (seed, trials, hist))
        sys.stdout.flush()


if __name__ == "__main__":
    main(set(sys.argv[1:]))
