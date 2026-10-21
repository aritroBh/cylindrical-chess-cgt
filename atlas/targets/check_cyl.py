#!/usr/bin/env python3
"""Validate pcgt on cylinders (and flat strips up to 8 files) against the
cylinder atlas (atlas/cylinder/values.jsonl + value_index.jsonl; cylcgt,
textbook passed test, count rule, e.p. on), comparing exact canonical keys.

Usage (from the project root):
  .venv/bin/python atlas/targets/check_cyl.py prepare   # writes work/cyl_atlas_positions.tsv
  atlas/targets/pcgt < atlas/targets/work/cyl_atlas_positions.tsv > atlas/targets/work/pcgt_cyl_atlas.tsv
  .venv/bin/python atlas/targets/check_cyl.py compare
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ATLAS = os.path.join(ROOT, "atlas", "cylinder")


def prepare():
    rows = []
    with open(os.path.join(ATLAS, "values.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            rows.append((r["n"], 1 if r["board"] == "cyl" else 0, r["pos"]))
    rows.sort()
    with open(os.path.join(HERE, "work", "cyl_atlas_positions.tsv"), "w") as fh:
        for n, wrap, p in rows:
            fh.write(f"{p}\t{n}\t{wrap}\n")
    print(len(rows), "positions")


def compare():
    keys = {}
    with open(os.path.join(ATLAS, "value_index.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            keys[r["vid"]] = r["key"]
    mine, vals = {}, {}
    with open(os.path.join(HERE, "work", "pcgt_cyl_atlas.tsv")) as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if p[0] == "#V":
                vals[int(p[1])] = p[5]
            else:
                mine[(p[0], int(p[1]), int(p[2]))] = int(p[6])
    n = bad = miss = 0
    by = {}
    ex = []
    with open(os.path.join(ATLAS, "values.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            k = (r["pos"], r["n"], 1 if r["board"] == "cyl" else 0)
            n += 1
            if k not in mine:
                miss += 1
                continue
            ok = vals[mine[k]] == keys[r["vid"]]
            t = by.setdefault((r["board"], r["n"]), [0, 0])
            t[0] += 1
            if not ok:
                bad += 1
                t[1] += 1
                if len(ex) < 5:
                    ex.append((r["board"], r["n"], r["pos"], keys[r["vid"]][:60], vals[mine[k]][:60]))
    print(f"cylinder atlas: {n} positions, missing {miss}, exact-key mismatches {bad}")
    for k in sorted(by):
        print(f"  {k[0]:4s} n={k[1]}: {by[k][0]} positions, {by[k][1]} mismatches")
    for e in ex:
        print("  ", e)


if __name__ == "__main__":
    {"prepare": prepare, "compare": compare}[sys.argv[1]]()
