"""Fresh, standalone re-check of claim V1 (written 2026-10-16 by the V1-refute verifier).

Imports nothing from cylcgt/, crosscheck/, verify/diagrams/*.py, or the earlier indep.py in this
directory.  Same stated conventions (Elkies 1996 as used in notes/audit.md):
  * White = Left, Black = Right, normal play; BIG = 256.
  * pawn moves: single step, double step from rank 2 (W) / rank 7 (B) only, diagonal captures;
    on the cylinder files a and h are adjacent (captures and e.p. wrap).
  * textbook passed test: no enemy pawn strictly ahead on the same or an adjacent file.
  * a child with exactly one side passed is the number +-BIG; both sides passed = race, scored by RULE:
      count    : opponent of the mover moves first; fewer moves to promote wins; ties to the opponent
      mover    : mover wins        opponent : mover loses
      white    : White always wins (upper bracket)     black : Black always wins (lower bracket)
    Since replacing a leaf by a larger game never lowers a game, ANY race resolution with values in
    [-BIG, +BIG] gives a value between G[black] and G[white].  So:
      "Left wins moving first" under black  => under every resolution;
      "Right wins moving first" under white => under every resolution.
  * e.p.: after a double step the opponent may capture e.p. as the next move IN THIS COMPONENT;
    any move in the component cancels the right (the solver's short-game approximation).
  * after each move the child splits into components at empty files (with wrap-around).
Equality test: G = X  iff  G + (-X) is a second-player win (P), by memoised minimax.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python -I verify/diagrams/V1-refute/fresh.py
"""
import sys
import threading
import time

NF = NR = 8
BIG = 256
LET = "abcdefgh"
OPT = {"wrap": True, "ep": True, "rule": "count", "epaware": False}
MEMO = {}
RACES = [0]


def S(name):
    return (LET.index(name[0]), int(name[1]))


def parse(t):
    w, b = t.split("/")
    return (frozenset(S(x) for x in w.split(":")[1].split()),
            frozenset(S(x) for x in b.split(":")[1].split()))


def nbrs(f):
    if OPT["wrap"]:
        return {(f + 1) % NF, (f - 1) % NF}
    return {g for g in (f - 1, f + 1) if 0 <= g < NF}


def has_passer(mine, theirs, white, exempt=None):
    for (f, r) in mine:
        if (f, r) == exempt:
            continue
        cols = nbrs(f) | {f}
        if white:
            if not any(g in cols and s > r for (g, s) in theirs):
                return True
        else:
            if not any(g in cols and s < r for (g, s) in theirs):
                return True
    return False


def steps_to_queen(W, B, white, exempt=None):
    occ = W | B
    mine, theirs = (W, B) if white else (B, W)
    best = 99
    for (f, r) in mine:
        if (f, r) == exempt:
            continue
        if not has_passer({(f, r)}, theirs, white):
            continue
        if white:
            if any((f, s) in occ for s in range(r + 1, NR + 1)):
                continue
            n = (NR - r) - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            n = (r - 1) - (1 if r == NR - 1 else 0)
        best = min(best, n)
    return best


def gen(W, B, ep, white):
    """children (W', B', ep') of one pawn move; ep is the right usable by the mover (or None)."""
    occ = W | B
    out = set()
    mine = W if white else B
    dr = 1 if white else -1
    home = 2 if white else NR - 1
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + dr
        if not 1 <= r1 <= NR:
            continue
        kids = []
        if (f, r1) not in occ:
            kids.append((rest | {(f, r1)}, None, None))
            r2 = r + 2 * dr
            if r == home and (f, r2) not in occ:
                right = ((f, r1), (f, r2), not white) if OPT["ep"] else None
                kids.append((rest | {(f, r2)}, None, right))
        for g in nbrs(f):
            if (g, r1) in (B if white else W):
                kids.append((rest | {(g, r1)}, (g, r1), None))
            elif ep is not None and ep[0] == (g, r1):
                kids.append((rest | {(g, r1)}, ep[1], None))
        for nm, victim, right in kids:
            if white:
                out.add((frozenset(nm), frozenset(B - {victim} if victim else B), right))
            else:
                out.add((frozenset(W - {victim} if victim else W), frozenset(nm), right))
    return out


def components(W, B, ep):
    files = sorted({f for f, _ in W | B})
    runs = []
    for f in files:
        if runs and runs[-1][-1] == f - 1:
            runs[-1].append(f)
        else:
            runs.append([f])
    if OPT["wrap"] and len(runs) > 1 and runs[0][0] == 0 and runs[-1][-1] == NF - 1:
        runs[0] = runs.pop() + runs[0]
    res = []
    for run in runs:
        fs = set(run)
        e = ep if (ep is not None and ep[0][0] in fs) else None
        res.append(("P", tuple(sorted(p for p in W if p[0] in fs)),
                    tuple(sorted(p for p in B if p[0] in fs)), e))
    return res


def score_child(W, B, ep, white_moved):
    """-> (integer, [components])"""
    ex = None
    if OPT["epaware"] and ep is not None:
        # e.p.-aware passed test: the pawn that just double-stepped is not passed while an enemy
        # pawn beside it can still take it en passant
        (cf, cr) = ep[1]
        capturers = W if ep[2] else B
        if any((g, cr) in capturers for g in nbrs(cf)):
            ex = (cf, cr)
    wp, bp = has_passer(W, B, True, ex), has_passer(B, W, False, ex)
    if wp and bp:
        RACES[0] += 1
        rule = OPT["rule"]
        if rule == "white":
            wwin = True
        elif rule == "black":
            wwin = False
        elif rule == "mover":
            wwin = white_moved
        elif rule == "opponent":
            wwin = not white_moved
        else:  # count: opponent of the mover moves first, ties to the opponent
            opp_white = not white_moved
            d_opp = steps_to_queen(W, B, opp_white, ex)
            d_mov = steps_to_queen(W, B, white_moved, ex)
            wwin = opp_white if d_opp <= d_mov else white_moved
        return (BIG if wwin else -BIG), []
    if wp:
        return BIG, []
    if bp:
        return -BIG, []
    return 0, components(W, B, ep)


