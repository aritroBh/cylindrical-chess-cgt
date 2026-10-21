"""Enumerate and certify the component library for ChessSums.

A *component* is a pawn position on a flat strip of w = 1..4 files and 8 ranks
in which every file is occupied, with 2..4 pawns of both colours on ranks 2-7.
(A single pawn is always passed, so 1-pawn components do not exist.)

Values come from cylcgt (`pawns.value` / `pawns._child`). A component is KEPT
only if all of the following hold:
  1. neither side has a passed pawn at the root;
  2. the canonical value is the same game under all six settings
     RACE_RULE in {count, mover, opponent} x en passant {on, off};
  3. for every legal move of either side, the value of the resulting position
     is also the same under all six settings (so winning-move sets cannot
     depend on the race rule or on en passant in any sum);
  4. the canonical value contains no +-BIG number anywhere in its game graph
     (no passed-pawn threat survives canonical simplification), which also
     makes every sum of kept components `sum_safe`;
  5. no en-passant capture is ever available anywhere in the component's game
     tree, so the per-component e.p. approximation of cylcgt never matters and
     real-chess e.p. semantics coincide with the model;
  5'. (added 2026-10-16 with the e.p.-aware passed test) at the positions
     where the textbook test ENDS the game, no double-stepped pawn is both
     passed (textbook) and capturable en passant.
     Why: the "textbook" passed test (cylcgt on main) and the adopted
     "e.p.-aware" test (a pawn that can still be taken e.p. is not passed;
     cylcgt.pawns.PASSED_RESPECTS_EP on branch ep-aware-passed) can disagree
     only about a pawn that has just double-stepped and can be taken e.p.,
     and only if the textbook test calls that pawn passed (the promotion
     distance used in races skips the same pawns). At a position that the
     textbook test does not end, no pawn is passed, so filter 5' only has to
     look at the leaves. With 5' no reachable position is judged differently,
     so both tests build the same game tree, and every kept component (and
     every child of it) has the same value under both.
     bench/conventions.py re-checks this by direct computation.
Sanity checks (asserted, not filters): the value is unchanged when the strip
is embedded in a wider flat board or in a cylinder with one empty file;
mirroring the files gives the same value; swapping colours (and flipping
ranks) gives the negative.

Run:  PYTHONPATH=. .venv/bin/python -m bench.components   (prints the summary)
"""
from __future__ import annotations

import itertools
import random
import time
from collections import Counter, defaultdict

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

from . import board as bd
from . import cgtfmt

RANKS = 8
RULES = ("count", "mover", "opponent")
EPS = (True, False)
BIG = pawns.BIG
HOLDOUT_VALUES = ("↑*", "↓*")      # value-class holdout (whole classes)
HOLDOUT_ORBIT_FRACTION = 0.10       # plus this fraction of the other orbits
HOLDOUT_SEED = 7


def candidates():
    """All (w, Pos) with w files all occupied, 2..4 pawns, both colours, no
    passer at the root. Deterministic order."""
    out = []
    for w in range(1, 5):
        sqs = [(f, r) for f in range(w) for r in range(2, RANKS)]
        b = Board(w, RANKS, False, True)
        for n in range(max(2, w), 5):
            for S in itertools.combinations(sqs, n):
                if len({f for f, _ in S}) != w:
                    continue
                for colors in itertools.product("WB", repeat=n):
                    if "W" not in colors or "B" not in colors:
                        continue
                    W = frozenset(s for s, c in zip(S, colors) if c == "W")
                    B = frozenset(s for s, c in zip(S, colors) if c == "B")
                    p = Pos(W, B)
                    if pawns.passed(b, p, "W") or pawns.passed(b, p, "B"):
                        continue
                    out.append((w, p))
    return out


def has_big(g: cgt.Game) -> bool:
    seen, stack = set(), [g]
    while stack:
        x = stack.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        if x.num is not None:
            if abs(x.num) >= BIG // 2:
                return True
            continue
        stack.extend(x.L + x.R)
    return False


def _ep_available(b: Board, q: Pos) -> bool:
    """Can the side holding the e.p. right in q capture en passant right now?"""
    if not (q.ep and b.ep):
        return False
    side = q.ep[2]
    return set(pawns.moves(b, q, side)) != set(pawns.moves(b, Pos(q.white, q.black, None), side))


def _ep_passer(b: Board, q: Pos) -> bool:
    """Has a pawn just double-stepped that the textbook test calls passed and
    that the opponent can take en passant? (the e.p.-aware test disagrees)"""
    if not _ep_available(b, q):
        return False
    sq_, mover = q.ep[1], ("W" if q.ep[2] == "B" else "B")
    alone = Pos(frozenset([sq_]), q.black) if mover == "W" else Pos(q.white, frozenset([sq_]))
    return _textbook_passed(b, alone, mover)


