import sys, random, time, threading
import os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # repository root
import sx2
from cylcgt import pawns as P   # black box only: used here for comparison, never by sx2.py
board = P.Board(8, 8, True, False)
def eng(w, b):
    pos = P.Pos(frozenset(w), frozenset(b))
    from cylcgt import cgt
    return cgt.outcome(P.value(board, pos))
def main():
    random.seed(7)
    # abstract integer sanity: empty sum is P (value 0)
    assert (sx2.win((), 0, 0), sx2.win((), 0, 1)) == (False, False)
    assert (sx2.win((), 3, 0), sx2.win((), 3, 1)) == (True, False)
    assert (sx2.win((), -2, 1), sx2.win((), -2, 0)) == (True, False)
    # {BIG|0}+{0|-BIG}=0 : emulate as integers: Left option +BIG... checked via generic minimax below
    def gwin(L1, R1, L2, R2, player):  # {BIG|0}+{0|-BIG}, then normal integers
        pass
    stat = []; n = ok = bad = 0; t0 = time.time(); bads = []
    tries = 0
    while n < 400 and time.time() - t0 < 600:
        tries += 1
        k = random.choice([4, 5, 6, 7, 8])
        sqs = set()
        while len(sqs) < k:
            sqs.add((random.randrange(8), random.randrange(2, 8)))
        sqs = list(sqs)
        w = [s for s in sqs if random.random() < .5]; b = [s for s in sqs if s not in w]
        # legal: white not on rank 1, black not on rank 8: ranks in 2..7 OK
        if not w or not b: continue
        w, b = tuple(sorted(w)), tuple(sorted(b))
        if sx2.verdict(w, b, 0) is not None: continue
        a = sx2.S_outcome(w, b)
        e = eng(w, b)
        n += 1
        ncomp = len(sx2.split(w, b)); wo = sx2.W_outcome(w, b); stat.append((a, wo, ncomp))
        if a == e: ok += 1
        else: bad += 1; bads.append((w, b, a, e))
    print("random cases", n, "agree", ok, "disagree", bad, "time %.0fs" % (time.time() - t0))
    for x in bads[:10]: print("DISAGREE", x)
    from collections import Counter
    print('S outcomes', Counter(x[0] for x in stat)); print('multi-component', sum(1 for x in stat if x[2]>1)); print('S != W outcome', sum(1 for x in stat if x[0]!=x[1])); print('S != W and agrees with engine', sum(1 for x in stat if x[0]!=x[1]) - bad)
threading.stack_size(512*1024*1024)
th = threading.Thread(target=main); th.start(); th.join()
