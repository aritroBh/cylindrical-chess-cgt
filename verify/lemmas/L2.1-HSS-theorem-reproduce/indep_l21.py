"""Independent re-implementation (verifier, lens REPRODUCE) for claim L2.1-HSS-theorem.

Written from the rules in notes/lemmas.md section 0 WITHOUT importing cylcgt, lemmas or crosscheck.
It provides:
  * its own move generator, passer test, components, race rules;
  * o(W): whole-board convention game by alternating minimax;
  * o(S): the sum model's game form F (live components with LOCAL e.p. rights + a frozen
    integer n), solved exactly for ANY value of BIG by a threshold recursion (no CGT library):
        t_L(L) = least n such that Left moving first wins L + n,
        t_R(L) = least n such that Left wins L + n when Right moves first;
    a = min over Left moves (L',d) of t_R(L') - d,  b = max over Right moves of t_L(L') - d,
    t_L = a if a <= 0 else min(a, max(1, b+1)),  t_R = b if b >= 0 else max(b, min(0, a-1)).
    (derived from: Left can move in n iff n >= 1, Right iff n <= -1.)
  * its own HSS test and its own (E) test.

Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/lemmas/L2.1-HSS-theorem-reproduce/indep_l21.py --n 1500 --seed 1
"""
from __future__ import annotations

import argparse
import random
import sys
from collections import Counter

sys.setrecursionlimit(1_000_000)
INF = float("inf")
FILES = "abcdefghijklmnopqrstuvwxyz"


class B:
    __slots__ = ("n", "m", "wrap", "ep", "_h")

    def __init__(self, n, m, wrap, ep):
        self.n, self.m, self.wrap, self.ep = n, m, wrap, ep
        self._h = hash((n, m, wrap, ep))

    def __hash__(self):
        return self._h

    def __eq__(self, o):
        return (self.n, self.m, self.wrap, self.ep) == (o.n, o.m, o.wrap, o.ep)

    def __repr__(self):
        return f"{self.n}x{self.m} {'cyl' if self.wrap else 'flat'} ep={'on' if self.ep else 'off'}"

    def adj(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.wrap:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return out


# position = (white frozenset, black frozenset, ep) ; ep = (target, captured, entitled side) or None

def show(p):
    w = " ".join(f"{FILES[f]}{r}" for f, r in sorted(p[0]))
    b = " ".join(f"{FILES[f]}{r}" for f, r in sorted(p[1]))
    return f"W: {w} / B: {b}" + (f" (ep {FILES[p[2][0][0]]}{p[2][0][1]} for {p[2][1 + 1]})" if p[2] else "")


def gen(bd: B, p, side):
    """children after one move of `side`; any right not belonging to `side` is ignored; children
    carry a right only if created by this move."""
    W_, K_, ep = p
    mine, theirs = (W_, K_) if side == "W" else (K_, W_)
    occ = W_ | K_
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else bd.m - 1
    usable = ep if (ep is not None and ep[2] == side) else None
    out = []
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if r1 < 1 or r1 > bd.m:
            continue
        if (f, r1) not in occ:
            out.append(_mk(side, rest | {(f, r1)}, theirs, None))
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= bd.m and (f, r2) not in occ:
                ne = ((f, r1), (f, r2), "B" if side == "W" else "W") if bd.ep else None
                out.append(_mk(side, rest | {(f, r2)}, theirs, ne))
        for g in bd.adj(f):
            t = (g, r1)
            if t in theirs:
                out.append(_mk(side, rest | {t}, theirs - {t}, None))
            elif usable is not None and usable[0] == t:
                out.append(_mk(side, rest | {t}, theirs - {usable[1]}, None))
    return out


def _mk(side, mine, theirs, ep):
    return (frozenset(mine), frozenset(theirs), ep) if side == "W" else (frozenset(theirs), frozenset(mine), ep)


def pawn_passed(bd, p, side, sqr):
    f, r = sqr
    files = {f, *bd.adj(f)}
    if side == "W":
        return not any(g in files and s > r for g, s in p[1])
    return not any(g in files and s < r for g, s in p[0])


def has_passer(bd, p, side):
    mine = p[0] if side == "W" else p[1]
    return any(pawn_passed(bd, p, side, s) for s in mine)


def term(bd, p):
    w, b = has_passer(bd, p, "W"), has_passer(bd, p, "B")
    if w and b:
        return 0
    if w:
        return 1
    if b:
        return -1
    return None


def pdist(bd, p, side):
    occ = p[0] | p[1]
    best = INF
    mine = p[0] if side == "W" else p[1]
    for (f, r) in mine:
        if not pawn_passed(bd, p, side, (f, r)):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, bd.m + 1)):
                continue
            dd = bd.m - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == bd.m - 1 else 0)
        best = min(best, dd)
    return best


