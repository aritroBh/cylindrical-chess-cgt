"""Run the naive second implementation (crosscheck.py) against product.py.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K4/xrun.py flat:3x4 cyl:3x4 ...

For each board: the 16 test games T and the negation of every candidate that some placement matched
(the difference tests), at every K+P vs K position with either side to move.  Prints one line per
board with the number of comparisons and mismatches.
"""

import json
import os
import sys
import time

import crosscheck
import graph
import testgames as tg
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))


def run(board):
    t0 = time.time()
    cg = graph.ChessGraph(board)
    starts = [cg.pos[i] for i in cg.kpk]
    rows = [json.loads(l) for l in open(os.path.join(HERE, board.replace(':', '_') + '.jsonl'))]
    used = sorted({v for r in rows for v in r['matched']})
    cands = dict(tg.candidates())
    games = [tg.GAMES[t] for t in tg.TESTS] + [tg.neg(cands[v]) for v in used]
    tot = bad = 0
    for T in games:
        nv = crosscheck.naive_results(cg.solver, starts, T)
        fast = solve_product(cg, T)
        for i in cg.kpk:
            tot += 1
            bad += nv[cg.pos[i]] != 'DWL'[fast[i * T.n + T.start]]
    print('%s: %d games, %d comparisons, %d mismatches, %.1fs' % (board, len(games), tot, bad, time.time() - t0),
          flush=True)
    return bad


if __name__ == '__main__':
    sys.exit(1 if sum(run(b) for b in sys.argv[1:]) else 0)
