"""Independent re-check (REFUTE lens, run 2) of claim L2.2.

Stdlib only. Imports NOTHING from cylcgt/, lemmas/, crosscheck/ or the earlier
verify/.../indep.py. Written from the rule text in notes/lemmas.md section 0.

Quantities, for a pawn position X on board (files, ranks, wrap, ep):

  oW   outcome class of the whole-board convention game W, by alternating
       minimax: a position where exactly one side has a passer is won by that
       side; a move that gives both sides a passer is scored by the race
       rule; a side with no move loses; an e.p. right is usable only on the
       very next move.

  oS   outcome class of the sum model S (= what cylcgt.pawns.value encodes),
       computed WITHOUT canonical forms by an integer-threshold recursion.
       Positions of S's game form are (Y, k): Y = live pawns (+ the e.p. right
       stored in each live component, which dies only when someone moves in
       that component), k = sum of the frozen +-BIG integers (an integer
       summand in canonical form). For each Y let
          a(Y) = least k with "Left wins Y + k, Left moving first",
          b(Y) = least k with "Left wins Y + k, Right moving first".
       These are well defined because Y + k is monotone in k. With
          A = min over Left pawn moves  (b(Y') - delta),
          B = max over Right pawn moves (a(Y') - delta),
       (delta = +-BIG if the move froze the component, else 0) and the
       integer's own tempo moves (Left k->k-1 if k>=1, Right k->k+1 if k<=-1):
          a = min(A, max(1, b+1)),  b = max(B, min(0, a-1)),
       whose unique solution is
          A <= 0: a = A, b = max(B, A-1);   A >= 1: b = max(B,0), a = min(A, b+1).

  oS2  the same sum model by brute-force alternating minimax on the explicit
       game form (Y, k, side to move), as a check on the threshold algebra.

  oSg  variant of S in which e.p. rights expire globally (any move anywhere
       kills them), to separate "nested +-BIG cancellation" from "stale e.p."

Race rules: count (opponent of the mover moves next; smaller promotion distance
of a passed front pawn wins; ties go to the opponent; a pawn on its start rank
counts the double step as one move), mover, opponent.
"""
from __future__ import annotations

import sys

sys.setrecursionlimit(200000)
BIG = 256
INF = 10 ** 9
LET = "abcdefgh"


class Board:
    def __init__(self, n, m, wrap, ep):
        self.n, self.m, self.wrap, self.ep = n, m, wrap, ep

    def adj(self, f):
        r = []
        for g in (f - 1, f + 1):
            if self.wrap:
                r.append(g % self.n)
            elif 0 <= g < self.n:
                r.append(g)
        return r

    def __repr__(self):
        return f"{self.n}x{self.m} {'cyl' if self.wrap else 'flat'} ep={'on' if self.ep else 'off'}"


def parse(t):
    a, b = t.split("/")
    sq = lambda s: (LET.index(s[0]), int(s[1:]))
    return (frozenset(sq(s) for s in a.split(":")[1].split()),
            frozenset(sq(s) for s in b.split(":")[1].split()))


def fmt(w, k):
    n = lambda s: f"{LET[s[0]]}{s[1]}"
    return "W: " + " ".join(sorted(map(n, w))) + " / B: " + " ".join(sorted(map(n, k)))


def pawn_passed(B, w, k, side, p):
    f, r = p
    files = {f, *B.adj(f)}
    if side == "W":
        return not any(g in files and s > r for g, s in k)
    return not any(g in files and s < r for g, s in w)


def has_passer(B, w, k, side):
    return any(pawn_passed(B, w, k, side, p) for p in (w if side == "W" else k))


def dist(B, w, k, side):
    best = INF
    occ = w | k
    for (f, r) in (w if side == "W" else k):
        if not pawn_passed(B, w, k, side, (f, r)):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, B.m + 1)):
                continue
            d = B.m - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == B.m - 1 else 0)
        best = min(best, d)
    return best


def race_winner(B, w, k, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if dist(B, w, k, other) <= dist(B, w, k, mover) else mover


def gen(B, w, k, side, ep):
    """Children (w', k', new_ep). ep = (target, captured, side_allowed) or None."""
    mine, theirs = (w, k) if side == "W" else (k, w)
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else B.m - 1
    occ = w | k
    use = ep if (ep is not None and ep[2] == side) else None
    out = []

    def emit(nm, nt, e=None):
        out.append((frozenset(nm), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm), e))

    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        if not 1 <= r1 <= B.m:
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= B.m and (f, r2) not in occ:
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if B.ep else None
                emit(rest | {(f, r2)}, theirs, e)
        for g in B.adj(f):
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif use is not None and use[0] == t:
                emit(rest | {t}, theirs - {use[1]})
    return out


def comp_files(B, w, k):
    occ = sorted({f for f, _ in w | k})
    s = set(occ)
    seen, groups = set(), []
    for f in occ:
        if f in seen:
            continue
        g, stack = set(), [f]
        while stack:
            x = stack.pop()
            if x in g:
                continue
            g.add(x)
            for y in (x - 1, x + 1):
                if B.wrap:
                    y %= B.n
                if y in s and y not in g:
                    stack.append(y)
        seen |= g
        groups.append(frozenset(g))
    return groups


