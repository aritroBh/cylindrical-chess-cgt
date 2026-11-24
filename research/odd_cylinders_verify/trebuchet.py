#!/usr/bin/env python3
"""Recompute the 5.1 trébuchet on cylinders C_n x R.

Pattern (paper's Position 5.1, rotated so that the pawn file is file 0).
All coordinates below are 0-based (file 0 .. n-1, rank 0 .. R-1):

    White pawn   (0, r)        Black pawn   (0, r+1)
    White king   (n-1, r+1)    Black king   (1, r)

For the paper's own 8-file diagram the pawn file is a, so n-1 = h and the
kings are h5 / b4 with pawns a4 / a5, i.e. r = 3 (0-based).

The script
  * checks legality by hand (distinct squares, kings not adjacent even across
    the seam, pawns off the first and last rank, the side not to move not in
    check);
  * writes the position to a file and calls a kpsolve binary for both sides to
    move;
  * prints a table.

Usage:
  python3 trebuchet.py --solver ../../kings/kpsolve --wide-solver ./kpsolve_wide
"""

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def fname(f):
    return chr(ord('a') + f)


def king_adjacent(wf, wr, bf, br, n):
    df = min(abs(wf - bf), n - abs(wf - bf))
    dr = abs(wr - br)
    return df <= 1 and dr <= 1


def legal(wf, wr, bf, br, wp, bp, n, R, white_to_move):
    """Hand legality check of the trébuchet.  All coordinates 0-based."""
    if len({(wf, wr), (bf, br), (wp, bp), (wp, bp + 1)}) != 4:
        return False, 'two pieces share a square'
    if king_adjacent(wf, wr, bf, br, n):
        return False, 'kings adjacent'
    if bp in (0, R - 1):
        return False, 'white pawn on first/last rank'
    if bp + 1 in (0, R - 1):
        return False, 'black pawn on first/last rank'
    # the side NOT to move may not be in check
    w_att = {(wp - 1) % n, (wp + 1) % n}       # squares the white pawn attacks
    b_att = {(wp - 1) % n, (wp + 1) % n}       # squares the black pawn attacks
    if white_to_move:                         # Black is not to move
        if bf in w_att and br == bp + 1:
            return False, 'black king in check with White to move'
    else:                                     # White is not to move
        if wf in b_att and wr == bp:
            return False, 'white king in check with Black to move'
    return True, 'legal'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solver', default=os.path.join(HERE, '../../kings/kpsolve'))
    ap.add_argument('--wide-solver', default=os.path.join(HERE, 'kpsolve_wide'))
    ap.add_argument('--out', default=os.path.join(HERE, 'trebuchet_results.txt'))
    args = ap.parse_args()

    rows = []
    for n in range(3, 10):
        for R in range(5, 9):
            for r in range(1, R - 2):          # 1 <= r <= R-3 (0-based) keeps both pawns legal
                wf, wr = n - 1, r + 1
                bf, br = 1, r
                wp = 0
                ok_w, why_w = legal(wf, wr, bf, br, wp, r, n, R, True)
                ok_b, why_b = legal(wf, wr, bf, br, wp, r, n, R, False)
                assert ok_w == ok_b, (why_w, why_b)
                pos = 'K%s%d P%s%d p%s%d k%s%d' % (fname(wf), wr + 1, fname(wp), r + 1,
                                                   fname(wp), r + 2, fname(bf), br + 1)
                solver = args.solver if n <= 8 else args.wide_solver
                board = 'cyl:%dx%d' % (n, R)
                inp = '%s w -\n%s b -\n' % (pos, pos)
                out = subprocess.run([solver, '--board', board, '--ep', 'on',
                                      '--promote', 'QRBN', '--cap', '1'],
                                     input=inp, capture_output=True, text=True)
                res = [l.split('|')[1].split() for l in out.stdout.strip().split('\n')]
                rows.append((n, R, r, pos, why_w, res[0], res[1]))

    with open(args.out, 'w') as fh:
        fh.write('%3s %3s %3s %-22s %-30s %-6s %-6s %s\n' %
                 ('n', 'R', 'r', 'position', 'legality', 'WTM', 'BTM', 'mutual zugzwang'))
        for n, R, r, pos, why, wtm, btm in rows:
            mz = 'yes' if (wtm == ['L', 'L'] and btm == ['W', 'W']) else 'NO'
            fh.write('%3d %3d %3d %-22s %-30s %-6s %-6s %s\n' %
                     (n, R, r, pos, why, ' '.join(wtm), ' '.join(btm), mz))
    print(open(args.out).read())
    return 0


if __name__ == '__main__':
    sys.exit(main())