def ep_relevant(w: int, p: Pos, at_terminals: bool = False) -> bool:
    """at_terminals=False (filter 5): is an en-passant capture ever available
    in the component's game tree? The tree is the one cylcgt searches under
    the textbook passed test: it is not expanded below a position where a side
    has a passed pawn, and such leaves are not examined.
    at_terminals=True (filters 5 and 5'): also True if at such a leaf the
    pawn that has just double-stepped is passed and can be taken e.p., the
    only case in which the e.p.-aware passed test judges a position
    differently (it would not call that pawn passed)."""
    b = Board(w, RANKS, False, True)
    seen, stack = set(), [p]
    while stack:
        q = stack.pop()
        if q in seen:
            continue
        seen.add(q)
        if _textbook_passed(b, q, "W") or _textbook_passed(b, q, "B"):
            if at_terminals and _ep_passer(b, q):
                return True
            continue
        if _ep_available(b, q):
            return True
        for side in "WB":
            stack.extend(pawns.moves(b, q, side))
    return False


def _textbook_passed(b: Board, q: Pos, side: str) -> bool:
    """pawns.passed with the textbook test, whichever cylcgt is imported."""
    flag = getattr(pawns, "PASSED_RESPECTS_EP", None)
    if flag is None:
        return pawns.passed(b, q, side)
    pawns.PASSED_RESPECTS_EP = False
    try:
        return pawns.passed(b, q, side)
    finally:
        pawns.PASSED_RESPECTS_EP = flag


def mirror(w, p: Pos) -> Pos:
    return Pos(frozenset((w - 1 - f, r) for f, r in p.white), frozenset((w - 1 - f, r) for f, r in p.black))


def colorflip(p: Pos) -> Pos:
    return Pos(frozenset((f, RANKS + 1 - r) for f, r in p.black), frozenset((f, RANKS + 1 - r) for f, r in p.white))


def ptext(p: Pos) -> str:
    return bd.pos_text(p.white, p.black)


def _children(w, p, ep):
    """[(side, move_name, child_Pos_with_ep)] in a deterministic order."""
    b = Board(w, RANKS, False, ep)
    geo = bd.Geometry(w, False)
    out = []
    for side in "WB":
        kids = pawns.moves(b, p, side)
        by_sets = {(k.white, k.black): k for k in kids}
        named = bd.gen_moves(geo, p.white, p.black, side)
        assert len(named) == len(kids) == len(by_sets), (ptext(p), side)
        for name, fr, to, nw, nb in named:
            out.append((side, name, by_sets[(nw, nb)]))
    return out


def build(verbose=True):
    """Certify the library. Values are always computed with the textbook passed
    test, so the output does not depend on which cylcgt is on the path (on the
    ep-aware-passed branch the flag is set to False for the duration); filter
    5' makes the kept components independent of that choice anyway."""
    flag = getattr(pawns, "PASSED_RESPECTS_EP", None)
    if flag is not None:
        pawns.PASSED_RESPECTS_EP = False
        pawns._value.cache_clear()
    try:
        return _build(verbose)
    finally:
        if flag is not None:
            pawns.PASSED_RESPECTS_EP = flag
            pawns._value.cache_clear()


