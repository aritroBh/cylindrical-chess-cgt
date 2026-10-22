"""T20 step 2: list the embedded terminal FENs by number of men, check
legality, and show which distinct FENs exist per (men, side-to-move).

    PYTHONPATH=. .venv/bin/python research/star2_oracle/list_fens.py A
"""
import json
import os
import sys
from collections import Counter, defaultdict

from cylcgt.pawns import Pos

from realchess import movegen as mg
from realchess.oracle_value import Terminals

HERE = os.path.dirname(os.path.abspath(__file__))
COMPONENTS = {
    "A": "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "B": "W: b4 c2 d2 / B: a6 a7 c6 d5",
}

name = sys.argv[1] if len(sys.argv) > 1 else "A"
T = Terminals(Pos.parse(COMPONENTS[name]))
by_men = defaultdict(set)
illegal = []
for t in T.terms:
    for s in "WB":
        pos = T.real_pos(t, s)
        errs = mg.validity_errors(pos)
        if errs:
            illegal.append((str(t), s, errs))
        by_men[(T.men(t), s)].add(mg.normal_fen(pos))
print("illegal:", len(illegal))
for x in illegal[:20]:
    print("  ", x)
rows = []
for (m, s), fens in sorted(by_men.items()):
    rows.append({"men": m, "stm": s, "distinct_fens": len(fens)})
    print(rows[-1])
out = {"component": COMPONENTS[name], "rows": rows, "illegal": illegal}
with open(os.path.join(HERE, f"fens_{name}.json"), "w") as fh:
    json.dump(out, fh, indent=1)
