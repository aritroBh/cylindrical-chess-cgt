"""Independent re-implementation (verifier C4-refute) of the pawn-endgame CGT model,
written from the stated conventions; it does NOT import cylcgt or any worker code.

  * own canonical-form CGT engine (numbers are atoms; dominated/reversible removal;
    number-avoidance shortcut only for canonical non-number games)
  * own pawn move generator, passed-pawn test, race rules (count/mover/opponent),
    en passant on/off, empty-file decomposition.

Value key format replicates atlas_run.vkey (numbers as a/b, nimbers *n, otherwise
"{sorted L keys|sorted R keys}") so that results can be compared to the worker's
files key-by-key.

Usage:
  cd /Users/aritro/Downloads/Research/Chessendgames/verify/cylatlas/C4-refute
  ../../../.venv/bin/python indep.py RULE EP OUTFILE      (RULE in count|mover|opponent, EP in 1|0)
"""
from __future__ import annotations

import itertools
import json
import sys
import threading
import time
from fractions import Fraction as Fr

sys.setrecursionlimit(1_000_000)

# ----------------------------------------------------------------------------- CGT
class Node:
    __slots__ = ("L", "R", "num", "id", "canon")


_tab: dict = {}
_nodes: list = []


def _node(L, R, num=None):
    if num is not None:
        key = ("n", num)
    else:
        key = (frozenset(x.id for x in L), frozenset(x.id for x in R))
    g = _tab.get(key)
    if g is None:
        g = Node()
        g.num = num
        g.L = tuple(L) if num is None else None
        g.R = tuple(R) if num is None else None
        g.id = len(_nodes)
        g.canon = num is not None
        _nodes.append(g)
        _tab[key] = g
    return g


def number(x) -> Node:
    return _node(None, None, Fr(x))


def lopts(g):
    if g.num is None:
        return g.L
    x = g.num
    if x.denominator == 1:
        return (number(x - 1),) if x > 0 else ()
    k = x.denominator
    return (number(x - Fr(1, k)),)


def ropts(g):
    if g.num is None:
        return g.R
    x = g.num
    if x.denominator == 1:
        return (number(x + 1),) if x < 0 else ()
    k = x.denominator
    return (number(x + Fr(1, k)),)


_le: dict = {}


def le(a, b) -> bool:
    if a is b:
        return True
    an, bn = a.num, b.num
    if an is not None and bn is not None:
        return an <= bn
    key = (a.id, b.id)
    r = _le.get(key)
    if r is not None:
        return r
    if an is not None and b.canon:
        # number avoidance: x <= G (G canonical, not a number) iff no G^R <= x
        r = not any(le(br, a) for br in b.R)
    elif bn is not None and a.canon:
        r = not any(le(b, al) for al in a.L)
    else:
        r = not any(le(b, al) for al in lopts(a)) and not any(le(br, a) for br in ropts(b))
    _le[key] = r
    return r


