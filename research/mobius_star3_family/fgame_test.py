import random, sys
from fgame import FBoard, Board
from mgame import code
rnd = random.Random(int(sys.argv[1])); bad = 0; N = int(sys.argv[2])
for i in range(N):
    n = rnd.randint(3, 12); cells = []
    for f in range(n):
        row = [0] * 8
        for _ in range(rnd.choice((0, 1, 1, 2, 3))): row[rnd.randint(1, 8) - 1] = code(rnd.randint(0, 1), rnd.choice((1, -1)))
        cells.append(tuple(row))
    pos = (tuple(cells), None)
    for tw in (True, False):
        A, F = Board(n, tw), FBoard(n, tw)
        for s in (0, 1):
            if A.passers(pos, s) != F.passers(pos, s): bad += 1
            for d, ch in A.moves(pos, s):
                for t in (0, 1):
                    if A.passers(ch, t) != F.passers(ch, t) or A.classify(ch, t) != F.classify(ch, t): bad += 1
print('positions', N, 'mismatches', bad)
