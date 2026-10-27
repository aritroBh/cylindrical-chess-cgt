"""Cross-check of the K19 move generator against `kp --moves` (private build of kings/kpsolve.c).
Random positions with 0..3 pawns a side, with and without e.p. rights, on several boards.
Compares: legality of the position, and the set of (piece, from, to, promotion?) moves."""
import random, subprocess, sys, re, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *

HERE = os.path.dirname(os.path.abspath(__file__))
KP = os.path.join(HERE, '..', 'kp')


def rand_pos(B, rng, ep_case):
    for _ in range(1000):
        npw, npb = rng.randint(0, 2), rng.randint(0, 2)
        sq = list(range(B.N))
        rng.shuffle(sq)
        wk, bk = sq[0], sq[1]
        rest = sq[2:]
        wp = [s for s in rest[:12] if 0 < B.rank[s] < B.H - 1][:npw]
        rest2 = [s for s in rest[12:] if 0 < B.rank[s] < B.H - 1 and s not in wp]
        bp = rest2[:npb]
        stm = rng.randint(0, 1)
        ep = -1
        if ep_case:
            # build an e.p. right: a pawn of colour (1-stm) has just double-stepped
            c = 1 - stm
            cands = []
            for p in (wp if c == 0 else bp):
                if (c == 0 and B.rank[p] == 3) or (c == B.H - 1 - 0 and False):
                    cands.append(p)
                if c == 1 and B.rank[p] == B.H - 4:
                    cands.append(p)
            if not cands:
                continue
            p = rng.choice(cands)
            tgt = p - B.W if c == 0 else p + B.W
            src = p - 2 * B.W if c == 0 else p + 2 * B.W
            occ = set([wk, bk] + wp + bp)
            if tgt in occ or src in occ:
                continue
            ep = tgt
        pos = (wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), ep, stm)
        return pos
    return None


def kp_text(B, pos):
    return fmt_pos(B, pos)


def main():
    rng = random.Random(20261027)
    total = bad = illeg_mismatch = nmoves = 0
    for spec, n_plain, n_ep in [('cyl:7x6', 150, 100), ('cyl:8x6', 80, 40), ('flat:6x6', 120, 60), ('cyl:6x5', 120, 60), ('flat:5x4', 150, 50), ('cyl:8x8', 60, 40)]:
        B = parse_board(spec)
        positions = []
        for i in range(n_plain + n_ep):
            pos = rand_pos(B, rng, i >= n_plain)
            if pos is not None:
                positions.append(pos)
        inp = '\n'.join(fmt_pos(B, p) for p in positions) + '\n'
        res = subprocess.run(['/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh', KP, '--board', spec, '--ep', 'on', '--promote', 'Q', '--cap', '0', '--moves'],
                             input=inp, capture_output=True, text=True).stdout.splitlines()
        lines = [l for l in res if not l.startswith('[')]
        assert len(lines) == len(positions), (len(lines), len(positions))
        for pos, line in zip(positions, lines):
            total += 1
            parts = line.split('|')
            legal_kp = parts[1].strip() != 'X X'
            legal_me = legal_position(B, pos)
            if legal_kp != legal_me:
                illeg_mismatch += 1
                print('LEGALITY MISMATCH', spec, line, legal_me)
                continue
            if not legal_me:
                continue
            kpm = set()
            if len(parts) > 2:
                for tok in parts[2].replace('A:', ' ').split():
                    m = re.match(r'([KkPp])([a-h]\d)([a-h]\d)(=Q)?:', tok)
                    kpm.add((m.group(1).upper(), B.sq(m.group(2)), B.sq(m.group(3)), bool(m.group(4))))
            me = set()
            for mv in legal_moves(B, pos):
                piece = 'K' if (mv.frm == pos[0 if pos[5] == 0 else 1]) else 'P'
                me.add((piece, mv.frm, mv.to, mv.kind == 'p'))
            nmoves += len(me)
            if me != kpm:
                bad += 1
                print('MOVE MISMATCH', spec, fmt_pos(B, pos), sorted(me ^ kpm))
    print('positions', total, 'legality mismatches', illeg_mismatch, 'move-set mismatches', bad, 'moves compared', nmoves)


main()
