"""Stops of the sandwich bounds (offline): stops are monotone, so
LeftStop(G) >= LeftStop(G_lo) and RightStop(G) <= RightStop(G_hi).

    PYTHONPATH=. .venv/bin/python -m realchess.stops_check --label _epaware_offline
"""
import argparse
import json

from cylcgt import cgt

from .oracle_value import TREATMENTS, sandwich
from .pin import load


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--label", required=True)
    a = ap.parse_args()
    comp, T, raw, byname, path = load(a.component, "pure", a.label)
    out = {"input": path.split("/")[-1]}
    for name, (kind, d) in TREATMENTS.items():
        g_lo, g_hi = sandwich(T, raw, kind, d)
        out[name] = {"stops(G_lo)": [str(x) for x in cgt.stops(g_lo)],
                     "stops(G_hi)": [str(x) for x in cgt.stops(g_hi)]}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
