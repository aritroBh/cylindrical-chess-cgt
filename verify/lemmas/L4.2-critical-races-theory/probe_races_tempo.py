"""Same 4 critical races, but with the MOVER to move again (as happens in
non-alternating / sum play, which is what the CGT value quantifies over).
If the mover also wins here, each race is a win for the same side whoever moves,
i.e. it behaves like a cold +-BIG locally.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/probe_races_tempo.py
"""
from realchess.probe import Prober
from realchess import movegen as m
D = "verify/lemmas/L4.2-critical-races-theory"
RACES = [
    ("W: a2 b5 / B: d7", "W", "8/3p4/8/1P3Kp1/6Pk/8/P7/8 w - - 0 1"),
    ("W: a2 / B: c4 d7", "B", "8/3p4/8/5Kp1/2p3Pk/8/P7/8 b - - 0 1"),
    ("W: a3 b5 / B: d6", "W", "8/8/3p4/1P3Kp1/6Pk/P7/8/8 w - - 0 1"),
    ("W: a3 / B: c4 d6", "B", "8/8/3p4/5Kp1/2p3Pk/P7/8/8 b - - 0 1"),
]
p = Prober(cap=40, ledger=f"{D}/ledger.jsonl", tag="L4.2-theory", verbose=True)
for race, mover, fen in RACES:
    pos = m.parse_fen(fen)
    assert not m.validity_errors(pos) and m.status(pos) == "ongoing", fen
    d = p.probe(fen).get("data") or {}
    stm = fen.split()[1].upper()
    cat = d.get("category")
    chess = {"win": stm, "loss": ("W" if stm == "B" else "B"), "draw": "draw"}.get(cat, cat)
    print(f"{race:22s} mover {mover} (mover to move) | {fen} | category={cat} dtz={d.get('dtz')} -> winner {chess}")
print("requests this process:", p.requests_this_process, "ledger count:", p.ledger_count())
