"""Independent re-computation for claim C1 (adversarial verifier, lens REFUTE).

Written from scratch: it does NOT import cylcgt or bench. It re-implements
  * a canonical-form short-game CGT engine (dominated / reversible options,
    hash-consing, number recognition, sums via the number-translation rule),
  * the pawn-only model on a flat w-file x 8-rank strip as specified in the
    task text / cylcgt docstrings: normal play, a lone passer = +-BIG (256),
    both passers after a move = race resolved by RACE_RULE, e.p. right usable
    only as the opponent's very next move in the component, components split
    at empty files,
  * the two passed-pawn tests: "textbook" and "e.p.-aware" (a pawn that has
    just double-stepped and can be taken e.p. right now is not passed, and is
    skipped by the race promotion distance),
  * the v1 library filters 1-5 (components.py docstring), to rebuild v1,
  * then the comparison claimed in C1.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I verify/bench/C1-refute/indep.py
"""
import itertools
import json
import math
import sys
import threading
import time
from fractions import Fraction

sys.setrecursionlimit(10 ** 7)

# ---------------------------------------------------------------- CGT engine
_next = itertools.count(1)
TABLE = {}
LE = {}
ADD = {}
NUMS = {}


class G:
    __slots__ = ("L", "R", "id", "num")

    def __init__(self, L, R, num=None, gid=None):
        self.L = tuple(L)
        self.R = tuple(R)
        self.num = num
        self.id = next(_next) if gid is None else gid


def le(a, b):
    if a is b:
        return True
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    k = (a.id, b.id)
    r = LE.get(k)
    if r is None:
        r = (not any(le(b, x) for x in a.L)) and (not any(le(y, a) for y in b.R))
        LE[k] = r
    return r


def simplest_between(lo, hi):
    """simplest number x with lo < x < hi (lo/hi may be None = -inf/+inf)."""
    if lo is None and hi is None:
        return Fraction(0)
    if lo is None:
        return Fraction(math.ceil(hi) - 1) if hi <= 0 else Fraction(0)
    if hi is None:
        return Fraction(math.floor(lo) + 1) if lo >= 0 else Fraction(0)
    if lo < 0 < hi:
        return Fraction(0)
    # integers strictly between
    a = math.floor(lo) + 1
    b = math.ceil(hi) - 1
    if a <= b:
        if a > 0:
            return Fraction(a)
        return Fraction(b)  # both <= 0 -> closest to 0 is b
    q = 1
    while True:
        den = 2 ** q
        k = math.floor(lo * den) + 1
        if Fraction(k, den) < hi:
            return Fraction(k, den)
        q += 1


def intern(Ls, Rs):
    key = (frozenset(g.id for g in Ls), frozenset(g.id for g in Rs))
    g = TABLE.get(key)
    if g is not None:
        return g
    num = None
    if all(x.num is not None for x in Ls) and all(x.num is not None for x in Rs):
        lo = max((x.num for x in Ls), default=None)
        hi = min((x.num for x in Rs), default=None)
        if lo is None or hi is None or lo < hi:
            num = simplest_between(lo, hi)
    g = G(sorted(Ls, key=lambda x: x.id), sorted(Rs, key=lambda x: x.id), num)
    TABLE[key] = g
    return g


def undom_left(S):
    S = list(dict.fromkeys(S))
    return [a for a in S if not any(b is not a and le(a, b) for b in S)]


def undom_right(S):
    S = list(dict.fromkeys(S))
    return [a for a in S if not any(b is not a and le(b, a) for b in S)]


def make(Ls, Rs):
    Ls = undom_left(Ls)
    Rs = undom_right(Rs)
    g0 = G(Ls, Rs)  # temporary form, same value; never interned
    while True:
        changed = False
        nL = []
        for a in Ls:
            rev = next((ar for ar in a.R if le(ar, g0)), None)
            if rev is None:
                nL.append(a)
            else:
                nL.extend(rev.L)
                changed = True
        nR = []
        for b in Rs:
            rev = next((bl for bl in b.L if le(g0, bl)), None)
            if rev is None:
                nR.append(b)
            else:
                nR.extend(rev.R)
                changed = True
        Ls, Rs = undom_left(nL), undom_right(nR)
        if not changed:
            break
    return intern(Ls, Rs)


ZERO = intern([], [])


