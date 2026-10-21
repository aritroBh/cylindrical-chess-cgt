"""Pinning and excluding the real-chess oracle value (offline; reads the
results of `solve_candidate oracle-all`).

Subcommands
  pin      1. greedy estimate: which incomplete terminal sides must be known
              to pin the value, if every unknown side were as the cylcgt model
              predicts (count rule)? (A planning aid; no claim rests on it.)
           2. certificate: enumerate the essential sides that are still open
              over EVERY possible result (win / draw / loss), with all other
              incomplete terminals free in their monotone sandwich. A case is
              pinned when G_lo == G_hi. If every case is pinned to the same
              game, that game is the value, whatever the open sides are.
  exclude  one-sided exclusion certificate of a target game, enumerating the
           minimal (lower test) or maximal (upper test) possible games of a
           chosen set of ambiguous partial terminals (default: the e.p.
           partials), everything else in the sandwich.

    PYTHONPATH=. .venv/bin/python -m realchess.pin pin --label _epaware_offline \
        --treatment "switch, draw = Black win"
    PYTHONPATH=. .venv/bin/python -m realchess.pin exclude --label _textbook_offline \
        --treatment "switch, draw = Black win" --test lower --target "*2"

For the e.p.-aware tree run it from inside the e.p.-aware worktree (cwd), with
PYTHONPATH=<worktree>:<project root>, because `python -m` puts the working
directory first on sys.path.
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import time
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from . import component as C
from .oracle_value import (TREATMENTS, Terminals, ambiguous_partials, interval_of, pair_game,
                           one_sided_certificate, sandwich)
from .solve_candidate import RESULTS, tag_of, write_json


def load(component, mode, label):
    comp = Pos.parse(component)
    T = Terminals(comp)
    path = os.path.join(RESULTS, f"{tag_of(comp)}_oracleall_{mode}{label}.json")
    d = json.load(open(path))
    byname = {str(t): t for t in T.terms}
    if set(byname) != {r["terminal"] for r in d["terminals"]}:
        raise SystemExit(f"{path} was made with a different terminal set (other passed-pawn test?)")
    raw = {byname[r["terminal"]]: (r["real_W_first"], r["real_B_first"]) for r in d["terminals"]}
    return comp, T, raw, byname, path


def greedy_needed(T, raw, kind, dr):
    prior = {t: C.model_terminal_value(T.board, t, next(iter(T.movers[t])), "count") for t in T.terms}
    fill = {t: tuple(v if v is not None else prior[t] for v in raw[t]) for t in T.terms}
    guess = {t: pair_game(*fill[t], kind, dr) for t in T.terms}
    iv = {t: interval_of(*raw[t], kind, dr) for t in T.terms}
    target = T.value(lambda t: guess[t])
    incomplete = sorted([t for t in T.terms if None in raw[t]], key=lambda t: (-T.men(t), str(t)))
    free = set()
    for t in incomplete:
        free.add(t)
        if T.value(lambda x: iv[x][0] if x in free else guess[x]) is not target or \
                T.value(lambda x: iv[x][1] if x in free else guess[x]) is not target:
            free.discard(t)
    need = [t for t in incomplete if t not in free]
    sides = [(t, s) for t in need for s, v in zip("WB", raw[t]) if v is None]
    return target, incomplete, sides


def cmd_pin(a):
    kind, dr = TREATMENTS[a.treatment]
    comp, T, raw, byname, path = load(a.component, a.mode, a.label)
    t0 = time.time()
    guess, incomplete, sides = greedy_needed(T, raw, kind, dr)
    out = {"input": os.path.basename(path), "treatment": a.treatment,
           "passed_test": "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook",
           "greedy": {"guess_value_unknown_sides_from_model": cgt.show(guess),
                      "incomplete_terminals": len(incomplete),
                      "essential_open_sides": [(str(t), s, T.men(t)) for t, s in sides]}}
    # distinct results per open side: under a "switch" treatment a draw is
    # mapped onto draw_as, so only +1 / -1 matter there
    results = (1, -1) if kind == "switch" else (1, 0, -1)
    if len(results) ** len(sides) > a.max_cases:
        out["certificate"] = (f"not attempted: {len(results)}^{len(sides)} cases > --max-cases {a.max_cases}")
    else:
        cases = []
        shard_i, shard_n = (int(x) for x in a.shard.split("/"))
        for k, combo in enumerate(itertools.product(results, repeat=len(sides))):
            if k % shard_n != shard_i:
                continue
            r2 = dict(raw)
            for (t, s), v in zip(sides, combo):
                rw, rb = r2[t]
                r2[t] = (v, rb) if s == "W" else (rw, v)
            g_lo, g_hi = sandwich(T, r2, kind, dr)
            cases.append({"open_side_results_white_view": {f"{t} {s}-first": v for (t, s), v in zip(sides, combo)},
                          "pinned": g_lo is g_hi, "G_lo": cgt.show(g_lo), "G_hi": cgt.show(g_hi)})
        vals = {c["G_lo"] for c in cases if c["pinned"]}
        allpinned = all(c["pinned"] for c in cases)
        out["certificate"] = {
            "shard": a.shard, "results_per_open_side": list(results),
            "cases": len(cases), "pinned_cases": sum(c["pinned"] for c in cases),
            "values_of_pinned_cases": sorted(vals),
            "value_certified": (next(iter(vals)) if allpinned and len(vals) == 1 else None),
            "overall_lower_bound_candidates": sorted({c["G_lo"] for c in cases}),
            "overall_upper_bound_candidates": sorted({c["G_hi"] for c in cases}),
            "cases_detail": cases}
    out["seconds"] = round(time.time() - t0, 1)
    tn = a.treatment.replace(", ", "_").replace(" = ", "_").replace(" ", "_")
    sh = "" if a.shard == "0/1" else "__shard" + a.shard.replace("/", "of")
    write_json(os.path.join(RESULTS, f"{tag_of(comp)}_pin{a.label}__{tn}{sh}.json"), out)
    brief = dict(out)
    if isinstance(brief.get("certificate"), dict):
        brief["certificate"] = {k: v for k, v in out["certificate"].items() if k != "cases_detail"}
    print(json.dumps(brief, indent=1))


EP_PARTIALS = ["W: a2 c4 / B: b7 d4 (ep c3)", "W: a2 c5 / B: b7 d5 (ep d6)", "W: a3 c4 / B: b5 d4 (ep c3)",
               "W: a3 c5 / B: b7 d5 (ep d6)", "W: a4 c2 / B: b4 d7 (ep a3)", "W: a4 c5 / B: b7 d5 (ep d6)",
               "W: a5 c2 / B: b5 d7 (ep b6)", "W: a5 c4 / B: b5 d6 (ep b6)", "W: a5 c4 / B: b5 d7 (ep b6)"]


def cmd_exclude(a):
    kind, dr = TREATMENTS[a.treatment]
    comp, T, raw, byname, path = load(a.component, a.mode, a.label)
    target = {"*2": cgt.nimber(2), "0": cgt.ZERO}[a.target]
    amb = ambiguous_partials(T, raw, kind, dr)
    names = a.set.split(";") if a.set else EP_PARTIALS
    S = [byname[x] for x in names if x in byname and byname[x] in amb]
    t0 = time.time()
    ok, n = one_sided_certificate(T, raw, target, kind, dr, S, a.test)
    out = {"input": os.path.basename(path), "treatment": a.treatment, "test": a.test, "target": a.target,
           "ambiguous_partials": len(amb), "enumerated": [str(t) for t in S], "combinations": n,
           "excludes_target": ok, "seconds": round(time.time() - t0, 1)}
    print(json.dumps(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["pin", "exclude"])
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--mode", default="pure")
    ap.add_argument("--label", required=True, help="label of the oracle-all results, e.g. _epaware_offline")
    ap.add_argument("--treatment", required=True, choices=list(TREATMENTS))
    ap.add_argument("--max-cases", type=int, default=729, help="pin: enumerate at most this many cases")
    ap.add_argument("--shard", default="0/1", help="pin: i/n, enumerate only cases with index %% n == i")
    ap.add_argument("--test", choices=["lower", "upper"], default="lower")
    ap.add_argument("--target", choices=["*2", "0"], default="*2")
    ap.add_argument("--set", default=None, help="exclude: ';'-separated terminal names to enumerate")
    a = ap.parse_args()
    {"pin": cmd_pin, "exclude": cmd_exclude}[a.cmd](a)


if __name__ == "__main__":
    main()
