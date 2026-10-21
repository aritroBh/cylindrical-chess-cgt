"""Check ChessSums under both passed-pawn tests: "textbook" and "e.p.-aware".

  textbook   a pawn is passed if no enemy pawn stands ahead of it on its own or
             an adjacent file (cylcgt on the main checkout; Elkies 1996);
  e.p.-aware the same, except that a pawn which can still be taken en passant
             is not passed (the convention adopted on 2026-10-16; flag
             cylcgt.pawns.PASSED_RESPECTS_EP on git branch ep-aware-passed).

This script needs a cylcgt that has the flag. Point --cylcgt-root at a checkout
of that branch (it is put first on sys.path); bench itself is imported from
this checkout:

    cd /Users/aritro/Downloads/Research/Chessendgames
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions \
        --cylcgt-root /private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt

Writes bench/results/conventions_report.md and conventions_summary.json.

Checks
 1. Every one of the 5,290 candidate components: root value and every child
    value under 2 passed tests x 3 race rules x 2 e.p. settings (12 settings).
    Reports how many change between the two tests.
 2. The library in data/components.jsonl: every component and every child has
    the same value in all 12 settings (must hold; asserted).
 3. Library v1 (git 28d790f: filters 1-5 with the textbook test, 518
    components; rebuilt here from the 12-setting values): which of its
    components change under the e.p.-aware test, with both values. Checked:
    every one that changes is removed by filter 5' (filter 5' is a sufficient
    condition), and the current library is v1 minus the filter-5' hits.
 4. The library that the e.p.-aware test ALONE would certify (filters 1-5 run
    with the e.p.-aware test), compared with the current library.
 5. Instances: every row of val, test and test_heldout plus --train rows of
    train, re-solved on the whole board by pawns.value with the e.p.-aware
    test (e.p. on and off), and the win/loss of every move (= bench.verify
    check B, but under the e.p.-aware test).
 6. The KEY-FACT position W a2 c2 / B b7 d7 (4 flat files) in all 12 settings.

Positive control for the bench/ab.c e.p. counter (writes
bench/results/conventions_positive_control.json; any cylcgt will do):
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions --positive-control
"""
from __future__ import annotations

import os
import sys


def _cylcgt_root():
    for i, x in enumerate(sys.argv):
        if x == "--cylcgt-root" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
        if x.startswith("--cylcgt-root="):
            return x.split("=", 1)[1]
    return os.environ.get("CYLCGT_ROOT")


if __name__ == "__main__" and _cylcgt_root():
    sys.path.insert(0, os.path.abspath(_cylcgt_root()))

import argparse  # noqa: E402
import json  # noqa: E402
import random  # noqa: E402
import time  # noqa: E402
from collections import Counter  # noqa: E402
from multiprocessing import get_context  # noqa: E402
from pathlib import Path  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402

from . import cgtfmt  # noqa: E402
from . import components as C  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RES = ROOT / "results"
TESTS = (("textbook", False), ("e.p.-aware", True))
SETTINGS = [(t, rule, ep) for t, _ in TESTS for rule in C.RULES for ep in C.EPS]
KEY_FACT = "W: a2 c2 / B: b7 d7"


def set_test(aware: bool):
    if pawns.PASSED_RESPECTS_EP != aware:
        pawns.PASSED_RESPECTS_EP = aware
        pawns._value.cache_clear()


def set_rule(rule: str):
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()


def evaluate(items):
    """items: [(w, Pos)] -> {setting: [(root Game|None, (child Game|None, ...))]}"""
    out = {}
    for tname, aware in TESTS:
        set_test(aware)
        for rule in C.RULES:
            set_rule(rule)
            for ep in C.EPS:
                res = []
                for w, p in items:
                    b = Board(w, C.RANKS, False, ep)
                    try:
                        g = pawns.value(b, p)
                    except pawns.RaceError:
                        g = None
                    kv = []
                    for side, _, c in C._children(w, p, ep):
                        try:
                            kv.append(pawns._child(b, c, side))
                        except pawns.RaceError:
                            kv.append(None)
                    res.append((g, tuple(kv)))
                out[(tname, rule, ep)] = res
    set_rule("count")
    set_test(True)
    return out


