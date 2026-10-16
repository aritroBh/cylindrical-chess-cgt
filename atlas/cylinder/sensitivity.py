"""Race-rule and en-passant sensitivity of chosen positions.

For each position, the value is recomputed under the three race rules
("count", "mover", "opponent") with en passant on and off, from a cleared
cache, and the number of race nodes met (pawns.race_hits) is reported.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python atlas/cylinder/sensitivity.py \
      "flat 4 W: a2 c2 / B: b7 d7" "cyl 3 W: a2 / B: b7"

Input lines are "<cyl|flat> <files> <position>"; with --file, one per line.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402

RULES = ("count", "mover", "opponent")


def sens(board_kind, n, text):
    wrap = board_kind == "cyl"
    pos = Pos.parse(text)
    row = {"board": board_kind, "n": n, "pos": text}
    for ep in (True, False):
        for rule in RULES:
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            pawns.race_hits.clear()
            g = pawns.value(Board(n, 8, wrap, ep), pos)
            row[f"{rule}/ep{'on' if ep else 'off'}"] = cgt.show(g)
            row[f"races/ep{'on' if ep else 'off'}"] = len(pawns.race_hits)
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    vals = {row[f"{r}/ep{e}"] for r in RULES for e in ("on", "off")}
    row["robust"] = len(vals) == 1
    row["race_robust_ep_on"] = len({row[f"{r}/epon"] for r in RULES}) == 1
    row["ep_robust_count"] = row["count/epon"] == row["count/epoff"]
    return row


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--out")
    ap.add_argument("items", nargs="*")
    a = ap.parse_args()
    items = list(a.items)
    if a.file:
        with open(a.file) as fh:
            items += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    rows = []
    for it in items:
        kind, n, text = it.split(" ", 2)
        rows.append(sens(kind, int(n), text))
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    if a.out:
        with open(a.out, "w") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
