"""Independent re-implementation (verifier C1) of the pawn-component model used by
bench/conventions.py, written from the documented conventions only; it does NOT
import cylcgt.pawns or bench.components. Canonical forms still come from
cylcgt.cgt (shared engine), printing from bench.cgtfmt (display only).

Model (same as cylcgt.pawns, as documented):
  - flat strip of w files, 8 ranks; White = Left moves up, Black = Right moves down;
  - exactly one side passed -> +-BIG; both passed after a move -> race rule;
  - groups separated by an empty file are summed (passed test on the whole first);
  - an e.p. right lives in the component of its target file and is dropped for
    the moves of the side that does not hold it (per-component approximation);
  - passed test "textbook" or "aware" (a pawn the opponent can take e.p. right
    now is not passed; it is also skipped in the race promotion distance).

Usage (from the project root):
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python verify/bench/C1-reproduce/indep.py
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

from cylcgt import cgt
from bench import cgtfmt

BIG = 256
RANKS = 8
HERE = Path(__file__).resolve().parent
PROJ = HERE.parents[2]

# global settings (cache keyed on them explicitly)
class S:
    aware = False
    rule = "count"


def fname(f):
    return "abcdefgh"[f]


def ptxt(W, B):
    w = " ".join(sorted(f"{fname(f)}{r}" for f, r in W))
    b = " ".join(sorted(f"{fname(f)}{r}" for f, r in B))
    return f"W: {w} / B: {b}"


def parse(t):
    a, b = t.split("/")
    sq = lambda s: ("abcdefgh".index(s[0]), int(s[1:]))
    return frozenset(map(sq, a.split(":")[1].split())), frozenset(map(sq, b.split(":")[1].split()))


def adj(w, f):
    return [g for g in (f - 1, f + 1) if 0 <= g < w]


def capturable_ep(w, W, B, ep, white_pawn, sq):
    """Is the pawn on sq (white if white_pawn) takeable e.p. right now?"""
    if ep is None:
        return False
    target, captured, capturer_white = ep
    if captured != sq or capturer_white == white_pawn:
        return False
    f, r = sq
    them = B if white_pawn else W
    return any((g, r) in them for g in adj(w, f))


def pawn_passed(w, W, B, ep, white_pawn, sq, aware):
    f, r = sq
    them = B if white_pawn else W
    files = {f, *adj(w, f)}
    for g, s in them:
        if g in files and ((s > r) if white_pawn else (s < r)):
            return False
    if aware and capturable_ep(w, W, B, ep, white_pawn, sq):
        return False
    return True


def side_passed(w, W, B, ep, white, aware):
    return any(pawn_passed(w, W, B, ep, white, sq, aware) for sq in (W if white else B))


def dist(w, W, B, ep, white, aware):
    occ = W | B
    best = 10 ** 6
    for f, r in (W if white else B):
        if not pawn_passed(w, W, B, ep, white, (f, r), aware):
            continue
        if white:
            if any((f, s) in occ for s in range(r + 1, RANKS + 1)):
                continue
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        best = min(best, d)
    return best


def gen(w, W, B, ep, white, ep_on):
    """children (W', B', ep') of `white` moving; ep is used only if held by mover."""
    mine, them = (W, B) if white else (B, W)
    occ = W | B
    d = 1 if white else -1
    start = 2 if white else RANKS - 1
    mine_ep = ep if (ep is not None and ep[2] == white) else None
    out = []

    def put(nm, nt, e=None):
        out.append((nm, nt, e) if white else (nt, nm, e))

    for f, r in sorted(mine):
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= RANKS:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, them)
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                put(rest | {(f, r2)}, them, ((f, r1), (f, r2), not white) if ep_on else None)
        for g in adj(w, f):
            t = (g, r1)
            if t in them:
                put(rest | {t}, them - {t})
            elif mine_ep is not None and mine_ep[0] == t:
                put(rest | {t}, them - {mine_ep[1]})
    res = []
    for x in out:
        x = (frozenset(x[0]), frozenset(x[1]), x[2])
        if x not in res:
            res.append(x)
    return res


