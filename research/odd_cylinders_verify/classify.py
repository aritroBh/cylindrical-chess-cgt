#!/usr/bin/env python3
"""Classify every K+P vs K cylinder position by the relation of the two kings.

Reads a kpsolve result file ("<position> | A B", A and B from White's point of
view) and reports, per board and per king relation, the W / D / L counts for
each side to move.

King relations (cylindrical file distance df = min(|f1-f2|, W-|f1-f2|),
rank distance dr = |r1-r2|):

  direct      df = 0, dr = 2   (kings on the same file, one square between)
  diag2       df = 1, dr = 2   (adjacent files, two ranks apart)
  diag1       df = 1, dr = 1   (classical diagonal opposition)
  horiz       df = 2, dr = 0   (same rank, one square between)
  samefile_d  df = 0, dr >= 3
  adjrank     df = 1, dr >= 3
  far         df >= 3
  samefile_1  df = 0, dr = 1   -> kings adjacent: illegal
  ...
"""

import argparse
import os
import sys
from collections import Counter, defaultdict

REL_ORDER = ['direct', 'diag2', 'diag1', 'horiz', 'samefile_d', 'adjrank', 'far']


def parse_sq(tok):
    return ord(tok[0]) - ord('a'), int(tok[1:]) - 1


def relation(wf, wr, bf, br, W, wrap=True):
    df = abs(wf - bf)
    if wrap:
        df = min(df, W - df)
    dr = abs(wr - br)
    if df == 0:
        if dr == 1:
            return 'adj_illegal'
        if dr == 2:
            return 'direct'
        return 'samefile_d'
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
    """-> dict (pawn, wk, bk) -> {'w': outcome, 'b': outcome} with outcome in W/D/L/X"""
    out = defaultdict(dict)
    with open(path) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if '|' not in line:
                continue
            pos, res = line.split('|')
            toks = pos.split()
            pieces = {}
            for t in toks[:-2]:
                pieces[t[0]] = t[1:]
            stm = toks[-2]
            a, b = res.split()
            assert a == b, line          # exact values only
            key = (pieces['P'], pieces['K'], pieces['k'])
            out[key][stm] = a
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True)
    ap.add_argument('--board', required=True)
    ap.add_argument('--label', default=None)
    args = ap.parse_args()
    kind, dims = args.board.split(':')
    W, H = (int(x) for x in dims.lower().split('x'))
    wrap = (kind == 'cyl')
    label = args.label or args.board

    tbl = load(args.results)

    # counters: relation -> stm -> outcome
    cnt = defaultdict(Counter)
    # per-triple: relation -> (both-draw, mixed, both-white-win, ...)
    triple = defaultdict(Counter)
    # relation -> list of (pos, w, b) for non-draw cases
    exceptions = defaultdict(list)
    illegal_half = Counter()

    for (psq, ksq, bsq), sides in sorted(tbl.items()):
        pf, pr = parse_sq(psq)
        kf, kr = parse_sq(ksq)
        bf, br = parse_sq(bsq)
        rel = relation(kf, kr, bf, br, W, wrap)
        w = sides.get('w')
        b = sides.get('b')
        # each side to move counted on its own
        if w is not None:
            cnt[rel][('w', w)] += 1
        if b is not None:
            cnt[rel][('b', b)] += 1
        if w is None or b is None:
            illegal_half[rel] += 1
            continue
        if w == 'D' and b == 'D':
            triple[rel]['both draw'] += 1
        elif w == 'W' and b == 'W':
            triple[rel]['both white win'] += 1
        elif 'X' in (w, b):
            triple[rel]['illegal'] += 1
        else:
            triple[rel]['mixed'] += 1
            if w == 'W' and b == 'D':
                triple[rel]['wtm white win, btm draw'] += 1
            elif w == 'D' and b == 'W':
                triple[rel]['wtm draw, btm white win'] += 1
            else:
                triple[rel]['other mixed'] += 1
            exceptions[rel].append((psq, ksq, bsq, w, b))

    print('=== %s ===' % label)
    print('%-12s %-9s %8s %8s %8s' % ('relation', 'stm', 'W', 'D', 'L'))
    for rel in REL_ORDER + ['adj_illegal']:
        if rel not in cnt:
            continue
        for stm in ('w', 'b'):
            c = cnt[rel]
            print('%-12s %-9s %8d %8d %8d' % (rel, stm, c[(stm, 'W')], c[(stm, 'D')], c[(stm, 'L')]))
    print()
    print('%-12s %14s %16s %14s %22s %20s' % (
        'relation', 'both draw', 'both white win', 'mixed', 'wtm W / btm D', 'wtm D / btm W'))
    for rel in REL_ORDER:
        if rel not in triple:
            continue
        t = triple[rel]
        print('%-12s %14d %16d %14d %22d %20d' % (
            rel, t['both draw'], t['both white win'], t['mixed'],
            t['wtm white win, btm draw'], t['wtm draw, btm white win']))
    if illegal_half:
        print('triples with an illegal side-to-move variant (pawn giving check):',
              dict(illegal_half))
    for rel in exceptions:
        print()
        print('--- %s: %d triples that are NOT a draw for both sides ---' % (rel, len(exceptions[rel])))
        for row in exceptions[rel]:
            print('   WP %s  WK %s  BK %s   WTM=%s BTM=%s' % row)
    return 0


if __name__ == '__main__':
    sys.exit(main())
