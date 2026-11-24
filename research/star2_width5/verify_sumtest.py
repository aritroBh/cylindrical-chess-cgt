#!/usr/bin/env python3
"""T21: third implementation check of every *k (k >= 2) hit.

`sumtest/sumsolver.py` is a brute-force outcome solver written from the rules
(whole-board minimax, no canonical forms; it imports neither cylcgt nor
crosscheck).  For a nimber test it is enough to ask for the outcome of G + *j:
G + *j = 0 exactly when G = *j, because negation fixes the nimbers.  So
"G + *k is a second-player win" decides G = *k with no canonical forms at all.

The solver is run in the same model as the C solver (`frontier_split`):
whole-board play, an e.p. right that lives in G and is cleared only by the
next move made in G ("component" scope), and the same race rules.  The
"comp" mode, in which components are summed, is also run, because that is the
model cylcgt implements.

Usage:  PYTHONPATH=. .venv/bin/python research/star2_width5/verify_sumtest.py
"""
import csv
import gzip
import os
import sys

from sumtest.sumsolver import Geometry, Rules, SumSolver, Trees, reference_set

HERE = os.path.dirname(os.path.abspath(__file__))

SETTINGS = (
    ("count", True, False),
    ("count", False, False),
    ("count", True, True),
    ("mover", True, False),
    ("mover", False, False),
    ("mover", True, True),
    ("opponent", True, False),
    ("opponent", False, False),
    ("opponent", True, True),
)
NAMES = ("C/T", "C/off", "C/aware", "M/T", "M/off", "M/aware", "O/T", "O/off", "O/aware")


def read_rows(path):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", newline="") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if row and not row[0].startswith("#"):
                yield row


def collect_hits():
    hits = {}
    total = 0
    for name in sorted(os.listdir(HERE)):
        if not (name.startswith("split_") and (name.endswith(".tsv") or name.endswith(".tsv.gz"))):
            continue
        for row in read_rows(os.path.join(HERE, name)):
            total += 1
            for setting, field in enumerate(row[3:12]):
                k = int(field.split(",", 1)[1])
                if k >= 2:
                    hits.setdefault((k, row[0]), set()).add(setting)
    return hits, total


def outcomes(position, race, ep_on, aware, mode):
    geo = Geometry(5, False)
    trees = Trees()
    ref = reference_set(trees)
    solver = SumSolver(Rules(geo, ep=ep_on, ep_aware=aware, race_rule=race),
                        trees, mode=mode, ep_scope="component")
    W, B = geo.parse(position)
    wl, wr = solver.solve(solver.start_state(W, B))
    return {n: solver.outcome(wl, wr, ref[n]) for n in ("0", "*", "*2", "*3")}


def main():
    hits, total = collect_hits()
    print(f"roots scanned: {total}; distinct *k>=2 hits: {len(hits)}")
    out_path = os.path.join(HERE, "verify_sumtest.tsv")
    disagree = []
    with open(out_path, "w") as out:
        out.write("c_k\tc_setting\tmode\tG\tG+*\tG+*2\tG+*3\tagrees\tposition\n")
        for (k, position), settings in sorted(hits.items()):
            for setting in sorted(settings):
                race, ep_on, aware = SETTINGS[setting]
                for mode in ("whole", "comp"):
                    o = outcomes(position, race, ep_on, aware, mode)
                    # G = *k iff G + *k is a second-player win
                    ok = (o["*2"] == "P") if k == 2 else (o["*3"] == "P")
                    out.write(f"{k}\t{NAMES[setting]}\t{mode}\t{o['0']}\t{o['*']}\t{o['*2']}\t"
                              f"{o['*3']}\t{int(ok)}\t{position}\n")
                    if not ok:
                        disagree.append((k, position, NAMES[setting], mode, o))
    print(f"checks written to {out_path}")
    print(f"disagreements: {len(disagree)}")
    for d in disagree:
        print("  DISAGREE:", d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
