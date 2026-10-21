#!/usr/bin/env python3
"""Tablebase-judged flip test for the N/P rows of claim C2.

Step 1 (offline): read every tablebase cache in the project (read-only), find the Lichess result
for each N/P original and its twin.  Step 2 (optional, --fetch K): probe up to K missing twins
through realchess/probe.py into THIS directory's own cache + ledger (hard cap 40, 3 s spacing),
P twins first, then N twins.  Step 3: judge each engine's flip delta against the tablebase.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/flip/tb_twins.py [--fetch K]
Needs indep_rows.json from indep_flip.py.
"""
import glob
import json
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

rows = json.loads((HERE / "indep_rows.json").read_text())
NP = [r for r in rows if r["o_x"] in "NP"]

# ---------------- offline cache scan (any JSON record with "fen" + "data")
cache = {}
for d in glob.glob(str(ROOT / "**" / "*cache*"), recursive=True):
    if not os.path.isdir(d) or "pycache" in d or ".venv" in d or "pytest" in d:
        continue
    for f in glob.glob(os.path.join(d, "**", "*.json"), recursive=True):
        try:
            rec = json.load(open(f))
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("status") == 200 and rec.get("data") and "fen" in rec:
            cache.setdefault(rec["fen"], (rec, os.path.relpath(d, ROOT)))
print("cached 200-records found:", len(cache))

fetch = 0
if "--fetch" in sys.argv:
    fetch = int(sys.argv[sys.argv.index("--fetch") + 1])
own = None
if fetch:
    from realchess import probe as P
    P.MIN_INTERVAL = 3.0
    own = P.Prober(40, ledger=str(HERE / "tb_ledger.jsonl"), cache_dir=str(HERE / "tbcache"),
                   tag="verify-C2-refute-flip", verbose=True)
    print("ledger used so far:", own.ledger_count(), "cap 40")


def look(fen):
    if fen in cache:
        return cache[fen][0]["data"]["category"], cache[fen][1]
    return None, None


todo = []
for r in NP:
    r["tb_orig"], r["src_orig"] = look(r["fen"])
    r["tb_twin"], r["src_twin"] = look(r["twin"])
    if r["tb_twin"] is None:
        todo.append(r)
print("N/P rows:", len(NP), "| originals with TB:", sum(r["tb_orig"] is not None for r in NP),
      "| twins with TB (cache):", sum(r["tb_twin"] is not None for r in NP))
todo.sort(key=lambda r: (r["o_x"] != "P", r["id"]))
done = 0
for r in todo:
    if done >= fetch:
        break
    rec = own.probe(r["twin"])
    done += 1
    if rec.get("status") == 200:
        r["tb_twin"], r["src_twin"] = rec["data"]["category"], "fetched:C2-refute/flip/tbcache"
print("fetched this run:", done, "| twins with TB now:", sum(r["tb_twin"] is not None for r in NP))


def white_pov(cat, stm, cursed_as_win):
    """+1 White wins, 0 draw, -1 Black wins; cat is for the side to move."""
    m = {"win": 1, "loss": -1, "draw": 0,
         "cursed-win": 1 if cursed_as_win else 0, "blessed-loss": -1 if cursed_as_win else 0}
    if cat not in m:
        return None
    v = m[cat]
    return v if stm == "W" else -v


for cursed_as_win in (False, True):
    print(f"\n## TB-judged flip (cursed-win/blessed-loss counted as {'win/loss' if cursed_as_win else 'draw'})")
    cls = Counter()
    sc = {k: Counter() for k in ("sf", "lc")}
    for r in NP:
        if r["tb_orig"] is None or r["tb_twin"] is None:
            continue
        tstm = "B" if r["stm"] == "W" else "W"
        vo = white_pov(r["tb_orig"], r["stm"], cursed_as_win)
        vt = white_pov(r["tb_twin"], tstm, cursed_as_win)
        vW, vB = (vo, vt) if r["stm"] == "W" else (vt, vo)
        true = (vW > vB) - (vW < vB)
        r[f"tb_delta_sign_{cursed_as_win}"] = true
        tbclass = {(1, 1): "L", (-1, -1): "R", (1, -1): "N", (-1, 1): "P"}.get((vW, vB), f"draw-involved({vW},{vB})")
        cls[(r["o_x"], tbclass)] += 1
        for eng, key in (("sf", "d_sf"), ("lc", "d_lc")):
            d = r[key]
            es = (d > 0) - (d < 0)
            if true == 0:
                sc[eng][(r["o_x"], "TB no direction")] += 1
            else:
                agrees = true == (1 if r["o_x"] == "N" else -1)
                sc[eng][(r["o_x"], "TB dir = model dir" if agrees else "TB dir != model dir",
                         "right" if es == true else "wrong")] += 1
    print("model class -> TB class (pairs with both results):", dict(sorted(cls.items())))
    for eng in ("sf", "lc"):
        print(eng, {k: v for k, v in sorted(sc[eng].items(), key=str) if v})
json.dump(NP, open(HERE / "tb_twins_rows.json", "w"), indent=0)
for r in NP:
    print(r["id"], r["o_x"], r["value_count"], r["component"], r["treb"], r["stm"], "| TB orig:", r["tb_orig"],
          "twin:", r["tb_twin"], f"| dSF {r['d_sf']:+.2f} dLc0 {r['d_lc']:+d}")