# explicit games: ("G", (left options), (right options)); options are ints or games
def G(L, R):
    return ("G", tuple(L), tuple(R))


def neg(x):
    if isinstance(x, int):
        return -x
    return ("G", tuple(neg(o) for o in x[2]), tuple(neg(o) for o in x[1]))


def moves(state, left):
    comps, n = state
    res = []
    if left and n > 0:
        res.append((comps, n - 1))
    if not left and n < 0:
        res.append((comps, n + 1))
    for i, c in enumerate(comps):
        rest = comps[:i] + comps[i + 1:]
        if c[0] == "P":
            W, B, ep = frozenset(c[1]), frozenset(c[2]), c[3]
            usable = ep if (ep is not None and ep[2] == left) else None
            for (W2, B2, e2) in gen(W, B, usable, left):
                k, new = score_child(W2, B2, e2, left)
                res.append((tuple(sorted(rest + tuple(new), key=repr)), n + k))
        else:
            for o in (c[1] if left else c[2]):
                if isinstance(o, int):
                    res.append((rest, n + o))
                else:
                    res.append((tuple(sorted(rest + (o,), key=repr)), n))
    return res


def first_player_wins(state, left):
    key = (state, left)
    v = MEMO.get(key)
    if v is None:
        v = any(not first_player_wins(s, not left) for s in moves(state, left))
        MEMO[key] = v
    return v


def start(text, *extra):
    W, B = parse(text)
    wp, bp = has_passer(W, B, True), has_passer(B, W, False)
    assert not (wp and bp)
    n, comps = 0, []
    if wp or bp:
        n = BIG if wp else -BIG
    else:
        comps = components(W, B, None)
    for x in extra:
        if isinstance(x, int):
            n += x
        else:
            comps.append(x)
    return (tuple(sorted(comps, key=repr)), n)


def outcome(state):
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[
        (first_player_wins(state, True), first_player_wins(state, False))]


def equal(text, X):
    return outcome(start(text, neg(X))) == "P"


STAR = G([0], [0])
UP = G([0], [STAR])
TINY1 = G([0], [G([0], [-1])])
PM1 = G([1], [-1])
F71 = G([G([2], [1])], [0])

POS = {
    "2.1": "W: e4 / B: e5", "2.2": "W: a2 h1 / B: a3 h4", "3.1": "W: a3 h1 / B: a4 h5",
    "3.2": "W: a4 h1 / B: a5 h6", "4.1": "W: e4 / B: e6", "4.2": "W: e3 / B: e6",
    "4.3": "W: a4 h2 h4 / B: a5 a6 a7 h3", "7.1c": "W: c2 c3 / B: c5 c6", "7.1f": "W: f3 f4 / B: f7",
    "7.1ah": "W: a4 a5 h2 h3 / B: a7 h6", "7.2abh": "W: a2 b2 h3 / B: a6 b7 h7",
    "7.3": "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4",
    "7.3cd": "W: c1 c3 d3 / B: c2 d4 d5 d6",
}


def claimed(label, ep):
    return {"2.1": [("0", 0)], "2.2": [("0", 0)], "3.1": [("1", 1)] if ep else [("2", 2)],
            "3.2": [("2", 2)], "4.1": [("*", STAR)], "4.2": [("0", 0)], "4.3": [("tiny(1)", TINY1)],
            "7.1c": [("+-1", PM1)], "7.1f": [("{{2|1}|0}", F71)],
            "7.1ah": [("{%d|*}" % k, G([k], [STAR])) for k in range(250, 262)],
            "7.3": [("BIG", BIG)], "7.3cd": [("tiny(1)", TINY1)]}.get(label)


def rivals(label):
    return {"2.1": [1, STAR], "2.2": [1, STAR, UP], "3.1": [STAR, G([0], [1])], "3.2": [1, 3],
            "4.1": [0, UP], "4.2": [UP, STAR], "4.3": [1, 0, UP], "7.1c": [0, STAR, 1],
            "7.1f": [G([2], [0]), 1, G([3, 2], [0])], "7.1ah": [1, G([BIG], [0]), BIG],
            "7.3": [BIG - 1, BIG + 1, 2], "7.3cd": [1, UP]}.get(label, [])


def main():
    t0 = time.time()
    for epaware, ep in ((False, True), (False, False), (True, True)):
        OPT["epaware"] = epaware
        for rule in ("count", "mover", "opponent", "white", "black"):
            OPT.update(ep=ep, rule=rule)
            MEMO.clear()
            RACES[0] = 0
            parts = []
            for label, text in POS.items():
                o = outcome(start(text))
                c = claimed(label, ep)
                if c is None:
                    parts.append(f"{label}:{o}")
                    continue
                hits = [nm for nm, X in c if equal(text, X)]
                bad = [repr(X)[:20] for X in rivals(label) if equal(text, X)]
                parts.append(f"{label}:{o}={'/'.join(hits) if hits else 'NONE-OF-CLAIMED'}"
                             + (f" ALSO-EQUALS{bad}" if bad else ""))
            print(f"{'epaware ' if epaware else 'textbook'} ep={'on ' if ep else 'off'} rule={rule:8s} | " + "  ".join(parts)
                  + f"  [races {RACES[0]}, memo {len(MEMO)}, {time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main)
    th.start()
    th.join()
