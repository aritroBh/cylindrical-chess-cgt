#!/usr/bin/env python3
"""Task 1b: outcomes of X+*h (h=0..3) from the existing Part B code (research/mobius/mob_pawns.py, cgt values)
for every position with <= MAXP pawns on WIDTH files (default directions, ranks 1..8), written as
'<tokens>\t<signature>' lines; compared afterwards with mob1/mob2.
usage (repo root): PYTHONPATH=. .venv/bin/python research/mobius_rings/partb_compare.py WIDTH MAXP OUT [START STEP]"""
import sys, itertools
from cylcgt import cgt
from research.mobius import mob_pawns as mp

W, MAXP, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
START, STEP = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
board = mp.Board(W, "mob")
sq = [(f, r) for f in range(W) for r in range(1, 9)]

def tokens(wsq, bsq):
    t = []
    for f in range(W):
        w = ''.join(str(r) for r in range(1, 9) if (f, r) in wsq)
        b = ''.join(str(r) for r in range(1, 9) if (f, r) in bsq)
        t.append(('W' + w if w else '') + ('B' + b if b else '') or '-')
    return ' '.join(t)

def sig(pos):
    try:
        g = mp.value(board, pos)
    except mp.RaceError:
        return "RACE"
    return ''.join(cgt.outcome(cgt.add(g, cgt.nimber(h))) for h in range(4))

n = 0
with open(OUT, "w") as out:
    for k in range(1, MAXP + 1):
        for comb in itertools.combinations(sq, k):
            for cols in itertools.product((0, 1), repeat=k):
                n += 1
                if (n - 1) % STEP != START: continue
                wsq = {s for s, c in zip(comb, cols) if c == 0}; bsq = {s for s, c in zip(comb, cols) if c == 1}
                pos = mp.Pos(frozenset((f, r, 1) for f, r in wsq), frozenset((f, r, -1) for f, r in bsq))
                out.write(tokens(wsq, bsq) + "\t" + sig(pos) + "\n")
print("positions", n)
