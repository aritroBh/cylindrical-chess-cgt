"""Probe the Lichess tablebase for the N-position twins not already cached anywhere on disk.
Own cache + ledger inside this directory, hard cap 40, 5 s spacing.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-refute/static_eval_c1/probe_twins.py
"""
import json, os
from realchess import probe as P
P.MIN_INTERVAL = 5.0
D = "/Users/aritro/Downloads/Research/Chessendgames/verify/engines/C1-refute/static_eval_c1/"
pr = P.Prober(40, ledger=D + "tb_ledger.jsonl", cache_dir=D + "tbcache", tag="engines-C1-refute", verbose=True)
tc = json.load(open(D + "twin_cache.json"))
out = dict(tc["found"])
for i, fen in tc["missing"]:
    rec = pr.probe(fen + " 0 1")
    out[i] = (rec.get("data") or {}).get("category")
    print(i, fen, out[i], flush=True)
json.dump(out, open(D + "twin_results.json", "w"), indent=0)
print("ledger entries:", pr.ledger_count())
