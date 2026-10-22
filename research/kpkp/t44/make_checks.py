#!/usr/bin/env python3
"""Build the input lists for the second-program (kings/ref/solve.py) spot checks.  Run from the project root:
    .venv/bin/python -I research/kpkp/t44/make_checks.py

Why strata.  The reference solver is pure Python.  A queen/rook/bishop/knight layer costs about 5 s, and a position
needs every layer reachable from it, so a uniform sample over all pawn files would need about 400 officer layers
per board.  The cap-1 check therefore samples uniformly inside two strata of pawn files:
    G1: White pawn on file a or h, Black pawn on file a or h              (the seam files; about 100 layers)
    G2: White pawn on file b, d or g, Black pawn on file b, e or g        (about 150 layers)
A third list (U, uniform over the whole board) is checked with --cap 0, where promotions are terminal and only
pawn layers are needed.  Expected values come from the kpsolve tables (cap 1) or from a fresh kpsolve --cap 0 run.

Writes (in this directory): chk_<board>_G1.exp, chk_<board>_G2.exp, chk_<board>_U.exp,
chk_cyl_mz.exp (the cylinder values of 20 cylinder-only mutual-zugzwang pairs = 40 positions),
chk_flat_mz.exp (the flat values of the same 40 positions), chk_cyl_mz_pairs.txt (which pairs).
Each .exp line is `position | A B` with A B read from the table (U lists: A B are those of the cap-1 table and are
replaced by the cap-0 values by run_checks.sh).
"""
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
G1W, G1B = set('ah'), set('ah')
G2W, G2B = set('bdg'), set('beg')
N1, N2 = 110, 110


def stream(board):
    for i in range(4):
        p = subprocess.Popen(['zstdcat', os.path.join(HERE, 'kpkp_%s_%d.out.zst' % (board, i))],
                             stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
        for line in p.stdout:
            yield line.rstrip('\n')
        p.wait()


def reservoir(lst, item, n, count, rng):
    if len(lst) < n:
        lst.append(item)
    else:
        j = rng.randrange(count)
        if j < n:
            lst[j] = item


def main():
    rng = random.Random(20261023)
    # the 20 cylinder-only mutual zugzwang pairs: stratified by type and pawn-file group
    pairs = []
    p = subprocess.run(['zstdcat', os.path.join(HERE, 'mz_cyl_only.tsv.zst')], capture_output=True, text=True)
    rows = [r.split('\t') for r in p.stdout.splitlines()[1:]]
    g1 = [r for r in rows if r[1][0] in G1W and r[3][0] in G1B]
    g2 = [r for r in rows if r[1][0] in G2W and r[3][0] in G2B]
    pick = []
    for pool, typ, k in ((g1, '4', 8), (g1, '3', 3), (g1, '5', 3), (g2, '3', 3), (g2, '5', 3)):
        cand = [r for r in pool if r[8] == typ]
        pick += rng.sample(cand, k)
    mzpos_cyl, mzpos_flat = [], []
    with open(os.path.join(HERE, 'chk_cyl_mz_pairs.txt'), 'w') as f:
        f.write('\t'.join(['wk', 'wp', 'bk', 'bp', 'cyl_w', 'cyl_b', 'flat_w', 'flat_b', 'type', 'seam', 'fen']) + '\n')
        for r in pick:
            f.write('\t'.join(r) + '\n')
    mz_keys = {}
    for r in pick:
        wk, wp, bk, bp = r[0], r[1], r[2], r[3]
        for stm, cv, fv in (('w', r[4], r[6]), ('b', r[5], r[7])):
            pos = 'K%s P%s k%s p%s %s -' % (wk, wp, bk, bp, stm)
            mz_keys[pos] = True
            mzpos_cyl.append('%s | %s %s' % (pos, cv[0], cv[1]))
            mzpos_flat.append('%s | %s %s' % (pos, fv[0], fv[1]))
    for name, lines in (('chk_cyl_mz.exp', mzpos_cyl), ('chk_flat_mz.exp', mzpos_flat)):
        with open(os.path.join(HERE, name), 'w') as f:
            f.write('\n'.join(lines) + '\n')

    for board in ('cyl', 'flat'):
        s1, s2, su = [], [], []
        c1 = c2 = cu = 0
        for line in stream(board):
            t = line.split()
            wf, bf = t[1][1], t[3][1]
            cu += 1
            reservoir(su, line, 300, cu, rng)
            if wf in G1W and bf in G1B:
                c1 += 1
                reservoir(s1, line, N1, c1, rng)
            elif wf in G2W and bf in G2B:
                c2 += 1
                reservoir(s2, line, N2, c2, rng)
        for tag, lst in (('G1', s1), ('G2', s2), ('U', su)):
            with open(os.path.join(HERE, 'chk_%s_%s.exp' % (board, tag)), 'w') as f:
                f.write('\n'.join(lst) + '\n')
        print(board, 'stratum sizes', c1, c2, cu, 'samples', len(s1), len(s2), len(su))


if __name__ == '__main__':
    main()
