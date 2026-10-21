#!/usr/bin/env python3
"""Random-sample validation of pcgt against cylcgt (Python, read-only) for the
settings the full-database checks do not cover: the e.p.-aware test with the mover
and opponent rules, cylinders under the e.p.-aware test, and width 5 (both tests).
(The full checks: check_db.py, check_cyl.py, check_sens.py.)

cylcgt is loaded from the ep-aware-passed worktree; PASSED_RESPECTS_EP is set per
setting (False = the main checkout's textbook test). cylcgt has no all-White /
all-Black race rule, so those two pcgt rules are checked only through nimscan.

Usage (from the project root):
  PYTHONPATH= .venv/bin/python atlas/targets/validate_sample.py SCOPE N SEED
"""
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EPWT = "/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt"
sys.path.insert(0, EPWT)
from cylcgt import cgt, pawns  # noqa: E402

sys.path.insert(1, HERE)
from check_db import norm_show  # noqa: E402


def main():
    scope, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if scope == "db":
        combos = [(0, "count", 1, 1), (0, "mover", 1, 1), (0, "opponent", 1, 1), (1, "count", 1, 1),
                  (1, "mover", 1, 1), (1, "opponent", 1, 1), (1, "mover", 1, 0), (1, "opponent", 0, 0)]
    else:
        combos = [(0, "count", 1, 0), (0, "count", 1, 1), (0, "mover", 1, 1), (0, "opponent", 0, 0),
                  (1, "count", 1, 1), (1, "count", 1, 0)]
    want = set(combos)
    rows, vals = {}, {}
    with open(os.path.join(HERE, "work", f"run_{scope}.tsv")) as fh:
        for line in fh:
            q = line.rstrip("\n").split("\t")
            if q[0] == "#V":
                vals[int(q[1])] = q[4]
                continue
            c = (int(q[2]), q[3], int(q[4]), int(q[5]))
            if c in want:
                rows.setdefault(c, []).append((q[0], int(q[1]), int(q[6])))
    rng = random.Random(seed)
    tot = bad = skipped = 0
    out = []
    for c in combos:
        wrap, race, ep, aw = c
        sample = rng.sample(rows[c], min(n, len(rows[c])))
        pawns.PASSED_RESPECTS_EP = bool(aw)
        pawns.RACE_RULE = race
        pawns._value.cache_clear()
        nb = 0
        t0 = time.process_time()
        for p, w, gid in sample:
            mine = vals[gid]
            if mine == "-":
                skipped += 1
                continue
            g = pawns.value(pawns.Board(w, 8, bool(wrap), bool(ep)), pawns.Pos.parse(p))
            ok = norm_show(cgt.show(g)) == mine
            tot += 1
            nb += not ok
            if not ok:
                out.append({"combo": c, "position": p, "width": w, "cylcgt": norm_show(cgt.show(g))[:80], "pcgt": mine[:80]})
        bad += nb
        print(f"{scope} wrap={wrap} {race} ep={ep} aware={aw}: {len(sample)} sampled, mismatches {nb}, "
              f"{time.process_time() - t0:.0f} cpu-s", flush=True)
    print(json.dumps({"scope": scope, "compared": tot, "mismatches": bad, "skipped_huge": skipped, "examples": out[:5]}))


if __name__ == "__main__":
    main()