def race_win(bd, p, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if pdist(bd, p, other) <= pdist(bd, p, mover) else mover


def comps(bd, p):
    occf = sorted({f for f, _ in p[0] | p[1]})
    if not occf:
        return []
    groups = []
    for f in occf:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if bd.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bd.n - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        fs = set(g)
        e = p[2] if (p[2] is not None and p[2][0][0] in fs) else None
        out.append((frozenset(s for s in p[0] if s[0] in fs), frozenset(s for s in p[1] if s[0] in fs), e))
    return out


# ------------------------------------------------------------------ W: alternating minimax
_Wm = {}


def w_win(bd, p, tomove, rule):
    key = (bd, p, tomove, rule)
    r = _Wm.get(key)
    if r is not None:
        return r
    other = "B" if tomove == "W" else "W"
    res = other
    for c in gen(bd, p, tomove):
        t = term(bd, c)
        if t == 0:
            wnr = race_win(bd, c, tomove, rule)
        elif t == 1:
            wnr = "W"
        elif t == -1:
            wnr = "B"
        else:
            wnr = w_win(bd, c, other, rule)
        if wnr == tomove:
            res = tomove
            break
    _Wm[key] = res
    return res


def cls(lf, rf_leftwins):
    if lf and rf_leftwins:
        return "L"
    if not lf and not rf_leftwins:
        return "R"
    return "N" if lf else "P"


def o_W(bd, p, rule):
    t = term(bd, p)
    assert t is None
    return cls(w_win(bd, p, "W", rule) == "W", w_win(bd, p, "B", rule) == "W")


# ------------------------------------------------------------------ S: sum game form, thresholds
_Fm = {}


def f_moves(bd, live, side, rule, BIG):
    """(new live multiset, integer delta) for each move of `side` in a live component."""
    for z in live:
        rest = live - {z}
        for c in gen(bd, z, side):
            t = term(bd, c)
            if t == 0:
                yield rest, (BIG if race_win(bd, c, side, rule) == "W" else -BIG)
            elif t == 1:
                yield rest, BIG
            elif t == -1:
                yield rest, -BIG
            else:
                yield rest | frozenset(comps(bd, c)), 0


def thr(bd, live, rule, BIG):
    key = (bd, live, rule, BIG)
    r = _Fm.get(key)
    if r is not None:
        return r
    a = INF
    for nl, dl in f_moves(bd, live, "W", rule, BIG):
        a = min(a, thr(bd, nl, rule, BIG)[1] - dl)
    b = -INF
    for nl, dl in f_moves(bd, live, "B", rule, BIG):
        b = max(b, thr(bd, nl, rule, BIG)[0] - dl)
    tL = a if a <= 0 else min(a, max(1, b + 1))
    tR = b if b >= 0 else max(b, min(0, a - 1))
    r = (tL, tR)
    _Fm[key] = r
    return r


def o_S(bd, p, rule, BIG=256):
    t = term(bd, p)
    if t is not None:
        raise ValueError("terminal root")
    tL, tR = thr(bd, frozenset(comps(bd, p)), rule, BIG)
    return cls(0 >= tL, 0 >= tR)


# ------------------------------------------------------------------ threats, HSS, (E)
_Tm = {}


def strip_for(p, side):
    """position from which `side` generates moves (rights of the other side expire)."""
    if p[2] is not None and p[2][2] != side:
        return (p[0], p[1], None)
    return p


def threats(bd, p):
    key = (bd, p)
    r = _Tm.get(key)
    if r is not None:
        return r
    out = set()
    if has_passer(bd, p, "W"):
        out.add(1)
    if has_passer(bd, p, "B"):
        out.add(-1)
    if not out:
        for side in ("W", "B"):
            for c in gen(bd, strip_for(p, side), side):
                out |= threats(bd, c)
                if len(out) == 2:
                    break
            if len(out) == 2:
                break
    r = frozenset(out)
    _Tm[key] = r
    return r


def reach(bd, p):
    seen = {p}
    st = [p]
    while st:
        x = st.pop()
        if term(bd, x) is not None:
            continue
        for side in ("W", "B"):
            for c in gen(bd, strip_for(x, side), side):
                if c not in seen:
                    seen.add(c)
                    st.append(c)
    return seen


def pw_safe(bd, y):
    ts = [threats(bd, c) for c in comps(bd, y)]
    for i, a in enumerate(ts):
        for j, b in enumerate(ts):
            if i != j and 1 in a and -1 in b:
                return False
    return True


def analyse(bd, p):
    """returns (HSS, E, nontrivial) where nontrivial = some reachable non-terminal node with >= 2
    components has a move into a terminal child while another component still holds pawns
    (i.e. the sum model really continues play after a freeze)."""
    R = reach(bd, p)
    hss = True
    E = True
    nontriv = False
    for y in R:
        if term(bd, y) is not None:
            continue
        cs = comps(bd, y)
        if len(cs) >= 2:
            if hss and not pw_safe(bd, y):
                hss = False
            if y[2] is not None and E:
                side = y[2][2]
                # usable iff the entitled side has an e.p. capture now
                plain = (y[0], y[1], None)
                with_ep = set(gen(bd, y, side))
                without = set(gen(bd, plain, side))
                if with_ep - without:
                    E = False
            if not nontriv:
                for z in cs:
                    for side in ("W", "B"):
                        if any(term(bd, c) is not None for c in gen(bd, strip_for(z, side), side)):
                            nontriv = True
                            break
                    if nontriv:
                        break
    return hss, E, nontriv


# ------------------------------------------------------------------ sample generator (replica of
# lemmas/test_L2_big.run + lemmas/common.random_position, RNG consumption identical)

def rand_pos(rng, bd, nw, nb):
    squares = [(f, r) for f in range(bd.n) for r in range(2, bd.m - 1 + 1)]
    pick = rng.sample(squares, nw + nb)
    return (frozenset(pick[:nw]), frozenset(pick[nw:]), None)


def samples(n, seed):
    rng = random.Random(seed)
    done = 0
    while done < n:
        files = rng.choice([4, 5, 6, 7, 8])
        ranks = rng.choice([6, 7, 8])
        bd = B(files, ranks, rng.random() < 0.6, rng.random() < 0.5)
        x = None
        nw, nb = rng.randint(1, 4), rng.randint(1, 4)
        for _ in range(300):
            q = rand_pos(rng, bd, nw, nb)
            if term(bd, q) is None:
                x = q
                break
        if x is None:
            continue
        rule = rng.choice(("count", "mover", "opponent"))
        done += 1
        yield bd, x, rule


def mbound(bd, p):
    return sum(bd.m - r for _, r in p[0]), sum(r - 1 for _, r in p[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    st = Counter()
    bad = []
    small_big_bad = []
    for bd, x, rule in samples(a.n, a.seed):
        hss, E, nontriv = analyse(bd, x)
        ow = o_W(bd, x, rule)
        os_ = o_S(bd, x, rule, 256)
        mw, mb = mbound(bd, x)
        bmin = max(mw, mb) + 1
        os_min = o_S(bd, x, rule, bmin)
        multi = len(comps(bd, x)) > 1
        st["total"] += 1
        st["HSS" if hss else "notHSS"] += 1
        st[("HSS" if hss else "notHSS", "agree" if os_ == ow else "DISAGREE")] += 1
        st[("HSS" if hss else "notHSS", "E" if E else "notE")] += 1
        if hss:
            st[("HSS", "nontrivial" if nontriv else "trivial")] += 1
            if nontriv:
                st[("HSS nontrivial", "multi-root" if multi else "single-root")] += 1
        if hss and E and os_ != ow:
            bad.append((repr(bd), show(x), rule, os_, ow))
        if hss and E and os_min != ow:
            small_big_bad.append((repr(bd), show(x), rule, bmin, os_min, ow))
        if os_min != os_:
            st["o(S) differs between BIG=256 and BIG=max(M)+1"] += 1
    for k in sorted(st, key=str):
        print(k, st[k])
    print("HSS & (E) & o(S)!=o(W) at BIG=256:", len(bad))
    for b in bad[:20]:
        print("   ", b)
    print("HSS & (E) & o(S)!=o(W) at BIG=max(M_W,M_B)+1:", len(small_big_bad))
    for b in small_big_bad[:20]:
        print("   ", b)


if __name__ == "__main__":
    main()
