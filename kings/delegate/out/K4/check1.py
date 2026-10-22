"""Check 1 of brief K4: chess variant (T = 0, stalemate = draw) against kpsolve.

Every node of the chess graph (all KPK positions with either side to move, plus the K+officer vs K
and K vs K positions they lead to) is written to a file, kpsolve (C) solves it, and the two answers
are compared.  The node set is every legal K+P vs K position with either side to move (some are unreachable
from any quiet placement: Black to move, in check from a second-rank pawn) plus the K+officer vs K and K vs K positions
they lead to.
kpsolve is built with:  cc -O2 -o kings/delegate/out/K4/kp kings/kpsolve.c
"""

import os
import subprocess

from testgames import GAMES
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))
KP = os.path.join(HERE, 'kp')


def check1(cg, workdir):
    """Returns dict(kpk=, other=, diffs=[...], x=, stale_loss_kpk=, stale_loss_all=).

    kpk / other: positions compared with and without a pawn.  stale_loss_kpk / stale_loss_all: how many of those
    positions get a different T = 0 result when a stalemate counts as a loss instead of a draw (they are NOT
    counts of stalemate positions)."""
    os.makedirs(workdir, exist_ok=True)
    tag = cg.board.replace(':', '_')
    inp = os.path.join(workdir, tag + '.in')
    outp = os.path.join(workdir, tag + '.out')
    with open(inp, 'w') as f:
        for i in range(cg.n):
            f.write(cg.kp_line(i) + '\n')
    cmd = ['nice', '-n', '10', KP, '--board', cg.board, '--ep', 'on', '--promote', 'QRBN',
           '--cap', '1', '--threads', '2']
    with open(inp) as fi, open(outp, 'w') as fo:
        subprocess.run(cmd, stdin=fi, stdout=fo, stderr=subprocess.DEVNULL, check=True)
    mine = solve_product(cg, GAMES['0'], stalemate_draw=True)
    stale = solve_product(cg, GAMES['0'], stalemate_draw=False)     # T = 0, stalemate is a loss
    lines = open(outp).read().splitlines()
    assert len(lines) == cg.n, (len(lines), cg.n)
    kpk = set(cg.kpk)
    r = dict(board=cg.board, kpk=0, other=0, x=0, diffs=[], stale_loss_kpk=0, stale_loss_all=0,
             nodes=cg.n, cmd=' '.join(cmd))
    for i, line in enumerate(lines):
        pos, res = line.rsplit(' | ', 1)
        a, b = res.split()
        if a == 'X' or b == 'X':
            r['x'] += 1
            r['diffs'].append((cg.kp_line(i), 'X', 'X', 'DWL'[mine[i]]))
            continue
        want = 'DWL'[mine[i]]
        if a != b or a != want:
            r['diffs'].append((cg.kp_line(i), a, b, want))
        r['kpk' if i in kpk else 'other'] += 1
        if mine[i] != stale[i]:
            r['stale_loss_all'] += 1
            if i in kpk:
                r['stale_loss_kpk'] += 1
    return r
