#!/usr/bin/env python3
"""Generate every K+P vs K position on a cylinder (or flat board) of W files x H ranks.

Independent of research/kp_tablebases/generate_kpk.py and of every T12 script.

Legality (kings/SPEC.md):
  * the three pieces sit on different squares;
  * a white pawn may not stand on rank 1 or rank H;
  * the kings may not be adjacent (cylindrically: across the seam too);
  * the side *not* to move may not be in check (here: the white pawn may not
    attack the black king when Black is not the side to move, and the black
    king may not attack the white king -- that is the king-adjacency rule).

Every position is emitted twice, once for each side to move, so the two
sides-to-move tables come out of one run.
"""

import argparse
import sys


def sq_name(f, r):
    return chr(ord('a') + f) + str(r + 1)


def king_attacks(f, r, W, H, wrap):
    out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            nf, nr = f + df, r + dr
            if not (0 <= nr < H):
                continue
            if wrap:
                nf %= W
            elif not (0 <= nf < W):
                continue
            out.append((nf, nr))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--board', required=True, help='cyl:WxH or flat:WxH')
    ap.add_argument('--out', default=None)
    args = ap.parse_args()
    kind, dims = args.board.split(':')
    w, h = dims.lower().split('x')
    W, H, wrap = int(w), int(h), (kind == 'cyl')

    out = open(args.out, 'w') if args.out else sys.stdout
    n = 0
    for wf in range(W):
        for wr in range(H):
            for pf in range(W):
                for pr in range(1, H - 1):          # a pawn may not stand on rank 1 or H
                    if (pf, pr) == (wf, wr):
                        continue
                    for bf in range(W):
                        for br in range(H):
                            if (bf, br) in ((wf, wr), (pf, pr)):
                                continue
                            if (bf, br) in king_attacks(wf, wr, W, H, wrap):
                                continue            # kings adjacent -> illegal
                            wk = sq_name(wf, wr)
                            wp = sq_name(pf, pr)
                            bk = sq_name(bf, br)
                            # The side *not* to move may not be in check (kings/SPEC.md 7).
                            # With only a white pawn on the board, the only extra check is
                            # the white pawn attacking the black king.  That is illegal
                            # when *White* is to move (Black just moved into check) and
                            # legal when Black is to move (White just gave check).
                            pawn_hits_bk = (abs(pf - bf) % W in (1, W - 1)) and pr + 1 == br
                            for stm in ('w', 'b'):
                                if stm == 'w' and pawn_hits_bk:
                                    continue
                                out.write('K%s P%s k%s %s -\n' % (wk, wp, bk, stm))
                                n += 1
    if args.out:
        out.close()
    else:
        sys.stderr.write('%d positions\n' % n)


if __name__ == '__main__':
    main()
