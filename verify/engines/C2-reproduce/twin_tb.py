#!/usr/bin/env python3
"""TB-grounded flip test for claim C2.

For each N/P position, the original's TB root is known (engine/suite/results.json). The twin's TB root is looked
up in every local tablebase cache (offline, no network). With --fetch K, up to K uncached N/P twins are fetched
through realchess/probe.py with a private ledger in this directory (cap enforced by the ledger).

Run from the project root:
    PYTHONPATH=. .venv/bin/python verify/engines/C2-reproduce/twin_tb.py [--fetch K]
"""
import argparse
import json
import glob
import os
from collections import Counter
from pathlib import Path

from realchess import probe

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LEDGER = HERE / "ledger_flip.jsonl"
CAP = 40

ap = argparse.ArgumentParser()
ap.add_argument("--fetch", type=int, default=0)
ap.add_argument("--ids", default="", help="comma-separated ids allowed to be fetched, in this order")
a = ap.parse_args()

caches = sorted({os.path.dirname(os.path.dirname(p)) for p in glob.glob(str(ROOT / "**/*.json"), recursive=True)
                 if "/tbcache/" in p or "/realchess/cache/" in p})
caches = [c for c in caches if ".venv" not in c]
probers = [probe.Prober(0, ledger=str(HERE / "unused_ledger.jsonl"), cache_dir=c, offline=True) for c in caches]
own = probe.Prober(CAP, ledger=str(LEDGER), cache_dir=str(HERE / "tbcache"), tag="verify-C2-reproduce-flip",
                   verbose=True)
probe.MIN_INTERVAL = 5.0  # other processes may be probing too


def lookup(fen):
    for pr in probers + [own]:
        rec = pr.cached(fen)
        if rec is not None and rec.get("data"):
            return rec
    return None


rows = {r["id"]: r for r in json.loads((HERE / "rerun_rows.json").read_text())}
recs = {r["id"]: r for r in json.loads((ROOT / "engine/suite/results.json").read_text())}
np_ids = [i for i in rows if rows[i]["o"] in "NP"]
allowed = [x for x in a.ids.split(",") if x]
fetched = 0
out = []
for i in np_ids:
    r = recs[i]
    f = r["fen"].split()
    twin = f"{f[0]} {'b' if f[1] == 'w' else 'w'} - - 0 1"
    rec = lookup(twin)
    if rec is None and fetched < a.fetch and i in allowed:
        rec = own.probe(twin)
        fetched += 1
    tw_root = rec["data"].get("category") if rec else None
    x = rows[i]
    # White-POV TB outcome with each side to move: +1 White wins, 0 draw, -1 Black wins
    def wpov(cat, stm):
        s = {"win": 1, "loss": -1, "draw": 0, "cursed-win": 0, "blessed-loss": 0}.get(cat)
        if s is None:
            return None
        return s if stm == "W" else -s
    ostm = r["stm"]
    tstm = "B" if ostm == "W" else "W"
    w_orig, w_twin = wpov(r["tb_root"], ostm), wpov(tw_root, tstm)
    if w_orig is None or w_twin is None:
        tb_delta_sign = None
    else:
        wW = w_orig if ostm == "W" else w_twin   # White to move
        wB = w_twin if ostm == "W" else w_orig   # Black to move
        tb_delta_sign = (wW > wB) - (wW < wB)
    out.append({"id": i, "o": x["o"], "o_all": x["o_all"], "orig_tb": r["tb_root"], "twin_tb": tw_root,
                "tb_delta_sign": tb_delta_sign, "sf_delta": x["sf_delta"], "lc_delta": x["lc_delta"]})
(HERE / "twin_tb_rows.json").write_text(json.dumps(out, indent=0))
print("caches searched:", len(caches), "; fetched this run:", fetched, "; ledger total:", own.ledger_count())
for o in "NP":
    rs = [x for x in out if x["o"] == o]
    print(f"\n{o}: n={len(rs)}; original TB roots {dict(Counter(x['orig_tb'] for x in rs))}; "
          f"twin TB roots known {sum(x['twin_tb'] is not None for x in rs)}: {dict(Counter(x['twin_tb'] for x in rs))}")
    # pairs where both TB results are known
    kn = [x for x in rs if x["tb_delta_sign"] is not None]
    print(f"  both halves known: {len(kn)}; TB delta sign (+ means White better with White to move): "
          f"{dict(Counter(x['tb_delta_sign'] for x in kn))}")
    model = 1 if o == "N" else -1
    agree = [x for x in kn if x["tb_delta_sign"] == model]
    print(f"  TB pair agrees with CGT {o}-prediction: {len(agree)}/{len(kn)}")
    for eng in ("sf_delta", "lc_delta"):
        ok_tb = sum((x[eng] > 0) == (x["tb_delta_sign"] > 0) and (x[eng] < 0) == (x["tb_delta_sign"] < 0)
                    for x in kn if x["tb_delta_sign"] != 0)
        nz = sum(1 for x in kn if x["tb_delta_sign"] != 0)
        ok_model_on_agree = sum(((x[eng] > 0) if o == "N" else (x[eng] < 0)) for x in agree)
        print(f"  {eng}: sign matches TB on {ok_tb}/{nz} pairs with nonzero TB delta; "
              f"right on {ok_model_on_agree}/{len(agree)} TB-confirmed pairs")

# snapshot every twin record used, so the numbers above can be re-derived after other caches change
snap = HERE / "twin_snapshot"
snap.mkdir(exist_ok=True)
for x in out:
    r = recs[x["id"]]
    f = r["fen"].split()
    rec = lookup(f"{f[0]} {'b' if f[1] == 'w' else 'w'} - - 0 1")
    if rec is not None:
        (snap / f"{x['id']}.json").write_text(json.dumps(rec))
print("snapshot records:", len(list(snap.glob("*.json"))))
