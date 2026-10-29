#!/usr/bin/env python3
"""K15 fin2: (1) which pawns of Z_B does cylcgt.pawns.passed call passed (flat 7x6)?  (2) is the root-passer test of grp.c
(the 'strict' variant) equal to cylcgt.passed on random pawn sets without e.p. right?  grp.c's test is re-implemented here
in the same words (a pawn is passed iff no enemy pawn on its file or the two neighbouring files is ahead of it)."""
import sys, random
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import pawns as P
def parse(s):
    w = set(); b = set()
    for t in s.split():
        if t[0] in 'Pp' and len(t) >= 3:
            sq = (ord(t[1]) - 97, int(t[2:]))
            (w if t[0] == 'P' else b).add(sq)
    return frozenset(w), frozenset(b)
fl = P.Board(7, 6, False, True)
w, b = parse('Pa3 Pb4 pb3 pc4')
pos = P.Pos(w, b, None)
print('Z_B pawns (flat 7x6): cylcgt passed(W) =', P.passed(fl, pos, 'W'), ' passed(B) =', P.passed(fl, pos, 'B'))
for side, pawns in (('W', w), ('B', b)):
    for pw in sorted(pawns):
        one = P.Pos(frozenset([pw]) if side == 'W' else w, b if side == 'W' else frozenset([pw]), None)
        # a single pawn is "passed" in the full position iff no enemy pawn of the full position is ahead on its files
        mine = pawns; ok = False
        files = {pw[0]} | {g for g in (fl.nb(pw[0], -1), fl.nb(pw[0], 1)) if g is not None}
        theirs = b if side == 'W' else w
        blocked = any(g in files and ((s > pw[1]) if side == 'W' else (s < pw[1])) for g, s in theirs)
        print('  %s pawn %s%d: passed=%s' % (side, 'abcdefg'[pw[0]], pw[1], not blocked))
def mine_passed(Wd, wp, bp, side, flat):
    me, th = (wp, bp) if side == 'W' else (bp, wp)
    for f, r in me:
        files = {f}
        for d in (-1, 1):
            g = f + d
            if flat:
                if 0 <= g < Wd: files.add(g)
            else: files.add(g % Wd)
        if not any(g in files and ((s > r) if side == 'W' else (s < r)) for g, s in th): return True
    return False
rnd = random.Random(5); bad = 0; n = 0
for (Wd, H, flat) in ((8, 6, False), (7, 6, False), (7, 6, True), (8, 8, False)):
    bd = P.Board(Wd, H, not flat, True)
    for _ in range(20000):
        F = rnd.randint(1, 5); k = rnd.randint(1, 6)
        sqs = [(rnd.randrange(F), rnd.randint(2, H - 1)) for _ in range(k)]
        sqs = list(dict.fromkeys(sqs)); rnd.shuffle(sqs)
        cut = rnd.randint(0, len(sqs)); wp = frozenset(sqs[:cut]); bp = frozenset(sqs[cut:])
        pos = P.Pos(wp, bp, None)
        for side in 'WB':
            n += 1
            if P.passed(bd, pos, side) != mine_passed(Wd, wp, bp, side, flat): bad += 1
print('random pawn sets compared:', n, 'differences:', bad)
