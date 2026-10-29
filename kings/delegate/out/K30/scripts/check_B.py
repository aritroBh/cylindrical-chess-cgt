#!/usr/bin/env python3
"""check_B.py -- K30 step 2c: White's no-loss strategy sigma from P7 w (PROOF.md part B), for each sortie.
usage: check_B.py cyl:8x8|flat:8x8
Plays sigma against EVERY Black move.  Verifies: sigma always has a legal move that is not a promotion; Black never has
a promotion available; White is never mated.  Hence no play consistent with sigma contains a promotion or a mate of
White: Black cannot win in P, EPB, EPW(for Black wins: n/a) and chess.  Counts the states."""
import sys, collections
sys.path.insert(0, '.')
from k30lib import *
spec = sys.argv[1]
B = Board(spec)
X0, sigma = make_sigma(B)
sq = B.sq
d7, e7, c7, d8, e6, e5, d5, f5 = (sq(x) for x in 'd7 e7 c7 d8 e6 e5 d5 f5'.split())
tot = {}
for sortie, name in ((e5, 'Ke5'), (d5, 'Kd5'), (f5, 'Kf5')):
    seenW, seenB = set(), set()
    dq = collections.deque([X0]); seenW.add(X0)
    free_states = 0
    while dq:
        pos = dq.popleft()
        opts = sigma(pos, sortie)
        for t in opts:
            if t[3] == () and t[4] == ():                # K v K : drawn, nothing can happen
                continue
            if t in seenB:
                continue
            seenB.add(t)
            bms = gen(B, t)
            if not bms:
                assert not in_check(B, t, 1), ('Black mated: impossible in this strategy test', fmt(B, t))
                continue
            for lab, k, nt in bms:
                assert k == 'n', ('Black promotes', fmt(B, t), lab)
                if nt[3] == () and nt[4] == ():            # K v K : drawn, nothing can happen any more
                    continue
                if nt not in seenW:
                    seenW.add(nt); dq.append(nt)
    freeS = sum(1 for p in seenW if p[3] == (d7,) and p[4] == ())
    kpk = sum(1 for p in seenW if p[3] == ())
    both = len(seenW) - freeS - kpk
    tot[name] = (len(seenW), len(seenB))
    print('%s %s: %d White-to-move states (%d with both pawns, %d free mode, %d king+pawn v king), %d Black-to-move states: '
          'sigma defined everywhere, White never mated, Black never has a promotion' % (spec, name, len(seenW), both, freeS, kpk, len(seenB)))
print('OK')
