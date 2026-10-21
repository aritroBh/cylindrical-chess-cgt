"""Planning aid (model only, no network): which terminals of a component's
tree must be resolved in real chess to EXCLUDE a target value (default *2)
from the real-chess oracle value, if every resolved terminal turned out as a
model rule predicts and every other terminal is left free in the wide
sandwich [-2BIG, +2BIG]?

Greedy one-sided passes (lower test: free terminals at -2BIG must keep
G_lo not <= target; upper test: free at +2BIG must keep target not <= G_hi),
freeing the terminals with the most men first. The result is only a plan:
the real classes may differ from the prior.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.plan --component "W: a3 b3 c2 / B: b5 b7 c6" --prior count
Run from the e.p.-aware worktree (cwd) for the e.p.-aware tree.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from realchess import component as C
from realchess.oracle_value import (G_BIG2, G_NBIG2, TREATMENTS, Terminals, pair_game)


def prior_results(T: Terminals, rule: str):
    """(rw, rb) White's view for every terminal under the model rule:
    rw = White moves first (so Black entered it), rb = Black moves first."""
    out = {}
    for t in T.terms:
        rw = C.model_terminal_value(T.board, t, "B", rule)
        rb = C.model_terminal_value(T.board, t, "W", rule)
        out[t] = (rw, rb)
    return out


def greedy(T, games, target, test, order):
    """Smallest-ish set of terminals to keep fixed (at `games`) so that the
    one-sided exclusion `test` still holds with the others free."""
    free_g = G_NBIG2 if test == "lower" else G_BIG2

    def holds(free):
        g = T.value(lambda t: free_g if t in free else games[t])
        return (not cgt.le(g, target)) if test == "lower" else (not cgt.le(target, g))

    if not holds(set()):
        return None
    free = set()
    for t in order:
        free.add(t)
        if not holds(free):
            free.discard(t)
    return [t for t in T.terms if t not in free]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--prior", default="count")
    ap.add_argument("--treatment", default="switch, draw = Black win", choices=list(TREATMENTS))
    ap.add_argument("--target", default="*2")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    kind, d = TREATMENTS[a.treatment]
    pr = prior_results(T, a.prior)
    games = {t: pair_game(*pr[t], kind, d) for t in T.terms}
    target = {"*2": cgt.nimber(2), "0": cgt.ZERO}[a.target]
    g_prior = T.value(lambda t: games[t])
    out = {"component": a.component,
           "passed_test": "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook",
           "prior": a.prior, "treatment": a.treatment, "target": a.target,
           "value_with_prior": cgt.show(g_prior), "internal": len(T.internal), "terminals": len(T.terms),
           "terminals_by_men": dict(sorted(Counter(T.men(t) for t in T.terms).items()))}
    order = sorted(T.terms, key=lambda t: (-T.men(t), str(t)))
    for test in ("lower", "upper"):
        need = greedy(T, games, target, test, order)
        if need is None:
            out[test] = "test fails even with every terminal at the prior"
            continue
        out[test] = {"needed": len(need), "needed_by_men": dict(sorted(Counter(T.men(t) for t in need).items())),
                     "terminals": [{"terminal": str(t), "men": T.men(t), "prior_rw_rb": pr[t]} for t in
                                   sorted(need, key=lambda t: (T.men(t), str(t)))]}
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)
    brief = {k: (v if not isinstance(v, dict) or "terminals" not in v else
                 {kk: vv for kk, vv in v.items() if kk != "terminals"}) for k, v in out.items()}
    print(json.dumps(brief, indent=1))


if __name__ == "__main__":
    main()
