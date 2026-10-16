"""Re-fetch a sample of C1-group positions from Lichess (fresh cache inside this dir, hard cap 40)
and compare every move category with the worker's cached response.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-reproduce/refetch.py
"""
import json, os, random, sys
from realchess import probe as P
sys.path.insert(0, "engine/suite")
import build_suite as BS
import tb
P.MIN_INTERVAL = 5.0
HERE = os.path.dirname(os.path.abspath(__file__))
pr = P.Prober(40, ledger=os.path.join(HERE, "ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache"), tag="verify-C1", verbose=True)
rows = json.load(open("engine/suite/results.json"))
grp = [r for r in rows if BS.tame(r["value"]["count"]) and not r["features"]["race_sensitive"] and r["treb"].startswith("A")]
must = ["cgt052", "cgt055", "cgt008", "cgt011", "cgt019", "cgt236", "cgt042", "cgt253", "cgt254", "cgt259"]
rest = [r["id"] for r in grp if r["id"] not in must]
pick = must + random.Random(7).sample(rest, 6)
diff = 0
for i in pick:
    r = next(x for x in grp if x["id"] == i)
    new = pr.probe(r["fen"])["data"]
    old = tb.lookup(r["fen"], allow_network=False)["data"]
    a = {m["uci"]: m["category"] for m in new["moves"]}; b = {m["uci"]: m["category"] for m in old["moves"]}
    same = a == b and new["category"] == old["category"]
    diff += not same
    print(i, r["fen"], "root", new["category"], "same-as-worker-cache:", same)
print("positions re-fetched:", len(pick), "differences:", diff, "ledger entries:", pr.ledger_count())
