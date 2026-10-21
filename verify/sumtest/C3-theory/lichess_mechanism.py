"""Offline (cache-only, 0 network requests) Lichess lookup of the C3 mechanism node.

X = W a2 c2 / B b4 d7 inside the 8x8 embedding (WK f5, BK h4, W Pg4 / B Pg5), after 2.a2-a4.
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/sumtest/C3-theory/lichess_mechanism.py
"""
from realchess.probe import Prober, categories, CapReached

p = Prober(cap=0, ledger="verify/sumtest/C3-theory/ledger.jsonl", offline=True)
for k, f in {
    "X after a2-a4, Black to move, e.p. square a3": "8/3p4/8/5Kp1/Pp4Pk/8/2P5/8 b - a3 0 1",
    "after b4xa3 e.p., White to move": "8/3p4/8/5Kp1/6Pk/p7/2P5/8 w - - 0 2",
}.items():
    try:
        root, mv = categories(p.probe(f))
        print(f"{k}: root={root} moves={mv}")
    except CapReached as e:
        print(k, "NOT CACHED:", e)
