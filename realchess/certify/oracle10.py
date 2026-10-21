"""Real-chess oracle analysis for components whose embedding has more than 8
men (here: the 6-pawn *2 candidates, 10 men with the trebuchet).

The real-chess oracle value (realchess/oracle_value.py) is the CGT value of
the component's model tree with every terminal T replaced by a game built
from its real-chess results rW (White to move in T) and rB (Black to move),
White's view. Terminals with 9-10 men are beyond the tablebase, so this tool
works with three kinds of terminal sides:
  * resolved: an exact real-chess result (realdb.jsonl, see termdb.py);
  * model-filled: an unresolved side of a ONE-SIDED terminal (only one side
    has a passed pawn) taken as a win for that side, i.e. the model's own
    convention (--fill model); this is an assumption and is reported as one;
  * free: the side may be anything (win, draw, loss); the monotone sandwich
    then bounds the value (oracle_value.sandwich).

Subcommands
  resolve  resolve terminal sides (both sides to move) selected by --races /
           --max-men / --only-critical, cheapest first, within --max-new.
  bounds   G_lo, G_hi, pinned value, exclusion of *2 and 0, for every
           treatment and fill policy.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.oracle10 resolve --component "W: a3 b2 c2 / B: a4 b6 c5" \
        --races --cap 1200 --max-new 50 --ext 4
    PYTHONPATH=. .venv/bin/python -m realchess.certify.oracle10 bounds --component "W: a3 b2 c2 / B: a4 b6 c5"
Run from the e.p.-aware worktree (cwd, PYTHONPATH=<worktree>:<root>) for the e.p.-aware tree.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg
from realchess.oracle_value import TREATMENTS, Terminals, describe_bounds, pair_game, sandwich
from realchess.probe import CapReached
from realchess.search import Searcher

from . import infra, termdb


def passed_test():
    return "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook"


def is_race(T, t):
    return pawns.passed(T.board, t, "W") and pawns.passed(T.board, t, "B")


def owner(T, t):
    """'W'/'B' for a one-sided terminal, None for a race."""
    w, b = pawns.passed(T.board, t, "W"), pawns.passed(T.board, t, "B")
    if w and b:
        return None
    return "W" if w else "B"


def side_fens(T, t):
    return {s: mg.normal_fen(C.embed(t, s)) for s in "WB"}


def raw_from_db(T, db, fill: str = "none", race_rule: str | None = None):
    """raw[t] = (rW, rB), White's view; None = unknown.
    fill='model': unknown sides of one-sided terminals = win for the owner.
    race_rule: also fill unknown race sides by that model rule."""
    raw, stats = {}, Counter()
    for t in T.terms:
        f = side_fens(T, t)
        vals = []
        for s in "WB":
            r = db.get(f[s])
            if r is not None:
                vals.append(r["white"])
                stats["resolved"] += 1
                continue
            o = owner(T, t)
            if fill == "model" and o is not None:
                vals.append(1 if o == "W" else -1)
                stats["model-filled one-sided"] += 1
            elif race_rule and o is None:
                mover = "B" if s == "W" else "W"
                vals.append(C.model_terminal_value(T.board, t, mover, race_rule))
                stats[f"model-filled race ({race_rule})"] += 1
            else:
                vals.append(None)
                stats["free"] += 1
        raw[t] = tuple(vals)
    return raw, dict(stats)


# ------------------------------------------------------------------ resolve
def make_searcher(pr, oracle, model):
    from realchess.solve_candidate import is_model_internal, make_order
    region = lambda pos: "model" if is_model_internal(pos, model) else "off"
    return Searcher(oracle, order_hint=make_order(model, pr.cached), region=region, cached=pr.cached,
                    kb=infra.kb())


def cmd_resolve(a):
    from realchess.solve_candidate import Model, RealOracle, OfflineOracle, deepen
    from realchess.oracle_value import plan_7man_probes
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    model = Model()
    pr = infra.CertProber(a.cap, tag=f"certify-oracle10", offline=a.offline)
    oracle = OfflineOracle(pr) if a.offline else RealOracle(pr, a.max_new)
    s = make_searcher(pr, oracle, model)
    db = termdb.load()
    sel = []
    crit = set()
    if a.only_from:
        for path in a.only_from:
            d = json.load(open(path))
            for conv, o in d.items():
                for e in o.get("single_flip_critical_race_entries", []) + o.get("pinning_race_set", []):
                    crit.add(e["terminal"])
    for t in T.order:
        m = T.men(t)
        if a.races and not is_race(T, t):
            continue
        if a.one_sided and is_race(T, t):
            continue
        if m > a.max_men or m < a.min_men:
            continue
        if crit and str(t) not in crit:
            continue
        sel.append(t)
    todo = [(t, side) for t in sel for side in "WB" if side_fens(T, t)[side] not in db]
    print(f"[resolve] {passed_test()} tree: {len(sel)} terminals selected, {len(todo)} sides unresolved", flush=True)
    # one parent probe can answer several <= 7-man sides
    small = sorted({t for t, side in todo if T.men(t) <= 7}, key=lambda t: (T.men(t), str(t)))
    if small and not a.offline and a.parents:
        chosen, cands = plan_7man_probes(T, small, pr.cached, frozenset(infra.kb().cat))
        print(f"[resolve] parent probes planned: {len(chosen)}", flush=True)
        for f in chosen:
            if oracle.new_requests >= a.max_new:
                break
            try:
                s._rec(mg.parse_fen(f))
            except CapReached:
                break
    rows, status = [], "complete"
    t0 = time.time()
    glob = oracle.max_new
    try:
        for t, side in sorted(todo, key=lambda ts: (T.men(ts[0]), str(ts[0]), ts[1])):
            if time.time() - t0 > a.max_seconds:
                status = f"stopped: --max-seconds {a.max_seconds}"
                break
            pos = C.embed(t, side)
            if mg.validity_errors(pos):
                continue
            oracle.max_new = min(glob, oracle.new_requests + a.per_target)
            try:
                if pos.men() <= 7:
                    iv, how = s.search(pos, 0), "tablebase (<=7 men)"
                else:
                    iv, how = deepen(s, pos, a.ext), f"search ({pos.men()} men, ext<={a.ext})"
            except CapReached:
                if oracle.new_requests >= glob:
                    status = "stopped: --max-new reached"
                    break
                continue
            finally:
                oracle.max_new = glob
            if iv[0] == iv[1]:
                r = termdb.make_row(pos, iv, how, a.ext)
                r["terminal"], r["side"], r["tree"] = str(t), side, passed_test()
                rows.append(r)
                termdb.append([r])
    except CapReached:
        status = "stopped: cap"
    out = {"component": a.component, "tree": passed_test(), "selected_terminals": len(sel),
           "sides_todo": len(todo), "resolved_now": len(rows), "status": status,
           "new_requests": oracle.new_requests, "ledger_count": pr.ledger_count(),
           "seconds": round(time.time() - t0, 1),
           "resolved_by_men": dict(Counter(r["men"] for r in rows))}
    print(json.dumps(out, indent=1))


# ------------------------------------------------------------------- bounds
def cmd_bounds(a):
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    db = termdb.load()
    targets = {"*2": cgt.nimber(2), "0": cgt.ZERO}
    mvals = {}
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        mvals[rule] = pawns.value(T.board, comp)
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    for rule, g in mvals.items():
        targets[f"model value under {rule}"] = g
    out = {"component": a.component, "tree": passed_test(), "internal_nodes": len(T.internal),
           "terminals": len(T.terms), "model_values": {k: cgt.show(v) for k, v in mvals.items()},
           "policies": {}}
    sides = Counter()
    for t in T.terms:
        f = side_fens(T, t)
        for s in "WB":
            key = ("race" if is_race(T, t) else "one-sided", T.men(t), f[s] in db)
            sides[key] += 1
    out["sides_resolved_by_kind_and_men"] = {f"{k[0]} {k[1]}-man {'resolved' if k[2] else 'open'}": v
                                            for k, v in sorted(sides.items())}
    # real vs model on resolved one-sided sides
    agree = Counter()
    for t in T.terms:
        o = owner(T, t)
        if o is None:
            continue
        for s, f in side_fens(T, t).items():
            r = db.get(f)
            if r is not None:
                agree[("agree" if r["white"] == (1 if o == "W" else -1) else
                       ("draw" if r["white"] == 0 else "DISAGREE"), T.men(t))] += 1
    out["one_sided_real_vs_model"] = {f"{k[0]} ({k[1]} men)": v for k, v in sorted(agree.items())}
    policies = [("free", "none", None), ("one-sided model-filled, races free", "model", None)]
    for rule in ("count", "opponent"):
        policies.append((f"all unknown sides model-filled (races: {rule})", "model", rule))
    for pname, fill, rr in policies:
        raw, st = raw_from_db(T, db, fill, rr)
        res = {"fill_stats": st}
        for tname, (kind, d) in TREATMENTS.items():
            g_lo, g_hi = sandwich(T, raw, kind, d)
            b = describe_bounds(g_lo, g_hi, targets)
            res[tname] = {k: v for k, v in b.items() if "(how)" not in k}
        out["policies"][pname] = res
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["resolve", "bounds"])
    ap.add_argument("--component", required=True)
    ap.add_argument("--cap", type=int, default=1200)
    ap.add_argument("--max-new", type=int, default=50)
    ap.add_argument("--per-target", type=int, default=6)
    ap.add_argument("--ext", type=int, default=4)
    ap.add_argument("--max-men", type=int, default=8)
    ap.add_argument("--min-men", type=int, default=0)
    ap.add_argument("--races", action="store_true")
    ap.add_argument("--one-sided", action="store_true")
    ap.add_argument("--only-from", action="append", help="tree_stats JSON: only its critical race terminals")
    ap.add_argument("--parents", action="store_true", help="probe covering parents for <=7-man sides first")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--max-seconds", type=float, default=1500)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    sys.setrecursionlimit(100000)
    {"resolve": cmd_resolve, "bounds": cmd_bounds}[a.cmd](a)


if __name__ == "__main__":
    main()