def ep_reachable_current_test(w, p):
    """Filter 5 with whatever passed test is active: is an e.p. capture ever available?"""
    b = Board(w, C.RANKS, False, True)
    seen, stack = set(), [p]
    while stack:
        q = stack.pop()
        if q in seen:
            continue
        seen.add(q)
        if pawns.passed(b, q, "W") or pawns.passed(b, q, "B"):
            continue
        if C._ep_available(b, q):
            return True
        for side in "WB":
            stack.extend(pawns.moves(b, q, side))
    return False


def _judge(b, q, aware):
    set_test(aware)
    wp, bp = pawns.passed(b, q, "W"), pawns.passed(b, q, "B")
    d = (pawns.promote_distance(b, q, "W"), pawns.promote_distance(b, q, "B")) if (wp and bp) else None
    return wp, bp, d


def judged_differently(w, p):
    """Exact divergence: is some position of the (textbook) game tree judged
    differently by the two tests (passed flags, or race distances)?"""
    b = Board(w, C.RANKS, False, True)
    seen, stack = set(), [p]
    try:
        while stack:
            q = stack.pop()
            if q in seen:
                continue
            seen.add(q)
            tb = _judge(b, q, False)
            if tb != _judge(b, q, True):
                return True
            if tb[0] or tb[1]:
                continue
            for side in "WB":
                stack.extend(pawns.moves(b, q, side))
        return False
    finally:
        set_test(True)


def f(g):
    return "race" if g is None else cgtfmt.fmt(g, ascii=True)


def passes_filters(i, ev, tname, w, p, aware):
    """Filters 1-5 of components.py using only the settings of one passed test."""
    keys = [(tname, r, e) for r in C.RULES for e in C.EPS]
    gs = [ev[k][i][0] for k in keys]
    if any(g is None for g in gs) or not all(g is gs[0] for g in gs):
        return False
    g = gs[0]
    if C.has_big(g):
        return False
    kv = [ev[k][i][1] for k in keys]
    if not all(x is not None and all(kv[s][j] is x for s in range(6)) for j, x in enumerate(kv[0])):
        return False
    set_test(aware)
    return not ep_reachable_current_test(w, p)


def positive_control():
    """Does the ab.c e.p. counter fire on the components that filter 5' removes?
    Rebuilds library v1 (filters 1-5 only), then searches every component alone
    with plain alpha-beta, both sides to move."""
    from . import board as bd
    from .baseline import c_solve
    orig = C.ep_relevant
    C.ep_relevant = lambda w, p, at_terminals=False: False if at_terminals else orig(w, p)
    try:
        v1, _ = C.build(verbose=False)
    finally:
        C.ep_relevant = orig
    cur = {json.loads(x)["position"] for x in (DATA / "components.jsonl").read_text().splitlines()}
    out = {}
    for name, cs in (("removed by filter 5'", [c for c in v1 if c["position"] not in cur]),
                     ("kept (library v2)", [c for c in v1 if c["position"] in cur])):
        jobs = []
        for c in cs:
            w, b = bd.parse_pos_text(c["position"])
            jobs += [(c["width"], False, w, b, side, False, 0, 0) for side in (True, False)]
        res = c_solve(jobs)
        fired = sum(1 for i in range(len(cs)) if res[2 * i][3] or res[2 * i + 1][3])
        out[name] = {"components": len(cs), "counter fires": fired, "events": sum(x[3] for x in res)}
    return out


