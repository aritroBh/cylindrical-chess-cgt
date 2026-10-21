"""Which twins are already cached anywhere (no network)."""
import json, glob, os, sys
from pathlib import Path
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from realchess.probe import Prober, categories
R = Path("/Users/aritro/Downloads/Research/Chessendgames")
se = json.loads((R/"engine/experiments/results/static_eval.json").read_text())["rows"]
dirs = [str(R/"realchess/cache")] + sorted(set(glob.glob(str(R/"verify/**/tbcache*"), recursive=True)))
probers = [Prober(cap=0, ledger="/dev/null", cache_dir=d, offline=True) for d in dirs]
found = {}
for r in se:
    for p in probers:
        rec = p.cached(r["twin"])
        if rec is not None:
            found[r["id"]] = (p.cache_dir, rec)
            break
from collections import Counter
print("twins cached:", len(found), Counter(r["o"] for r in se if r["id"] in found))
print("uncached by class:", Counter(r["o"] for r in se if r["id"] not in found))
print("cache dirs used:", Counter(v[0] for v in found.values()))
