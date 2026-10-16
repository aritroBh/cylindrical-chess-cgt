"""Real-chess status of the 4 critical races of claim L4.2 in the 8x8 embedding
(WK f5, WP g4 / BK h4, BP g5). Each is a 7-man position, so the Lichess (Syzygy)
tablebase resolves it. Side to move = the side that did NOT make the race move.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/probe_races.py [--offline]
Ledger: verify/lemmas/L4.2-critical-races-theory/ledger.jsonl (cap 40).
"""
import sys, json
from realchess.probe import Prober

D = "verify/lemmas/L4.2-critical-races-theory"
RACES = [
    # (race (after move), mover, count verdict, FEN with the other side to move)
    ("W: a2 b5 / B: d7", "W", "W", "8/3p4/8/1P3Kp1/6Pk/8/P7/8 b - - 0 1"),
    ("W: a2 / B: c4 d7", "B", "B", "8/3p4/8/5Kp1/2p3Pk/8/P7/8 w - - 0 1"),
    ("W: a3 b5 / B: d6", "W", "W", "8/8/3p4/1P3Kp1/6Pk/P7/8/8 b - - 0 1"),
    ("W: a3 / B: c4 d6", "B", "B", "8/8/3p4/5Kp1/2p3Pk/P7/8/8 w - - 0 1"),
]
offline = "--offline" in sys.argv
p = Prober(cap=40, ledger=f"{D}/ledger.jsonl", tag="L4.2-theory", offline=offline, verbose=True)
for race, mover, cnt, fen in RACES:
    rec = p.probe(fen)
    d = rec.get("data") or {}
    stm = fen.split()[1].upper()
    cat = d.get("category")
    # root category is for the side to move; the mover is the other side
    chess = {"win": stm, "loss": ("W" if stm == "B" else "B"), "draw": "draw"}.get(cat, cat)
    print(f"{race:22s} mover {mover} count-verdict {cnt} | FEN {fen} | status {rec['status']} "
          f"root category ({stm} to move) = {cat}, dtz={d.get('dtz')}, dtm={d.get('dtm')} -> chess winner {chess} "
          f"| count {'AGREES' if chess == cnt else 'DISAGREES'}")
print("requests this process:", p.requests_this_process, "ledger count:", p.ledger_count(), "cache hits:", p.hits)
