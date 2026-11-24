#!/usr/bin/env python3
"""Summary tables for the T25 verification of T12 (odd-width cylinders).

For every board: totals, per-side-to-move W/D/L, the number of mutual
zugzwangs (White to move draws but Black to move loses) and the same split by
the relation of the two kings.  Finally an odd/even comparison.
"""

import argparse
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_sq(tok):
    return ord(tok[0]) - ord('a'), int(tok[1:]) - 1


def relation(wf, wr, bf, br, W):
    df = abs(wf - bf)
    df = min(df, W - df)
    dr = abs(wr - br)
    if df == 0:
        return 'direct' if dr == 2 else ('adj_illegal' if dr == 1 else 'samefile_d')
    if df == 1:
        if dr == 0:
            return 'adj_illegal'
        if dr == 1:
            return 'diag1'
        if dr == 2:
            return 'diag2'
        return 'adjrank'
    if df == 2 and dr == 0:
        return 'horiz'
    return 'far'


def load(path):
    out = defaultdict(dict)
    with open(path) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if '|' not in line:
                continue
            pos, res = line.split('|')
            toks = pos.split()
            pieces = {t[0]: t[1:] for t in toks[:-2]}
            stm = toks[-2]
            a, b = res.split()
            assert a == b, line
            out[(pieces['P'], pieces['K'], pieces['k'])][stm] = a
    return out


def board_stats(path, W):
    tbl = load(path)
    stm_cnt = {'w': Counter(), 'b': Counter()}
    rel_stm = defaultdict(lambda: {'w': Counter(), 'b': Counter()})
    triples = Counter()
    rel_triples = defaultdict(Counter)
    for (psq, ksq, bsq), sides in tbl.items():
        pf, pr = parse_sq(psq)
        kf, kr = parse_sq(ksq)
        bf, br = parse_sq(bsq)
        rel = relation(kf, kr, bf, br, W)
        w, b = sides.get('w'), sides.get('b')
        # each side to move is counted on its own: the variant "Black to move"
        # of a position in which the white pawn gives check is legal, the
        # variant "White to move" is not.
        if w is not None:
            stm_cnt['w'][w] += 1
            rel_stm[rel]['w'][w] += 1
        if b is not None:
            stm_cnt['b'][b] += 1
            rel_stm[rel]['b'][b] += 1
        if w is None or b is None:
            triples['one side to move illegal'] += 1
            rel_triples[rel]['one side to move illegal'] += 1
            continue
        if w == 'D' and b == 'D':
            triples['both draw'] += 1
            rel_triples[rel]['both draw'] += 1
        elif w == 'W' and b == 'W':
            triples['both white win'] += 1
            rel_triples[rel]['both white win'] += 1
        elif w == 'D' and b == 'W':
            triples['mutual zugzwang'] += 1
            rel_triples[rel]['mutual zugzwang'] += 1
        else:
            triples['white win only if White moves first'] += 1
            rel_triples[rel]['white win only if White moves first'] += 1
    return tbl, stm_cnt, rel_stm, triples, rel_triples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default=HERE)
    args = ap.parse_args()

    boards = ['3x8', '4x8', '5x8', '6x8', '7x8', '8x8', '5x6', '7x6', '9x8', '10x8']
    print('## Totals per board (cylinders, 8 ranks unless stated)\n')
    print('%-9s %9s %8s %8s %8s | %8s %8s %8s | %9s %9s' %
          ('board', 'positions', 'WTM W', 'WTM D', 'WTM L', 'BTM W', 'BTM D', 'BTM L',
           'W win %', 'mut. zug'))
    stats = {}
    for b in boards:
        path = os.path.join(args.dir, 'res_c_cyl%s_qrbn.txt' % b)
        if not os.path.exists(path):
            path = os.path.join(args.dir, 'res_wide_cyl%s_qrbn.txt' % b)
        W = int(b.split('x')[0])
        tbl, stm_cnt, rel_stm, triples, rel_triples = board_stats(path, W)
        stats[b] = (stm_cnt, rel_stm, triples, rel_triples)
        nw = stm_cnt['w']['W']
        nd = stm_cnt['w']['D']
        tot = nw + nd + stm_cnt['w']['L']
        totall = tot + stm_cnt['b']['W'] + stm_cnt['b']['D'] + stm_cnt['b']['L']
        print('%-9s %9d %8d %8d %8d | %8d %8d %8d | %8.2f%% %9d' %
              ('cyl:' + b, totall, nw, nd, stm_cnt['w']['L'],
               stm_cnt['b']['W'], stm_cnt['b']['D'], stm_cnt['b']['L'],
               100.0 * nw / tot, triples['mutual zugzwang']))

    print('\n## Triples (WP, WK, BK) by outcome of the two side-to-move variants\n')
    print('%-9s %12s %14s %14s %22s' %
          ('board', 'both draw', 'both white win', 'mutual zugzwang', 'W win iff White moves'))
    for b in boards:
        t = stats[b][2]
        print('%-9s %12d %14d %14d %22d' %
              ('cyl:' + b, t['both draw'], t['both white win'], t['mutual zugzwang'],
               t['white win only if White moves first']))

    for rel in ('direct', 'diag2', 'horiz'):
        print('\n## Relation "%s" (df, dr) per board\n' % rel)
        print('%-9s %12s %14s %14s %22s' %
              ('board', 'both draw', 'both white win', 'mutual zugzwang', 'W win iff White moves'))
        for b in boards:
            t = stats[b][3].get(rel, Counter())
            print('%-9s %12d %14d %14d %22d' %
                  ('cyl:' + b, t['both draw'], t['both white win'], t['mutual zugzwang'],
                   t['white win only if White moves first']))

    print('\n## Odd vs even (8 ranks)\n')
    print('%-9s %10s %10s %10s %10s' %
          ('n', 'positions', 'W win % (WTM)', 'mut. zug', 'WTM draw %'))
    for b in ['3x8', '4x8', '5x8', '6x8', '7x8', '8x8', '9x8', '10x8']:
        stm_cnt, rel_stm, triples, rel_triples = stats[b]
        nw = stm_cnt['w']['W']
        nd = stm_cnt['w']['D']
        tot = nw + nd + stm_cnt['w']['L']
        print('%-9s %10d %13.2f%% %10d %13.2f%%' %
              ('cyl:' + b, tot, 100.0 * nw / tot, triples['mutual zugzwang'],
               100.0 * nd / tot))
    return 0


if __name__ == '__main__':
    sys.exit(main())
