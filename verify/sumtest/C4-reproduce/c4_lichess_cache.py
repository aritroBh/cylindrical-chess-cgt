"""C4 verifier: read the Lichess tablebase answers for the C4 line from the shared
cache ONLY (offline=True: no network, no ledger entry).  FENs built by hand:
X embedded = W Kf5 Pa2 Pc2 Pg4 / B Kh4 Pb4 Pd7 Pg5 (files a-d component, e empty, trebuchet f-h).
  PYTHONPATH=. .venv/bin/python verify/sumtest/C4-reproduce/c4_lichess_cache.py
"""
import os
from realchess.probe import Prober, categories, CapReached
HERE = os.path.dirname(os.path.abspath(__file__))
FENS = [("after 1.a2-a4 (Black to move, e.p. on a3)", "8/3p4/8/5Kp1/Pp4Pk/8/2P5/8 b - a3 0 1"),
        ("after 1.a2-a4 b4xa3 e.p. (White to move)", "8/3p4/8/5Kp1/6Pk/p7/2P5/8 w - - 0 1")]
pr = Prober(0, ledger=os.path.join(HERE, "ledger_unused.jsonl"), offline=True)
for name, fen in FENS:
    try:
        rec = pr.probe(fen)
    except CapReached as e:
        print(name, "NOT CACHED", e); continue
    root, mv = categories(rec)
    print(f"{name}: {rec['fen']} http={rec['status']} root(side to move)={root} dtz={rec['data'].get('dtz')} dtm={rec['data'].get('dtm')}")
    for m in rec["data"]["moves"]:
        print(f"    {m['uci']:6s} san={m.get('san'):8s} category-after-move={m.get('category')} dtm={m.get('dtm')}")
print("new requests:", pr.requests_this_process, "cache hits:", pr.hits)
