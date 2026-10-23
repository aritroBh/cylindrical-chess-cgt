"""run_a.py -- (a) outcomes of G + *h, h = 0..7, of the full game (no poison pruning) for P_n, even n in a given range.

Three solvers per n:
  T  = T50 verifier engine (t50/eng.py, unchanged), eng.outcomes
  Mk = myeng.Full('keep')    (e.p. flag survives a heap move: cylcgt sum semantics)
  Me = myeng.Full('expire')  (e.p. flag cleared by a heap move: textbook chess)
and, for the small n listed in EXH, an exhaustive solver that evaluates EVERY child of EVERY reachable state (no early
exit at all) -- to rule out an error caused by the short-circuit search.
Signature letters per h: N = first player wins, P = second player wins (L / R = only Left / Right wins).  P_n = *2 iff the
signature is NNPNNNNN.
Usage:  python -B run_a.py LO HI   (even n from LO to HI)
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 't50'))
import myeng as M
import eng as T

HS = tuple(range(8))
EXH = (8, 10)


def exhaustive_sig(pos0, hs):
    memo = {}

    def wins(pos, ep, h, mover):
        key = (pos, ep, h, mover)
        v = memo.get(key)
        if v is not None:
            return v
        e = 1 - mover
        results = []                                   # evaluate every option, no early exit
        for np_, ne in M.gen_moves(pos, ep, mover):
            v2 = M.verdict(np_, ne, mover)
            if v2 == mover:
                results.append(True)
            elif v2 == e:
                results.append(False)
            else:
                results.append(not wins(np_, ne, h, e))
        for h2 in range(h):
            results.append(not wins(pos, ep, h2, e))
        r = any(results)
        memo[key] = r
        return r

    sig = ''
    for h in hs:
        a, b = wins(pos0, None, h, 0), wins(pos0, None, h, 1)
        sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return sig, len(memo)


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    allok = True
    for n in range(lo, hi + 1, 2):
        if n < 8:
            continue
        pm = M.P_start(n)
        pt = T.parse(M.P_tokens(n))
        assert pm == pt, 'parsers disagree'
        t0 = time.time()
        sT, nT = T.outcomes(pt, HS)
        t1 = time.time()
        fk = M.Full('keep'); sK = fk.signature(pm, HS)
        t2 = time.time()
        fe = M.Full('expire'); sE = fe.signature(pm, HS)
        t3 = time.time()
        line = 'n=%2d pawns=%2d T50=%s (%d nodes, %.1fs) mine-keep=%s (%d, %.1fs) mine-expire=%s (%d, %.1fs)' % (
            n, T.npawns(pt), sT, nT, t1 - t0, sK, fk.nodes, t2 - t1, sE, fe.nodes, t3 - t2)
        if n in EXH:
            sX, nX = exhaustive_sig(pm, HS)
            line += ' exhaustive=%s (%d states)' % (sX, nX)
            agree_x = (sX == sT)
        else:
            agree_x = True
        ok = (sT == sK == sE == 'NNPNNNNN') and agree_x
        allok &= ok
        print(line + ('' if ok else '   <<<<<< DIFFERENCE / NOT NNPNNNNN'), flush=True)
    print('ALL OK' if allok else 'SOME DIFFERENCE')


main()
