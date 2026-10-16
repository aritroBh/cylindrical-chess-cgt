"""Independent outcome-class check of atlas atoms with crosscheck/minimax.py.

crosscheck/minimax.py (written by Codex, does not import cylcgt) plays the
whole position out with alternating moves and the same conventions
(passed pawn wins, race rule = promotion count, e.p. on).  Its outcome class
(L/R/N/P) must equal the outcome class of the CGT value in the atlas.
This checks outcomes only, not the full values.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python atlas/cylinder/crosscheck_outcomes.py
"""
import json
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

from crosscheck.minimax import Board, outcome_class, parse_position  # noqa: E402

idx = {}
for line in open(os.path.join(HERE, "value_index.jsonl")):
    d = json.loads(line)
    idx[d["vid"]] = d

rings, flats = [], []
for line in open(os.path.join(HERE, "values.jsonl")):
    r = json.loads(line)
    if r["board"] == "cyl" and r["ring"]:
        rings.append(r)
    elif r["board"] == "flat" and r["ncomp"] == 1 and r["n"] in (3, 4, 5):
        flats.append(r)
rng = random.Random(20261016)
sample = rings + rng.sample(flats, min(4000, len(flats)))
stats = Counter()
bad = []
for r in sample:
    b = Board(r["n"], 8, r["board"] == "cyl", True)
    oc = outcome_class(b, parse_position(r["pos"]))
    ok = oc == idx[r["vid"]]["out"]
    key = f"{'ring' if r['ring'] else 'flat-connected'} n={r['n']}"
    stats[(key, ok)] += 1
    if not ok:
        bad.append((r["board"], r["n"], r["pos"], idx[r["vid"]]["show"][:60], idx[r["vid"]]["out"], oc))
for (k, ok), c in sorted(stats.items()):
    print(k, "agree" if ok else "DISAGREE", c)
for x in bad[:30]:
    print("DISAGREE", x)
print("total checked", len(sample), "disagreements", len(bad))