# ------------------------------------------------------------ W (exact) ---
def make_W(B, rule):
    memo = {}

    def win(w, k, ep, side):
        key = (w, k, ep, side)
        if key in memo:
            return memo[key]
        other = "B" if side == "W" else "W"
        res = False
        for w2, k2, e2 in gen(B, w, k, side, ep):
            pw, pb = has_passer(B, w2, k2, "W"), has_passer(B, w2, k2, "B")
            if pw and pb:
                ok = race_winner(B, w2, k2, side, rule) == side
            elif pw or pb:
                ok = ("W" if pw else "B") == side
            else:
                ok = not win(w2, k2, e2, other)
            if ok:
                res = True
                break
        memo[key] = res
        return res

    return win


def cls(lf, ls):
    """lf: Left wins moving first; ls: Left wins moving second."""
    if lf and ls:
        return "L"
    if not lf and not ls:
        return "R"
    return "N" if lf else "P"


def oW(B, x, rule):
    w, k = x
    pw, pb = has_passer(B, w, k, "W"), has_passer(B, w, k, "B")
    if pw != pb:
        return "L" if pw else "R"
    assert not pw
    win = make_W(B, rule)
    return cls(win(w, k, None, "W"), not win(w, k, None, "B"))


# ------------------------------------------------------------ S models ---
def split_rights(eps, files):
    mine = [e for e in eps if e[0][0] in files]
    assert len(mine) <= 1
    return (mine[0] if mine else None), frozenset(e for e in eps if e[0][0] not in files)


def s_children(B, w, k, eps, side, rule, global_ep):
    """Pawn moves of the S game form from live state (w, k, eps):
    yields (w', k', eps', delta)."""
    for files in comp_files(B, w, k):
        zw = frozenset(p for p in w if p[0] in files)
        zk = frozenset(p for p in k if p[0] in files)
        epz, others = split_rights(eps, files)
        restw, restk = w - zw, k - zk
        for cw, ck, e in gen(B, zw, zk, side, epz):
            pw, pb = has_passer(B, cw, ck, "W"), has_passer(B, cw, ck, "B")
            base = frozenset() if global_ep else others
            if pw and pb:
                win = race_winner(B, cw, ck, side, rule)
                yield restw, restk, base, (BIG if win == "W" else -BIG)
            elif pw or pb:
                yield restw, restk, base, (BIG if pw else -BIG)
            else:
                ne = base | ({e} if e is not None else frozenset())
                yield restw | cw, restk | ck, frozenset(ne), 0


def make_S(B, rule, global_ep=False):
    memo = {}

    def ab(w, k, eps):
        key = (w, k, eps)
        if key in memo:
            return memo[key]
        A = INF
        for w2, k2, e2, dl in s_children(B, w, k, eps, "W", rule, global_ep):
            A = min(A, ab(w2, k2, e2)[1] - dl)
        Bv = -INF
        for w2, k2, e2, dl in s_children(B, w, k, eps, "B", rule, global_ep):
            Bv = max(Bv, ab(w2, k2, e2)[0] - dl)
        t_eps = frozenset() if global_ep else eps   # state after a tempo move
        if t_eps == eps:
            if A <= 0:
                a, b = A, max(Bv, A - 1)
            else:
                b = max(Bv, 0)
                a = min(A, b + 1)
        else:
            at, bt = ab(w, k, t_eps)
            a = min(A, max(1, bt + 1))
            b = max(Bv, min(0, at - 1))
        memo[key] = (a, b)
        return a, b

    return ab


def oS(B, x, rule, global_ep=False):
    w, k = x
    pw, pb = has_passer(B, w, k, "W"), has_passer(B, w, k, "B")
    if pw != pb:
        return "L" if pw else "R"
    assert not pw
    a, b = make_S(B, rule, global_ep)(w, k, frozenset())
    return cls(a <= 0, b <= 0)


def oS2(B, x, rule):
    """Brute force on the explicit game form (Y, n, side to move)."""
    memo = {}

    def win(w, k, eps, n, side):
        key = (w, k, eps, n, side)
        if key in memo:
            return memo[key]
        other = "B" if side == "W" else "W"
        res = False
        if side == "W" and n >= 1 and not win(w, k, eps, n - 1, other):
            res = True
        if not res and side == "B" and n <= -1 and not win(w, k, eps, n + 1, other):
            res = True
        if not res:
            for w2, k2, e2, dl in s_children(B, w, k, eps, side, rule, False):
                if not win(w2, k2, e2, n + dl, other):
                    res = True
                    break
        memo[key] = res
        return res

    w, k = x
    return cls(win(w, k, frozenset(), 0, "W"), not win(w, k, frozenset(), 0, "B"))


def threats(B, w, k, memo):
    key = (w, k)
    if key in memo:
        return memo[key]
    out = set()
    if has_passer(B, w, k, "W"):
        out.add("+")
    if has_passer(B, w, k, "B"):
        out.add("-")
    if not out:
        for side in "WB":
            for w2, k2, _ in gen(B, w, k, side, None):
                out |= threats(B, w2, k2, memo)
    memo[key] = frozenset(out)
    return memo[key]
