"""Unreduced full-game search (NO poison pruning, no reduction) with engine D for R_n, Qo_n, odd n: signature of G+*h, h=0..4,
under both e.p.-across-heap readings, vs the reduced-game signature (Lemma 1).  Also, as a no-short-circuit control for the
smallest n, a solver that evaluates every child of every position.
usage: t_unreduced_odd.py FAM n1 n2 ..."""
import sys, time
from common import *

def sig_unreduced(start, hs, expire):
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
                if not win(pos, None if expire else ep, h2, y):
                    res = True; break
        memo[key] = res
        return res
    s = ''
    for h in hs:
        a = win(start, None, h, 'W'); b = win(start, None, h, 'B')
        s += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return s, len(memo)

def sig_exhaustive(start, hs):
    """evaluates EVERY child of every position (no early exit), keep reading"""
    memo = {}
    def win(pos, ep, h, mover):
        key = (pos, ep, h, mover)
        if key in memo: return memo[key]
        y = other(mover)
        vals = []
        for npos, nep, src, kind in moves(pos, ep, mover):
            st = status(npos, nep, mover)
            if st == mover: vals.append(True)
            elif st == y: vals.append(False)
            else: vals.append(not win(npos, nep, h, y))
        for h2 in range(h):
            vals.append(not win(pos, ep, h2, y))
        memo[key] = any(vals)
        return memo[key]
    s = ''
    for h in hs:
        a = win(start, None, h, 'W'); b = win(start, None, h, 'B')
        s += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return s, len(memo)

if __name__ == '__main__':
    fam = sys.argv[1]
    want = 'NNPNN' if fam == 'R' else 'NNNPN'
    for n in map(int, sys.argv[2:]):
        t0 = time.time()
        start = parse(TOKS[fam](n))
        hs = (0, 1, 2, 3, 4)
        sk, mk = sig_unreduced(start, hs, False)
        engineD._cache.clear()
        se, me = sig_unreduced(start, hs, True)
        order, edges = build(start)
        sr = solve_sig(order, edges, hs)
        ex = ''
        if n <= int(__import__("os").environ.get("EXH_MAX", "13")):
            sx, mx = sig_exhaustive(start, hs)
            ex = f' exhaustive(no early exit)={sx}({mx})'
        print(f'{fam}_{n}: unreduced keep={sk}({mk}) expire={se}({me}) reduced={sr}{ex}  want {want}: {"OK" if sk == se == sr == want else "DIFFERS"}  ({time.time()-t0:.0f}s)', flush=True)
        engineD._cache.clear()
