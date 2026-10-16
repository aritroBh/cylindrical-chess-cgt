"""Fresh Lichess fetch (own cache + ledger in this dir, hard cap 15) of C2-relevant positions
not already re-fetched by verify/engines/C1-reproduce, compared move-by-move with the
worker's cached response. Includes the 5 positions of the quoted Ke6 line.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-reproduce/refetch_c2.py
"""
import glob
import json
import os

from realchess import probe as P

P.MIN_INTERVAL = 5.0
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
pr = P.Prober(15, ledger=os.path.join(HERE, "ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache"),
              tag="verify-C2-reproduce", verbose=True)
W = {}
for p in glob.glob(f"{ROOT}/engine/suite/tbcache/*/*.json"):
    r = json.load(open(p))
    W[r["fen"]] = r
byid = {r["id"]: r["fen"] for r in json.load(open(f"{ROOT}/engine/suite/results.json"))}
fens = [byid[i] for i in ("cgt002", "cgt020", "cgt238", "cgt202", "cgt207", "cgt209", "cgt228")]
fens += ["8/8/3pK3/6p1/6Pk/2P5/8/8 b - - 0 1", "8/8/3pK3/6p1/6k1/2P5/8/8 w - - 0 1",
         "8/8/3K4/6p1/6k1/2P5/8/8 b - - 0 1", "8/8/3K4/6p1/8/2P2k2/8/8 w - - 0 1",
         "8/8/3K4/6p1/2P5/5k2/8/8 b - - 0 1"]
diff = 0
for f in fens:
    new = pr.probe(f)["data"]
    old = W[P.fen_key(f)]["data"]
    a = {m["uci"]: m["category"] for m in new["moves"]}
    b = {m["uci"]: m["category"] for m in old["moves"]}
    same = a == b and new["category"] == old["category"]
    diff += not same
    print(f, "root", new["category"], "first", new["moves"][0]["uci"] if new["moves"] else None,
          "same-as-worker-cache:", same, {u: c for u, c in a.items()})
print("re-fetched:", len(fens), "differences:", diff, "ledger entries:", pr.ledger_count())
