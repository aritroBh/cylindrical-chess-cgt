#!/usr/bin/env python3
"""Print counterexamples with a FEN string and an ASCII board.

The FEN is the ordinary 8-file, 8-rank FEN of the position read on a flat
board; for a cylinder of n < 8 files only the first n files are used and files
a and n-1 are glued.  (For n = 8 the FEN is the usual one.)
"""

import sys

FILES = 'abcdefgh'


def parse(sq):
    return FILES.index(sq[0]), int(sq[1:]) - 1


def board(pieces, W=8, H=8):
    """pieces: list of (char, file, rank index, 0-based)"""
    grid = [['.' for _ in range(W)] for _ in range(H)]
    for ch, f, r in pieces:
        grid[r][f] = ch
    head = '  ' + ' '.join(FILES[i] for i in range(W))
    body = '\n'.join('%s ' % (r + 1) + ' '.join(grid[r]) for r in range(H - 1, -1, -1))
    return head + '\n' + body


def fen(pieces, W=8, H=8):
    grid = [['.' for _ in range(W)] for _ in range(H)]
    for ch, f, r in pieces:
        grid[r][f] = ch
    rows = []
    for r in range(H - 1, -1, -1):
        row, run = '', 0
        for f in range(W):
            c = grid[r][f]
            if c == '.':
                run += 1
            else:
                if run:
                    row += str(run)
                    run = 0
                row += c
        if run:
            row += str(run)
        rows.append(row)
    return '/'.join(rows)


def show(desc, wksq, pasq, bksq, W=8, H=8, stm='w'):
    kf, kr = parse(wksq)
    pf, pr = parse(pasq)
    bf, br = parse(bksq)
    pieces = [('K', kf, kr), ('P', pf, pr), ('k', bf, br)]
    print(desc)
    print('  position: WK %s  WP %s  BK %s   (%s to move)' % (wksq, pasq, bksq, stm))
    print('  FEN (files a..%s, cylinder: a and %s glued): %s w - - 0 1'
          % (FILES[W - 1], FILES[W - 1], fen(pieces, 8, 8)))
    print(board(pieces, W, H))
    print()


if __name__ == '__main__':
    show('cyl:4x8  direct opposition (kings a3 / a5, two ranks apart)',
         'a3', 'a2', 'a5', W=4, H=8)
    show('cyl:4x8  direct opposition, kings b3 / b5',
         'b3', 'a2', 'b5', W=4, H=8)
    show('cyl:8x8  direct opposition, kings a3 / a5',
         'a3', 'a2', 'a5', W=8, H=8)
    show('cyl:8x8  direct opposition, kings a6 / a8, pawn a7 between them',
         'a6', 'a7', 'a8', W=8, H=8)
    show('cyl:3x8  K+P vs K, white pawn one step from promotion',
         'a1', 'a7', 'a3', W=3, H=8)