def _b_task(arg):
    from .verify import check_cylcgt
    set_test(True)
    split, row = arg
    return split, row["id"], check_cylcgt(row, ("count",))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cylcgt-root", help="checkout whose cylcgt has PASSED_RESPECTS_EP (put first on sys.path)")
    ap.add_argument("--train", type=int, default=3000, help="train rows re-solved in check 5")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--positive-control", action="store_true",
                    help="only run the ab.c e.p.-counter positive control (needs no e.p.-aware cylcgt)")
    a = ap.parse_args(argv)
    if a.positive_control:
        res = positive_control()
        RES.mkdir(exist_ok=True)
        (RES / "conventions_positive_control.json").write_text(json.dumps(res, indent=1) + "\n")
        print(json.dumps(res, indent=1))
        return
    if not hasattr(pawns, "PASSED_RESPECTS_EP"):
        sys.exit(f"{pawns.__file__} has no PASSED_RESPECTS_EP; pass --cylcgt-root <ep-aware-passed checkout>")
    t0 = time.time()
    summ, lines = {"cylcgt": pawns.__file__}, []

    print("1. candidates in 12 settings ...", flush=True)
    cands = C.candidates()
    if a.quick:
        cands = cands[::25]
    ev = evaluate(cands)
    idx = {(w, p): i for i, (w, p) in enumerate(cands)}
    n_root_diff = Counter()
    for rule in C.RULES:
        for ep in C.EPS:
            n_root_diff[f"{rule}, e.p. {'on' if ep else 'off'}"] = sum(
                ev[("textbook", rule, ep)][i][0] is not ev[("e.p.-aware", rule, ep)][i][0] for i in range(len(cands)))
    any_diff = [i for i in range(len(cands)) if any(
        ev[("textbook", r, e)][i] != ev[("e.p.-aware", r, e)][i] for r in C.RULES for e in C.EPS)]
    summ["candidates"] = len(cands)
    summ["candidates whose root value differs between the tests"] = dict(n_root_diff)
    summ["candidates with any root or child difference between the tests"] = len(any_diff)
    print(f"   done [{time.time() - t0:.0f}s]", flush=True)

    print("2. current library ...", flush=True)
    lib = [json.loads(x) for x in (DATA / "components.jsonl").read_text().splitlines()]
    lib_bad = []
    for c in lib:
        i = idx.get((c["width"], Pos.parse(c["position"])))
        if i is None:
            assert a.quick
            continue
        vals = [ev[s][i] for s in SETTINGS]
        if not all(v == vals[0] for v in vals) or vals[0][0] is None or any(x is None for x in vals[0][1]):
            lib_bad.append(c["comp_id"])
        assert f(vals[0][0]) == c["value_ascii"], c["comp_id"]
        assert [f(x) for x in vals[0][1]] == [m["value"] for m in c["moves"]], c["comp_id"]
    summ["library components"] = len(lib)
    summ["library components differing in some setting (must be 0)"] = len(lib_bad)
    assert not lib_bad, lib_bad
    print(f"   {len(lib)} components, all identical in 12 settings [{time.time() - t0:.0f}s]", flush=True)

    print("3. library v1 (rebuilt: filters 1-5 with the textbook test) ...", flush=True)
    keep_tb = [i for i, (w, p) in enumerate(cands) if passes_filters(i, ev, "textbook", w, p, False)]
    # v1 ids: components.py sorts kept components by (width, number of pawns, position text)
    keep_tb.sort(key=lambda i: (cands[i][0], len(cands[i][1].white) + len(cands[i][1].black), C.ptext(cands[i][1])))
    cur = {(c["width"], c["position"]) for c in lib}
    v1_rows, combos = [], Counter()
    for n, i in enumerate(keep_tb):
        w, p = cands[i]
        tb, aw = ev[("textbook", "count", True)][i], ev[("e.p.-aware", "count", True)][i]
        differs = any(ev[("textbook", r, e)][i] != ev[("e.p.-aware", r, e)][i] for r in C.RULES for e in C.EPS)
        f5p = C.ep_relevant(w, p, at_terminals=True)
        exact = judged_differently(w, p)
        set_test(True)
        ep_aw = ep_reachable_current_test(w, p)
        in_cur = (w, C.ptext(p)) in cur
        combos[f"filter 5' fires={f5p}, some position judged differently={exact}, "
               f"e.p. capture playable in the e.p.-aware tree={ep_aw}, values differ={differs}, kept now={in_cur}"] += 1
        assert in_cur == (not f5p), C.ptext(p)
        assert not (differs and not f5p), C.ptext(p)       # filter 5' is a sufficient condition (proof in components.py)
        assert exact or not (differs or ep_aw), C.ptext(p)  # identical judgements => identical trees
        if differs:
            names = [f"{s_} {m}" for s_, m, _ in C._children(w, p, True)]
            kids = [(m, f(x), f(y)) for m, x, y in zip(names, tb[1], aw[1]) if x is not y]
            v1_rows.append({"v1_id": f"C{n:04d}", "position": C.ptext(p), "textbook": f(tb[0]),
                            "aware": f(aw[0]), "root_differs": tb[0] is not aw[0], "children": kids})
    summ["library v1 components (textbook filters 1-5)"] = len(keep_tb)
    summ["library v1 components that change under the e.p.-aware test"] = len(v1_rows)
    summ["... of which the root value changes"] = sum(r["root_differs"] for r in v1_rows)
    summ["library v1 cases"] = dict(sorted(combos.items()))
    print(f"   {len(v1_rows)} of {len(keep_tb)} change [{time.time() - t0:.0f}s]", flush=True)

    print("4. what the e.p.-aware test alone would certify ...", flush=True)
    keep_aw = [i for i, (w, p) in enumerate(cands) if passes_filters(i, ev, "e.p.-aware", w, p, True)]
    cur_idx = {idx[(c["width"], Pos.parse(c["position"]))] for c in lib if (c["width"], Pos.parse(c["position"])) in idx}
    keep_tb_5p = {i for i in keep_tb if not C.ep_relevant(*cands[i], at_terminals=True)}
    summ["filters 1-5, textbook test (library v1)"] = len(keep_tb)
    summ["filters 1-5, e.p.-aware test"] = len(keep_aw)
    summ["both (intersection)"] = len(set(keep_tb) & set(keep_aw))
    summ["current library (textbook filters 1-5 + filter 5')"] = len(cur_idx)
    summ["current library equals library v1 minus the filter-5' hits?"] = keep_tb_5p == cur_idx if not a.quick else None
    summ["current library equals the intersection of the two single-test libraries?"] = \
        (set(keep_tb) & set(keep_aw)) == cur_idx
    only_aw = sorted(set(keep_aw) - set(keep_tb))
    only_aw_rows = []
    for i in only_aw:
        w, p = cands[i]
        only_aw_rows.append((C.ptext(p), w, f(ev[("textbook", "count", True)][i][0]),
                             f(ev[("e.p.-aware", "count", True)][i][0])))
    summ["certified by the e.p.-aware test only"] = len(only_aw)
    print(f"   aware-only {len(keep_aw)}, textbook-only {len(keep_tb)} [{time.time() - t0:.0f}s]", flush=True)

    print("6. KEY-FACT position ...", flush=True)
    kf = Pos.parse(KEY_FACT)
    kfv = {}
    for tname, aware in TESTS:
        set_test(aware)
        for rule in C.RULES:
            set_rule(rule)
            for ep in C.EPS:
                kfv[f"{tname}, {rule}, e.p. {'on' if ep else 'off'}"] = cgtfmt.fmt(pawns.value(Board(4, 8, False, ep), kf))
    set_rule("count")
    set_test(True)
    summ["KEY-FACT " + KEY_FACT + " (4 flat files)"] = kfv

    print("5. instances under the e.p.-aware test ...", flush=True)
    rng = random.Random(a.seed)
    tasks = []
    for sp in ("train", "val", "test", "test_heldout"):
        rows = [json.loads(x) for x in (DATA / f"{sp}.jsonl").read_text().splitlines()]
        if sp == "train":
            rows = rng.sample(rows, min(a.train, len(rows)))
        if a.quick:
            rows = rows[:40]
        tasks += [(sp, r) for r in rows]
    inst = Counter()
    bad = []
    with get_context("fork").Pool(a.jobs) as pool:
        for sp, rid, res in pool.imap_unordered(_b_task, tasks, chunksize=20):
            inst[f"{sp} (agree)"] += res["count"]
            inst[f"{sp} (total)"] += 1
            if not res["count"]:
                bad.append(rid)
    summ["instances re-solved under the e.p.-aware test"] = dict(sorted(inst.items()))
    summ["instance disagreements"] = bad[:50]
    summ["seconds"] = round(time.time() - t0)
    print(f"   done, {len(bad)} disagreements [{time.time() - t0:.0f}s]", flush=True)

    RES.mkdir(exist_ok=True)
    name = "conventions_quick" if a.quick else "conventions"
    (RES / f"{name}_summary.json").write_text(json.dumps(
        {"summary": summ, "v1_changed": v1_rows, "aware_only": only_aw_rows}, indent=1, ensure_ascii=False) + "\n")
    (RES / f"{name}_report.md").write_text(report(summ, v1_rows, only_aw_rows, inst, bad))
    print(report(summ, v1_rows, only_aw_rows, inst, bad))


