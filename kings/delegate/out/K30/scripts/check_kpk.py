#!/usr/bin/env python3
"""check_kpk.py -- K30 step 2a: the White drawing rule of PROOF.md (part B1) in king + Black pawn vs king.
usage: check_kpk.py cyl:8x8|flat:8x8
 (1) S is closed under every Black move and the rule (all of S, brute force);
 (2) the three start positions (after the sortie and ...Kxd7, White to move) lead into S;
 (3) the states actually reached from the starts by play against every Black move are counted."""
import sys, collections
sys.path.insert(0, '.')
from k30lib import *
spec = sys.argv[1]
B = Board(spec)
S = all_S(B)
bypawn = collections.Counter(B.r(p[4][0]) + 1 for p in S)
print(spec, '|S| =', len(S), 'by pawn rank', dict(sorted(bypawn.items(), reverse=True)))
pairs, wstates, stats = check_S_closure(B, S)
print('closure of S: %d (position, Black move) pairs; %d distinct White-to-move positions; replies: %s' % (pairs, len(wstates), dict(stats)))
# (2),(3): reachable from the three starts
starts = [parse(B, t) for t in ('Ke5 kd7 pe7 w -', 'Kd5 kd7 pe7 w -', 'Kf5 kd7 pe7 w -')]
seenB, seenW = set(), set(starts)
dq = collections.deque(starts)
while dq:
    t = dq.popleft()
    rep = white_rule(B, t)
    if rep is None or rep[4] == ():
        continue
    assert inS(B, rep)
    if rep in seenB:
        continue
    seenB.add(rep)
    for lab, k, nt in gen(B, rep):
        assert k == 'n'
        if nt not in seenW:
            seenW.add(nt); dq.append(nt)
print('reached from the starts: %d Black-to-move positions (all in S), %d White-to-move positions' % (len(seenB), len(seenW)))
assert seenB <= set(S)
for s in starts:
    print('  start', fmt(B, s), '-> rule move ->', fmt(B, white_rule(B, s)))
print('OK')
