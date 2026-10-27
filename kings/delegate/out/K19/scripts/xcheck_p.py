"""Cross-check of the K19 full-board P solver (fullp.py) against kp_p (private build of K7's patched kpsolve with
--pmodel). Random legal positions with 1..3 pawns a side on small boards, both sides to move, e.p. on.
Results compared from White's point of view."""
import random, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from fullp import *

HERE = os.path.dirname(os.path.abspath(__file__))
KPP = os.path.join(HERE, '..', 'kp_p')


def rand_pos(B, rng):
    while True:
        npw, npb = rng.randint(0, 2), rng.randint(0, 2)
        if npw + npb == 0:
            continue
        sq = list(range(B.N))
        rng.shuffle(sq)
        wk, bk = sq[0], sq[1]
        rest = [s for s in sq[2:] if 0 < B.rank[s] < B.H - 1]
        if len(rest) < npw + npb:
            continue
        wp, bp = rest[:npw], rest[npw:npw + npb]
        pos = (wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), -1, rng.randint(0, 1))
        if legal_position(B, pos):
            return pos


def main():
    rng = random.Random(1027)
    tot = bad = 0
    dist = {}
    for spec, n in [('cyl:6x5', 150), ('flat:5x5', 100), ('cyl:7x6', 60), ('flat:6x6', 40)]:
        B = parse_board(spec)
        positions = [rand_pos(B, rng) for _ in range(n)]
        inp = '\n'.join(fmt_pos(B, p) for p in positions) + '\n'
        out = subprocess.run([KPP, '--board', spec, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel'],
                             input=inp, capture_output=True, text=True).stdout.splitlines()
        lines = [l for l in out if not l.startswith('[')]
        mine, ns = solve_p(B, positions)
        for pos, line in zip(positions, lines):
            a, b = line.split('|')[1].split()
            mv = white_pov(pos, mine[pos])
            tot += 1
            dist[(spec, mv)] = dist.get((spec, mv), 0) + 1
            if not (a == b == mv):
                bad += 1
                print('MISMATCH', spec, fmt_pos(B, pos), 'kp_p:', a, b, 'mine:', mv)
    print('positions', tot, 'mismatches', bad)
    print(sorted(dist.items()))


if __name__ == '__main__':
    main()
