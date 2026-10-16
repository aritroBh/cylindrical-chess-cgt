"""Follow the tablebase's first-listed (best) move for a few plies (1 request per ply).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python engine/suite/pv.py "<FEN>" <first-move-uci> <plies>

Lichess lists moves best-first for the side to move. Used only to explain a few
CGT/tablebase disagreements in README.md; every step is cached.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tb  # noqa: E402
from realchess import movegen as MG  # noqa: E402


def main():
    fen, first, plies = sys.argv[1], sys.argv[2], int(sys.argv[3])
    pos = MG.parse_fen(fen)
    line = []
    mv = first
    for i in range(plies):
        m = next(x for x in MG.legal_moves(pos) if x.uci() == mv)
        pos = MG.make(pos, m)
        line.append(mv)
        f = MG.normal_fen(pos)
        if pos.men() > 7:
            break
        rec = tb.lookup(f)
        d = rec.get("data") or {}
        moves = d.get("moves", [])
        print(f"after {' '.join(line):40s} {f:45s} stm-category={d.get('category')} dtz={d.get('dtz')}")
        if not moves:
            break
        mv = moves[0]["uci"]
    print("line:", " ".join(line), f"(requests used {tb.requests_used()})")


if __name__ == "__main__":
    main()
