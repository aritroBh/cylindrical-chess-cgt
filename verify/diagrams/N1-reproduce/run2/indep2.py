"""Second, from-scratch check of claim N1 (paper 7.3 {c,d} sub-game).

Imports nothing from cylcgt/ or crosscheck/ (or the earlier N1-reproduce scripts).
  * own pawn move generator (flat/cylinder, e.p. on/off; double step from own 2nd rank)
  * passed pawn = no enemy pawn strictly ahead on own or adjacent file  ->  +-BIG (BIG = 256)
  * both sides passed after a move -> race, resolved by RACE in {"count","mover","opponent"}
  * games are explicit (L-set, R-set) trees, interned by id but NEVER simplified;
    comparison by Conway's recursive definition only.
  * own whole-board minimax ("first passer ends the game") for sum tests on real combined positions.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/N1-reproduce/run2/indep2.py
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(200000)
BIG = 256
FL = "abcdefgh"
CFG = dict(wrap=False, ep=True, race="count", F=8, R=8)
STAT = dict(nodes=set(), race=0, double=0, epcap=0, term_w=0, term_b=0)

# ---------------------------------------------------------------- explicit games
_ids = {}
_games = []


def G(L, R):
    key = (tuple(sorted(set(L))), tuple(sorted(set(R))))
    if key not in _ids:
        _ids[key] = len(_games)
        _games.append(key)
    return _ids[key]


ZERO = G([], [])
_int = {0: ZERO}


def integer(n):
    if n not in _int:
        _int[n] = G([integer(n - 1)], []) if n > 0 else G([], [integer(n + 1)])
    return _int[n]


@lru_cache(maxsize=None)
def le(a, b):
    """a <= b iff no a^L >= b and no b^R <= a"""
    aL, _ = _games[a]
    _, bR = _games[b]
    return not any(le(b, x) for x in aL) and not any(le(y, a) for y in bR)


def eq(a, b):
    return le(a, b) and le(b, a)


def neg(a):
    L, R = _games[a]
    return G([neg(y) for y in R], [neg(x) for x in L])


@lru_cache(maxsize=None)
def add(a, b):
    aL, aR = _games[a]
    bL, bR = _games[b]
    return G([add(x, b) for x in aL] + [add(a, y) for y in bL],
             [add(x, b) for x in aR] + [add(a, y) for y in bR])


def outcome(a):
    lf = not le(a, ZERO)       # Left wins moving first iff not a <= 0
    rf = not le(ZERO, a)       # Right wins moving first iff not a >= 0
    return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lf, rf)]


STAR = G([ZERO], [ZERO])
ONE = integer(1)
MONE = integer(-1)
SW01 = G([ZERO], [MONE])                 # {0 | -1}
TINY1 = G([ZERO], [SW01])                # {0 || 0 | -1}
MINY1 = neg(TINY1)

# ---------------------------------------------------------------- pawn rules


def sq(s):
    return (FL.index(s[0]), int(s[1:]))


def nm(s):
    return f"{FL[s[0]]}{s[1]}"


def parse(t):
    w, b = t.split("/")
    return (frozenset(sq(x) for x in w.split(":")[1].split()),
            frozenset(sq(x) for x in b.split(":")[1].split()), None)


def show(p):
    w, b, ep = p
    return ("W: " + " ".join(nm(s) for s in sorted(w)) + " / B: " + " ".join(nm(s) for s in sorted(b))
            + (f" [ep {nm(ep[0])} for {ep[2]}]" if ep else ""))


def side_files(f):
    out = [f]
    for d in (-1, 1):
        g = f + d
        if CFG["wrap"]:
            out.append(g % CFG["F"])
        elif 0 <= g < CFG["F"]:
            out.append(g)
    return out


def has_passer(p, side):
    w, b, _ = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    for (f, r) in mine:
        fs = side_files(f)
        if side == "W":
            stop = any(g in fs and s > r for (g, s) in theirs)
        else:
            stop = any(g in fs and s < r for (g, s) in theirs)
        if not stop:
            return True
    return False


def gen(p, side):
    w, b, ep = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    occ = w | b
    dr = 1 if side == "W" else -1
    home = 2 if side == "W" else CFG["R"] - 1
    other = "B" if side == "W" else "W"
    res = []

    def put(m, t, e=None):
        res.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))

    for (f, r) in sorted(mine):
        rest = mine - {(f, r)}
        n1 = r + dr
        if not (1 <= n1 <= CFG["R"]):
            continue
        if (f, n1) not in occ:
            put(rest | {(f, n1)}, theirs)
            n2 = r + 2 * dr
            if r == home and 1 <= n2 <= CFG["R"] and (f, n2) not in occ:
                STAT["double"] += 1
                put(rest | {(f, n2)}, theirs, ((f, n1), (f, n2), other) if CFG["ep"] else None)
        for g in side_files(f)[1:]:
            t = (g, n1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif ep and ep[2] == side and ep[0] == t and ep[1] in theirs:
                STAT["epcap"] += 1
                put(rest | {t}, theirs - {ep[1]})
    return list(dict.fromkeys(res))


def promo_dist(p, side):
    w, b, _ = p
    mine, theirs = (w, b) if side == "W" else (b, w)
    best = 10 ** 6
    for (f, r) in mine:
        fs = side_files(f)
        if side == "W":
            if any(g in fs and s > r for (g, s) in theirs) or any(g == f and s > r for (g, s) in mine):
                continue
            d = CFG["R"] - r - (1 if r == 2 else 0)
        else:
            if any(g in fs and s < r for (g, s) in theirs) or any(g == f and s < r for (g, s) in mine):
                continue
            d = r - 1 - (1 if r == CFG["R"] - 1 else 0)
        best = min(best, d)
    return best


def after_move(p, mover):
    """Game value of position p just after `mover` moved (opponent's e.p. right kept)."""
    wp, bp = has_passer(p, "W"), has_passer(p, "B")
    if wp and bp:
        STAT["race"] += 1
        opp = "B" if mover == "W" else "W"
        rule = CFG["race"]
        if rule == "mover":
            win = mover
        elif rule == "opponent":
            win = opp
        else:
            win = opp if promo_dist(p, opp) <= promo_dist(p, mover) else mover
        return integer(BIG if win == "W" else -BIG)
    return val(p)


@lru_cache(maxsize=None)
def val_cached(p, cfgkey):
    STAT["nodes"].add((p, cfgkey))
    wp, bp = has_passer(p, "W"), has_passer(p, "B")
    assert not (wp and bp)
    if wp:
        STAT["term_w"] += 1
        return integer(BIG)
    if bp:
        STAT["term_b"] += 1
        return integer(-BIG)
    w, b, ep = p
    plain = (w, b, None)
    pl = p if (ep and ep[2] == "W") else plain     # a stale right for the other side is dropped
    pr = p if (ep and ep[2] == "B") else plain
    L = [after_move(q, "W") for q in gen(pl, "W")]
    R = [after_move(q, "B") for q in gen(pr, "B")]
    return G(L, R)


def val(p):
    return val_cached(p, (CFG["wrap"], CFG["ep"], CFG["race"]))


# ---------------------------------------------------------------- whole-board minimax


@lru_cache(maxsize=None)
def wins_to_move(p, side, cfgkey):
    """True iff `side` to move wins (passer anywhere ends the game; no move = loss)."""
    opp = "B" if side == "W" else "W"
    for q in gen(p, side):
        wp, bp = has_passer(q, "W"), has_passer(q, "B")
        if wp and bp:
            rule = CFG["race"]
            if rule == "mover":
                win = side
            elif rule == "opponent":
                win = opp
            else:
                win = opp if promo_dist(q, opp) <= promo_dist(q, side) else side
            if win == side:
                return True
            continue
        if wp or bp:
            if (wp and side == "W") or (bp and side == "B"):
                return True
            continue
        if not wins_to_move(q, opp, cfgkey):
            return True
    return False


def board_outcome(text):
    p = parse(text)
    k = (CFG["wrap"], CFG["ep"], CFG["race"])
    lf = wins_to_move(p, "W", k)
    rf = wins_to_move(p, "B", k)
    return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lf, rf)]


