#!/usr/bin/env python3
"""Sub-classify the "direct opposition" (same file, two ranks apart) positions by
where the white pawn stands relative to the two kings, and do the same for the
"diagonal" class (adjacent files, two ranks apart).

pawn role:
  between   the pawn stands on the same file strictly between the two kings
  behind_w  the pawn is on the kings' file, below both kings
  behind_b  the pawn is on the kings' file, above both kings
  otherfile the pawn is on a different file
"""

import argparse
import sys
from collections import Counter, defaultdict


def parse_sq(tok):
    return ord(tok[0]) - ord('a'), int(tok[1:]) - 1


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


def pawn_role(pf, pr, kf, kr, bf, br):
    if pf != kf:
        return 'otherfile'
    lo, hi = sorted((kr, br))
    if lo < pr < hi:
        return 'between'
    if pr <= lo:
        return 'behind_w'
    return 'behind_b'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True)
    ap.add_argument('--board', required=True)
    ap.add_argument('--rel', default='direct', choices=('direct', 'diag2'))
    args = ap.parse_args()
    kind, dims = args.board.split(':')
    W = int(dims.lower().split('x')[0])
    tbl = load(args.results)

    cnt = defaultdict(Counter)
    bad = defaultdict(list)
    for (psq, ksq, bsq), sides in sorted(tbl.items()):
        pf, pr = parse_sq(psq)
        kf, kr = parse_sq(ksq)
        bf, br = parse_sq(bsq)
        df = min(abs(kf - bf), W - abs(kf - bf))
        dr = abs(kr - br)
        if args.rel == 'direct':
            if not (df == 0 and dr == 2):
                continue
        else:
            if not (df == 1 and dr == 2):
                continue
        role = pawn_role(pf, pr, kf, kr, bf, br)
        w, b = sides.get('w'), sides.get('b')
        if w is None or b is None:
            cnt[role]['illegal half'] += 1
            continue
        cnt[role]['WTM ' + w] += 1
        cnt[role]['BTM ' + b] += 1
        if w == 'D' and b == 'D':
            cnt[role]['both draw'] += 1
        elif w == 'W' and b == 'W':
            cnt[role]['both white win'] += 1
        else:
            cnt[role]['mixed'] += 1
            bad[role].append((psq, ksq, bsq, w, b))

    print('=== %s  relation=%s ===' % (args.board, args.rel))
    keys = ['both draw', 'both white win', 'mixed', 'WTM W', 'WTM D', 'BTM W', 'BTM D',
            'illegal half']
    print('%-11s' % 'pawn role' + ''.join('%18s' % k for k in keys))
    for role in ('between', 'behind_w', 'behind_b', 'otherfile'):
        if role not in cnt:
            continue
        print('%-11s' % role + ''.join('%18d' % cnt[role][k] for k in keys))
    for role, rows in bad.items():
        print()
        print('--- %s: %d non-draw triples ---' % (role, len(rows)))
        for row in rows[:25]:
            print('   WP %s  WK %s  BK %s   WTM=%s BTM=%s' % row)
    return 0


if __name__ == '__main__':
    sys.exit(main())
