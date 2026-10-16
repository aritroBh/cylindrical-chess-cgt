"""Probe the 3 children of the count-rule misses (Black to move after the race-creating move).
Own cache + ledger inside verify/engines/C3-refute/, hard cap 3 requests, 5 s spacing.
    cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C3-refute/probe_misses.py
"""
import os
from realchess import probe as P
HERE = os.path.dirname(os.path.abspath(__file__))
P.MIN_INTERVAL = 5.0
pr = P.Prober(3, ledger=os.path.join(HERE, "ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache"), tag="C3-refute", verbose=True)
for fen in ["8/8/8/3p1Kp1/6Pk/1P6/8/8 b - - 0 1",      # after c2xb3 (W b3 / B d5)
            "8/p7/8/5Kp1/6Pk/2P5/8/8 b - - 0 1",       # after b2xc3 (W c3 / B a7)
            "8/8/8/1pPp1Kp1/6Pk/8/8/8 b - - 0 1"]:     # after c4-c5 (W c5 / B b5 d5)
    rec = pr.probe(fen)
    d = rec["data"] or {}
    print(fen, "root:", d.get("category"), "dtz", d.get("dtz"))
    for m in d.get("moves", []):
        print("   ", m["san"], m["uci"], "->", m["category"], "dtz", m.get("dtz"))
print("ledger entries:", pr.ledger_count())