def report(summ, v1_rows, only_aw_rows, inst, bad):
    L = ["# ChessSums under both passed-pawn tests", "",
         "Generated by `bench/conventions.py` (command in its docstring), with cylcgt from",
         f"`{summ['cylcgt']}`.", "",
         "- **textbook**: a pawn with no enemy pawn ahead on its own or an adjacent file is passed.",
         "- **e.p.-aware** (adopted 2026-10-16): the same, but a pawn that can still be taken en passant is not passed.",
         "", "All values are computed once, by cylcgt; the two tests differ only by `pawns.PASSED_RESPECTS_EP`.", "",
         "## Summary", "", "| quantity | value |", "|---|---|"]
    for k, v in summ.items():
        if k in ("cylcgt", "instances re-solved under the e.p.-aware test", "instance disagreements") or isinstance(v, dict):
            continue
        L.append(f"| {k} | {v} |")
    L += ["", "Candidates whose root value differs between the tests, by setting (all 5,290 candidates):", "",
          "| race rule, e.p. | candidates |", "|---|---|"]
    for k, v in summ["candidates whose root value differs between the tests"].items():
        L.append(f"| {k} | {v} |")
    combos = summ.get("library v1 cases", {})
    if combos:
        L += ["", "Library v1 (518 components), by case:", "",
              "| case | components |", "|---|---|"]
        L += [f"| {k} | {v} |" for k, v in combos.items()]
    key = [k for k in summ if k.startswith("KEY-FACT")][0]
    L += ["", f"## {key}", "", "| passed test, race rule, e.p. | value |", "|---|---|"]
    L += [f"| {k} | `{v}` |" for k, v in summ[key].items()]
    L += ["", "## Instances re-solved on the whole board under the e.p.-aware test", "",
          "Value with e.p. on and off, and the win/loss of every legal move (as `bench.verify` check B).", "",
          "| split | agree | total |", "|---|---|---|"]
    for sp in ("train", "val", "test", "test_heldout"):
        if f"{sp} (total)" in inst:
            L.append(f"| {sp} | {inst[sp + ' (agree)']} | {inst[sp + ' (total)']} |")
    L += ["", f"Disagreements: {len(bad)}."]
    if v1_rows:
        L += ["", "## Library v1 components that change under the e.p.-aware test (removed by filter 5')", "",
              "Race rule count, e.p. on; v1 ids as in git 28d790f. With e.p. off the two tests coincide (no e.p. right is",
              "ever set), so each of these components is e.p.-dependent under the e.p.-aware test.", "",
              "| v1 id | position | textbook | e.p.-aware | children that change (textbook → e.p.-aware) |",
              "|---|---|---|---|---|"]
        for r in v1_rows:
            kids = "; ".join(f"{m}: `{x}` → `{y}`" for m, x, y in r["children"])
            L.append(f"| {r['v1_id']} | {r['position']} | `{r['textbook']}` | `{r['aware']}` | {kids} |")
    if only_aw_rows:
        L += ["", "## Candidates certified by the e.p.-aware test alone (not used: they fail the textbook test)", "",
              "| position | width | textbook (count, e.p. on) | e.p.-aware (count, e.p. on) |", "|---|---|---|---|"]
        L += [f"| {p} | {w} | `{x}` | `{y}` |" for p, w, x, y in only_aw_rows]
    L += ["", f"Run time {summ['seconds']} s."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
