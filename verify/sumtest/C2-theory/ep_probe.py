"""One-position Lichess check of the e.p. mechanism (theory-lens verifier, cap 40, own ledger).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C2-theory/ep_probe.py
"""
import json
from realchess.probe import Prober

P = Prober(cap=40, ledger="verify/sumtest/C2-theory/ledger.jsonl", tag="C2-theory", verbose=True)
FENS = {
    # after 1.a2-a4 in X = W a2 c2 / B b4 d7 (+ trebuchet Kf5 Pg4 / Kh4 Pg5), Black to move, e.p. on a3
    "after a2-a4, ep a3, BTM": "8/3p4/8/5Kp1/Pp4Pk/8/2P5/8 b - a3 0 1",
}
for name, fen in FENS.items():
    rec = P.probe(fen)
    d = rec["data"] or {}
    print(name, "| fen:", rec["fen"], "| root:", d.get("category"))
    for mv in d.get("moves", []):
        print("   ", mv.get("uci"), mv.get("san"), mv.get("category"), "dtz", mv.get("dtz"), "dtm", mv.get("dtm"))
print("requests this process:", P.requests_this_process, "ledger:", P.ledger_count())
