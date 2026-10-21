"""Adaptive real-chess EXCLUSION of a target (default *2) from the oracle
value of a component whose embedding has 9-10 men.

Goal: an unconditional one-sided certificate, i.e. with every terminal that
is not a certain real-chess L or R left FREE in [-2BIG, +2BIG] (treatment
"free (only L/R fixed)", which bounds every other treatment), either
    lower test:  G_lo is not <= target   (G_lo: free terminals at -2BIG), or
    upper test:  target is not <= G_hi   (G_hi: free terminals at +2BIG).
By monotonicity the oracle value then differs from the target whatever the
free terminals are (and whatever the draw convention is).

Loop: (1) with unresolved sides of one-sided terminals filled by the model
(a win for the passer's owner) and unresolved race sides free, find by a
chunked greedy a small set of model-filled terminals the test still relies
on; (2) resolve their sides in real chess (<= 7 men: tablebase; 8 men: search
with the tablebase at every capture; 9+ men: search9.DeepSearcher); a side
that cannot be resolved makes its terminal permanently free; (3) repeat until
nothing model-filled is needed (certificate) or the test fails with the
unresolvable terminals free (then report what it is conditional on).

    PYTHONPATH=. .venv/bin/python -m realchess.certify.iterate --component "W: a3 b2 c2 / B: a4 b6 c5" \
        --cap 1200 --max-new 150 --ext 6
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg
from realchess.oracle_value import TREATMENTS, Terminals, interval_of
from realchess.probe import CapReached

from . import infra, termdb
from .oracle10 import is_race, owner, passed_test, side_fens
from .search9 import DeepSearcher


def holds_fn(T, kind, d, target, test):
    low = test == "lower"

    def holds(rawmap):
        def g(t):
            lo, hi = interval_of(*rawmap[t], kind, d)
            return lo if low else hi
        v = T.value(g)
        return (not cgt.le(v, target)) if low else (not cgt.le(target, v))
    return holds


def chunked_greedy(items, ok, chunk=64):
    """Largest-ish F subset of items with ok(F) true, F grown greedily in
    chunks (a chunk that fails is bisected). ok(set()) must be true."""
    free = set()

    def try_block(block):
        if not block:
            return
        if ok(free | set(block)):
            free.update(block)
            return
        if len(block) == 1:
            return
        mid = len(block) // 2
        try_block(block[:mid])
        try_block(block[mid:])

    for i in range(0, len(items), chunk):
        try_block(items[i:i + chunk])
    return free


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--component", required=True)
    ap.add_argument("--target", default="*2")
    ap.add_argument("--treatment", default="free (only L/R fixed)", choices=list(TREATMENTS))
    ap.add_argument("--tests", default="lower,upper")
    ap.add_argument("--cap", type=int, default=1200)
    ap.add_argument("--max-new", type=int, default=100)
    ap.add_argument("--per-side", type=int, default=12)
    ap.add_argument("--ext", type=int, default=6)
    ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--max-seconds", type=float, default=1600)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--use-l8", action="store_true",
                    help="trust Lichess's own categories of 8-man positions (labelled l8 in realdb)")
    ap.add_argument("--no-l8-rows", action="store_true",
                    help="ignore realdb rows that may depend on Lichess 8-man categories")
    ap.add_argument("--race-prior", default=None, choices=["count", "mover", "opponent"],
                    help="planning only: fill unresolved race sides by this rule (they then become "
                         "candidates for resolution like the model-filled one-sided terminals)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.setrecursionlimit(100000)
    t_start = time.time()
    from realchess.solve_candidate import Model, RealOracle, OfflineOracle, deepen, is_model_internal, make_order
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    kind, d = TREATMENTS[a.treatment]
    target = {"*2": cgt.nimber(2), "0": cgt.ZERO}[a.target]
    model = Model()
    pr = infra.CertProber(a.cap, tag="certify-iterate", offline=a.offline)
    oracle = OfflineOracle(pr) if a.offline else RealOracle(pr, a.max_new)
    region = lambda pos: "model" if is_model_internal(pos, model) else "off"
    s = DeepSearcher(oracle, order_hint=make_order(model, pr.cached), region=region, cached=pr.cached,
                     kb=infra.kb(), max_nodes=4 * 10**6)
    if a.use_l8:
        s.l8 = True
        s.kb_max_men = 8
    prev = {}
    if os.path.exists(a.out):
        prev = json.load(open(a.out))
    unresolvable = set(prev.get("unresolvable_sides", []))  # fen strings
    log = prev.get("log", [])
    status = "running"
    result = None
    glob = oracle.max_new
    for rnd in range(a.rounds):
        if time.time() - t_start > a.max_seconds:
            status = "stopped: time"
            break
        db = termdb.load()
        if a.no_l8_rows:
            db = {k: v for k, v in db.items() if not v.get("l8")}
        f = {t: side_fens(T, t) for t in T.terms}
        open_raw, base = {}, {}
        filled = []
        for t in T.terms:
            vals_open, vals_base = [], []
            o = owner(T, t)
            for sd in "WB":
                r = db.get(f[t][sd])
                if r is not None:
                    vals_open.append(r["white"])
                    vals_base.append(r["white"])
                else:
                    vals_open.append(None)
                    if f[t][sd] in unresolvable:
                        vals_base.append(None)
                    elif o is not None:
                        vals_base.append(1 if o == "W" else -1)
                    elif a.race_prior:
                        mover = "B" if sd == "W" else "W"
                        vals_base.append(C.model_terminal_value(T.board, t, mover, a.race_prior))
                    else:
                        vals_base.append(None)
            open_raw[t], base[t] = tuple(vals_open), tuple(vals_base)
            if base[t] != open_raw[t]:
                filled.append(t)
        entry = {"round": rnd, "requests_so_far": oracle.new_requests, "ledger": pr.ledger_count(),
                 "resolved_sides": sum(v is not None for t in T.terms for v in open_raw[t]),
                 "model_filled_terminals": len(filled), "unresolvable_sides": len(unresolvable)}
        # unconditional check first
        done = False
        for test in a.tests.split(","):
            if holds_fn(T, kind, d, target, test)(open_raw):
                result = {"certified": True, "test": test,
                          "statement": f"{a.target} excluded with every non-L/R terminal free ({test} test)"}
                done = True
                break
        if done:
            entry["certified"] = result
            log.append(entry)
            print(json.dumps(entry), flush=True)
            status = "certified"
            break
        # plan with the model fill
        plan = None
        for test in a.tests.split(","):
            h = holds_fn(T, kind, d, target, test)
            if not h(base):
                entry[f"{test}_with_model_fill"] = False
                continue
            order = sorted(filled, key=lambda t: (-T.men(t), str(t)))
            free = chunked_greedy(order, lambda F: h({t: (open_raw[t] if t in F else base[t]) for t in T.terms}))
            need = [t for t in filled if t not in free]
            cand = {"test": test, "need": need}
            if plan is None or len(need) < len(plan["need"]):
                plan = cand
            entry[f"{test}_needs"] = dict(sorted(Counter(T.men(t) for t in need).items()))
        if plan is None:
            status = "not excludable with the model fill and the unresolvable sides free"
            entry["status"] = status
            log.append(entry)
            print(json.dumps(entry), flush=True)
            break
        todo = [(t, sd) for t in plan["need"] for sd in "WB"
                if open_raw[t][("WB").index(sd)] is None and f[t][sd] not in unresolvable]
        entry["plan_test"] = plan["test"]
        entry["sides_to_resolve"] = len(todo)
        newrows = []
        try:
            for t, sd in sorted(todo, key=lambda x: (T.men(x[0]), str(x[0]), x[1])):
                pos = C.embed(t, sd)
                oracle.max_new = min(glob, oracle.new_requests + a.per_side)
                try:
                    if pos.men() <= 7:
                        iv, how = s.search(pos, 0), "tablebase (<=7 men)"
                    else:
                        iv, how = deepen(s, pos, a.ext), f"search ({pos.men()} men, ext<={a.ext})"
                except CapReached:
                    if oracle.new_requests >= glob:
                        raise
                    iv, how = (-1, 1), "per-side budget"
                except RuntimeError as e:  # node limit
                    iv, how = (-1, 1), repr(e)
                finally:
                    oracle.max_new = glob
                if iv[0] == iv[1]:
                    r = termdb.make_row(pos, iv, how, a.ext)
                    r.update(terminal=str(t), side=sd, tree=passed_test(), source="iterate",
                             l8=bool(a.use_l8))
                    if a.use_l8:
                        r["how"] += " [may use Lichess 8-man categories]"
                    termdb.append([r])
                    newrows.append((str(t), sd, r["white"], T.men(t)))
                else:
                    unresolvable.add(f[t][sd])
                    newrows.append((str(t), sd, None, T.men(t)))
        except CapReached:
            status = "stopped: --max-new"
            entry["resolved"] = newrows
            log.append(entry)
            print(json.dumps(entry), flush=True)
            break
        entry["resolved"] = newrows
        log.append(entry)
        print(json.dumps(entry), flush=True)
        out = {"component": a.component, "tree": passed_test(), "treatment": a.treatment, "target": a.target,
               "status": status, "result": result, "unresolvable_sides": sorted(unresolvable), "log": log}
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)
    out = {"component": a.component, "tree": passed_test(), "treatment": a.treatment, "target": a.target,
           "status": status, "result": result, "unresolvable_sides": sorted(unresolvable), "log": log,
           "new_requests_this_run": oracle.new_requests, "ledger": pr.ledger_count(),
           "seconds": round(time.time() - t_start, 1)}
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "log"}, indent=1))


if __name__ == "__main__":
    main()
