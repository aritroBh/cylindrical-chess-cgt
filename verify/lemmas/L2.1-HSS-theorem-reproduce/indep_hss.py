"""Independent re-implementation (verifier, claim L2.1-HSS-theorem).

Written from the rules stated in notes/lemmas.md section 0, WITHOUT importing
cylcgt or lemmas.common for any game logic.  It provides:

  * gen(B, pos, side)       pawn moves M1-M4 (own code)
  * passed(B, pos, side)    passed-pawn test (own code)
  * comps(B, pos)           components (own code; e.p. right goes with target file)
  * w_outcome(B, pos, rule) alternating-play outcome of the whole-board game W
  * s_outcome(B, pos, rule) outcome of the sum model S, computed by a direct
                            game-sum minimax over states (live components,
                            integer k, side to move) -- no CGT at all.  Frozen
                            +-BIG summands are merged into one integer k, which
                            is value-preserving (integers add exactly).
  * hss(B, pos)             hereditarily sum-safe test (own threat sets)
  * cond_E(B, pos)          condition (E): no position reachable (any order,
                            not past a passer) with >= 2 components carries a
                            usable e.p. right.

Positions: (frozenset white, frozenset black, ep) with ep = (target, captured,
side) or None.  Board: (files, ranks, wrap, ep_on).
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
BIG = 256


def nb(B, f):
    n, _, wrap, _ = B
    out = []
    for d in (-1, 1):
        g = f + d
        if wrap:
            out.append(g % n)
        elif 0 <= g < n:
            out.append(g)
    return out


def gen(B, pos, side):
    """All children after one move of `side`.  The right in pos is usable only
    if it belongs to `side`; children carry a right only after a double step."""
    n, m, wrap, ep_on = B
    W, K, ep = pos
    mine, theirs = (W, K) if side == "W" else (K, W)
    occ = W | K
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else m - 1
    right = ep if (ep is not None and ep[2] == side) else None
    res = set()

    def put(nm, nt, e=None):
        if side == "W":
            res.add((frozenset(nm), frozenset(nt), e))
        else:
            res.add((frozenset(nt), frozenset(nm), e))

    for p in mine:
        f, r = p
        r1 = r + d
        if r1 < 1 or r1 > m:
            continue
        rest = mine - {p}
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= m and (f, r2) not in occ:
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if ep_on else None
                put(rest | {(f, r2)}, theirs, e)
        for g in nb(B, f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif right is not None and right[0] == t:
                put(rest | {t}, theirs - {right[1]})
    return res


def pawn_passed(B, pos, side, p):
    W, K, _ = pos
    f, r = p
    fs = {f, *nb(B, f)}
    if side == "W":
        return not any(g in fs and s > r for (g, s) in K)
    return not any(g in fs and s < r for (g, s) in W)


def passed(B, pos, side):
    W, K, _ = pos
    return any(pawn_passed(B, pos, side, p) for p in (W if side == "W" else K))


def term(B, pos):
    wp, bp = passed(B, pos, "W"), passed(B, pos, "B")
    if wp and bp:
        return 0
    if wp:
        return 1
    if bp:
        return -1
    return None


def pdist(B, pos, side):
    n, m, _, _ = B
    W, K, _ = pos
    mine = W if side == "W" else K
    best = 10 ** 6
    for p in mine:
        f, r = p
        if not pawn_passed(B, pos, side, p):
            continue
        if side == "W":
            if any(g == f and s > r for (g, s) in mine):
                continue
            dd = m - r - (1 if r == 2 else 0)
        else:
            if any(g == f and s < r for (g, s) in mine):
                continue
            dd = r - 1 - (1 if r == m - 1 else 0)
        best = min(best, dd)
    return best


def race_sign(B, pos, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        win = mover
    elif rule == "opponent":
        win = other
    else:
        win = other if pdist(B, pos, other) <= pdist(B, pos, mover) else mover
    return 1 if win == "W" else -1


# ------------------------------------------------------------- whole board W
@lru_cache(maxsize=None)
def w_win(B, pos, side, rule):
    """Winner ('W'/'B') of the whole-board convention game, `side` to move."""
    t = term(B, pos)
    assert t is None
    other = "B" if side == "W" else "W"
    for c in gen(B, pos, side):
        tc = term(B, c)
        if tc == 0:
            r = "W" if race_sign(B, c, side, rule) > 0 else "B"
        elif tc is not None:
            r = "W" if tc > 0 else "B"
        else:
            r = w_win(B, c, other, rule)
        if r == side:
            return side
    return other


def outcome_from(wf, ws):
    """wf: Left wins moving first; ws: Left wins moving second."""
    if wf and ws:
        return "L"
    if not wf and not ws:
        return "R"
    return "N" if wf else "P"


def w_outcome(B, pos, rule):
    return outcome_from(w_win(B, pos, "W", rule) == "W", w_win(B, pos, "B", rule) == "W")


# ------------------------------------------------------------- components
def comps(B, pos):
    n, _, wrap, _ = B
    W, K, ep = pos
    occf = sorted({f for f, _ in W | K})
    if not occf:
        return []
    # union-find over occupied files with adjacency
    parent = {f: f for f in occf}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    s = set(occf)
    for f in occf:
        for g in nb(B, f):
            if g in s:
                parent[find(f)] = find(g)
    groups = {}
    for f in occf:
        groups.setdefault(find(f), set()).add(f)
    out = []
    for fs in groups.values():
        e = ep if (ep is not None and ep[0][0] in fs) else None
        out.append((frozenset(p for p in W if p[0] in fs), frozenset(p for p in K if p[0] in fs), e))
    return out


def ckey(c):
    W, K, e = c
    return (tuple(sorted(W)), tuple(sorted(K)), e)


# ------------------------------------------------------------- sum model S
def s_outcome(B, pos, rule):
    assert term(B, pos) is None
    live = tuple(sorted((ckey(c) for c in comps(B, pos))))
    wf = s_win(B, live, 0, "W", rule) == "W"
    ws = s_win(B, live, 0, "B", rule) == "W"
    return outcome_from(wf, ws)


def unkey(k):
    return (frozenset(k[0]), frozenset(k[1]), k[2])


@lru_cache(maxsize=None)
def comp_moves(B, ck, side, rule):
    """Moves of `side` inside one live component, local e.p. (a right not
    belonging to `side` is stripped; others' rights are never touched).
    Returns tuples (delta_k, new_component_keys)."""
    c = unkey(ck)
    W, K, e = c
    src = c if (e is not None and e[2] == side) else (W, K, None)
    out = set()
    for ch in gen(B, src, side):
        t = term(B, ch)
        if t == 0:
            out.add((race_sign(B, ch, side, rule) * BIG, ()))
        elif t is not None:
            out.add((t * BIG, ()))
        else:
            out.add((0, tuple(sorted(ckey(x) for x in comps(B, ch)))))
    return tuple(out)


@lru_cache(maxsize=None)
def s_win(B, live, k, side, rule):
    other = "B" if side == "W" else "W"
    # integer move
    if side == "W" and k >= 1:
        if s_win(B, live, k - 1, other, rule) == "W":
            return "W"
    if side == "B" and k <= -1:
        if s_win(B, live, k + 1, other, rule) == "B":
            return "B"
    for i, ck in enumerate(live):
        rest = live[:i] + live[i + 1:]
        for dk, new in comp_moves(B, ck, side, rule):
            nl = tuple(sorted(rest + new))
            if s_win(B, nl, k + dk, other, rule) == side:
                return side
    return other


# ------------------------------------------------------------- threats / HSS / (E)
def moves_any(B, pos):
    W, K, e = pos
    for side in ("W", "B"):
        src = pos if (e is not None and e[2] == side) else (W, K, None)
        for c in gen(B, src, side):
            yield c


@lru_cache(maxsize=None)
def tau(B, pos):
    out = set()
    if passed(B, pos, "W"):
        out.add(1)
    if passed(B, pos, "B"):
        out.add(-1)
    if not out:
        for c in moves_any(B, pos):
            out |= tau(B, c)
    return frozenset(out)


def reach(B, pos):
    seen = {pos}
    st = [pos]
    while st:
        x = st.pop()
        if term(B, x) is not None:
            continue
        for c in moves_any(B, x):
            if c not in seen:
                seen.add(c)
                st.append(c)
    return seen


def pair_safe(B, pos):
    ts = [tau(B, c) for c in comps(B, pos)]
    for i, a in enumerate(ts):
        for j, b in enumerate(ts):
            if i != j and 1 in a and -1 in b:
                return False
    return True


def hss(B, pos):
    return all(pair_safe(B, y) for y in reach(B, pos) if term(B, y) is None)


def right_usable(B, pos):
    W, K, e = pos
    if e is None:
        return False
    (tf, tr), _, s = e
    if s == "W":
        return any((g, tr - 1) in W for g in nb(B, tf))
    return any((g, tr + 1) in K for g in nb(B, tf))


def cond_E(B, pos):
    if not B[3]:
        return True
    for y in reach(B, pos):
        if term(B, y) is not None:
            continue
        if y[2] is not None and len(comps(B, y)) >= 2 and right_usable(B, y):
            return False
    return True


def parse(text):
    F = "abcdefghijklmnopqrstuvwxyz"
    wp, bp = text.split("/")
    w = frozenset((F.index(t[0]), int(t[1:])) for t in wp.split(":")[1].split())
    b = frozenset((F.index(t[0]), int(t[1:])) for t in bp.split(":")[1].split())
    return (w, b, None)


def show(pos):
    F = "abcdefghijklmnopqrstuvwxyz"
    W, K, e = pos
    s = "W: " + " ".join(sorted(f"{F[f]}{r}" for f, r in W)) + " / B: " + " ".join(sorted(f"{F[f]}{r}" for f, r in K))
    if e:
        s += f" (ep {F[e[0][0]]}{e[0][1]} for {e[2]})"
    return s
