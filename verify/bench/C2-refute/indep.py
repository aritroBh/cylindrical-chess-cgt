"""Independent check of claim C2 (verifier, REFUTE lens).

Self-contained: imports neither bench/ nor cylcgt/. Own pawn move generator,
own textbook and e.p.-aware passed tests, own race rules, own canonical-form
CGT (dominance + reversal + simplest-number), all written from the stated
conventions:

  * flat strip of w files x 8 ranks; White up, Black down; double steps from
    rank 2 / 7; diagonal captures; en passant (only as the holder's very next
    move in this component, FEN-style: the right is recorded only when an
    adjacent enemy pawn can actually take);
  * exactly one side has a passed pawn -> +-256; normal play otherwise;
  * both sides passed after a move = race: "mover" -> mover wins, "opponent"
    -> mover loses, "count" -> opponent moves first, fewer moves to promote
    wins, ties to the opponent (moves of the front passed pawn, minus one for
    a double step from the start rank);
  * textbook passed: no enemy pawn ahead on own/adjacent file;
    e.p.-aware: additionally, a pawn that may be taken e.p. right now is not
    passed (and is not counted in race distances).

Modes
  lib      : the 418 components of bench/data/components.jsonl
  control  : positive controls (KEY-FACT position, the 48 v1 components the
             worker lists as changing)
  full     : enumerate all candidates myself and run filters 1-5 and 5'

Usage (from the project root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I verify/bench/C2-refute/indep.py lib
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.setrecursionlimit(1_000_000)

ROOT = Path(__file__).resolve().parents[3]
BIG = 256
RANKS = 8
INF = 10 ** 6

# ----------------------------------------------------------------- own CGT
_ids = itertools.count()
_tab: dict = {}
_numtab: dict = {}
_le: dict = {}


class G:
    __slots__ = ("L", "R", "num", "id")

    def __repr__(self):
        return fmt(self)


def _new(L, R, num=None):
    g = G()
    g.L, g.R, g.num, g.id = tuple(L), tuple(R), num, next(_ids)
    return g


def _key(L, R):
    return (tuple(sorted(x.id for x in L)), tuple(sorted(x.id for x in R)))


def number(x) -> G:
    x = Fraction(x)
    g = _numtab.get(x)
    if g is not None:
        return g
    if x.denominator == 1:
        n = int(x)
        L, R = ((number(n - 1),), ()) if n > 0 else (((), (number(n + 1),)) if n < 0 else ((), ()))
    else:
        p, q = x.numerator, x.denominator
        L, R = (number(Fraction(p - 1, q)),), (number(Fraction(p + 1, q)),)
    g = _new(L, R, x)
    _numtab[x] = g
    _tab[_key(L, R)] = g
    return g


def le(a: G, b: G) -> bool:
    if a is b:
        return True
    if a.num is not None and b.num is not None:
        return a.num <= b.num
    k = (a.id, b.id)
    r = _le.get(k)
    if r is None:
        r = not any(le(b, al) for al in a.L) and not any(le(br, a) for br in b.R)
        _le[k] = r
    return r


def _dedupe(xs):
    seen, out = set(), []
    for x in xs:
        if x.id not in seen:
            seen.add(x.id)
            out.append(x)
    return out


def _simplest(lo, hi):
    if (lo is None or lo < 0) and (hi is None or hi > 0):
        return Fraction(0)
    if lo is not None and lo >= 0:
        n = (lo.numerator // lo.denominator) + 1
        if hi is None or n < hi:
            return Fraction(n)
    else:
        n = -((-hi.numerator) // hi.denominator) - 1   # ceil(hi) - 1
        if lo is None or n > lo:
            return Fraction(n)
    d = 1
    while True:
        d *= 2
        k = (lo * d).numerator // (lo * d).denominator + 1
        c = Fraction(k, d)
        if c < hi:
            return c


def make(L, R) -> G:
    L, R = _dedupe(L), _dedupe(R)
    while True:
        # dominated options (distinct canonical games are unequal, so <= is <)
        L = [x for x in L if not any(y is not x and le(x, y) for y in L)]
        R = [x for x in R if not any(y is not x and le(y, x) for y in R)]
        tmp = _new(L, R)
        changed = False
        nL = []
        for a in L:
            rv = next((ar for ar in a.R if le(ar, tmp)), None)
            if rv is None:
                nL.append(a)
            else:
                nL.extend(rv.L)
                changed = True
        nR = []
        for b in R:
            rv = next((bl for bl in b.L if le(tmp, bl)), None)
            if rv is None:
                nR.append(b)
            else:
                nR.extend(rv.R)
                changed = True
        L, R = _dedupe(nL), _dedupe(nR)
        if not changed:
            break
    if all(x.num is not None for x in L + R):
        lo = max((x.num for x in L), default=None)
        hi = min((x.num for x in R), default=None)
        if lo is None or hi is None or lo < hi:
            return number(_simplest(lo, hi))
    k = _key(L, R)
    g = _tab.get(k)
    if g is None:
        g = _new(L, R)
        _tab[k] = g
    return g


ZERO = number(0)
STAR = make([ZERO], [ZERO])


def star(n):
    opts = [ZERO] + [star(i) for i in range(1, n)]
    return make(opts, opts)


def has_big(g: G) -> bool:
    seen, st = set(), [g]
    while st:
        x = st.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        if x.num is not None:
            if abs(x.num) >= BIG // 2:
                return True
            continue
        st.extend(x.L + x.R)
    return False


def fmt(g: G) -> str:
    if g.num is not None:
        return str(g.num)
    for n in range(1, 5):
        if g is star(n):
            return "*" if n == 1 else f"*{n}"
    return "{" + ", ".join(map(fmt, g.L)) + " | " + ", ".join(map(fmt, g.R)) + "}"


# ------------------------------------------------------- own pawn semantics
def other(s):
    return "B" if s == "W" else "W"


def parse(text):
    wp, bp = text.split("/")
    f = lambda part: frozenset((ord(t[0]) - 97, int(t[1:])) for t in part.split(":")[1].split())
    return (f(wp), f(bp), None)


def ptext(st):
    nm = lambda s: f"{chr(97 + s[0])}{s[1]}"
    return "W: " + " ".join(sorted(map(nm, st[0]))) + " / B: " + " ".join(sorted(map(nm, st[1])))


def gen(w, st, side, ep_on):
    """States after one move of `side`. st = (White set, Black set, ep) with
    ep = (double-stepped pawn square, skipped square, holder) or None."""
    W, B, ep = st
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else RANKS - 1
    out = []

    def emit(m, t, e=None):
        out.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))

    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= RANKS:
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                e = None
                if ep_on and any((g, r2) in theirs for g in (f - 1, f + 1) if 0 <= g < w):
                    e = ((f, r2), (f, r1), other(side))
                emit(rest | {(f, r2)}, theirs, e)
        for g in (f - 1, f + 1):
            if not 0 <= g < w:
                continue
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif ep is not None and ep[2] == side and ep[1] == t:
                emit(rest | {t}, theirs - {ep[0]})
    return list(dict.fromkeys(out))


def passers(st, side, aware):
    W, B, ep = st
    mine, theirs = (W, B) if side == "W" else (B, W)
    res = []
    for (f, r) in mine:
        if side == "W":
            blocked = any(abs(g - f) <= 1 and s > r for g, s in theirs)
        else:
            blocked = any(abs(g - f) <= 1 and s < r for g, s in theirs)
        if blocked:
            continue
        if aware and ep is not None and ep[0] == (f, r) and ep[2] != side:
            continue  # may be taken e.p. right now
        res.append((f, r))
    return res


def dist(st, side, aware):
    occ = st[0] | st[1]
    best = INF
    for (f, r) in passers(st, side, aware):
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                continue
            dd = RANKS - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == RANKS - 1 else 0)
        best = min(best, dd)
    return best


def judge(st, aware):
    wp, bp = bool(passers(st, "W", aware)), bool(passers(st, "B", aware))
    d = (dist(st, "W", aware), dist(st, "B", aware)) if (wp and bp) else None
    return wp, bp, d


class Solver:
    def __init__(self, w, aware, rule, ep_on):
        self.w, self.aware, self.rule, self.ep_on = w, aware, rule, ep_on
        self.memo = {}

    def child(self, st, mover):
        wp, bp, d = judge(st, self.aware)
        if wp and bp:
            opp = other(mover)
            if self.rule == "mover":
                win = mover
            elif self.rule == "opponent":
                win = opp
            else:
                dm, do = (d[0], d[1]) if mover == "W" else (d[1], d[0])
                win = opp if do <= dm else mover
            return number(BIG if win == "W" else -BIG)
        return self.node(st)

    def node(self, st):
        g = self.memo.get(st)
        if g is not None:
            return g
        wp, bp, _ = judge(st, self.aware)
        if wp and bp:
            raise RuntimeError("race at a non-child node " + ptext(st))
        if wp:
            g = number(BIG)
        elif bp:
            g = number(-BIG)
        else:
            L = [self.child(c, "W") for c in gen(self.w, st, "W", self.ep_on)]
            R = [self.child(c, "B") for c in gen(self.w, st, "B", self.ep_on)]
            g = make(L, R)
        self.memo[st] = g
        return g

    def root_and_children(self, st):
        root = self.node(st)
        kids = {}
        for side in "WB":
            for c in gen(self.w, st, side, self.ep_on):
                kids[(side, c[0], c[1])] = self.child(c, side)
        return root, kids


def tree(w, st0, aware, ep_on=True):
    """All states reachable by any sequence of moves (either side) from the root,
    expansion stopped at states where some side has a passed pawn.
    Returns {state: judgement} plus statistics."""
    seen = {}
    stack = [st0]
    stats = {"nonterminal_ep_states": 0, "terminal_ep_states": 0,
             "terminal_ep_pawn_textbook_passed": 0, "race_states": 0}
    while stack:
        q = stack.pop()
        if q in seen:
            continue
        j = judge(q, aware)
        seen[q] = j
        if j[0] or j[1]:
            if j[0] and j[1]:
                stats["race_states"] += 1
            if q[2] is not None:
                stats["terminal_ep_states"] += 1
                side = other(q[2][2])
                if q[2][0] in passers((q[0], q[1], None), side, False):
                    stats["terminal_ep_pawn_textbook_passed"] += 1
            continue
        if q[2] is not None:
            stats["nonterminal_ep_states"] += 1  # an e.p. capture is playable here
        for side in "WB":
            stack.extend(gen(w, q, side, ep_on))
    return seen, stats


SETTINGS = [(aware, rule, ep) for aware in (False, True) for rule in ("count", "mover", "opponent") for ep in (True, False)]


def sname(s):
    return f"{'aware' if s[0] else 'textbook'}/{s[1]}/ep-{'on' if s[2] else 'off'}"


def evaluate(items):
    """items: [(w, state)] -> {setting: [(root, kids)]}"""
    out = {}
    for s in SETTINGS:
        solvers = {}
        res = []
        for w, st in items:
            sv = solvers.setdefault(w, Solver(w, *s))
            res.append(sv.root_and_children(st))
        out[s] = res
    return out


def same_all(ev, i):
    vals = [ev[s][i] for s in SETTINGS]
    r0, k0 = vals[0]
    for r, k in vals[1:]:
        if r is not r0 or k.keys() != k0.keys() or any(k[x] is not k0[x] for x in k0):
            return False
    return True


def run_lib():
    t0 = time.time()
    rows = [json.loads(x) for x in (ROOT / "bench/data/components.jsonl").read_text().splitlines()]
    items = [(r["width"], parse(r["position"])) for r in rows]
    res = {"components": len(items)}
    # 1. trees under the two tests (e.p. on): identical judgement maps?
    tree_diff, nt_ep, term_ep, term_ep_passed, races, nodes = [], 0, 0, 0, 0, 0
    with_race = 0
    for (w, st), r in zip(items, rows):
        a, sa = tree(w, st, False)
        b, sb = tree(w, st, True)
        nodes += len(a)
        if a != b:
            tree_diff.append(r["position"])
        nt_ep += sa["nonterminal_ep_states"] > 0
        term_ep += sa["terminal_ep_states"] > 0
        term_ep_passed += sa["terminal_ep_pawn_textbook_passed"] > 0
        races += sa["race_states"]
        with_race += sa["race_states"] > 0
    res["tree nodes (textbook, e.p. on), total"] = nodes
    res["components whose e.p.-on tree differs between tests"] = len(tree_diff)
    res["tree differs (positions)"] = tree_diff[:20]
    res["components with an e.p. capture playable at a non-terminal node"] = nt_ep
    res["components with an e.p. right at some terminal node"] = term_ep
    res["components with a textbook-passed e.p.-capturable pawn at a terminal node"] = term_ep_passed
    res["race states, total"] = races
    res["components whose tree contains a race state"] = with_race
    # e.p.-off trees vs e.p.-on trees (modulo ep flags)
    off_diff = 0
    for w, st in items:
        a, _ = tree(w, st, False, True)
        c, _ = tree(w, st, False, False)
        strip = {(q[0], q[1]) for q in a}
        if strip != {(q[0], q[1]) for q in c}:
            off_diff += 1
    res["components whose e.p.-off tree has different positions from the e.p.-on tree"] = off_diff
    print(f"trees done [{time.time() - t0:.0f}s]", flush=True)
    # 2. values in 12 settings
    ev = evaluate(items)
    bad = [rows[i]["position"] for i in range(len(items)) if not same_all(ev, i)]
    res["components with root or some child differing across the 12 settings"] = len(bad)
    res["differing (positions)"] = bad[:20]
    res["root values with +-BIG inside"] = sum(has_big(ev[SETTINGS[0]][i][0]) for i in range(len(items)))
    # 3. outcome vs the stored outcome
    def outcome(g):
        ge0, le0 = le(ZERO, g), le(g, ZERO)
        return "P" if ge0 and le0 else "L" if ge0 else "R" if le0 else "N"
    mism = [r["position"] for i, r in enumerate(rows) if outcome(ev[SETTINGS[0]][i][0]) != r["outcome"]]
    res["root outcome mismatches vs components.jsonl"] = len(mism)
    res["root outcome mismatches (positions)"] = mism[:20]
    # stored child count vs mine
    kid_count_mism = sum(len(ev[SETTINGS[0]][i][1]) != len(r["moves"]) for i, r in enumerate(rows))
    res["child-count mismatches vs components.jsonl"] = kid_count_mism
    res["values (textbook/count/ep-on), distinct"] = len({ev[SETTINGS[0]][i][0].id for i in range(len(items))})
    res["seconds"] = round(time.time() - t0, 1)
    # dump my values for the cylcgt cross-check
    dump = []
    for i, r in enumerate(rows):
        root, kids = ev[SETTINGS[0]][i]
        dump.append({"position": r["position"], "width": r["width"], "root": fmt(root),
                     "kids": {f"{k[0]} {ptext((k[1], k[2], None))}": fmt(v) for k, v in kids.items()}})
    out = Path(__file__).with_name("lib_values.json")
    out.write_text(json.dumps(dump, indent=0) + "\n")
    return res


def run_control():
    t0 = time.time()
    res = {}
    # KEY-FACT
    kf = parse("W: a2 c2 / B: b7 d7")
    pm = lambda a, b: make([number(a)], [number(b)])
    expect_aware = make([pm(3, 1)], [pm(-1, -3)])
    kv = {}
    for s in SETTINGS:
        g = Solver(4, *s).node(kf)
        kv[sname(s)] = fmt(g) if g not in (star(2), expect_aware) else ("*2" if g is star(2) else "{2+-1 | -2+-1}")
    res["KEY-FACT W a2 c2 / B b7 d7 (4 flat files)"] = kv
    # the 48 components the worker lists as changing
    summ = json.loads((ROOT / "bench/results/conventions_summary.json").read_text())
    ch = summ["v1_changed"]
    det_tree, det_val, details = 0, 0, []
    for r in ch:
        st = parse(r["position"])
        w = max(f for f, _ in st[0] | st[1]) + 1
        a, _ = tree(w, st, False)
        b, _ = tree(w, st, True)
        det_tree += a != b
        tb = Solver(w, False, "count", True).root_and_children(st)
        aw = Solver(w, True, "count", True).root_and_children(st)
        diff = tb[0] is not aw[0] or any(tb[1][k] is not aw[1][k] for k in tb[1])
        det_val += diff
        details.append((r["position"], fmt(tb[0]), fmt(aw[0]), r["textbook"], r["aware"]))
    res["worker-listed changing v1 components"] = len(ch)
    res["... my trees differ"] = det_tree
    res["... my values differ (count, e.p. on)"] = det_val
    res["examples (mine textbook, mine aware, worker textbook, worker aware)"] = details[:6]
    res["seconds"] = round(time.time() - t0, 1)
    return res


def candidates():
    out = []
    for w in range(1, 5):
        sqs = [(f, r) for f in range(w) for r in range(2, RANKS)]
        for n in range(max(2, w), 5):
            for S in itertools.combinations(sqs, n):
                if len({f for f, _ in S}) != w:
                    continue
                for cols in itertools.product("WB", repeat=n):
                    if "W" not in cols or "B" not in cols:
                        continue
                    st = (frozenset(s for s, c in zip(S, cols) if c == "W"),
                          frozenset(s for s, c in zip(S, cols) if c == "B"), None)
                    if passers(st, "W", False) or passers(st, "B", False):
                        continue
                    out.append((w, st))
    return out


def run_full():
    """Own enumeration + own filters 1-5 and 5' (textbook test), and the same
    filters 1-5 under the e.p.-aware test."""
    t0 = time.time()
    cands = candidates()
    print(f"{len(cands)} candidates", flush=True)
    ev = evaluate(cands)
    print(f"values done [{time.time() - t0:.0f}s]", flush=True)

    def f1to4(i, aware):
        keys = [s for s in SETTINGS if s[0] == aware]
        r0, k0 = ev[keys[0]][i]
        for s in keys[1:]:
            r, k = ev[s][i]
            if r is not r0 or any(k[x] is not k0[x] for x in k0):
                return False
        return not has_big(r0)

    def f5(w, st, aware):
        _, s = tree(w, st, aware)
        return s["nonterminal_ep_states"] == 0

    def f5p(w, st):
        _, s = tree(w, st, False)
        return s["terminal_ep_pawn_textbook_passed"] == 0

    v1, v2, aw, diffs = [], [], [], 0
    for i, (w, st) in enumerate(cands):
        if f1to4(i, False) and f5(w, st, False):
            v1.append(i)
            if f5p(w, st):
                v2.append(i)
        if f1to4(i, True) and f5(w, st, True):
            aw.append(i)
    lib = {(r["width"], frozenset(parse(r["position"])[:2])) for r in
           (json.loads(x) for x in (ROOT / "bench/data/components.jsonl").read_text().splitlines())}
    mine = {(cands[i][0], frozenset(cands[i][1][:2])) for i in v2}
    # the textbook and aware trees of every v1 component
    v1_tree_diff = sum(tree(*cands[i], False)[0] != tree(*cands[i], True)[0] for i in v1)
    v1_val_diff = sum(any(ev[(False, r, e)][i][0] is not ev[(True, r, e)][i][0] or
                          any(ev[(False, r, e)][i][1][k] is not ev[(True, r, e)][i][1][k] for k in ev[(False, r, e)][i][1])
                          for r in ("count", "mover", "opponent") for e in (True, False)) for i in v1)
    res = {
        "candidates": len(cands),
        "my v1 (filters 1-5, textbook)": len(v1),
        "my v2 (v1 + filter 5')": len(v2),
        "my filters 1-5 under the e.p.-aware test": len(aw),
        "intersection v1 & aware": len(set(v1) & set(aw)),
        "my v2 equals bench/data/components.jsonl as a set": mine == lib,
        "in mine not in bench": len(mine - lib),
        "in bench not in mine": len(lib - mine),
        "my v1 components whose tree differs between tests": v1_tree_diff,
        "my v1 components with a root/child value differing between tests (any rule/e.p.)": v1_val_diff,
        "seconds": round(time.time() - t0, 1),
    }
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "lib"
    r = {"lib": run_lib, "control": run_control, "full": run_full}[mode]()
    txt = json.dumps(r, indent=1, default=str)
    Path(__file__).with_name(f"result_{mode}.json").write_text(txt + "\n")
    print(txt)
