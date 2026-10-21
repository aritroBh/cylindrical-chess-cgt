"""Which model-filled terminals must be checked in real chess for the
exclusion of a target (default *2) to hold with them FREE instead?

Start (policy "one-sided model-filled, races free" of oracle10.py): resolved
sides from realdb.jsonl, unresolved sides of one-sided terminals filled with
the model (win for the passer's owner), unresolved race sides free. If the
one-sided test (lower: G_lo not <= target; upper: target not <= G_hi) holds,
greedily free the model-filled terminals (most men first) while it still
holds. The terminals left are the ones whose model verdict the exclusion
still relies on; resolving them (and finding the model right) would make the
exclusion unconditional.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.need --component "W: a3 b2 c2 / B: a4 b6 c5" \
        --treatment "free (only L/R fixed)"
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess import component as C
from realchess.oracle_value import TREATMENTS, Terminals, interval_of

from . import termdb
from .oracle10 import passed_test, raw_from_db, side_fens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--treatment", default="free (only L/R fixed)", choices=list(TREATMENTS))
    ap.add_argument("--target", default="*2")
    ap.add_argument("--tests", default="lower,upper")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    comp = Pos.parse(a.component)
    T = Terminals(comp)
    db = termdb.load()
    kind, d = TREATMENTS[a.treatment]
    target = {"*2": cgt.nimber(2), "0": cgt.ZERO}[a.target]
    raw_filled, _ = raw_from_db(T, db, "model")
    raw_open, _ = raw_from_db(T, db, "none")
    from .oracle10 import is_race
    base = {t: (raw_filled[t] if not is_race(T, t) else raw_open[t]) for t in T.terms}
    filled = [t for t in T.terms if base[t] != raw_open[t]]
    out = {"component": a.component, "tree": passed_test(), "treatment": a.treatment, "target": a.target,
           "model_filled_terminals": len(filled),
           "model_filled_by_men": dict(sorted(Counter(T.men(t) for t in filled).items()))}
    for test in a.tests.split(","):
        low = test == "lower"

        def holds(free):
            def g(t):
                rw, rb = raw_open[t] if t in free else base[t]
                lo, hi = interval_of(rw, rb, kind, d)
                return lo if low else hi
            v = T.value(g)
            return (not cgt.le(v, target)) if low else (not cgt.le(target, v))

        if not holds(set()):
            out[test] = "does not hold even with the model fill"
            print(test, out[test], flush=True)
            continue
        free = set()
        order = sorted(filled, key=lambda t: (-T.men(t), str(t)))
        for i, t in enumerate(order):
            free.add(t)
            if not holds(free):
                free.discard(t)
        need = [t for t in filled if t not in free]
        out[test] = {"needed": len(need), "needed_by_men": dict(sorted(Counter(T.men(t) for t in need).items())),
                     "terminals": [{"terminal": str(t), "men": T.men(t), "model_rw_rb": base[t],
                                    "real_rw_rb": raw_open[t], "fen_W": side_fens(T, t)["W"],
                                    "fen_B": side_fens(T, t)["B"]}
                                   for t in sorted(need, key=lambda t: (T.men(t), str(t)))]}
        print(test, json.dumps({k: v for k, v in out[test].items() if k != "terminals"}), flush=True)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
