"""Unreduced full-game search (no poison pruning) with the fresh engine: signature of G+*h, h=0..3, for P_n (checks Lemma 1 and C2')."""
import sys, time
from engine import *
sys.setrecursionlimit(1000000)

def sig_unreduced(start, hs=(0, 1, 2, 3)):
    memo = {}
    def win(pos, ep, h, mover):
        key = (pos, ep, h, mover)
        v = memo.get(key)
        if v is not None:
            return v
        y = other(mover)
        res = False
        nonterm = []
        for npos, nep, src, kind in moves(pos, ep, mover):
            st = status(npos, nep, mover)
            if st == mover:
                res = True; break
            if st is None:
                nonterm.append((npos, nep))
        if not res:
            for npos, nep in nonterm:
                if not win(npos, nep, h, y):
                    res = True; break
        if not res:
            for h2 in range(h):
                if not win(pos, ep, h2, y):
                    res = True; break
        memo[key] = res
        return res
    s = ''
    for h in hs:
        a = win(start, None, h, 'W'); b = win(start, None, h, 'B')
        s += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return s, len(memo)

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        t0 = time.time()
        start = parse(P_toks(n))
        s, m = sig_unreduced(start)
        order, edges = build(start)
        print('n', n, 'unreduced sig', s, 'states', m, '| reduced sig', solve_sig(order, edges), '%.1fs' % (time.time() - t0), flush=True)
