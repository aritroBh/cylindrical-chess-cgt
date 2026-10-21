"""Cache-only (0 network requests) real-chess status of the 4 critical races of L4.2,
in the 8x8 embedding (WK f5 Pg4 / BK h4 Pg5), with EACH side to move.
Lichess root category is for the side to move.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/probe_offline_both.py
"""
from realchess.probe import Prober
from realchess import movegen as m
RACES = [("W: a2 b5 / B: d7", "W", "8/3p4/8/1P3Kp1/6Pk/8/P7/8"),
         ("W: a2 / B: c4 d7", "B", "8/3p4/8/5Kp1/2p3Pk/8/P7/8"),
         ("W: a3 b5 / B: d6", "W", "8/8/3p4/1P3Kp1/6Pk/P7/8/8"),
         ("W: a3 / B: c4 d6", "B", "8/8/3p4/5Kp1/2p3Pk/P7/8/8")]
p = Prober(cap=40, ledger="verify/lemmas/L4.2-critical-races-theory/ledger.jsonl", offline=True)
for race, mover, board in RACES:
    for stm in "wb":
        fen = f"{board} {stm} - - 0 1"
        pos = m.parse_fen(fen)
        assert not m.validity_errors(pos) and m.status(pos) == "ongoing", fen
        d = p.probe(fen)["data"]
        cat = d["category"]
        s = stm.upper()
        win = {"win": s, "loss": "B" if s == "W" else "W"}.get(cat, cat)
        print(f"{race:18s} mover {mover} | {fen:38s} | {s} to move: category {cat:5s} dtz {d.get('dtz')} -> winner {win}"
              f" | mover wins: {win == mover}")
print("network requests this process:", p.requests_this_process, "| ledger entries:", p.ledger_count())
