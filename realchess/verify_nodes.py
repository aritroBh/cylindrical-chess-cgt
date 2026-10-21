"""Re-prove, with the independent AND/OR prover of verify_proof.py, every win
and loss that the main search reported for the model nodes (offline).

    PYTHONPATH=. .venv/bin/python -m realchess.verify_nodes --label _offline --depth 12
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter

from cylcgt.pawns import Pos

from . import movegen as mg
from .kb import default_kb
from .solve_candidate import RESULTS, tag_of, write_json
from .verify_proof import Prover, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--mode", default="pure")
    ap.add_argument("--label", default="_offline")
    ap.add_argument("--depth", type=int, default=12)
    ap.add_argument("--oracleall", default=None,
                    help="instead: the 8-man terminal results of this oracle-all JSON (file name in results/)")
    a = ap.parse_args()
    sys.setrecursionlimit(100000)
    tag = tag_of(Pos.parse(a.component))
    kb = default_kb()
    P = Prover(kb=kb)
    tally, rows = Counter(), []
    items = []  # (fen, value for side to move)
    if a.oracleall:
        d = json.load(open(os.path.join(RESULTS, a.oracleall)))
        for r in d["terminals"]:
            if r["men"] < 8:
                continue
            for side, key in (("W", "real_W_first"), ("B", "real_B_first")):
                v = r[key]
                if v is not None:
                    items.append((r["fen_" + side], v if side == "W" else -v))
        src = a.oracleall
    else:
        d = json.load(open(os.path.join(RESULTS, f"{tag}_nodes_{a.mode}{a.label}.json")))
        for r in d["nodes"]:
            for side in "WB":
                fen, iv = r.get(side + "_fen"), r.get(side)
                if fen and iv and iv[0] == iv[1]:
                    items.append((fen, iv[0]))
        src = f"{tag}_nodes_{a.mode}{a.label}.json"
    l8 = Counter()
    for fen, v in items:
        c = kb.category(fen)  # Lichess's own 8-man category, if it gave one
        if c is not None:
            l8["agree" if {"win": 1, "draw": 0, "loss": -1}[c] == v else "DISAGREE"] += 1
        else:
            l8["no Lichess category"] += 1
        if v == 0:
            tally["draw (not re-provable by this prover)"] += 1
            continue
    for fen, v in items:
        if v == 0:
            continue
        if True:
            claim = "win" if v == 1 else "loss"
            cert = P.prove(mg.parse_fen(fen), claim, a.depth)
            ok = cert is not None
            # the opposite claim must NOT be provable
            opp = P.prove(mg.parse_fen(fen), "loss" if claim == "win" else "win", a.depth)
            tally[(claim, ok, opp is not None)] += 1
            rows.append({"fen": fen, "claim": claim, "proved": ok,
                         "opposite_proved": opp is not None, **(stats(cert) if ok else {})})
    out = {"input": src, "depth": a.depth,
           "tally": {(f"{k[0]}: proved={k[1]}, opposite proved={k[2]}" if isinstance(k, tuple) else k): n
                     for k, n in tally.items()},
           "vs_lichess_8man_category": dict(l8),
           "rows": rows}
    name = (f"{tag}_terminals8_verified_{a.oracleall.split('oracleall_')[-1]}" if a.oracleall
            else f"{tag}_nodes_verified{a.label}.json")
    write_json(os.path.join(RESULTS, name), out)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
