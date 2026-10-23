"""Audit of the hypotheses of T50's Lemmas 2 and 3 on every node of the reduced game R_n of P_n (fresh engine).
For each node and side:
  H-a  no passed pawn, no flag;  H-b  files c-4..c+5 (= 8..17 for c = 12) hold exactly the pattern pawn (W2 even / B4 odd);
  L2   every move of a pawn on files 9..16 is L or P (never T or K), and the poisoning reply of the hand table exists
       (capture / e.p. capture by the neighbour on the window side landing on the file of q, winning for Y);
  Q    which files the T-moves and K-moves come from (K-moves of pawns on files >= 7 would break the zone claim)."""
import sys, time, collections
from engine import *

def pat(j):
    return parse_file('W2') if j % 2 == 0 else parse_file('B4')

def audit(n, c=12):
    start = parse(P_toks(n))
    order, edges = build(start)
    lo, hi = c - 4, c + 5
    bad = collections.Counter()
    srcK = collections.Counter(); srcT = collections.Counter(); cls_arc = collections.Counter()
    table_ok = table_tot = 0
    for nd in order:
        pos, ep = nd
        if ep is not None: bad['flag'] += 1
        if passed_list(pos, ep, 'W') or passed_list(pos, ep, 'B'): bad['passed'] += 1
        for j in range(lo, hi + 1):
            if pos[j] != pat(j): bad['arc_not_pattern'] += 1
        for side in 'WB':
            y = other(side)
            for cl, npos, nep, src, kind, pr in classify(pos, ep, side):
                if cl == 'K': srcK[src] += 1
                if cl == 'T': srcT[src] += 1
                if lo + 1 <= src <= hi - 1:
                    cls_arc[(cl, kind)] += 1
                    if cl in 'TK': bad['arc_move_TK'] += 1
                    # table reply: capture by the neighbour on a window side
                    wins = []
                    if src + 3 <= hi and src - 1 >= lo: wins.append(+1)
                    if src - 3 >= lo and src + 1 <= hi: wins.append(-1)
                    assert wins, src
                    table_tot += 1
                    okany = False
                    for s in wins:
                        for p2, e2, s2, k2 in moves(npos, nep, y):
                            if s2 == src + s and k2 in ('cap', 'epcap') and status(p2, e2, y) == y:
                                okany = True
                    if okany: table_ok += 1
                    else: bad['no_table_reply'] += 1
    return len(order), dict(bad), dict(srcK), dict(srcT), dict(cls_arc), table_ok, table_tot

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        t0 = time.time()
        nn, bad, srcK, srcT, cls_arc, tok, ttot = audit(n)
        print('n', n, 'nodes', nn, 'violations', bad)
        print('   K-move source files', sorted(srcK.items()))
        print('   T-move source files', sorted(srcT.items()))
        print('   arc-interior (files 9..16) move classes', sorted(cls_arc.items()), 'table reply found', tok, '/', ttot, '%.1fs' % (time.time() - t0), flush=True)
