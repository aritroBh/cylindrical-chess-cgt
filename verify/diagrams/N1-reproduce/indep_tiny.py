"""Independent re-derivation of claim N1 (7.3 {c,d} sub-game = tiny(1)).

Written from scratch for the N1 verification; imports nothing from cylcgt/ or crosscheck/.
  * own pawn move generator (flat or cylinder, e.p. on/off, double step from own 2nd rank)
  * passed pawn (no enemy pawn strictly ahead on own/adjacent file) => +-BIG, BIG = 256
  * both sides passed after a move => race, resolved by RACE in {"count","mover","opponent"}
  * own explicit-tree CGT comparison (Conway's recursive <=), no canonical forms, no sums library.
G = tiny(1) is tested as (G <= T) and (T <= G) with T = {0 | {0 | -1}} built by hand.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/N1-reproduce/indep_tiny.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
BIG = 256
FILES = "abcdefgh"

# ---------------------------------------------------------------- pawn rules
CFG = {"wrap": False, "ep": True, "race": "count", "files": 8, "ranks": 8}
STATS = {"races": set(), "doubles": set(), "ep_caps": set()}


def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def nm(s):
    return f"{FILES[s[0]]}{s[1]}"


def parse(t):
    w, b = t.split("/")
    return (frozenset(sq(x) for x in w.split(":")[1].split()),
            frozenset(sq(x) for x in b.split(":")[1].split()), None)


def fmt(p):
    w, b, ep = p
    s = "W: " + " ".join(sorted(map(nm, w))) + " / B: " + " ".join(sorted(map(nm, b)))
    return s + (f" [ep {nm(ep[0])} for {ep[2]}]" if ep else "")


def adj(f):
    out = {f}
    for d in (-1, 1):
        g = f + d
        if CFG["wrap"]:
            out.add(g % CFG["files"])
        elif 0 <= g < CFG["files"]:
            out.add(g)
    return out


def has_passer(p, side):
    w, b, _ = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    for f, r in mine:
        fs = adj(f)
        if side == "W" and not any(g in fs and s > r for g, s in theirs):
            return True
        if side == "B" and not any(g in fs and s < r for g, s in theirs):
            return True
    return False


def gen(p, side):
    """All positions after one move by `side`. An e.p. right in p is used only if it is `side`'s."""
    w, b, ep = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    occ = w | b
    d = 1 if side == "W" else -1
    home = 2 if side == "W" else CFG["ranks"] - 1
    out = []

    def put(nm_, nt_, e=None):
        out.append((frozenset(nm_), frozenset(nt_), e) if side == "W" else (frozenset(nt_), frozenset(nm_), e))

    for (f, r) in sorted(mine):
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= CFG["ranks"]:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == home and 1 <= r2 <= CFG["ranks"] and (f, r2) not in occ:
                STATS["doubles"].add(fmt(p))
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if CFG["ep"] else None
                put(rest | {(f, r2)}, theirs, e)
        for g in adj(f) - {f}:
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep and ep[2] == side and ep[0] == t and t not in occ:
                STATS["ep_caps"].add(fmt(p))
                put(rest | {t}, theirs - {ep[1]})
    return list(dict.fromkeys(out))


def dist(p, side):
    w, b, _ = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    best = 10 ** 6
    for f, r in mine:
        fs = adj(f)
        if side == "W":
            if any(g in fs and s > r for g, s in theirs) or any(g == f and s > r for g, s in mine):
                continue
            best = min(best, CFG["ranks"] - r - (r == 2))
        else:
            if any(g in fs and s < r for g, s in theirs) or any(g == f and s < r for g, s in mine):
                continue
            best = min(best, r - 1 - (r == CFG["ranks"] - 1))
    return best


# ------------------------------------------------- explicit game objects
# ("n", k) integer k ; ("g", L, R) explicit ; ("p", pos) pawn position (options lazily generated)
def N(k):
    return ("n", k)


def G(L, R):
    return ("g", tuple(L), tuple(R))


def after_move(q, mover):
    wp, bp = has_passer(q, "W"), has_passer(q, "B")
    if wp and bp:
        STATS["races"].add(fmt(q) + " after " + mover)
        rule = CFG["race"]
        other = "B" if mover == "W" else "W"
        if rule == "mover":
            win = mover
        elif rule == "opponent":
            win = other
        else:
            win = other if dist(q, other) <= dist(q, mover) else mover
        return N(BIG if win == "W" else -BIG)
    return pawnnode(q)


def pawnnode(p):
    wp, bp = has_passer(p, "W"), has_passer(p, "B")
    if wp and bp:
        raise RuntimeError("race at a node " + fmt(p))
    if wp:
        return N(BIG)
    if bp:
        return N(-BIG)
    return ("p", p)


