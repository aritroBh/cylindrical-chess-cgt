"""Independent re-implementation (theory-lens verifier, L2.2) of
  * the whole-board convention game W  (first passer ends everything; races by rule),
  * the sum model S of cylcgt.pawns.value, evaluated WITHOUT any CGT code, by
    alternating-play search on the sum game form F = (live components, frozen integer k),
  * a variant S_glob of S in which e.p. rights are global (expire after any move),
    to separate the "stale e.p. right" effect (L1.7) from nested +-BIG cancellation,
  * threat sets and the HSS test.
Nothing here imports cylcgt, lemmas or crosscheck.

Usage (from project root):
  .venv/bin/python verify/lemmas/L2.2-sum_safe-counterexample-theory/indep.py
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
BIG = 256
EP_AWARE = False  # True: a pawn that may still be taken e.p. is not passed (project convention of 2026-10-16)
FL = "abcdefghijklmnopqrstuvwxyz"


def parse(text):
    w, b = text.split("/")
    sq = lambda t: (FL.index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()), None)


def show(p):
    n = lambda s: f"{FL[s[0]]}{s[1]}"
    return "W: " + " ".join(sorted(map(n, p[0]))) + " / B: " + " ".join(sorted(map(n, p[1]))) + \
        (f" (ep {n(p[2][0])} for {p[2][2]})" if p[2] else "")


class Bd:
    def __init__(self, nf, nr, wrap, ep):
        self.nf, self.nr, self.wrap, self.ep = nf, nr, wrap, ep

    def adj(self, f):
        out = []
        for g in (f - 1, f + 1):
            if self.wrap:
                out.append(g % self.nf)
            elif 0 <= g < self.nf:
                out.append(g)
        return out

    def key(self):
        return (self.nf, self.nr, self.wrap, self.ep)


def gen(bd, p, side):
    """children of p after a move by side; side's own e.p. right (if any) is usable."""
    W_, B_, ep = p
    mine, theirs = (W_, B_) if side == "W" else (B_, W_)
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else bd.nr - 1
    occ = W_ | B_
    right = ep if (ep is not None and ep[2] == side) else None
    res = []

    def put(m, t, e=None):
        res.append((m, t, e) if side == "W" else (t, m, e))
    for (f, r) in mine:
        r1 = r + d
        if r1 < 1 or r1 > bd.nr:
            continue
        rest = mine - {(f, r)}
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= bd.nr and (f, r2) not in occ:
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if bd.ep else None
                put(rest | {(f, r2)}, theirs, e)
        for g in bd.adj(f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif right is not None and right[0] == t:
                put(rest | {t}, theirs - {right[1]})
    out = []
    for m, t, e in res:
        x = (frozenset(m), frozenset(t), e)
        if x not in out:
            out.append(x)
    return out


def ep_capt(bd, p, side, sq):
    ep = p[2]
    if not (EP_AWARE and ep is not None and ep[1] == sq and ep[2] != side):
        return False
    theirs = p[1] if side == "W" else p[0]
    return any((g, sq[1]) in theirs for g in bd.adj(sq[0]))


def has_passer(bd, p, side):
    W_, B_, _ = p
    mine, theirs = (W_, B_) if side == "W" else (B_, W_)
    for (f, r) in mine:
        if ep_capt(bd, p, side, (f, r)):
            continue
        fs = {f, *bd.adj(f)}
        if side == "W":
            if not any(g in fs and s > r for g, s in theirs):
                return True
        else:
            if not any(g in fs and s < r for g, s in theirs):
                return True
    return False


def pdist(bd, p, side):
    W_, B_, _ = p
    mine = W_ if side == "W" else B_
    best = 10 ** 9
    for (f, r) in mine:
        if ep_capt(bd, p, side, (f, r)):
            continue
        single = (frozenset([(f, r)]), B_, None) if side == "W" else (W_, frozenset([(f, r)]), None)
        if not has_passer(bd, single, side):
            continue
        if side == "W":
            if any(g == f and s > r for g, s in W_ | B_):
                continue
            dd = bd.nr - r - (1 if r == 2 else 0)
        else:
            if any(g == f and s < r for g, s in W_ | B_):
                continue
            dd = r - 1 - (1 if r == bd.nr - 1 else 0)
        best = min(best, dd)
    return best


def race_winner(bd, p, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if pdist(bd, p, other) <= pdist(bd, p, mover) else mover


def term(bd, p):
    w, b = has_passer(bd, p, "W"), has_passer(bd, p, "B")
    if w and b:
        return 0
    if w:
        return 1
    if b:
        return -1
    return None


def comps(bd, p):
    W_, B_, ep = p
    files = sorted({f for f, _ in W_ | B_})
    groups = []
    for f in files:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.nf - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        s = set(g)
        e = ep if (ep is not None and ep[0][0] in s) else None
        out.append((frozenset(q for q in W_ if q[0] in s), frozenset(q for q in B_ if q[0] in s), e))
    return out


# ------------------------------------------------------------------ W (whole board)
_BD = {}


def _bd(k):
    return _BD[k]


@lru_cache(maxsize=None)
def w_win(bk, p, side, rule):
    bd = _bd(bk)
    t = term(bd, p)
    assert t != 0
    if t is not None:
        return "W" if t == 1 else "B"
    other = "B" if side == "W" else "W"
    for c in gen(bd, p, side):
        tc = term(bd, c)
        if tc == 0:
            r = race_winner(bd, c, side, rule)
        elif tc is not None:
            r = "W" if tc == 1 else "B"
        else:
            r = w_win(bk, c, other, rule)
        if r == side:
            return side
    return other


def outcome(fn, *args):
    a = fn(*args, "W") == "W"  # White moves first, White wins?
    b = fn(*args, "B") == "W"
    return "L" if a and b else "R" if (not a and not b) else ("N" if a else "P")


def oW(bd, p, rule="count"):
    _BD[bd.key()] = bd
    return outcome(lambda pp, s: w_win(bd.key(), pp, s, rule), p)


# ------------------------------------------------------------------ S via the sum form F
def canon(cs):
    return tuple(sorted(cs, key=lambda c: (sorted(c[0]), sorted(c[1]), str(c[2]))))


def strip(bd, cs):
    """glob mode: remove every e.p. right; a component whose pawn was 'not passed'
    only because of a right (EP_AWARE) now freezes to +-BIG."""
    out, dk = [], 0
    for c in cs:
        c2 = (c[0], c[1], None)
        t = term(bd, c2)
        if t is None:
            out.append(c2)
        else:
            assert t != 0
            dk += t * BIG
    return out, dk


@lru_cache(maxsize=None)
def s_win(bk, cs, k, side, rule, glob):
    """winner of F = sum of live components cs + integer k, `side` to move.
    glob=False: e.p. rights local to components (pawns.value semantics).
    glob=True : every right expires after any move anywhere."""
    bd = _bd(bk)
    other = "B" if side == "W" else "W"
    sgn = 1 if side == "W" else -1
    # move in the integer
    if (side == "W" and k > 0) or (side == "B" and k < 0):
        ncs, dk = (cs, 0) if not glob else strip(bd, cs)
        if s_win(bk, canon(ncs), k - sgn + dk, other, rule, glob) == side:
            return side
    for i, z in enumerate(cs):
        rest = list(cs[:i] + cs[i + 1:])
        dk = 0
        if glob:
            rest, dk = strip(bd, rest)
        # pawns._value: the other side's right in z expires when side moves in z
        zz = z if (z[2] is None or z[2][2] == side) else (z[0], z[1], None)
        for c in gen(bd, zz, side):
            t = term(bd, c)
            if t == 0:
                kk = k + dk + (BIG if race_winner(bd, c, side, rule) == "W" else -BIG)
                ncs = canon(rest)
            elif t is not None:
                kk = k + dk + t * BIG
                ncs = canon(rest)
            else:
                kk = k + dk
                ncs = canon(rest + comps(bd, c))
            if s_win(bk, ncs, kk, other, rule, glob) == side:
                return side
    return other


def oS(bd, p, rule="count", glob=False):
    _BD[bd.key()] = bd
    t = term(bd, p)
    if t in (1, -1):
        return "L" if t == 1 else "R"
    cs = canon(comps(bd, p))
    return outcome(lambda c, s: s_win(bd.key(), c, 0, s, rule, glob), cs)


# ------------------------------------------------------------------ threats, HSS
@lru_cache(maxsize=None)
def tau(bk, p):
    bd = _bd(bk)
    out = set()
    if has_passer(bd, p, "W"):
        out.add(1)
    if has_passer(bd, p, "B"):
        out.add(-1)
    if not out:
        for side in ("W", "B"):
            src = p if (p[2] is None or p[2][2] == side) else (p[0], p[1], None)
            for c in gen(bd, src, side):
                out |= tau(bk, c)
    return frozenset(out)


def reach(bd, p):
    seen, st = {p}, [p]
    while st:
        x = st.pop()
        if term(bd, x) is not None:
            continue
        for side in ("W", "B"):
            src = x if (x[2] is None or x[2][2] == side) else (x[0], x[1], None)
            for c in gen(bd, src, side):
                if c not in seen:
                    seen.add(c)
                    st.append(c)
    return seen


def unsafe_nodes(bd, p):
    _BD[bd.key()] = bd
    out = []
    for y in reach(bd, p):
        if term(bd, y) is not None:
            continue
        cc = comps(bd, y)
        ts = [tau(bd.key(), c) for c in cc]
        if any(1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts) if i != j):
            out.append(y)
    return out


ROWS = [
    (Bd(8, 8, True, False), "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
    (Bd(8, 8, True, False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
    (Bd(8, 8, True, False), "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
    (Bd(8, 8, True, True), "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
    (Bd(8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
    (Bd(8, 7, True, False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
    (Bd(7, 6, False, True), "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
    (Bd(8, 8, True, True), "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
    (Bd(6, 8, False, False), "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
]

if __name__ == "__main__":
    import time
    only = sys.argv[1:] and int(sys.argv[1])
    for i, (bd, txt, rule, cS, cW) in enumerate(ROWS):
        if only and i + 1 != only:
            continue
        t0 = time.time()
        p = parse(txt)
        nc = len(comps(bd, p))
        s = oS(bd, p, rule)
        w = oW(bd, p, rule)
        sg = oS(bd, p, rule, glob=True) if bd.ep else "-"
        print(f"row {i+1}: {bd.key()} {txt} [{rule}] comps={nc} | indep o(S)={s} (claimed {cS}) "
              f"o(W)={w} (claimed {cW}) o(S_glob-ep)={sg} | {time.time()-t0:.1f}s", flush=True)
