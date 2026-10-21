"""Randomised sanity check of the sandwich/pin logic (offline): give every
unresolved terminal side a random result (win / draw / loss, White's view),
keep every resolved side, build the replacement games with the treatment and
compute the value directly. Every sample must lie in [G_lo, G_hi] and, where
a value was certified, equal it. A check of the code, not a proof.

    PYTHONPATH=. .venv/bin/python -m realchess.random_check --label _epaware_offline \
        --treatment "switch, draw = Black win" --samples 40 --certified "{2±1 | -2±1}"
"""
import argparse
import json
import random

from cylcgt import cgt

from .oracle_value import TREATMENTS, pair_game, sandwich
from .pin import load


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--mode", default="pure")
    ap.add_argument("--label", required=True)
    ap.add_argument("--treatment", required=True, choices=[k for k, v in TREATMENTS.items() if v[0] != "free"])
    ap.add_argument("--samples", type=int, default=40)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--certified", default=None)
    a = ap.parse_args()
    kind, dr = TREATMENTS[a.treatment]
    comp, T, raw, byname, path = load(a.component, a.mode, a.label)
    g_lo, g_hi = sandwich(T, raw, kind, dr)
    rng = random.Random(a.seed)
    seen, inside, match = {}, 0, 0
    for _ in range(a.samples):
        full = {t: tuple(v if v is not None else rng.choice((1, 0, -1)) for v in raw[t]) for t in T.terms}
        g = T.value(lambda t: pair_game(*full[t], kind, dr))
        seen[cgt.show(g)] = seen.get(cgt.show(g), 0) + 1
        inside += cgt.le(g_lo, g) and cgt.le(g, g_hi)
        match += a.certified is not None and cgt.show(g) == a.certified
    print(json.dumps({"input": path.split("/")[-1], "treatment": a.treatment, "samples": a.samples,
                      "inside_sandwich": inside, "equal_to_certified": match if a.certified else None,
                      "values_seen": seen}, ensure_ascii=False))


if __name__ == "__main__":
    main()