@lru_cache(maxsize=None)
def opts(x):
    if x[0] == "n":
        k = x[1]
        return ((N(k - 1),), ()) if k > 0 else (((), (N(k + 1),)) if k < 0 else ((), ()))
    if x[0] == "g":
        return x[1], x[2]
    p = x[1]
    w, b, ep = p
    lp = p if (ep and ep[2] == "W") else (w, b, None)   # e.p. right only for the side entitled
    rp = p if (ep and ep[2] == "B") else (w, b, None)
    L = tuple(after_move(q, "W") for q in gen(lp, "W"))
    R = tuple(after_move(q, "B") for q in gen(rp, "B"))
    return L, R


@lru_cache(maxsize=None)
def le(a, b):
    if a[0] == "n" and b[0] == "n":
        return a[1] <= b[1]
    aL, _ = opts(a)
    _, bR = opts(b)
    return not any(le(b, al) for al in aL) and not any(le(br, a) for br in bR)


def eq(a, b):
    return le(a, b) and le(b, a)


def winner_first(x, side):
    """Who wins x alone when `side` moves first (normal play)."""
    L, R = opts(x)
    if side == "W":
        return "W" if any(winner_first(c, "B") == "W" for c in L) else "B"
    return "B" if any(winner_first(c, "W") == "B" for c in R) else "W"


def outcome(x):
    a, b = winner_first(x, "W"), winner_first(x, "B")
    return {("W", "W"): "L", ("B", "B"): "R", ("W", "B"): "N", ("B", "W"): "P"}[(a, b)]


def reset():
    opts.cache_clear(); le.cache_clear()
    for v in STATS.values():
        v.clear()


ZERO, ONE, MONE = N(0), N(1), N(-1)
STAR = G([ZERO], [ZERO])
H01 = G([ZERO], [MONE])                     # {0|-1}
TINY1 = G([ZERO], [H01])                    # {0 || 0|-1}
BIGSTAR_NEG = G([N(-BIG)], [N(-BIG)])       # -W* = {-BIG | -BIG}
OPT_C4 = G([ZERO], [BIGSTAR_NEG])           # {0 | -W*}
UP = G([ZERO], [STAR])
CANDIDATES = {"0": ZERO, "1": ONE, "*": STAR, "up": UP, "tiny(1)": TINY1, "{0|-1}": H01}

if __name__ == "__main__":
    root = "W: c1 c3 d3 / B: c2 d4 d5 d6"
    for wrap in (False, True):
        for ep in (True, False):
            for race in ("count", "mover", "opponent"):
                CFG.update(wrap=wrap, ep=ep, race=race)
                reset()
                g = pawnnode(parse(root))
                L, R = opts(g)
                Lp = gen((parse(root)[0], parse(root)[1], None), "W")
                Rp = gen((parse(root)[0], parse(root)[1], None), "B")
                matches = [k for k, v in CANDIDATES.items() if eq(g, v)]
                print(f"wrap={wrap!s:5} ep={ep!s:5} race={race:8} outcome {outcome(g)}  equals {matches}  "
                      f"G==tiny(1): {eq(g, TINY1)}  G==1: {eq(g, ONE)}  G>0: {le(ZERO, g) and not le(g, ZERO)}")
                for q, c in zip(Lp, L):
                    tag = [k for k, v in {"0": ZERO, "{0|-W*}": OPT_C4}.items() if eq(c, v)]
                    print(f"     W -> {fmt(q):34s} equals {tag}")
                for q, c in zip(Rp, R):
                    tag = [k for k, v in {"{0|-1}": H01, "-1/2+-1/2 check: {0|-1}": H01}.items() if eq(c, v)][:1]
                    print(f"     B -> {fmt(q):34s} equals {tag}")
                print(f"     race nodes reached: {len(STATS['races'])}; positions with a double step available: "
                      f"{len(STATS['doubles'])}; e.p. captures generated: {len(STATS['ep_caps'])}")
    # sum tests mirrored from the worker, but with abstract components (not pawns): G + (-1), G + *, G - tiny(1)
    CFG.update(wrap=False, ep=True, race="count"); reset()
    g = pawnnode(parse(root))
    MINY1 = G([G([ONE], [ZERO])], [ZERO])   # -tiny(1) = {{1|0} | 0}
    for lab, h in (("G + (-1)", MONE), ("G + *", STAR), ("G + miny(1)", MINY1), ("G + (-up)", G([STAR], [ZERO]))):
        # sum outcome via le: G+H >= 0 iff -H <= G ; G+H <= 0 iff G <= -H
        negh = {"G + (-1)": ONE, "G + *": STAR, "G + miny(1)": TINY1, "G + (-up)": UP}[lab]
        ge0, le0 = le(negh, g), le(g, negh)
        oc = "P" if (ge0 and le0) else "L" if ge0 else "R" if le0 else "N"
        print(f"{lab:12s} outcome {oc}")
    # what the -W* option actually is
    q = parse("W: c1 c4 d3 / B: c2 d4 d5 d6")
    for side in ("W", "B"):
        for r in gen(q, side):
            print(f"   after c3-c4, {side} -> {fmt(r):34s} node {after_move(r, side)[0]}  passers W={has_passer(r,'W')} B={has_passer(r,'B')}")
