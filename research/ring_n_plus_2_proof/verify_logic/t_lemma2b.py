"""Lemma 2(b) on every node of R_n (no flag in nodes): every move of a wall pawn q whose window j-1..j+3 (or j-3..j+1)
consists of pattern files is L or P."""
import sys, collections
from engine import *
def pat(j): return parse_file('W2') if j % 2 == 0 else parse_file('B4')
for n in map(int, sys.argv[1:]):
    start = parse(P_toks(n)); order, edges = build(start)
    cls_ = collections.Counter(); bad = 0
    for nd in order:
        pos, ep = nd
        for side in 'WB':
            for c, npos, nep, src, kind, pr in classify(pos, ep, side):
                j = src
                if j < 8 or j > n - 1: continue
                def ok(lo, hi):
                    return lo >= 7 and hi <= n - 1 and all(pos[k] == pat(k) for k in range(lo, hi + 1))
                if ok(j - 1, j + 3) or ok(j - 3, j + 1):
                    cls_[c] += 1
                    if c in 'TK': bad += 1
    print('n', n, 'wall-pawn moves with a pattern window', dict(cls_), 'T-or-K violations', bad)