def simplest(lo, hi):
    """Simplest number strictly between lo and hi (None = unbounded)."""
    if lo is None and hi is None:
        return Fr(0)
    if lo is None:
        return Fr(0) if hi > 0 else Fr(-(-hi.numerator // hi.denominator) - 1)  # ceil(hi)-1
    if hi is None:
        return Fr(0) if lo < 0 else Fr(lo.numerator // lo.denominator + 1)  # floor(lo)+1
    assert lo < hi
    if lo < 0 < hi:
        return Fr(0)
    if lo >= 0:
        n = lo.numerator // lo.denominator + 1
        if n < hi:
            return Fr(n)
    else:
        n = -(-hi.numerator // hi.denominator) - 1
        if n > lo:
            return Fr(n)
    k = 1
    while True:
        d = 2 ** k
        # smallest m/d > lo
        m = (lo * d).numerator // (lo * d).denominator + 1
        if Fr(m, d) < hi:
            return Fr(m, d)
        k += 1


def _maximal(S):
    S = list(S)
    return [x for x in S if not any(y is not x and le(x, y) for y in S)]


def _minimal(S):
    S = list(S)
    return [x for x in S if not any(y is not x and le(y, x) for y in S)]


def make(L, R) -> Node:
    L = set(L)
    R = set(R)
    while True:
        L = _maximal(L)
        R = _minimal(R)
        if all(x.num is not None for x in L) and all(x.num is not None for x in R):
            lm = max((x.num for x in L), default=None)
            rm = min((x.num for x in R), default=None)
            if lm is None or rm is None or lm < rm:
                return number(simplest(lm, rm))
        T = _node(L, R)
        if T.canon:
            return T
        changed = False
        nL = set()
        for x in L:
            rev = next((xr for xr in ropts(x) if le(xr, T)), None)
            if rev is None:
                nL.add(x)
            else:
                nL.update(lopts(rev))
                changed = True
        nR = set()
        for y in R:
            rev = next((yl for yl in lopts(y) if le(T, yl)), None)
            if rev is None:
                nR.add(y)
            else:
                nR.update(ropts(rev))
                changed = True
        if not changed:
            T.canon = True
            return T
        L, R = nL, nR


_neg: dict = {}


def neg(g):
    if g.num is not None:
        return number(-g.num)
    r = _neg.get(g.id)
    if r is None:
        r = make([neg(x) for x in g.R], [neg(x) for x in g.L])
        _neg[g.id] = r
    return r


_add: dict = {}


def add(a, b):
    if a.num is not None and b.num is not None:
        return number(a.num + b.num)
    if a.num is not None:
        a, b = b, a
    key = (a.id, b.id) if a.id <= b.id else (b.id, a.id)
    r = _add.get(key)
    if r is not None:
        return r
    if b.num is not None:
        # number translation (a canonical, not a number)
        r = make([add(x, b) for x in a.L], [add(x, b) for x in a.R])
    else:
        r = make([add(x, b) for x in a.L] + [add(a, y) for y in b.L],
                 [add(x, b) for x in a.R] + [add(a, y) for y in b.R])
    _add[key] = r
    return r


_key: dict = {}


def nim_value(g):
    """n if canonical g == *n (n>=1), else None."""
    if g.num is not None or set(g.L) != set(g.R):
        return None
    ks = set()
    for x in g.L:
        if x.num is not None:
            if x.num != 0:
                return None
            ks.add(0)
        else:
            v = nim_value(x)
            if v is None:
                return None
            ks.add(v)
    n = len(ks)
    return n if ks == set(range(n)) and n >= 1 else None


def vkey(g) -> str:
    r = _key.get(g.id)
    if r is not None:
        return r
    if g.num is not None:
        x = g.num
        r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    else:
        nv = nim_value(g)
        if nv is not None:
            r = f"*{nv}"
        else:
            r = "{" + ",".join(sorted(vkey(x) for x in g.L)) + "|" + ",".join(sorted(vkey(x) for x in g.R)) + "}"
    _key[g.id] = r
    return r


BIG = 256
_bigm: dict = {}


def has_big(g) -> bool:
    if g.num is not None:
        return abs(g.num) >= BIG // 2
    r = _bigm.get(g.id)
    if r is None:
        r = any(has_big(x) for x in g.L + g.R)
        _bigm[g.id] = r
    return r


# ----------------------------------------------------------------------------- pawns
RANKS = 8


class Model:
    def __init__(self, rule: str, ep: bool):
        self.rule = rule
        self.ep = ep
        self.memo = {}
        self.races = 0

    # geometry ------------------------------------------------------------
    @staticmethod
    def side_files(n, wrap, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if wrap:
                out.append(g % n)
            elif 0 <= g < n:
                out.append(g)
        return out

    def near(self, n, wrap, f):
        return {f, *self.side_files(n, wrap, f)}

    def pawn_passed(self, n, wrap, p, side, W, B):
        f, r = p
        nf = self.near(n, wrap, f)
        if side == "W":
            return not any(g in nf and s > r for g, s in B)
        return not any(g in nf and s < r for g, s in W)

    def any_passed(self, n, wrap, side, W, B):
        mine = W if side == "W" else B
        return any(self.pawn_passed(n, wrap, p, side, W, B) for p in mine)

    def dist(self, n, wrap, side, W, B):
        occ = W | B
        best = 10 ** 6
        mine = W if side == "W" else B
        for (f, r) in mine:
            if not self.pawn_passed(n, wrap, (f, r), side, W, B):
                continue
            if side == "W":
                if any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                    continue
                d = RANKS - r - (1 if r == 2 else 0)
            else:
                if any((f, s) in occ for s in range(1, r)):
                    continue
                d = r - 1 - (1 if r == RANKS - 1 else 0)
            best = min(best, d)
        return best

    def gen(self, n, wrap, W, B, ep, side):
        """Children (W, B, ep) after a move by side. ep=(target, captured, side_may_capture)."""
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        start = 2 if side == "W" else RANKS - 1
        other = "B" if side == "W" else "W"
        out = set()
        for p in mine:
            f, r = p
            rest = mine - {p}
            r1 = r + d
            if not (1 <= r1 <= RANKS):
                continue
            if (f, r1) not in occ:
                out.add(self._pack(side, rest | {(f, r1)}, theirs, None))
                r2 = r + 2 * d
                if r == start and (f, r2) not in occ:
                    e = ((f, r1), (f, r2), other) if self.ep else None
                    out.add(self._pack(side, rest | {(f, r2)}, theirs, e))
            for g in self.side_files(n, wrap, f):
                t = (g, r1)
                if t in theirs:
                    out.add(self._pack(side, rest | {t}, theirs - {t}, None))
                elif ep is not None and ep[2] == side and ep[0] == t:
                    out.add(self._pack(side, rest | {t}, theirs - {ep[1]}, None))
        return out

    @staticmethod
    def _pack(side, mine, theirs, e):
        if side == "W":
            return (frozenset(mine), frozenset(theirs), e)
        return (frozenset(theirs), frozenset(mine), e)

    def split(self, n, wrap, W, B, ep):
        occ = sorted({f for f, _ in W | B})
        if not occ:
            return []
        occs = set(occ)
        if wrap and len(occ) == n:
            return [(W, B, ep)]
        # runs of consecutive occupied files (cyclic on a cylinder)
        runs = []
        if wrap:
            # start just after an empty file
            e0 = next(f for f in range(n) if f not in occs)
            cur = []
            for k in range(1, n + 1):
                f = (e0 + k) % n
                if f in occs:
                    cur.append(f)
                elif cur:
                    runs.append(cur)
                    cur = []
            if cur:
                runs.append(cur)
        else:
            cur = []
            for f in range(n):
                if f in occs:
                    cur.append(f)
                elif cur:
                    runs.append(cur)
                    cur = []
            if cur:
                runs.append(cur)
        comps = []
        for run in runs:
            fs = set(run)
            e = ep if (ep is not None and ep[0][0] in fs) else None
            comps.append((frozenset(p for p in W if p[0] in fs), frozenset(p for p in B if p[0] in fs), e))
        return comps

    def whole(self, n, wrap, W, B, ep):
        wp = self.any_passed(n, wrap, "W", W, B)
        bp = self.any_passed(n, wrap, "B", W, B)
        if wp != bp:
            return number(BIG if wp else -BIG)
        comps = self.split(n, wrap, W, B, ep)
        if len(comps) > 1:
            g = number(0)
            for c in comps:
                g = add(g, self.comp(n, wrap, *c))
            return g
        return self.comp(n, wrap, W, B, ep)

    def comp(self, n, wrap, W, B, ep):
        key = (n, wrap, W, B, ep)
        r = self.memo.get(key)
        if r is not None:
            return r
        wp = self.any_passed(n, wrap, "W", W, B)
        bp = self.any_passed(n, wrap, "B", W, B)
        if wp and bp:
            raise RuntimeError("race at component root")
        if wp or bp:
            r = number(BIG if wp else -BIG)
        else:
            epL = ep if (ep is not None and ep[2] == "W") else None
            epR = ep if (ep is not None and ep[2] == "B") else None
            L = [self.child(n, wrap, c, "W") for c in self.gen(n, wrap, W, B, epL, "W")]
            R = [self.child(n, wrap, c, "B") for c in self.gen(n, wrap, W, B, epR, "B")]
            r = make(L, R)
        self.memo[key] = r
        return r

    def child(self, n, wrap, c, mover):
        W, B, ep = c
        if self.any_passed(n, wrap, "W", W, B) and self.any_passed(n, wrap, "B", W, B):
            self.races += 1
            other = "B" if mover == "W" else "W"
            if self.rule == "mover":
                win = mover
            elif self.rule == "opponent":
                win = other
            elif self.rule == "count":
                win = other if self.dist(n, wrap, other, W, B) <= self.dist(n, wrap, mover, W, B) else mover
            else:
                raise ValueError(self.rule)
            return number(BIG if win == "W" else -BIG)
        return self.whole(n, wrap, W, B, ep)


# ----------------------------------------------------------------------------- enumeration
def components_enum(n, wrap, tot, model, full_width=True):
    """All (raw, not symmetry-reduced) pawn sets on an n-file board, ranks 2..7, with
    tot pawns (>=1 of each colour), every file occupied (full_width), no passed pawn."""
    sqs = [(f, r) for f in range(n) for r in range(2, RANKS)]
    for w in range(1, tot):
        b = tot - w
        for Ws in itertools.combinations(sqs, w):
            W = frozenset(Ws)
            rest = [s for s in sqs if s not in W]
            for Bs in itertools.combinations(rest, b):
                B = frozenset(Bs)
                if full_width and len({f for f, _ in W | B}) != n:
                    continue
                if model.any_passed(n, wrap, "W", W, B) or model.any_passed(n, wrap, "B", W, B):
                    continue
                yield W, B


FILES = "abcdefgh"


def txt(W, B):
    return ("W: " + " ".join(f"{FILES[f]}{r}" for f, r in sorted(W)) +
            " / B: " + " ".join(f"{FILES[f]}{r}" for f, r in sorted(B)))


def parse(s):
    w, b = s.split("/")
    W = frozenset((FILES.index(t[0]), int(t[1:])) for t in w.split(":")[1].split())
    B = frozenset((FILES.index(t[0]), int(t[1:])) for t in b.split(":")[1].split())
    return W, B


def show(g) -> str:
    if g.num is not None:
        x = g.num
        s = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
        return s
    nv = nim_value(g)
    if nv is not None:
        return "*" if nv == 1 else f"*{nv}"
    if len(g.L) == 1 and len(g.R) == 1 and g.L[0].num is not None and g.R[0].num is not None:
        a, b = g.L[0].num, g.R[0].num
        m, d = (a + b) / 2, (a - b) / 2
        if a == b:
            return f"{show(g.L[0])}*"
        return (f"±{show(number(d))}" if m == 0 else f"{show(number(m))}±{show(number(d))}")
    return "{" + ", ".join(sorted(show(x) for x in g.L)) + " | " + ", ".join(sorted(show(x) for x in g.R)) + "}"


def run(rule, ep, outfile):
    t0 = time.time()
    m = Model(rule, ep)
    out = {"rule": rule, "ep": ep, "flat_single": {}, "flat_pair": {}, "ring3": {}, "ring4": {}}
    # flat single components, widths 1..4, 2..4 pawns, every file of the strip occupied
    two_pawn = []
    for w in range(1, 5):
        for tot in range(max(2, w), 5):
            for W, B in components_enum(w, False, tot, m):
                g = m.whole(w, False, W, B, None)
                k = vkey(g)
                out["flat_single"].setdefault(k, [txt(W, B), w, has_big(g), show(g)])
                if tot == 2:
                    two_pawn.append(g)
        print(f"flat width {w} done, {time.time()-t0:.0f}s", flush=True)
    # sums of two 2-pawn components (any two, with repetition)
    uniq = {}
    for g in two_pawn:
        uniq[g.id] = g
    U = list(uniq.values())
    for i in range(len(U)):
        for j in range(i, len(U)):
            g = add(U[i], U[j])
            k = vkey(g)
            out["flat_pair"].setdefault(k, [vkey(U[i]), vkey(U[j]), has_big(g), show(g)])
    print(f"flat pairs done ({len(U)} distinct 2-pawn values), {time.time()-t0:.0f}s", flush=True)
    for n, tots, name in ((3, (3, 4), "ring3"), (4, (4,), "ring4")):
        for tot in tots:
            for W, B in components_enum(n, True, tot, m):
                g = m.whole(n, True, W, B, None)
                k = vkey(g)
                out[name].setdefault(k, [txt(W, B), n, has_big(g), show(g)])
        print(f"{name} done, {time.time()-t0:.0f}s", flush=True)
    # headline positions
    heads = [("cyl", 4, "W: a2 c2 / B: b7 d7"), ("flat", 4, "W: a2 c2 / B: b7 d7"),
             ("cyl", 3, "W: a2 b4 / B: b7 c6"), ("cyl", 3, "W: a2 b3 / B: a5 c7"),
             ("cyl", 4, "W: a2 c2 / B: b6 d6"), ("cyl", 4, "W: a3 c3 / B: b7 d7"),
             ("cyl", 4, "W: a2 c3 / B: b7 d7"), ("cyl", 4, "W: a2 c2 / B: b6 d7")]
    out["heads"] = {}
    for kind, n, s in heads:
        W, B = parse(s)
        m.races = 0
        g = m.whole(n, kind == "cyl", W, B, None)
        out["heads"][f"{kind}{n} {s}"] = [vkey(g), show(g)]
    out["seconds"] = time.time() - t0
    with open(outfile, "w") as fh:
        json.dump(out, fh, ensure_ascii=False)
    print(f"wrote {outfile}, {time.time()-t0:.0f}s, nodes={len(_nodes)}", flush=True)


if __name__ == "__main__":
    rule, ep, outfile = sys.argv[1], sys.argv[2] == "1", sys.argv[3]
    threading.stack_size(1 << 29)
    th = threading.Thread(target=run, args=(rule, ep, outfile))
    th.start()
    th.join()
