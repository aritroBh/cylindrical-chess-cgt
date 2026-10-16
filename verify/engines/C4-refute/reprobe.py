"""Re-fetch a seeded random sample of suite positions from Lichess into a FRESH cache
(this directory only) and compare with the worker's cached responses.
    cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C4-refute/reprobe.py
Hard cap: 30 HTTP attempts (ledger verify/engines/C4-refute/ledger.jsonl)."""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import refute_c4 as R
from realchess import probe as P
P.MIN_INTERVAL = 2.5
pr = P.Prober(30, ledger=os.path.join(HERE, "ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache_fresh"),
              tag="C4-refute", verbose=True)
old = R.load_cache()
ver = [R.parse_epd(l)[0] + " 0 1" for l in open(os.path.join(R.SUITE, "cgt_verified.epd")) if l.strip()]
dis = [R.parse_epd(l)[0] + " 0 1" for l in open(os.path.join(R.SUITE, "cgt_disagree.epd")) if l.strip()]
rnd = random.Random(4041)
sample = rnd.sample(ver, 20) + rnd.sample(dis, 10)
same = diff = 0
for fen in sample:
    try:
        rec = pr.probe(fen)
    except P.CapReached as e:
        print("CAP", e); break
    a = {m["uci"]: m["category"] for m in rec["data"]["moves"]}
    b = {m["uci"]: m["category"] for m in old[fen]["data"]["moves"]}
    ok = a == b and rec["data"]["category"] == old[fen]["data"]["category"]
    same += ok; diff += not ok
    print("SAME" if ok else "DIFF", fen, rec["data"]["category"], flush=True)
print("same", same, "diff", diff, "http attempts", pr.ledger_count())
