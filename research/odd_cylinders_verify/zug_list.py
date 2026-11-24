#!/usr/bin/env python3
"""List the mutual zugzwangs (White to move draws, Black to move loses) of a
K+P vs K cylinder, grouped by the relation of the two kings and the pawn role.
"""

import argparse
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_sq(tok):
    return ord(tok[0]) - ord('a'), int(tok[1:]) - 1


def relation(wf, wr, bf, br, W):
    df = min(abs(wf - bf), W - abs(wf - bf))
    dr = abs(wr - br)
    if df == 0:
        return 'direct' if dr == 2 else 'samefile_d'
    if df == 1:
        return 'diag2' if dr == 2 else 'adjrank'
    if df == 2 and dr == 0:
        return 'horiz'
    return 'far'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True)
    ap.add_argument('--board', required=True)
    ap.add_argument('--show', type=int, default=0)
    args = ap.parse_args()
    W = int(args.board.split(':')[1].split('x')[0])
    tbl = defaultdict(dict)
    with open(args.results) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if '|' not in line:
                continue
            pos, res = line.split('|')
            toks = pos.split()
            pieces = {t[0]: t[1:] for t in toks[:-2]}
            a, b = res.split()
            tbl[(pieces['P'], pieces['K'], pieces['k'])][toks[-2]] = a
    cnt = Counter()
    rows = []
    for (p, k, b), s in sorted(tbl.items()):
        if s.get('w') == 'D' and s.get('b') == 'W':
            pf, pr = parse_sq(p)
            kf, kr = parse_sq(k)
            bf, br = parse_sq(b)
            rel = relation(kf, kr, bf, br, W)
            role = 'same file as kings' if pf == kf else 'other file'
            cnt[(rel, role)] += 1
            rows.append((rel, role, p, k, b))
    print('=== %s: %d mutual zugzwangs ===' % (args.board, len(rows)))
    for (rel, role), n in sorted(cnt.items()):
        print('  %-10s %-20s %6d' % (rel, role, n))
    for row in rows[:args.show]:
        print('   ', row)


if __name__ == '__main__':
    sys.exit(main())