class Race(Exception):
    pass


def split(W, B, ep):
    files = sorted({f for f, _ in W | B})
    groups = []
    for f in files:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    out = []
    for g in groups:
        gs = set(g)
        e = ep if (ep is not None and ep[0][0] in gs) else None
        out.append((frozenset(p for p in W if p[0] in gs), frozenset(p for p in B if p[0] in gs), e))
    return out


@lru_cache(maxsize=None)
def val(w, W, B, ep, ep_on, aware, rule):
    wp = side_passed(w, W, B, ep, True, aware)
    bp = side_passed(w, W, B, ep, False, aware)
    if wp != bp:
        return cgt.integer(BIG if wp else -BIG)
    if wp and bp:
        raise Race()
    parts = split(W, B, ep)
    if len(parts) > 1:
        return cgt.total(val(w, *p, ep_on, aware, rule) for p in parts)
    L = [child(w, c, True, ep_on, aware, rule) for c in gen(w, W, B, ep if (ep and ep[2]) else None, True, ep_on)]
    R = [child(w, c, False, ep_on, aware, rule) for c in gen(w, W, B, ep if (ep and not ep[2]) else None, False, ep_on)]
    return cgt.make(L, R)


def child(w, c, mover_white, ep_on, aware, rule):
    W, B, ep = c
    if side_passed(w, W, B, ep, True, aware) and side_passed(w, W, B, ep, False, aware):
        if rule == "mover":
            win_white = mover_white
        elif rule == "opponent":
            win_white = not mover_white
        else:
            do = dist(w, W, B, ep, not mover_white, aware)
            dm = dist(w, W, B, ep, mover_white, aware)
            win_white = (not mover_white) if do <= dm else mover_white
        return cgt.integer(BIG if win_white else -BIG)
    return val(w, W, B, ep, ep_on, aware, rule)


def candidates():
    out = []
    for w in range(1, 5):
        sqs = [(f, r) for f in range(w) for r in range(2, RANKS)]
        for n in range(max(2, w), 5):
            for Sq in itertools.combinations(sqs, n):
                if len({f for f, _ in Sq}) != w:
                    continue
                for cols in itertools.product((True, False), repeat=n):
                    if all(cols) or not any(cols):
                        continue
                    W = frozenset(s for s, c in zip(Sq, cols) if c)
                    B = frozenset(s for s, c in zip(Sq, cols) if not c)
                    if side_passed(w, W, B, None, True, False) or side_passed(w, W, B, None, False, False):
                        continue
                    out.append((w, W, B))
    return out


def has_big(g):
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


def kids(w, W, B, ep_on):
    return [(m, c) for m in (True, False) for c in gen(w, W, B, None, m, ep_on)]


def evaluate(w, W, B, ep_on, aware, rule):
    try:
        g = val(w, W, B, None, ep_on, aware, rule)
    except Race:
        g = None
    ks = []
    for m, c in kids(w, W, B, ep_on):
        try:
            ks.append(child(w, c, m, ep_on, aware, rule))
        except Race:
            ks.append(None)
    return g, tuple(ks)


def ep_capture_in_tree(w, W, B, aware):
    """filter 5 (textbook) : any e.p. capture available in the tree not expanded below passer positions."""
    seen, st = set(), [(W, B, None)]
    while st:
        q = st.pop()
        if q in seen:
            continue
        seen.add(q)
        qW, qB, e = q
        if side_passed(w, qW, qB, e, True, aware) or side_passed(w, qW, qB, e, False, aware):
            continue
        if e is not None:
            holder = e[2]
            with_ep = set(gen(w, qW, qB, e, holder, True))
            without = set(gen(w, qW, qB, None, holder, True))
            if with_ep != without:
                return True
        for m in (True, False):
            st.extend(gen(w, qW, qB, e, m, True))
    return False


RULES = ("count", "mover", "opponent")
EPS = (True, False)


