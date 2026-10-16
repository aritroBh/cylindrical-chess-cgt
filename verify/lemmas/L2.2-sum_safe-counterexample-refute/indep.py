"""Independent re-implementation (adversarial verifier, claim L2.2).

Imports NOTHING from cylcgt/, lemmas/ or crosscheck/. Stdlib only.

Computes, for a pawn position X on a board (files, ranks, wrap, ep):

  oW(X)  outcome class of the whole-board convention game (first passer ends
         the game; a move that creates passers for both sides is scored by the
         race rule; e.p. right valid only on the very next move), by plain
         alternating minimax.

  oS(X)  outcome class of the project's sum model S = cylcgt.pawns.value, by
         plain minimax over an explicit GAME FORM of S (no canonical forms):
         state = (live pawns, per-component e.p. rights, N) where N is the sum
         of all frozen integers +-BIG. A move is either
           - a pawn move inside one live component Z (Z's e.p. right, if any,
             dies with any move in Z; a double step creates a new right in the
             child component holding that file), after which the new
             component Z' is frozen into the race score (both sides passed)
             or +-BIG (exactly one side passed) and its pawns leave the board;
           - Left: N -> N-1 if N > 0;  Right: N -> N+1 if N < 0
             (the canonical options of an integer).
         Equal games have equal outcomes and integer summands add, so this has
         the same outcome as the CGT sum of canonical component values.
         At the root, S checks passers on the whole position first.

Race rules: "count" (opponent of the mover moves first; smaller promotion
distance wins, ties to the opponent; a pawn on its start rank counts the
double step as one move), "mover", "opponent".
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
BIG = 256
LET = "abcdefghijklmnopqrstuvwxyz"

# ----------------------------------------------------------------- board ---
class Bd:
    def __init__(self, files, ranks, wrap, ep):
        self.n, self.m, self.wrap, self.ep = files, ranks, wrap, ep

    def key(self):
        return (self.n, self.m, self.wrap, self.ep)

    def adj(self, f):
        out = []
        for g in (f - 1, f + 1):
            if self.wrap:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return out


def parse(text):
    a, b = text.split("/")
    sq = lambda t: (LET.index(t[0]), int(t[1:]))
    w = frozenset(sq(t) for t in a.split(":")[1].split())
    k = frozenset(sq(t) for t in b.split(":")[1].split())
    return w, k


def fmt(w, k):
    s = lambda S: " ".join(f"{LET[f]}{r}" for f, r in sorted(S))
    return f"W: {s(w)} / B: {s(k)}"


def pawn_passed(B, w, k, side, p):
    f, r = p
    files = {f, *B.adj(f)}
    if side == "W":
        return not any(g in files and s > r for g, s in k)
    return not any(g in files and s < r for g, s in w)


def has_passer(B, w, k, side):
    mine = w if side == "W" else k
    return any(pawn_passed(B, w, k, side, p) for p in mine)


def prom_dist(B, w, k, side):
    mine = w if side == "W" else k
    best = None
    for f, r in mine:
        if not pawn_passed(B, w, k, side, (f, r)):
            continue
        if side == "W":
            if any(g == f and s > r for g, s in mine):
                continue
            d = B.m - r - (1 if r == 2 else 0)
        else:
            if any(g == f and s < r for g, s in mine):
                continue
            d = r - 1 - (1 if r == B.m - 1 else 0)
        best = d if best is None else min(best, d)
    return 10**9 if best is None else best


def race_winner(B, w, k, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if prom_dist(B, w, k, other) <= prom_dist(B, w, k, mover) else mover


def gen(B, w, k, side, right):
    """Moves of `side`. right = (target, captured) usable by side, or None.
    Yields (w', k', newright) where newright = (target, captured, holder) or None."""
    mine, theirs = (w, k) if side == "W" else (k, w)
    occ = w | k
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else B.m - 1
    holder = "B" if side == "W" else "W"
    out = []

    def put(nm, nt, nr=None):
        out.append(((nm, nt, nr) if side == "W" else (nt, nm, nr)))

    for (f, r) in mine:
        r1 = r + d
        if not (1 <= r1 <= B.m):
            continue
        rest = mine - {(f, r)}
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= B.m and (f, r2) not in occ:
                put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), holder) if B.ep else None)
        for g in B.adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif right is not None and right[0] == t and right[1] in theirs:
                put(rest | {t}, theirs - {right[1]})
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def comps(B, w, k):
    """List of sets of files, one per component (files joined if adjacent)."""
    occ = sorted({f for f, _ in w | k})
    par = {f: f for f in occ}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for f in occ:
        for g in B.adj(f):
            if g in par:
                par[find(f)] = find(g)
    groups = {}
    for f in occ:
        groups.setdefault(find(f), set()).add(f)
    return list(groups.values())


# --------------------------------------------- W: whole-board convention ---
_WM = {}


def w_win(B, w, k, ep, tomove, rule):
    """True iff `tomove` wins the whole-board convention game. ep = (target,
    captured, holder) or None (only meaningful for the side to move)."""
    key = (B.key(), w, k, ep, tomove, rule)
    v = _WM.get(key)
    if v is not None:
        return v
    wp, bp = has_passer(B, w, k, "W"), has_passer(B, w, k, "B")
    assert not (wp or bp), "w_win called on terminal"
    other = "B" if tomove == "W" else "W"
    right = (ep[0], ep[1]) if (ep and ep[2] == tomove) else None
    res = False
    for w2, k2, nr in gen(B, w, k, tomove, right):
        p2w, p2b = has_passer(B, w2, k2, "W"), has_passer(B, w2, k2, "B")
        if p2w and p2b:
            win = race_winner(B, w2, k2, tomove, rule) == tomove
        elif p2w or p2b:
            win = (p2w and tomove == "W") or (p2b and tomove == "B")
        else:
            win = not w_win(B, w2, k2, nr, other, rule)
        if win:
            res = True
            break
    _WM[key] = res
    return res


def outcome(first_W_wins_moving_first, W_wins_when_B_first):
    if first_W_wins_moving_first and W_wins_when_B_first:
        return "L"
    if not first_W_wins_moving_first and not W_wins_when_B_first:
        return "R"
    return "N" if first_W_wins_moving_first else "P"


def oW(B, w, k, rule):
    wp, bp = has_passer(B, w, k, "W"), has_passer(B, w, k, "B")
    if wp != bp:
        return "L" if wp else "R"
    assert not wp
    a = w_win(B, w, k, None, "W", rule)
    b = not w_win(B, w, k, None, "B", rule)
    return outcome(a, b)


# ------------------------------------------------- S: sum-model game form ---
_SM = {}


def s_win(B, w, k, rights, N, tomove, rule):
    """True iff `tomove` wins the sum-model game form, `tomove` to move.
    rights: frozenset of (target, captured, holder), each tied to the component
    containing its file. N: net frozen integer."""
    key = (B.key(), w, k, rights, N, tomove, rule)
    v = _SM.get(key)
    if v is not None:
        return v
    other = "B" if tomove == "W" else "W"
    res = False
    # integer move
    if (tomove == "W" and N > 0) or (tomove == "B" and N < 0):
        if not s_win(B, w, k, rights, N - 1 if tomove == "W" else N + 1, other, rule):
            res = True
    if not res:
        for cf in comps(B, w, k):
            zw = frozenset(p for p in w if p[0] in cf)
            zk = frozenset(p for p in k if p[0] in cf)
            ow = w - zw
            ok = k - zk
            zr = [r for r in rights if r[0][0] in cf]
            assert len(zr) <= 1
            orights = rights - set(zr)
            right = None
            if zr and zr[0][2] == tomove:
                right = (zr[0][0], zr[0][1])
            for w2, k2, nr in gen(B, zw, zk, tomove, right):
                p2w, p2b = has_passer(B, w2, k2, "W"), has_passer(B, w2, k2, "B")
                if p2w and p2b:
                    win_side = race_winner(B, w2, k2, tomove, rule)
                    nw, nk, nrs = ow, ok, orights
                    N2 = N + (BIG if win_side == "W" else -BIG)
                elif p2w or p2b:
                    nw, nk, nrs = ow, ok, orights
                    N2 = N + (BIG if p2w else -BIG)
                else:
                    nw, nk = ow | w2, ok | k2
                    nrs = orights | ({nr} if nr else set())
                    N2 = N
                if not s_win(B, nw, nk, frozenset(nrs), N2, other, rule):
                    res = True
                    break
            if res:
                break
    _SM[key] = res
    return res


def oS(B, w, k, rule):
    wp, bp = has_passer(B, w, k, "W"), has_passer(B, w, k, "B")
    if wp != bp:
        return "L" if wp else "R"
    assert not wp
    a = s_win(B, w, k, frozenset(), 0, "W", rule)
    b = not s_win(B, w, k, frozenset(), 0, "B", rule)
    return outcome(a, b)


def clear():
    _WM.clear()
    _SM.clear()


CASES = [
    # (files, ranks, wrap, ep, position, rule, claimed oS, claimed oW)
    (8, 8, True, False, "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
    (8, 8, True, False, "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
    (8, 8, True, False, "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
    (8, 8, True, True, "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
    (8, 8, True, True, "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
    (8, 7, True, False, "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
    (7, 6, False, True, "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
    (8, 8, True, True, "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
    (6, 8, False, False, "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
]

if __name__ == "__main__":
    import time
    for (n, m, wrap, ep, text, rule, cs, cw) in CASES:
        B = Bd(n, m, wrap, ep)
        w, k = parse(text)
        t0 = time.time()
        nc = len(comps(B, w, k))
        s, ww = oS(B, w, k, rule), oW(B, w, k, rule)
        print(f"{n}x{m} {'cyl' if wrap else 'flat'} ep={'on' if ep else 'off'} {text} rule={rule}: "
              f"components={nc} oS={s} (claim {cs}) oW={ww} (claim {cw}) "
              f"{'MATCH' if (s, ww) == (cs, cw) else 'MISMATCH'}  [{time.time()-t0:.1f}s, "
              f"memo W={len(_WM)} S={len(_SM)}]", flush=True)
        clear()
