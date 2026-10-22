"""Check 1: chess variant (T = 0, stalemate = draw) against kpsolve.

Every node of the chess graph (all KPK positions with either side to move, plus the K+officer vs K
and K vs K positions they lead to) is written to a file, kpsolve (C) solves it, and the two answers
are compared.  The node set is every legal K+P vs K position with either side to move (some are unreachable
from any quiet placement: Black to move, in check from a second-rank pawn) plus the K+officer vs K and K vs K positions
they lead to.
kpsolve is built with:  cc -O2 -o kings/delegate/out/K4/kp kings/kpsolve.c
"""

import gzip
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
    inp = os.path.join(workdir, tag + '.in.gz')
    outp = os.path.join(workdir, tag + '.out.gz')
    raw = ('\n'.join(cg.kp_line(i) for i in range(cg.n)) + '\n').encode()
    if len(raw) > 100 * 1024 * 1024:
        raise ValueError('kpsolve input exceeds 100 MB')
    packed_input = gzip.compress(raw, mtime=0)
    if len(packed_input) > 50 * 1024 * 1024:
        raise ValueError('compressed kpsolve input would exceed 50 MB')
    with open(inp, 'wb') as f:
        f.write(packed_input)
    cmd = ['nice', '-n', '10', KP, '--board', cg.board, '--ep', 'on', '--promote', 'QRBN',
           '--cap', '1', '--threads', '2']
    # Popen's stdin/stdout file-descriptor path bypasses gzip's Python wrappers. Feed the bounded
    # uncompressed bytes through communicate, then compress the result before writing it.
    result = subprocess.run(cmd, input=raw, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True).stdout
    packed_output = gzip.compress(result, mtime=0)
    if len(packed_output) > 50 * 1024 * 1024:
        raise ValueError('compressed kpsolve output would exceed 50 MB')
    with open(outp, 'wb') as f:
        f.write(packed_output)
    mine = solve_product(cg, GAMES['0'], stalemate_draw=True)
    stale = solve_product(cg, GAMES['0'], stalemate_draw=False)     # T = 0, stalemate is a loss
    kpk_results = {}
    mutual_placements = []
    kpk = set(cg.kpk)
    r = dict(board=cg.board, kpk=0, other=0, x=0, diffs=[], stale_loss_kpk=0, stale_loss_all=0,
             nodes=cg.n, cmd=' '.join(cmd))
    rank = {'L': 0, 'D': 1, 'W': 2}
    with gzip.open(outp, 'rt') as f:
        for i, line in enumerate(f):
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
            if i in kpk:
                kpk_results[i] = a
            if mine[i] != stale[i]:
                r['stale_loss_all'] += 1
                if i in kpk:
                    r['stale_loss_kpk'] += 1
    assert r['kpk'] + r['other'] + r['x'] == cg.n, (r['kpk'], r['other'], r['x'], cg.n)
    for cw, cb in cg.quiet_kpk:
        pl = cg.placement(cw)
        white, black = kpk_results[cw], kpk_results[cb]
        if rank[black] > rank[white]:
            mutual_placements.append(pl)
    r['mutual_placements'] = mutual_placements
    r['mutual_zugzwangs'] = len(mutual_placements)
    r['kpk_outcomes'] = {cg.placement(cw): [kpk_results[cw], kpk_results[cb]] for cw, cb in cg.quiet_kpk}
    return r
