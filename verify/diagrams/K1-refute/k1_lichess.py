"""Real-chess (flat 8x8) status of the isolated 7.2 king group, via the Lichess tablebase.
Uses realchess/probe.py (shared cache, rate limit). Own ledger, hard cap 6 requests.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/K1-refute/k1_lichess.py
"""
import json, sys
from realchess.probe import Prober

LEDGER = "verify/diagrams/K1-refute/ledger.jsonl"
p = Prober(cap=6, ledger=LEDGER, tag="K1-refute", offline="--offline" in sys.argv)
for stm in ("w", "b"):
    fen = f"3k4/3Pp3/4K3/8/8/8/8/8 {stm} - - 0 1"
    rec = p.probe(fen)
    d = rec["data"]
    print(f"\n{fen}\n  HTTP {rec['status']}  root category (side to move): {d.get('category')}  dtz={d.get('dtz')} dtm={d.get('dtm')}")
    for m in d.get("moves", []):
        print(f"    {m['san']:8s} -> category after move (opponent's view): {m['category']:13s} dtz={m.get('dtz')} dtm={m.get('dtm')}")
print(f"\ncache hits={p.hits} requests this process={p.requests_this_process} ledger total={p.ledger_count()}")