# ---------------------------------------------------------------- the checks
CD = "W: c1 c3 d3 / B: c2 d4 d5 d6"
OPTS = [("W c3xd4", "W", "W: c1 d3 d4 / B: c2 d5 d6"),
        ("W c3-c4", "W", "W: c1 c4 d3 / B: c2 d4 d5 d6"),
        ("B d4xc3", "B", "W: c1 d3 / B: c2 c3 d5 d6")]


def name_of(g):
    cands = {"0": ZERO, "1": ONE, "-1": MONE, "*": STAR, "{0|-1}": SW01, "tiny(1)": TINY1, "miny(1)": MINY1}
    for k in (BIG - 1, BIG, BIG + 1, BIG + 2):
        cands[f"-{k}"] = integer(-k)
        cands[f"-{k}*"] = add(integer(-k), STAR)
        cands[f"{{0|-{k}*}}"] = G([ZERO], [add(integer(-k), STAR)])
        cands[f"{{0|-{k}}}"] = G([ZERO], [integer(-k)])
    return [k for k, v in cands.items() if eq(g, v)]


if __name__ == "__main__":
    # negative/positive controls of the machinery
    CFG.update(wrap=False, ep=True, race="count")
    for t, want in [("W: e4 / B: e5", "0"), ("W: e4 / B: e6", "*"), ("W: f4 / B: f5 f7", "-1"),
                    ("W: f2 f4 / B: f5", "1"), ("W: f4 / B: f6", "*")]:
        print(f"control {t:22s} expect {want:3s} got {name_of(val(parse(t)))}")
    print()
    for wrap in (False, True):
        for ep in (True, False):
            for race in ("count", "mover", "opponent"):
                CFG.update(wrap=wrap, ep=ep, race=race)
                for k in ("race", "double", "epcap", "term_w", "term_b"):
                    STAT[k] = 0
                STAT["nodes"] = set()
                val_cached.cache_clear()
                g = val(parse(CD))
                nn = len(STAT["nodes"])
                st = dict(STAT)
                print(f"wrap={wrap!s:5} ep={ep!s:5} race={race:8s} {CD}: value-matches {name_of(g)}; "
                      f"==tiny(1) {eq(g, TINY1)}; ==1 {eq(g, ONE)}; outcome {outcome(g)}")
                print(f"    nodes {nn}, race nodes {st['race']}, double-steps generated {st['double']}, "
                      f"e.p. captures {st['epcap']}, terminal +BIG {st['term_w']}, -BIG {st['term_b']}")
                # literal options, and that there are exactly 3 legal moves
                p = parse(CD)
                lm = [show(q) for q in gen(p, "W")]
                rm = [show(q) for q in gen(p, "B")]
                print(f"    legal W moves {len(lm)}, legal B moves {len(rm)}")
                for lab, s, t in OPTS:
                    assert show(parse(t)) in (lm if s == "W" else rm), lab
                    print(f"    {lab}: {t:32s} -> {name_of(after_move(parse(t), s))}")
                # sum tests on real combined boards via whole-board minimax (no CGT addition)
                for lab, t, pred in [("{c,d}+(-1)", "W: c1 c3 d3 f4 / B: c2 d4 d5 d6 f5 f7", "tiny:R  1:P"),
                                     ("{c,d}+*", "W: c1 c3 d3 f4 / B: c2 d4 d5 d6 f6", "tiny:N  1:L"),
                                     ("{c,d}+miny(1)[h-mirror f..h? see M]", None, "")]:
                    if t is None:
                        continue
                    wins_to_move.cache_clear()
                    oc = board_outcome(t)
                    gs = add(g, val(parse(t.replace("c1 c3 d3 ", "").replace("c2 d4 d5 d6 ", ""))))
                    print(f"    board minimax {lab:12s} {oc}   explicit-sum {outcome(gs)}   ({pred})")
                # exact pin: G + M with M a DIFFERENT position (not a mirror of G, which would be vacuous):
                # colour-swapped, rank-mirrored copy of the paper's 4.3 a/h "tiny" position; needs wrap=True.
                if wrap:
                    M = "W: a2 a3 a4 h6 / B: a5 h5 h7"
                    gm = val(parse(M))
                    wins_to_move.cache_clear()
                    comb = "W: a2 a3 a4 c1 c3 d3 h6 / B: a5 c2 d4 d5 d6 h5 h7"
                    print(f"    M={M}: value-matches {name_of(gm)}; board minimax of G+M {board_outcome(comb)} "
                          f"(P and M=miny(1) => G=tiny(1)); explicit-sum outcome {outcome(add(g, gm))}")
