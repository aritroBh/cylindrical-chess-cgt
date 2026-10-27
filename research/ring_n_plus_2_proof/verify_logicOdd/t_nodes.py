"""On the ACTUAL reduced nodes of R_n / Qo_n (n = 19, 21), engine D:
 (1) Lemma 2 (a),(b) for every central wall pawn (files 3..n-9 .. as in the proof: arc 2..11 resp. 2..13), windows as in the proof, tallies by (file, class);
 (2) a finer version of Lemma 3 (ii)-(iii) with the race rule exercised: for every node p and every move mu of a FAR pawn (source file not central)
     compare the verdict of the child c_mu with that of ins_6(c_mu): T / L / non-terminal, and, for non-terminal ones, P vs K.  Count how many children
     are races (both sides have a passed pawn), how many races are won by each side, and how many are ties;
 (3) the left-end facts: every move of the file-2 pawn W2 and of the file-3 pawn B4 is P (resp. L) in every node;  K-moves by source file.
usage: t_nodes.py FAM n"""
import sys, time
from collections import Counter
from common import *

def kind(pos, ep, side, npos, nep):
    y = other(side)
    st = status(npos, nep, side)
    if st == side: return 'T'
    if st == y: return 'L'
    for p2, e2, s2, k2 in moves(npos, nep, y):
        if status(p2, e2, y) == y: return 'P'
    return 'K'

def main(fam, n):
    c = 6
    t0 = time.time()
    start = parse(TOKS[fam](n))
    order, edges = build(start)
    arc_hi = n - 8
    arc_hi = min(arc_hi, 13) if n >= 21 else 11
    central = list(range(c - 3, c + 5))             # 3..10 for the p of the pump (arc 2..11)
    lo = 2
    # Lemma 2 windows for the arc 2..arc_hi
    hi = c + 5 if n == 19 else arc_hi
    cen = list(range(3, hi))
    stats = Counter(); l2 = Counter()
    for nd in order:
        pos, ep = nd
        assert ep is None
        for j in cen:
            w = (j - 1, j + 3) if j + 3 <= hi else (j - 3, j + 1)
            assert all(pos[f] == pat(f) for f in range(w[0], w[1] + 1))
            side = 'W' if j % 2 == 0 else 'B'
            for npos, nep, src, kd in moves(pos, ep, side):
                if src != j: continue
                assert not passed_list(npos, nep, side), 'Lemma 2(a)'
                k = kind(pos, ep, side, npos, nep)
                assert k in 'LP', ('Lemma 2(b)', j, k)
                l2[(j, k)] += 1
    print(f'{fam}_{n}: Lemma 2 (a),(b) on the nodes: central files 3..{hi-1}: 0 violations; tally {dict(sorted(l2.items()))}', flush=True)
    # (2) far moves, ins_6 correspondence, with races
    race = Counter(); corr = Counter(); bysrc = Counter()
    for nd in order:
        pos, ep = nd
        for side in 'WB':
            for npos, nep, src, kd in moves(pos, ep, side):
                if 3 <= src <= hi - 1: continue            # central pawns: Lemma 2
                a = kind(pos, ep, side, npos, nep)
                bysrc[(src, a)] += 1
                ipos, iep = ins(npos, c), None
                if nep is not None: iep = (nep[0] if nep[0] <= c else nep[0] + 2, nep[1])
                b = kind(ins(pos, c), None, side, ipos, iep)
                corr['moves'] += 1
                if a != b: corr['MISMATCH'] += 1; corr.setdefault('ex', (fmt(pos), side, src, a, b))
                wp, bp = passed_list(npos, nep, 'W'), passed_list(npos, nep, 'B')
                if wp and bp:
                    race['races'] += 1
                    w = status(npos, nep, side)
                    race['won_by_mover' if w == side else 'won_by_opponent'] += 1
                    dm, do = front_dist(npos, nep, side), front_dist(npos, nep, other(side))
                    if dm == do: race['tie'] += 1
    print(f'{fam}_{n}: far moves (source file not central) compared with ins_6: {dict(corr)}; races (both sides passed after the move): {dict(race)}', flush=True)
    s = Counter()
    for (src, k), v in bysrc.items(): s[(src, k)] += v
    ks = {}
    for (src, k), v in sorted(s.items()):
        ks.setdefault(src, {})[k] = v
    print(f'{fam}_{n}: far-pawn moves by source file and class: {ks}   ({time.time()-t0:.0f}s)', flush=True)

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
