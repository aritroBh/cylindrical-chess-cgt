#!/usr/bin/env python3
"""Recompute the TB-grounded flip counts from the frozen snapshot only (twin_snapshot/*.json), so the numbers do
not drift as other workstreams add to their caches. Needs rerun_rows.json.
Run from the project root: .venv/bin/python verify/engines/C2-reproduce/from_snapshot.py"""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]
rows = {r["id"]: r for r in json.loads((H / "rerun_rows.json").read_text())}
recs = {r["id"]: r for r in json.loads((ROOT / "engine/suite/results.json").read_text())}
S = {"win": 1, "loss": -1, "draw": 0}
for o in "NP":
    known = conf = sf = lc = zero = 0
    for i, x in rows.items():
        if x["o"] != o:
            continue
        p = H / "twin_snapshot" / f"{i}.json"
        if not p.exists():
            continue
        rec = json.loads(p.read_text())
        f = recs[i]["fen"].split()
        assert rec["fen"].split()[:2] == [f[0], "b" if f[1] == "w" else "w"], i
        t = rec["data"]["category"]
        ostm = recs[i]["stm"]
        wo = S[recs[i]["tb_root"]] * (1 if ostm == "W" else -1)
        wt = S[t] * (1 if ostm == "B" else -1)
        wW, wB = (wo, wt) if ostm == "W" else (wt, wo)
        sign = (wW > wB) - (wW < wB)
        known += 1
        model = 1 if o == "N" else -1
        if sign == model:
            conf += 1
            sf += (x["sf_delta"] > 0) == (model > 0)
            lc += (x["lc_delta"] > 0) == (model > 0)
        zero += sign == 0
    print(f"{o}: twins in snapshot {known}; TB confirms the {o} direction in {conf} (TB delta 0 in {zero}); "
          f"on those, Stockfish right {sf}/{conf}, Lc0 right {lc}/{conf}")
