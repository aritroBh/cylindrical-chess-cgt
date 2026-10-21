"""Write the decisive terminals of a component (from a min_support JSON) as kpsolve input lines,
both sides to move, on the flat 8x8 embedding used by the oracle (trebuchet on f-h).

    PYTHONPATH=. .venv/bin/python realchess/targets18/to_kpsolve.py <min_support.json> > positions.txt
"""
import json
import sys

from cylcgt.pawns import Pos

from realchess.certify.oracle10 import side_fens
from realchess.oracle_value import Terminals

d = json.load(open(sys.argv[1]))
T = Terminals(Pos.parse(d["component"]))
byname = {str(t): t for t in T.terms}


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


print(f"# decisive terminals of {d['component']} ({d['treatment']}); model assignment in comments")
for x in d["needed_terminals"]:
    t = byname[x["terminal"]]
    f = side_fens(T, t)
    print(f"# {x['terminal']}  men={x['men']}  model={x['model_assignment']}")
    for side in "WB":
        print(tokens(f[side]))
