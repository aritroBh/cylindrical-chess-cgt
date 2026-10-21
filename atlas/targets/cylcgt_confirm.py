#!/usr/bin/env python3
"""Confirm headline values with cylcgt itself (Python, read-only), independently of pcgt.

Runs cylcgt.pawns.value on the flat board of the given width under one setting.
The e.p.-aware passed test is taken from the ep-aware-passed worktree (flag
PASSED_RESPECTS_EP); --textbook sets the flag False (= the main checkout's test).

Usage (from the project root):
  .venv/bin/python atlas/targets/cylcgt_confirm.py --race count --ep 1 [--textbook] [--wrap] \
      "W: a4 b3 d2 d3 / B: a7 b7 c5" 4  ["pos" width ...]
"""
import argparse
import json
import sys
import time

EPWT = "/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt"
sys.path.insert(0, EPWT)
from cylcgt import cgt, pawns  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--race", default="count")
ap.add_argument("--ep", type=int, default=1)
ap.add_argument("--textbook", action="store_true")
ap.add_argument("--wrap", action="store_true")
ap.add_argument("items", nargs="+")
a = ap.parse_args()
pawns.PASSED_RESPECTS_EP = not a.textbook
pawns.RACE_RULE = a.race
pawns._value.cache_clear()
for i in range(0, len(a.items), 2):
    p, w = a.items[i], int(a.items[i + 1])
    t0 = time.process_time()
    g = pawns.value(pawns.Board(w, 8, a.wrap, bool(a.ep)), pawns.Pos.parse(p))
    print(json.dumps({"position": p, "width": w, "wrap": a.wrap, "race": a.race, "ep": a.ep,
                      "passed_test": "textbook" if a.textbook else "aware", "value": cgt.show(g),
                      "outcome": cgt.outcome(g), "cpu_s": round(time.process_time() - t0, 1),
                      "module": pawns.__file__}, ensure_ascii=False), flush=True)