def main():
    t0 = time.time()
    cands = candidates()
    print("candidates", len(cands), flush=True)
    ev = {}
    for aware in (False, True):
        for rule in RULES:
            for ep_on in EPS:
                for (w, W, B) in cands:
                    ev[(aware, rule, ep_on, w, W, B)] = evaluate(w, W, B, ep_on, aware, rule)
        print("aware", aware, "done", round(time.time() - t0), flush=True)
    # v1 = filters 1-5 under the textbook test
    v1 = []
    for (w, W, B) in cands:
        rs = [ev[(False, r, e, w, W, B)] for r in RULES for e in EPS]
        gs = [x[0] for x in rs]
        if any(g is None for g in gs) or not all(g is gs[0] for g in gs):
            continue
        g = gs[0]
        if has_big(g):
            continue
        k0 = rs[0][1]
        if not all(x is not None for x in k0) or not all(all(a is b for a, b in zip(x[1], k0)) for x in rs):
            continue
        if ep_capture_in_tree(w, W, B, False):
            continue
        v1.append((w, W, B))
    print("v1 size", len(v1), flush=True)
    half, mhalf = cgt.number(__import__("fractions").Fraction(1, 2)), cgt.number(__import__("fractions").Fraction(-1, 2))
    halfs = {half, mhalf, cgt.add(half, cgt.nimber(1)), cgt.add(mhalf, cgt.nimber(1))}
    rows = []
    for (w, W, B) in v1:
        per = {}
        for r in RULES:
            for e in EPS:
                a, b = ev[(False, r, e, w, W, B)], ev[(True, r, e, w, W, B)]
                per[f"{r},{'on' if e else 'off'}"] = {"root": a[0] is not b[0], "child": any(x is not y for x, y in zip(a[1], b[1]))}
        tb = ev[(False, "count", True, w, W, B)][0]
        rows.append({
            "w": w, "position": ptxt(W, B),
            "textbook": cgtfmt.fmt(tb, ascii=True),
            "aware_count_on": "race" if ev[(True, "count", True, w, W, B)][0] is None else cgtfmt.fmt(ev[(True, "count", True, w, W, B)][0], ascii=True),
            "half_class": tb in halfs,
            "is_number": tb.num is not None,
            "per_setting": per,
            "any_change": any(v["root"] or v["child"] for v in per.values()),
            "root_change_any_setting": any(v["root"] for v in per.values()),
            "root_change_count_on": per["count,on"]["root"],
            "change_epoff": any(v["root"] or v["child"] for k, v in per.items() if k.endswith("off")),
        })
    # e.p. off over all candidates
    epoff_cand = sum(1 for (w, W, B) in cands for r in RULES
                     if ev[(False, r, False, w, W, B)] != ev[(True, r, False, w, W, B)])
    out = {
        "candidates": len(cands),
        "v1": len(v1),
        "v1_changed_any": sum(r["any_change"] for r in rows),
        "v1_root_changed_count_on": sum(r["root_change_count_on"] for r in rows),
        "v1_root_changed_any_setting": sum(r["root_change_any_setting"] for r in rows),
        "v1_root_changed_by_setting": {k: sum(r["per_setting"][k]["root"] for r in rows) for k in rows[0]["per_setting"]},
        "v1_any_changed_by_setting": {k: sum(r["per_setting"][k]["root"] or r["per_setting"][k]["child"] for r in rows) for k in rows[0]["per_setting"]},
        "v1_half_class": sum(r["half_class"] for r in rows),
        "v1_half_class_changed": sum(r["half_class"] and r["any_change"] for r in rows),
        "v1_noninteger_numbers": sorted({r["textbook"] for r in rows if r["is_number"] and "/" in r["textbook"]}),
        "v1_noninteger_number_count": sum(1 for r in rows if r["is_number"] and "/" in r["textbook"]),
        "v1_changed_epoff": sum(r["change_epoff"] for r in rows),
        "candidate (setting) pairs differing with e.p. off": epoff_cand,
        "seconds": round(time.time() - t0),
    }
    print(json.dumps(out, indent=1))
    (HERE / "indep_result.json").write_text(json.dumps({"summary": out, "rows": rows}, indent=1) + "\n")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
