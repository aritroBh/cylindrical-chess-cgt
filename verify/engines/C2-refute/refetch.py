"""Fresh Lichess re-fetch of a sample of positions into THIS verifier's own cache/ledger
(cap 40 HTTP attempts, 3 s spacing), then compare with the worker's cached records.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/refetch.py
"""
import glob, json, os, sys
from realchess import probe as P
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
P.MIN_INTERVAL = 3.0
pr = P.Prober(40, ledger=os.path.join(HERE, "ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache"),
              tag="verify-C2-refute", verbose=True)
worker = {}
for p in glob.glob(os.path.join(ROOT, "engine", "suite", "tbcache", "*", "*.json")):
    r = json.load(open(p)); worker[r["fen"]] = r
FENS = [
    "8/8/3p4/5Kp1/6Pk/2P5/8/8 w - - 0 1",        # PV root (A4, value *)
    "8/8/3pK3/6p1/6Pk/2P5/8/8 b - - 0 1",        # after Ke6 (should be draw for Black to move)
    "8/2p5/8/3P1Kp1/6Pk/8/3P4/8 w - - 0 1",      # A4, Ke6 claimed to WIN
    "8/2p1K3/8/3P2p1/6Pk/8/3P4/8 b - - 0 1",     # after Ke6 there (Black to move: should be 'loss')
    "8/3p4/3P1Kp1/6Pk/8/8/3P4/8 w - - 0 1",      # A5, 4 king moves claimed to win
    "8/1p3Kp1/6Pk/P7/8/8/P7/8 w - - 0 1",        # A6, 4 drawing king moves
    "8/2p5/8/1P3Kp1/6Pk/8/1P6/8 w - - 0 1",      # A4, 4 drawing king moves
    "8/8/8/1p4pK/1P3kP1/8/2P5/8 w - - 0 1",      # B4, 2 drawing king moves
    "8/8/1p6/6pK/5kP1/1p6/1P6/8 b - - 0 1",      # B4 Black to move, 2 drawing Black-king moves
    "8/8/8/2p3pK/2P2kP1/3P4/8/8 w - - 0 1",      # B4, root draw, h5g6 draw
]
n_diff = 0
for f in FENS:
    rec = pr.probe(f)
    mine = {m["uci"]: m["category"] for m in rec["data"]["moves"]}
    w = worker.get(rec["fen"])
    wm = {m["uci"]: m["category"] for m in w["data"]["moves"]} if w else None
    same = w is not None and wm == mine and w["data"]["category"] == rec["data"]["category"]
    n_diff += not same
    km = {u: c for u, c in mine.items() if u[:2] == [s for s in ["f5","f6","f7","h5","f4","e6","e7"] if s][0] or True}
    print(("SAME " if same else ("NOTINWORKERCACHE " if w is None else "DIFF ")), rec["fen"], "root", rec["data"]["category"],
          {m["san"]: m["category"] for m in rec["data"]["moves"]})
print("differences vs worker cache:", n_diff, "; ledger entries:", pr.ledger_count())
