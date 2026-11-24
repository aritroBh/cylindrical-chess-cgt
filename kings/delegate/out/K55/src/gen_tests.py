"""K47: the test games T of the brief, as D-games without terminals, for za.cpp.
Base games: the integers -6..6, on, off, dud, *, up, down, +-1, over, under; then every sum of two base games
(unordered pairs, a game with itself included).  Output line: "name | m | 0: L=.. R=.. ; 1: ..." (position 0 = start).
usage: python3 gen_tests.py > tests.txt"""
import itertools


def integer(n):
    # positions k = |n|, ..., 0 ; index i holds value sign*(|n|-i)
    a = abs(n)
    L = [[] for _ in range(a + 1)]
    R = [[] for _ in range(a + 1)]
    for i in range(a):
        (L if n > 0 else R)[i].append(i + 1)
    return (L, R)


BASE = {}
for n in range(-6, 7):
    BASE[str(n)] = integer(n)
BASE['on'] = ([[0]], [[]])
BASE['off'] = ([[]], [[0]])
BASE['dud'] = ([[0]], [[0]])
BASE['*'] = ([[1], []], [[1], []])                    # * = {0|0}
BASE['up'] = ([[2], [2], []], [[1], [2], []])         # up = {0|*}: 0 up, 1 *, 2 zero
BASE['down'] = ([[1], [2], []], [[2], [2], []])       # down = {*|0}
BASE['pm1'] = ([[1], [3], [], []], [[2], [], [3], []])  # +-1 = {1|-1}: 0 pm, 1 one, 2 minus one, 3 zero
BASE['over'] = ([[1], []], [[0], []])                 # over = {0|over}
BASE['under'] = ([[0], []], [[1], []])                # under = {under|0}


def gsum(g, h):
    (L1, R1), (L2, R2) = g, h
    m1, m2 = len(L1), len(L2)
    idx = lambda i, j: i * m2 + j
    L = [[] for _ in range(m1 * m2)]
    R = [[] for _ in range(m1 * m2)]
    for i in range(m1):
        for j in range(m2):
            for x in L1[i]: L[idx(i, j)].append(idx(x, j))
            for y in L2[j]: L[idx(i, j)].append(idx(i, y))
            for x in R1[i]: R[idx(i, j)].append(idx(x, j))
            for y in R2[j]: R[idx(i, j)].append(idx(i, y))
    return (L, R)


def line(name, g):
    L, R = g
    parts = ["%d: L=%s R=%s" % (i, ",".join(map(str, L[i])), ",".join(map(str, R[i]))) for i in range(len(L))]
    return "%s | %d | %s" % (name, len(L), " ; ".join(parts))


names = list(BASE)
for n in names:
    print(line(n, BASE[n]))
for a, b in itertools.combinations_with_replacement(names, 2):
    print(line(a + "+" + b, gsum(BASE[a], BASE[b])))
