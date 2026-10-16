"""Real-chess (Lichess tablebase) check of the C4 line in the 8x8 embedding.
X embedded: W Kf5 Pa2 Pc2 Pg4 / B Kh4 Pb4 Pd7 Pg5.
Run (cache first; --online allows new requests, cap 40, own ledger):
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C4-refute/realchess_c4.py [--online]
"""
import os, sys, json
from realchess.probe import Prober, categories, CapReached

HERE = os.path.dirname(os.path.abspath(__file__))
FENS = {
    # "X, White to move (8 men)": "8/3p4/8/5Kp1/1p4Pk/8/P1P5/8 w - - 0 1",
    "X after 1.a4, Black to move, ep a3 (8 men)": "8/3p4/8/5Kp1/Pp4Pk/8/2P5/8 b - a3 0 1",
    "X after 1.a4 bxa3 e.p., White to move (7 men)": "8/3p4/8/5Kp1/6Pk/p7/2P5/8 w - - 0 1",
}
online = "--online" in sys.argv
pr = Prober(40, ledger=os.path.join(HERE, "ledger.jsonl"), tag="C4-refute", offline=not online)
for name, fen in FENS.items():
    try:
        rec = pr.probe(fen)
    except CapReached as e:
        print(f"{name}: NOT CACHED ({e})")
        continue
    root, mv = categories(rec)
    print(f"{name}\n  fen {rec['fen']}  http {rec['status']}  root category (side to move): {root}")
    for u, c in sorted(mv.items()):
        print(f"    {u}: {c}")
print("ledger entries:", pr.ledger_count(), " cache hits:", pr.hits)
