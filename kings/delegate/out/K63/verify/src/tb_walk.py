"""K63 referee: follow one drawing line in the tablebase from F2's qB with Black to move
(Ka4 kc5 Pb3 Pf5 pb6 pf6, Black to move), to see how chess differs from P there.
Both sides keep the value (draw): among the moves that keep it, each side prefers a promotion, then
a capture, then a pawn move, then a king move (first in the API's order).  At most MAXN probes.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K63/verify/src/tb_walk.py
"""
from realchess.probe import Prober
from realchess import movegen as mg

V = "kings/delegate/out/K63/verify"
PR = Prober(cap=150, ledger=f"{V}/tb_ledger.jsonl", cache_dir=f"{V}/tbcache", tag="K63ref-walk")
MAXN = 24
fen = "8/8/1p3p2/2k2P2/K7/1P6/8/8 b - - 0 1"
line = []
for i in range(MAXN):
    rec = PR.probe(fen)
    d = rec["data"]
    if not d["moves"]:
        print("no moves:", d.get("category")); break
    keep = [m for m in d["moves"] if m["category"] == "draw"]
    if not keep:
        print("value is not a draw here:", d["category"]); break
    def pri(m):
        return (0 if m.get("promotion") else 1 if m.get("capture") else 2 if m["san"][0].islower() else 3)
    m = sorted(keep, key=pri)[0]
    line.append(m["san"])
    print(f"{fen:45s} {d['category']:5s} plays {m['san']:7s} (draw-keeping moves: {', '.join(x['san'] for x in keep)})")
    pos = mg.parse_fen(fen)
    mv = [x for x in mg.legal_moves(pos) if x.uci() == m["uci"]][0]
    fen = mg.normal_fen(mg.make(pos, mv))
    if sum(c in "QRBNqrbn" for c in fen.split()[0]) >= 2:
        print("both sides have promoted:", fen); break
print("line:", " ".join(line))
print("final:", fen, " ledger:", PR.ledger_count())
