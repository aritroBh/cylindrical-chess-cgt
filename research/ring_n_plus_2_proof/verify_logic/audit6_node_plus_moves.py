"""Lemma 3 on positions of the FULL game near R_n: every node p of R_n, followed by 1 (or 2) arbitrary moves of either side
(heap moves allow any move order).  Positions with a passed pawn or an e.p. flag are outside the lemma's hypotheses and skipped.
For every admissible cut c (arc c-4..c+5 exactly the wall pattern) compare classify(q) with classify(ins_c q)."""
import sys, time, collections
import engine
from engine import *

def pat(j):
    return parse_file('W2') if j % 2 == 0 else parse_file('B4')

def cls(pos, ep=None):
    out = {}
    for side in 'WB':
        cl = classify(pos, ep, side)
        out[side] = (any(c == 'T' for c, *_ in cl), frozenset((npos, nep) for c, npos, nep, *_ in cl if c == 'K'))
    return out

def test_pos(pos, n, stats, tested_set):
    if (pos) in tested_set: return
    tested_set.add(pos)
    cuts = [c for c in range(4, n - 5) if all(pos[j] == pat(j) for j in range(c - 4, c + 6))]
    if not cuts:
        stats['nocut'] += 1; return
    a = cls(pos)
    for c in cuts:
        ph = ins(pos, c)
        if passed_list(ph, None, 'W') or passed_list(ph, None, 'B'):
            stats['bad'] += 1; stats['ex'] = stats.get('ex') or ('phat passed', fmt(pos), c); continue
        b = cls(ph)
        stats['cutchecks'] += 1
        stats['cut%d' % c] += 1
        if not all(a[s][0] == b[s][0] and {ins_nd(k, c) for k in a[s][1]} == set(b[s][1]) for s in 'WB'):
            stats['bad'] += 1; stats['ex'] = stats.get('ex') or ('mismatch', fmt(pos), c)
    stats['tested'] += 1
    if stats['tested'] % 1500 == 0: engine._cache.clear()

def main(n, depth, tmax):
    start = parse(P_toks(n))
    order, edges = build(start)
    stats = collections.Counter(); tested_set = set()
    t0 = time.time()
    def succ(pos):
        for side in 'WB':
            for npos, nep, src, kind in moves(pos, None, side):
                if nep is not None: continue
                if passed_list(npos, nep, 'W') or passed_list(npos, nep, 'B'): continue
                yield npos
    level = {nd[0] for nd in order if nd[1] is None}
    for d in range(1, depth + 1):
        nxt = set()
        for pos in level:
            for q in succ(pos):
                nxt.add(q)
        stats['level%d' % d] = len(nxt)
        for q in nxt:
            test_pos(q, n, stats, tested_set)
            if time.time() - t0 > tmax:
                stats['timeout'] = 1; return stats
        level = nxt
    return stats

if __name__ == '__main__':
    n = int(sys.argv[1]); depth = int(sys.argv[2]); tmax = float(sys.argv[3])
    t0 = time.time()
    st = main(n, depth, tmax)
    print('n', n, 'depth', depth, dict(st), '%.0fs' % (time.time() - t0), flush=True)