def number(q):
    q = Fraction(q)
    g = NUMS.get(q)
    if g is not None:
        return g
    if q.denominator == 1:
        n = int(q)
        if n == 0:
            g = ZERO
        elif n > 0:
            g = make([number(n - 1)], [])
        else:
            g = make([], [number(n + 1)])
    else:
        e = Fraction(1, q.denominator)
        g = make([number(q - e)], [number(q + e)])
    assert g.num == q, (q, g.num)
    NUMS[q] = g
    return g


def add(a, b):
    if a.num is not None and b.num is not None:
        return number(a.num + b.num)
    if a is ZERO:
        return b
    if b is ZERO:
        return a
    k = (a.id, b.id) if a.id < b.id else (b.id, a.id)
    r = ADD.get(k)
    if r is not None:
        return r
    if b.num is not None:      # number translation: a not a number
        r = make([add(x, b) for x in a.L], [add(x, b) for x in a.R])
    elif a.num is not None:
        r = make([add(a, x) for x in b.L], [add(a, x) for x in b.R])
    else:
        r = make([add(x, b) for x in a.L] + [add(a, y) for y in b.L],
                 [add(x, b) for x in a.R] + [add(a, y) for y in b.R])
    ADD[k] = r
    return r


STAR = make([ZERO], [ZERO])
UP = make([ZERO], [STAR])
DOWN = make([STAR], [ZERO])


def show(g, depth=0):
    if g.num is not None:
        q = g.num
        return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"
    if g is STAR:
        return "*"
    if g is UP:
        return "^"
    if g is DOWN:
        return "v"
    # x* : {x | x}
    if len(g.L) == 1 and len(g.R) == 1 and g.L[0] is g.R[0] and g.L[0].num is not None:
        return show(g.L[0]) + "*"
    return "{" + ", ".join(show(x) for x in g.L) + " | " + ", ".join(show(x) for x in g.R) + "}"


def has_big(g, big=128):
    seen, st = set(), [g]
    while st:
        x = st.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        if x.num is not None:
            if abs(x.num) >= big:
                return True
            continue
        st.extend(x.L)
        st.extend(x.R)
    return False


# --------------------------------------------------------------- pawn model
RANKS = 8
BIG = 256


