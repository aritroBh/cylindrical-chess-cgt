"""Merge newly resolved terminal sides into the A2-realchess oracle-all file
of W a2 c2 / B b7 d7 (read-only input in realchess/results) and write the
merged copy into realchess/certify/results, so that realchess.pin (patched by
certify.run to read and write here) can re-run the pins.

Sources of new results (exact only):
  * realchess/certify/results/realdb.jsonl (termdb);
  * the outputs of `solve_candidate resolve` given with --resolve (position
    rows with an exact interval);
  * the knowledge base (<= 7-man categories in any cached record).

    PYTHONPATH=. .venv/bin/python -m realchess.certify.orig_update --label _epaware_offline \
        --resolve realchess/certify/results/comp_Wa2c2_Bb7d7_draw0_sides_resolve.json
Output label: <label>_certify.
"""
from __future__ import annotations

import argparse
import json
import os

from realchess import movegen as mg

from . import infra, termdb

SRC = os.path.join(infra.REALCHESS, "results")
TAG = "comp_Wa2c2_Bb7d7"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, help="_textbook_offline or _epaware_offline")
    ap.add_argument("--resolve", action="append", default=[])
    a = ap.parse_args()
    src = os.path.join(SRC, f"{TAG}_oracleall_pure{a.label}.json")
    d = json.load(open(src))
    known = {}
    for fen, r in termdb.load().items():
        known[fen] = (r["white"], "certify realdb: " + r["how"])
    for p in a.resolve:
        for row in json.load(open(p))["positions"]:
            iv = row["interval"]
            if iv[0] == iv[1]:
                pos = mg.parse_fen(row["fen"])
                known[row["fen"]] = (iv[0] if pos.stm == mg.WHITE else -iv[0],
                                     f"certify resolve ({os.path.basename(p)})")
    k = infra.kb()
    added = []
    for r in d["terminals"]:
        for s, key in (("W", "real_W_first"), ("B", "real_B_first")):
            if r[key] is not None:
                continue
            fen = r["fen_" + s]
            v = None
            if fen in known:
                v, how = known[fen]
            else:
                pos = mg.parse_fen(fen)
                if pos.men() <= 7:
                    c = k.category(pos)
                    if c in ("win", "loss", "draw"):
                        x = {"win": 1, "loss": -1, "draw": 0}[c]
                        v, how = (x if pos.stm == mg.WHITE else -x), "certify kb (<=7 men)"
            if v is not None:
                r[key] = v
                r["how_" + s] = how
                added.append((r["terminal"], s, v, how))
    d["certify_merge"] = {"source": os.path.relpath(src, infra.REALCHESS), "added_sides": added}
    out = os.path.join(infra.RESULTS, f"{TAG}_oracleall_pure{a.label}_certify.json")
    with open(out, "w") as fh:
        json.dump(d, fh, indent=1)
    print(json.dumps({"out": out, "added": len(added), "rows": added}, indent=1))


if __name__ == "__main__":
    main()
