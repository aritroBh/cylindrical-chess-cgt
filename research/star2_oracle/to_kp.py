"""T20: write kpsolve input lines for terminal positions of a component.

    PYTHONPATH=. .venv/bin/python research/star2_oracle/to_kp.py A 8 \
        > research/star2_oracle/kp_A_8men.txt

Prints, for every terminal of the given number of men, the kpsolve token line
for White to move and for Black to move, with a comment naming the terminal.
"""
import os
import sys

from cylcgt.pawns import Pos

from realchess import movegen as mg
from realchess.oracle_value import Terminals

HERE = os.path.dirname(os.path.abspath(__file__))
COMPONENTS = {
    "A": "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "B": "W: b4 c2 d2 / B: a6 a7 c6 d5",
}


def tokens(fen):
    board, stm, _castle, ep = fen.split()[:4]
    out = []
    for i, row in enumerate(board.split("/")):
        rank, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
                continue
            out.append(f"{ch}{'abcdefgh'[f]}{rank}")
            f += 1
    return " ".join(out) + f" {stm} {ep}"


name = sys.argv[1]
max_men = int(sys.argv[2]) if len(sys.argv) > 2 else 99
only = sys.argv[3:] if len(sys.argv) > 3 else None
T = Terminals(Pos.parse(COMPONENTS[name]))
for t in T.order:
    if T.men(t) > max_men:
        continue
    if only and str(t) not in only:
        continue
    print(f"# {t}  men={T.men(t)}")
    for side in "WB":
        print(tokens(mg.normal_fen(T.real_pos(t, side))))