class Model:
    def __init__(self, w, ep_on, aware, rule):
        self.w, self.ep_on, self.aware, self.rule = w, ep_on, aware, rule
        self.memo = {}
        self.BIGP = number(BIG)
        self.BIGN = number(-BIG)

    # pos = (white frozenset, black frozenset, ep) ; ep = (target, victim_sq, capturer) or None
    def adj(self, f):
        return [g for g in (f - 1, f + 1) if 0 <= g < self.w]

    def ep_capturable(self, pos, side, sq):
        if not self.aware:
            return False
        W, B, ep = pos
        if ep is None or ep[1] != sq or ep[2] == side:
            return False
        f, r = sq
        theirs = B if side == "W" else W
        return any((g, r) in theirs for g in self.adj(f))

    def pawn_free(self, sq, side, theirs):
        f, r = sq
        files = {f, *self.adj(f)}
        if side == "W":
            return not any(g in files and s > r for g, s in theirs)
        return not any(g in files and s < r for g, s in theirs)

    def passed(self, pos, side):
        W, B, _ = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        for sq in mine:
            if self.pawn_free(sq, side, theirs) and not self.ep_capturable(pos, side, sq):
                return True
        return False

    def pdist(self, pos, side):
        W, B, _ = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        best = None
        for (f, r) in mine:
            if self.ep_capturable(pos, side, (f, r)):
                continue
            if not self.pawn_free((f, r), side, theirs):
                continue
            if side == "W":
                if any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                    continue
                d = RANKS - r - (1 if r == 2 else 0)
            else:
                if any((f, s) in occ for s in range(1, r)):
                    continue
                d = r - 1 - (1 if r == RANKS - 1 else 0)
            best = d if best is None else min(best, d)
        return 10 ** 6 if best is None else best

    def moves(self, pos, side):
        W, B, ep = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        start = 2 if side == "W" else RANKS - 1
        other = "B" if side == "W" else "W"
        ept = ep if (ep is not None and ep[2] == side) else None
        out = set()

        def emit(m, t, e=None):
            m, t = frozenset(m), frozenset(t)
            out.add((m, t, e) if side == "W" else (t, m, e))

        for (f, r) in mine:
            rest = mine - {(f, r)}
            r1 = r + d
            if not 1 <= r1 <= RANKS:
                continue
            if (f, r1) not in occ:
                emit(rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == start and 1 <= r2 <= RANKS and (f, r2) not in occ:
                    emit(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if self.ep_on else None)
            for g in self.adj(f):
                t = (g, r1)
                if t in theirs:
                    emit(rest | {t}, theirs - {t})
                elif ept is not None and ept[0] == t:
                    emit(rest | {t}, theirs - {ept[1]})
        return out

    def comps(self, pos):
        W, B, ep = pos
        files = sorted({f for f, _ in W | B})
        groups = []
        for f in files:
            if groups and f == groups[-1][-1] + 1:
                groups[-1].append(f)
            else:
                groups.append([f])
        out = []
        for gr in groups:
            fs = set(gr)
            e = ep if (ep is not None and ep[0][0] in fs) else None
            out.append((frozenset(p for p in W if p[0] in fs), frozenset(p for p in B if p[0] in fs), e))
        return out

    def value(self, pos):
        wp, bp = self.passed(pos, "W"), self.passed(pos, "B")
        if wp != bp:
            return self.BIGP if wp else self.BIGN
        cs = self.comps(pos)
        if len(cs) > 1:
            t = ZERO
            for c in cs:
                t = add(t, self._value(c))
            return t
        return self._value(pos)

    def _value(self, pos):
        r = self.memo.get(pos)
        if r is not None:
            return r
        wp, bp = self.passed(pos, "W"), self.passed(pos, "B")
        if wp and bp:
            raise RuntimeError("race at node " + str(pos))
        if wp:
            r = self.BIGP
        elif bp:
            r = self.BIGN
        else:
            W, B, ep = pos
            plain = (W, B, None)
            lpos = plain if (ep is not None and ep[2] != "W") else pos
            rpos = plain if (ep is not None and ep[2] != "B") else pos
            L = [self.child(c, "W") for c in self.moves(lpos, "W")]
            R = [self.child(c, "B") for c in self.moves(rpos, "B")]
            r = make(L, R)
        self.memo[pos] = r
        return r

    def child(self, pos, mover):
        if self.passed(pos, "W") and self.passed(pos, "B"):
            other = "B" if mover == "W" else "W"
            if self.rule == "mover":
                win = mover
            elif self.rule == "opponent":
                win = other
            else:
                win = other if self.pdist(pos, other) <= self.pdist(pos, mover) else mover
            return self.BIGP if win == "W" else self.BIGN
        return self.value(pos)


# ------------------------------------------------------------ candidates
def tb_passed(w, pos, side):
    return Model(w, True, False, "count").passed(pos, side)


def candidates():
    out = []
    for w in range(1, 5):
        sqs = [(f, r) for f in range(w) for r in range(2, RANKS)]
        m = Model(w, True, False, "count")
        for n in range(max(2, w), 5):
            for S in itertools.combinations(sqs, n):
                if len({f for f, _ in S}) != w:
                    continue
                for cols in itertools.product("WB", repeat=n):
                    if "W" not in cols or "B" not in cols:
                        continue
                    W = frozenset(s for s, c in zip(S, cols) if c == "W")
                    B = frozenset(s for s, c in zip(S, cols) if c == "B")
                    p = (W, B, None)
                    if m.passed(p, "W") or m.passed(p, "B"):
                        continue
                    out.append((w, p))
    return out


def ep_ever_available(w, p):
    """filter 5: in the textbook tree (both sides move freely, not expanded below
    a position where some side has a textbook passer), is an e.p. capture ever
    available?"""
    m = Model(w, True, False, "count")
    seen, st = set(), [p]
    while st:
        q = st.pop()
        if q in seen:
            continue
        seen.add(q)
        if m.passed(q, "W") or m.passed(q, "B"):
            continue
        W, B, ep = q
        if ep is not None:
            side = ep[2]
            if m.moves(q, side) != m.moves((W, B, None), side):
                return True
        for side in "WB":
            st.extend(m.moves(q, side))
    return False


def ptext(p):
    F = "abcdefgh"
    W, B, _ = p
    return "W: " + " ".join(sorted(F[f] + str(r) for f, r in W)) + " / B: " + " ".join(sorted(F[f] + str(r) for f, r in B))


RULES = ("count", "mover", "opponent")
EPS = (True, False)


def evaluate(w, p, aware, rule, ep, models):
    key = (w, aware, rule, ep)
    m = models.get(key)
    if m is None:
        m = models[key] = Model(w, ep, aware, rule)
    root = m.value(p)
    kids = {}
    for side in "WB":
        for c in m.moves(p, side):
            kids[(side, c[0], c[1])] = m.child(c, side)
    return root, kids


def main():
    t0 = time.time()
    cands = candidates()
    print("candidates", len(cands), flush=True)
    models = {}
    TB = {}
    for rule in RULES:
        for ep in EPS:
            for w, p in cands:
                TB[(w, p, rule, ep)] = evaluate(w, p, False, rule, ep, models)
            print(f"textbook {rule} ep={ep} done [{time.time()-t0:.0f}s]", flush=True)
    v1 = []
    drops = {}
    for w, p in cands:
        rs = [TB[(w, p, r, e)] for r in RULES for e in EPS]
        g = rs[0][0]
        reason = None
        if not all(x[0] is g for x in rs):
            reason = "root varies"
        elif has_big(g):
            reason = "big"
        elif not all(x[1].keys() == rs[0][1].keys() and all(x[1][k] is rs[0][1][k] for k in x[1]) for x in rs):
            reason = "child varies"
        elif ep_ever_available(w, p):
            reason = "ep available"
        if reason:
            drops[reason] = drops.get(reason, 0) + 1
        else:
            v1.append((w, p))
    print("drops", drops, "v1", len(v1), f"[{time.time()-t0:.0f}s]", flush=True)
    v1.sort(key=lambda t: (t[0], len(t[1][0]) + len(t[1][1]), ptext(t[1])))
    AW = {}
    for rule in RULES:
        for ep in EPS:
            for w, p in v1:
                AW[(w, p, rule, ep)] = evaluate(w, p, True, rule, ep, models)
            print(f"aware {rule} ep={ep} done [{time.time()-t0:.0f}s]", flush=True)
    rows = []
    halves = []
    setting_counts = {}
    for n, (w, p) in enumerate(v1):
        tbv = TB[(w, p, "count", True)][0]
        if tbv.num is not None and abs(tbv.num) == Fraction(1, 2) or show(tbv) in ("1/2*", "-1/2*"):
            halves.append(ptext(p))
        per = {}
        for rule in RULES:
            for ep in EPS:
                a, b = TB[(w, p, rule, ep)], AW[(w, p, rule, ep)]
                rootd = a[0] is not b[0]
                kidd = [k for k in a[1] if a[1][k] is not b[1][k]]
                assert a[1].keys() == b[1].keys()
                per[(rule, ep)] = (rootd, kidd, show(a[0]), show(b[0]))
                if rootd or kidd:
                    s = setting_counts.setdefault(f"{rule},ep={ep}", [0, 0])
                    s[0] += 1
                    s[1] += rootd
        if any(v[0] or v[1] for v in per.values()):
            rows.append({"idx": f"C{n:04d}", "pos": ptext(p),
                         "per_setting": {f"{r},ep={e}": {"root_changes": v[0], "n_children_change": len(v[1]),
                                                          "tb": v[2], "aw": v[3]} for (r, e), v in per.items()}})
    print("v1 size", len(v1))
    print("v1 components changing (any setting, root or child):", len(rows))
    print("per setting [components changed, of which root changes]:", setting_counts)
    print("root changes under count, e.p. on:", sum(r["per_setting"]["count,ep=True"]["root_changes"] for r in rows))
    print("root changes under any setting:", sum(any(v["root_changes"] for v in r["per_setting"].values()) for r in rows))
    print("halves in v1:", len(halves))
    changed_pos = {r["pos"] for r in rows}
    print("halves all among changed:", all(h in changed_pos for h in halves), [h for h in halves if h not in changed_pos])
    from collections import Counter
    vc = Counter(show(TB[(w, p, "count", True)][0]) for w, p in v1)
    print("v1 values:", sorted(vc.items(), key=lambda kv: -kv[1]))
    nonint = {k: v for k, v in vc.items() if "/" in k and "{" not in k}
    print("v1 non-integer-number(ish) values:", nonint)
    json.dump({"v1": [ptext(p) for _, p in v1], "changed": rows, "halves": halves,
               "setting_counts": setting_counts, "values": vc},
              open(__file__.replace("indep.py", "indep_out.json"), "w"), indent=1)
    print(f"done [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main)
    t.start()
    t.join()
