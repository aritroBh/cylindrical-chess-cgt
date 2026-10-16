"""Probe (2 new Lichess requests, own cache + ledger, hard cap 4 HTTP attempts) the
B4-trebuchet versions of the two A4 count-rule misses that have no B4 twin in any cache:
  miss 1: component W b2 / B a7 c3, move bxc3  (A4: 8/p7/8/5Kp1/6Pk/2p5/1P6/8 w)
  miss 3: component W c4 / B b5 d5, move c5    (A4: 8/8/8/1p1p1Kp1/2P3Pk/8/8/8 w)
B4 = W Pg4, B Pg5, WK h5, BK f4 (engine/suite/cgtpos.trebuchet('B', 4)).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C3-reproduce/probe_b4_misses.py
"""
import os

from realchess import movegen as MG
from realchess import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
P.MIN_INTERVAL = 5.0
pr = P.Prober(4, ledger=os.path.join(HERE, "ledger.jsonl"), cache_dir=os.path.join(HERE, "tbcache"),
              tag="verify-C3", verbose=True)
FENS = {"miss1-B4": ("8/p7/8/6pK/5kP1/2p5/1P6/8 w - - 0 1", "b2c3"),
        "miss3-B4": ("8/8/8/1p1p2pK/2P2kP1/8/8/8 w - - 0 1", "c4c5")}
for name, (fen, mv) in FENS.items():
    errs = MG.validity_errors(MG.parse_fen(fen))
    assert not errs, (fen, errs)
    rec = pr.probe(fen)
    root, cats = P.categories(rec)
    print(name, fen, "root:", root, "| move", mv, "category (side to move after):", cats.get(mv))
    print("   all moves:", cats)
print("ledger entries:", pr.ledger_count())
