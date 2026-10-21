"""Per-position sign agreement with the tablebase (White POV) on the 86 N/P pairs, both twins.
    cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C2-refute/flip/sign_vs_tb.py"""
import json
from collections import Counter
from pathlib import Path
H = Path(__file__).resolve().parent
NP = json.loads((H / "tb_twins_rows.json").read_text())
M = {"win": 1, "loss": -1, "draw": 0}
c = Counter()
for r in NP:
    tstm = "B" if r["stm"] == "W" else "W"
    vo = M[r["tb_orig"]] * (1 if r["stm"] == "W" else -1)
    vt = M[r["tb_twin"]] * (1 if tstm == "W" else -1)
    for tb, lc, sf in ((vo, r["lc_white"], r["sf_final"]), (vt, r["lc_twin_white"], r["sf_twin_final"])):
        if tb == 0:
            c[(r["o_x"], "TB draw")] += 1
            continue
        c[(r["o_x"], "decisive")] += 1
        c[(r["o_x"], "Lc0 sign = TB")] += (lc > 0) == (tb > 0)
        c[(r["o_x"], "SF sign = TB")] += (sf > 0) == (tb > 0)
    if 0 not in (vo, vt):
        c[(r["o_x"], "pairs both decisive")] += 1
        c[(r["o_x"], "Lc0 both signs = TB")] += ((r["lc_white"] > 0) == (vo > 0)) and ((r["lc_twin_white"] > 0) == (vt > 0))
        c[(r["o_x"], "SF both signs = TB")] += ((r["sf_final"] > 0) == (vo > 0)) and ((r["sf_twin_final"] > 0) == (vt > 0))
for k in sorted(c): print(k, c[k])
