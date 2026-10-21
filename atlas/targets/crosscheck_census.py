#!/usr/bin/env python3
"""Compare pcgt with the independent C census (work/nimscan_copy --max 7: a copy of
atlas/flat8/rerun/nimscan.c with one enumeration-bound patch) on every flat
position of widths 1-4 with up to 7 pawns: outcome class and nimber column
(G = *k, k <= 15, else -1) under 9 settings.

Usage (from the project root):
  atlas/targets/work/nimscan_copy --max 7 > atlas/targets/work/nimscan_census_max7.tsv
  PYTHONPATH=. .venv/bin/python atlas/targets/crosscheck_census.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402

COLS = {"count/epon": ("count", 1, 0), "count/epoff": ("count", 0, 0), "count/epon/aware": ("count", 1, 1),
        "mover/epon": ("mover", 1, 0), "mover/epoff": ("mover", 0, 0), "mover/epon/aware": ("mover", 1, 1),
        "opponent/epon": ("opponent", 1, 0), "opponent/epoff": ("opponent", 0, 0),
        "opponent/epon/aware": ("opponent", 1, 1)}


def norm(p, w):
    return min(p, C.mirror(p, w))


def main():
    pc = {}
    nimstats = Counter()
    for scope in ("db", "n7"):
        run = C.Run(os.path.join(C.WORK, f"run_{scope}.tsv"))
        with C.opener(os.path.join(C.WORK, f"classes_{scope}.json")) as fh:
            classes = {int(k): v for k, v in json.load(fh).items()}
        for i in range(len(run.pos)):
            k = (norm(run.pos[i], run.width[i]), run.width[i])
            d = {}
            for col, s in COLS.items():
                gid = run.g(i, 0, s)
                c = classes.get(gid)
                nim = -1
                if c is not None:
                    if c["cls"] == "nimber":
                        nim = c["nim"]
                    elif c["cls"] == "integer" and c["num"] == "0":
                        nim = 0
                d[col] = (run.o(i, 0, s), nim)
            pc[k] = d
        del run
    n = bad_o = bad_n = missing = 0
    ex = []
    with C.opener(os.path.join(C.WORK, "nimscan_census_max7.tsv")) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        names = header[3:]
        for line in fh:
            p = line.rstrip("\n").split("\t")
            w = int(p[1])
            k = (norm(p[0], w), w)
            if k not in pc:
                missing += 1
                continue
            n += 1
            for nm, cell in zip(names, p[3:]):
                o, kk = cell.split(",")
                mo, mn = pc[k][nm]
                if o != mo:
                    bad_o += 1
                    if len(ex) < 5:
                        ex.append((p[0], w, nm, o, mo))
                if int(kk) != mn:
                    bad_n += 1
                    if len(ex) < 5:
                        ex.append((p[0], w, nm, kk, mn))
                if int(kk) >= 2:
                    nimstats[(nm, int(kk), int(p[2]))] += 1
    res = {"positions_compared": n, "census_positions_not_in_pcgt_runs": missing, "pcgt_positions": len(pc),
           "outcome_mismatches": bad_o, "nimber_mismatches": bad_n, "settings": list(COLS),
           "census_nimbers_k_ge_2": {f"{a} *{b} ({c} pawns)": v for (a, b, c), v in sorted(nimstats.items())}}
    with open(os.path.join(HERE, "crosscheck_census.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    for e in ex:
        print("  example mismatch", e)


if __name__ == "__main__":
    main()
