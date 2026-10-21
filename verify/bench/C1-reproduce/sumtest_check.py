"""Third code path: sumtest (whole-board tree, its own move generator and e.p.-aware
passer test; canonical forms via cylcgt.cgt) on the 48 changed v1 components.
Run: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python verify/bench/C1-reproduce/sumtest_check.py"""
import json
from pathlib import Path
from sumtest.aware_value import value
from bench import cgtfmt
HERE = Path(__file__).resolve().parent
rows = json.load(open("bench/results/conventions_summary.json"))["v1_changed"]
mine = {r["position"]: r for r in json.load(open(HERE / "indep_result.json"))["rows"]}
bad = 0
for r in rows:
    w = mine[r["position"]]["w"]
    out = []
    for aware in (False, True):
        v, brute, pred = value(r["position"], w, False, ep=True, aware=aware, race_rule="count")
        out.append((cgtfmt.fmt(v, ascii=True), brute == pred))
    ok = out[0][0] == r["textbook"] and out[1][0] == r["aware"]
    bad += not ok
    print(r["v1_id"], r["position"], "textbook", out[0], "aware", out[1], "OK" if ok else "MISMATCH", flush=True)
print("mismatches:", bad, "of", len(rows))
