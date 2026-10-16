"""Real-chess (flat 8x8, orthodox rules) probe of the isolated 7.2 king group via the Lichess tablebase,
through realchess/probe.py (shared cache; own ledger, hard cap 8 requests).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/K1-refute/probe_k1.py"""
import json, os
from realchess.probe import Prober, categories
HERE = os.path.dirname(os.path.abspath(__file__))
pr = Prober(cap=8, ledger=os.path.join(HERE, "ledger.jsonl"), tag="K1-refute")
for fen in ["3k4/3Pp3/4K3/8/8/8/8/8 w - - 0 1", "3k4/3Pp3/4K3/8/8/8/8/8 b - - 0 1"]:
    rec = pr.probe(fen)
    root, mv = categories(rec)
    d = rec["data"] or {}
    print(f"{fen}: root={root} dtz={d.get('dtz')} dtm={d.get('dtm')}")
    for m in d.get("moves", []):
        print(f"   {m['san']:7s} after-move category (side to move after it) = {m['category']:12s} dtz={m.get('dtz')} dtm={m.get('dtm')}")
print(f"cache hits={pr.hits} new requests this process={pr.requests_this_process} ledger total={pr.ledger_count()}")
