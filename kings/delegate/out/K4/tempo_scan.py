"""Integer scan: results of x (+) n for n = -10..10 at every quiet K+P vs K placement.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K4/tempo_scan.py flat:3x4 cyl:3x4 ...

An integer n is a finite supply of |n| spare moves for White (n > 0) or Black (n < 0).  A placement
whose results change between n and n+1 has a tempo threshold there.  The scan extends the signature,
which only has n = -2..2, to see whether any threshold lies beyond +-2.
"""

import collections
import json
import os
import sys

import graph
import testgames as tg
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))
RANGE = range(-10, 11)


def scan(board):
    cg = graph.ChessGraph(board)
    prof = {pair: [] for pair in cg.quiet_kpk}
    for n in RANGE:
        T = tg.integer(n)
        res = solve_product(cg, T)
        for cw, cb in cg.quiet_kpk:
            prof[(cw, cb)].append('DWL'[res[cw * T.n + T.start]] + 'DWL'[res[cb * T.n + T.start]])
    out = []
    for (cw, cb), pr in prof.items():
        jumps = [n for n, a, b in zip(list(RANGE), pr, pr[1:]) if a != b]    # change between n and n+1
        out.append((cg.placement(cw), pr, jumps))
    return out


def summarize(board, rows):
    c = collections.Counter()
    for pl, pr, jumps in rows:
        c['max|jump| = %s' % (max(max(j, -j - 1) + (1 if j >= 0 else 0) for j in jumps) if jumps else 'none')] += 1
    return c


if __name__ == '__main__':
    lines = []
    for board in sys.argv[1:]:
        rows = scan(board)
        nj = collections.Counter(len(j) for _, _, j in rows)
        jump_at = collections.Counter(n for _, _, js in rows for n in js)
        far = [(pl, js) for pl, _, js in rows if any(j >= 2 or j <= -3 for j in js)]
        rec = dict(board=board, placements=len(rows), number_of_jumps=dict(sorted(nj.items())),
                   jump_between_n_and_n_plus_1={str(k): v for k, v in sorted(jump_at.items())},
                   placements_with_a_jump_beyond_pm2=len(far), examples_beyond_pm2=far[:5],
                   all_profiles_constant_for_n_ge_2_and_n_le_minus_2=(not far))
        print(json.dumps(rec), flush=True)