def _build(verbose=True):
    t0 = time.time()
    cands = candidates()
    stats = Counter(candidates=len(cands))
    vals = defaultdict(list)          # (w,p) -> [value per setting]
    kids = defaultdict(list)          # (w,p) -> [[child value per move] per setting]
    names = {}
    for rule in RULES:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        for ep in EPS:
            for w, p in cands:
                b = Board(w, RANKS, False, ep)
                try:
                    g = pawns.value(b, p)
                except pawns.RaceError:  # pragma: no cover (cannot happen: no root passers)
                    g = None
                vals[(w, p)].append(g)
                ch = _children(w, p, ep)
                names[(w, p)] = [(s, n) for s, n, _ in ch]
                kv = []
                for side, n, c in ch:
                    try:
                        kv.append(pawns._child(b, c, side))
                    except pawns.RaceError:
                        kv.append(None)
                kids[(w, p)].append(kv)
        if verbose:
            print(f"  race rule {rule}: done ({time.time() - t0:.0f}s)", flush=True)
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()

    kept = []
    for w, p in cands:
        gs = vals[(w, p)]
        if any(g is None for g in gs):
            stats["drop: race error at root"] += 1
            continue
        if not all(g is gs[0] for g in gs):
            rule_var = not all(gs[i] is gs[i % 2] for i in range(6))
            ep_var = not all(gs[2 * i] is gs[2 * i + 1] for i in range(3))
            stats["drop: value depends on " + ("race rule and e.p." if rule_var and ep_var else
                                               "race rule" if rule_var else "e.p.")] += 1
            continue
        g = gs[0]
        if g.num is not None and abs(g.num) >= BIG // 2:
            stats["drop: value is +-BIG"] += 1
            continue
        if has_big(g):
            stats["drop: canonical form contains a +-BIG threat"] += 1
            continue
        kv = kids[(w, p)]
        if not all(kv[0][i] is not None and all(kv[s][i] is kv[0][i] for s in range(6)) for i in range(len(kv[0]))):
            stats["drop: some child value depends on race rule / e.p."] += 1
            continue
        if ep_relevant(w, p):
            stats["drop: an e.p. capture can occur in the game tree"] += 1
            continue
        if ep_relevant(w, p, at_terminals=True):
            stats["drop: a double step can make a passer that may be taken e.p. (e.p.-aware test differs)"] += 1
            continue
        kept.append((w, p, g, kv[0]))
    stats["kept"] = len(kept)

    # sanity checks: embedding, mirror, colour flip
    pawns.RACE_RULE = "count"
    for w, p, g, _ in kept:
        cyl = Board(w + 1, RANKS, True, True)
        assert pawns.value(cyl, p) is g, ("cylinder embedding", ptext(p))
        wide = Board(w + 2, RANKS, False, True)
        shifted = Pos(frozenset((f + 1, r) for f, r in p.white), frozenset((f + 1, r) for f, r in p.black))
        assert pawns.value(wide, shifted) is g, ("flat embedding", ptext(p))
        b = Board(w, RANKS, False, True)
        assert pawns.value(b, mirror(w, p)) is g, ("mirror", ptext(p))
        assert pawns.value(b, colorflip(p)) is cgt.neg(g), ("colour flip", ptext(p))
    # no child of a kept component gives the mover a passed pawn (would be +-BIG for the mover)
    for w, p, g, kv in kept:
        for (side, name), cv in zip(names[(w, p)], kv):
            if cv.num is not None and abs(cv.num) >= BIG // 2:
                assert (cv.num > 0) == (side == "B"), ("mover gets a passer", ptext(p), name)

    # orbits and hold-outs
    kept.sort(key=lambda t: (t[0], len(t[1].white) + len(t[1].black), ptext(t[1])))
    def orbit_key(w, p):
        forms = [p, mirror(w, p), colorflip(p), colorflip(mirror(w, p))]
        return f"w{w}:" + min(ptext(q) for q in forms)
    orbits = sorted({orbit_key(w, p) for w, p, _, _ in kept})
    orbit_index = {o: i for i, o in enumerate(orbits)}
    rng = random.Random(HOLDOUT_SEED)
    value_held = set()
    for w, p, g, _ in kept:
        if cgtfmt.fmt(g) in HOLDOUT_VALUES:
            value_held.add(orbit_key(w, p))
    rest = [o for o in orbits if o not in value_held]
    struct_held = set(rng.sample(rest, round(HOLDOUT_ORBIT_FRACTION * len(rest))))

    records = []
    for i, (w, p, g, kv) in enumerate(kept):
        ok = orbit_key(w, p)
        moves = []
        for (side, name), cv in zip(names[(w, p)], kv):
            moves.append({"side": side, "move": name, "value": cgtfmt.fmt(cv, ascii=True), "_game": cv})
        t = cgt.temperature(g)
        rec = {
            "comp_id": f"C{i:04d}",
            "width": w,
            "n_pawns": len(p.white) + len(p.black),
            "position": ptext(p),
            "value": cgtfmt.fmt(g),
            "value_ascii": cgtfmt.fmt(g, ascii=True),
            "kind": cgtfmt.kind(g),
            "outcome": cgt.outcome(g),
            "mean": cgtfmt.fnum(cgt.mean(g)),
            "temperature": None if t is None else cgtfmt.fnum(t),
            "orbit": orbit_index[ok],
            "heldout": "value-class" if ok in value_held else "structure" if ok in struct_held else None,
            "moves": moves,
            "_game": g,
            "_pos": p,
        }
        records.append(rec)
    stats["orbits"] = len(orbits)
    stats["heldout orbits (value class)"] = len(value_held)
    stats["heldout orbits (structure)"] = len(struct_held)
    stats["heldout components"] = sum(1 for r in records if r["heldout"])
    stats["distinct values"] = len({r["value"] for r in records})
    stats["seconds"] = round(time.time() - t0, 1)
    return records, stats


def public(rec: dict) -> dict:
    out = {k: v for k, v in rec.items() if not k.startswith("_")}
    out["moves"] = [{k: v for k, v in m.items() if not k.startswith("_")} for m in rec["moves"]]
    return out


if __name__ == "__main__":
    recs, st = build()
    for k, v in st.items():
        print(f"{k}: {v}")
    vc = Counter(r["value"] for r in recs)
    print("values:", ", ".join(f"{v} x{c}" for v, c in sorted(vc.items(), key=lambda kv: (-kv[1], kv[0]))))
