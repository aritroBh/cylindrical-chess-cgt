"""Lemma 2(a) on every node of R_n: after any move of a wall pawn q (pattern files j-1,j,j+1) the mover has no passed pawn;
also H3: such a pawn has no capture / e.p. capture."""
import sys, collections
from engine import *
def pat(j): return parse_file('W2') if j % 2 == 0 else parse_file('B4')
for n in map(int, sys.argv[1:]):
    start = parse(P_toks(n)); order, edges = build(start)
    tot = bad = caps = 0; files = set()
    for nd in order:
        pos, ep = nd
        for side in 'WB':
            for npos, nep, src, kind in moves(pos, ep, side):
                j = src
                if j < 7 or j > n - 1: continue
                if not all(pos[(j + d) % n] == pat((j + d) % n) for d in (-1, 0, 1)): continue
                # j+-1 pattern requires j-1 >= 7 (file 6 is not a pattern file) and (j+1) % n == 0 is not a pattern file
                if j - 1 < 7 or j + 1 > n - 1: continue
                tot += 1; files.add(j)
                if kind in ('cap', 'epcap'): caps += 1
                if passed_list(npos, nep, side): bad += 1
    print('n', n, 'moves of wall pawns with pattern neighbours', tot, 'files', min(files), '..', max(files), '| Z has passed pawn after:', bad, '| captures:', caps)
