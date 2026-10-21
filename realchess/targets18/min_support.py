"""Which unresolved terminals decide the real-chess oracle value of a component?

Start from the model-filled assignment (every unresolved one-sided side = a win for
the passer's owner, races by the count rule), under which the value is pinned.
Then free unresolved terminals one at a time (9-man first), keeping a terminal
free whenever the monotone sandwich still pins the same value. The terminals
that cannot be freed are the ones a certificate must resolve.

    PYTHONPATH=. .venv/bin/python realchess/targets18/min_support.py "W: a2 b2 b3 / B: a5 a6 b6" \
        --out realchess/targets18/min_support.json
"""
import argparse
import json
import time

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess.certify import termdb
from realchess.certify.oracle10 import raw_from_db
from realchess.oracle_value import TREATMENTS
from realchess.oracle_value import Terminals, sandwich

ap = argparse.ArgumentParser()
ap.add_argument("component")
ap.add_argument("--treatment", default="free (only L/R fixed)")
ap.add_argument("--race-rule", default="count")
ap.add_argument("--out", default=None)
a = ap.parse_args()

T = Terminals(Pos.parse(a.component))
db = termdb.load()
raw_none, _ = raw_from_db(T, db, "none", None)
raw_model, _ = raw_from_db(T, db, "model", a.race_rule)
kind, d = TREATMENTS[a.treatment]


def pinned(raw):
    lo, hi = sandwich(T, raw, kind, d)
    return (lo if lo is hi else None), lo, hi


val, lo, hi = pinned(raw_model)
assert val is not None, f"not pinned even when model-filled: {cgt.show(lo)} .. {cgt.show(hi)}"
lo0, hi0 = sandwich(T, raw_none, kind, d)
print(f"model-filled value {cgt.show(val)}; with only resolved sides fixed: {cgt.show(lo0)} .. {cgt.show(hi0)}")

# terminals whose assignment differs between "resolved only" and "model-filled"
cands = [t for t in T.terms if raw_model.get(t) != raw_none.get(t)]
cands.sort(key=lambda t: (-T.men(t), str(t)))
print(f"{len(cands)} terminals carry model-filled sides", flush=True)

raw = dict(raw_model)
needed = []
t0 = time.time()
for i, t in enumerate(cands):
    trial = dict(raw)
    if t in raw_none:
        trial[t] = raw_none[t]
    else:
        trial.pop(t, None)
    v, _, _ = pinned(trial)
    if v is val:
        raw = trial
    else:
        needed.append(t)
    if i % 50 == 0:
        print(f"  {i}/{len(cands)} examined, {len(needed)} needed, {time.time() - t0:.0f}s", flush=True)

v, lo, hi = pinned(raw)
assert v is val
out = {"component": a.component, "treatment": a.treatment, "race_rule_for_fill": a.race_rule,
       "value_if_needed_sides_as_model": cgt.show(val),
       "bounds_with_resolved_only": [cgt.show(lo0), cgt.show(hi0)],
       "candidates": len(cands), "needed": len(needed),
       "needed_terminals": [{"terminal": str(t), "men": T.men(t), "model_assignment": str(raw_model.get(t))}
                            for t in needed]}
print(json.dumps(out, indent=1))
if a.out:
    json.dump(out, open(a.out, "w"), indent=1)
