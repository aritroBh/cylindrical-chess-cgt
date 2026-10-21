"""Probe the four critical race positions, placed in the proposed 8x8 embedding
(trebuchet W Pg4 / B Pg5, WK f5, BK h4), with the side to move = the side that
did NOT make the race-starting move. Cache first; at most 40 requests (ledger in this dir)."""
import json, os, sys
from realchess.probe import Prober, categories
D = os.path.dirname(os.path.abspath(__file__))
POS = [
    ("W: a2 b5 / B: d7", "W", "8/3p4/8/1P3Kp1/6Pk/8/P7/8 b - - 0 1"),
    ("W: a2 / B: c4 d7", "B", "8/3p4/8/5Kp1/2p3Pk/8/P7/8 w - - 0 1"),
    ("W: a3 b5 / B: d6", "W", "8/8/3p4/1P3Kp1/6Pk/P7/8/8 b - - 0 1"),
    ("W: a3 / B: c4 d6", "B", "8/8/3p4/5Kp1/2p3Pk/P7/8/8 w - - 0 1"),
]
offline = "--offline" in sys.argv
pr = Prober(40, ledger=os.path.join(D, "ledger.jsonl"), tag="L4.2-verify", offline=offline)
for txt, mover, fen in POS:
    try:
        rec = pr.probe(fen)
    except Exception as e:
        print(txt, mover, fen, "->", type(e).__name__, e); continue
    root, mv = categories(rec)
    print(f"{txt} (mover {mover}) FEN {fen}: root category (side to move) = {root}; dtz={rec.get('dtz')} dtm={rec.get('dtm')}")
    for m in rec.get("moves", []):
        print(f"     {m.get('uci'):6s} {m.get('san'):8s} after-move category {m.get('category')} dtz={m.get('dtz')}")
print("requests this process:", pr.requests_this_process, "ledger:", pr.ledger_count())
