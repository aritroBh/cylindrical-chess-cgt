"""Independent literal finite game trees, with separate games added after a split."""
from functools import cache
from itertools import combinations
from sys import argv
import sys
sys.setrecursionlimit(10000)

trees = []
seen = {}


def node(left, right):
    key = tuple(sorted(set(left))), tuple(sorted(set(right)))
    if key not in seen:
        seen[key] = len(trees)
        trees.append(key)
    return seen[key]


zero = node([], [])
star = node([zero], [zero])
white_win = black_win = zero
for _ in range(256):
    white_win, black_win = node([white_win], []), node([], [black_win])


@cache
def le(a, b):
    return (a == b or
            (not any(le(b, x) for x in trees[a][0]) and
             not any(le(x, a) for x in trees[b][1])))


@cache
def plus(a, b):
    if a == zero or b == zero:
        return b if a == zero else a
    return node(*([plus(x, b) for x in trees[a][side]] +
                  [plus(a, x) for x in trees[b][side]] for side in (0, 1)))


def passed(own, foe, step, flag):
    # None = no passer; 99 = passer, but all passed pawns have an own-file blocker.
    best = None
    for q in own:
        if q == flag:
            continue
        f, r = divmod(q, 8)
        ahead = lambda x: step * (x % 8 - r) > 0
        if any(abs(x // 8 - f) <= 1 and ahead(x) for x in foe):
            continue
        distance = (7-r if step == 1 else r) - (r == (1 if step == 1 else 6))
        if any(x // 8 == f and ahead(x) for x in own):
            distance = 99
        best = distance if best is None else min(best, distance)
    return best


def terminal(w, b, flag, side):
    a, c = passed(w, b, 1, flag), passed(b, w, -1, flag)
    if a is None and c is None:
        return None
    if c is None or (a is not None and (a < c or (a == c and side == 1))):
        return white_win
    return black_win


def moves(w, b, flag, side):
    own, foe, step = (b, w, -1) if side else (w, b, 1)
    for p in own:
        dest = p + step
        candidates = []
        if dest not in own and dest not in foe:
            candidates.append((dest, -1, -1))
            landing = dest + step
            if p % 8 == (6 if side else 1) and landing not in own and landing not in foe:
                capturable = any(abs(q - landing) == 8 for q in foe)
                candidates.append((landing, -1, landing if capturable else -1))
        for sideways in (-8, 8):
            target = dest + sideways
            if target in foe:
                candidates.append((target, target, -1))
            elif flag >= 0 and p + sideways == flag and flag in foe:
                candidates.append((target, flag, -1))
        for target, victim, newflag in candidates:
            us = tuple(sorted((set(own) - {p}) | {target}))
            them = tuple(q for q in foe if q != victim)
            yield (them, us, newflag) if side else (us, them, newflag)


@cache
def game(w, b, flag):
    files = sorted({q // 8 for q in w+b})
    for i, j in zip(files, files[1:]):
        if j > i + 1:
            games = []
            for lo, hi in ((0, j), (j, files[-1]+1)):
                us, them = (tuple(q-8*lo for q in s if lo <= q//8 < hi) for s in (w,b))
                games.append(game(us, them, flag-8*lo if lo <= flag//8 < hi else -1))
            return plus(*games)

    def options(side):
        for child in moves(w, b, flag, side):
            end = terminal(*child, side)
            yield game(*child) if end is None else end
    return node(options(0), options(1))


@cache
def canonical(g):
    if g <= black_win:  # The startup trees are canonical integers and star.
        return g
    sides = []
    for side in (0, 1):
        pending = [canonical(x) for x in trees[g][side]]
        visited = set()
        keep = set()
        while pending:
            x = pending.pop()
            if x in visited:
                continue
            visited.add(x)
            for reply in trees[x][1-side]:
                reversible = le(reply, g) if side == 0 else le(g, reply)
                if reversible:
                    pending.extend(trees[reply][side])
                    break
            else:
                keep.add(x)
        sides.append([x for x in keep if not any(
            x != y and (le(x, y) if side == 0 else le(y, x)) for y in keep)])
    return node(*sides)


@cache
def nimber(g):
    left, right = trees[g]
    if left != right:
        return -1
    values = sorted(nimber(x) for x in left)
    return len(left) if values == list(range(len(left))) else -1


def census(n, limit):
    from collections import Counter
    counts = Counter()
    details = Counter()
    for k in range(2, limit+1):
        if len(argv) > 5 and k != int(argv[5]):
            continue
        for squares in combinations(range(n*6), k):
            if squares[0]//6 != 0 or squares[-1]//6 != n-1:
                continue
            sq = tuple(8*(s//6) + s%6 + 1 for s in squares)
            full = len({s//8 for s in sq}) == n
            if len(argv) > 4 and squares[0] % 6 != int(argv[4]):
                continue
            for nw in range(1,k):
                for w in combinations(sq, nw):
                    b = tuple(sorted(set(sq)-set(w)))
                    mirror = tuple(tuple(sorted(8*(n-1-x//8)+x%8 for x in army)) for army in (w,b))
                    if (w,b) > mirror or terminal(w,b,-1,0) is not None:
                        continue
                    g = game(w,b,-1)
                    row = (1, 1+int((w,b) != mirror), int(le(g,zero) and le(zero,g)),
                           int(le(g,star) and le(star,g)))
                    if len(argv) > 3:
                        nim = nimber(canonical(g))
                        assert (nim == 0, nim == 1) == row[2:4]
                        counts[k, 4] += int(nim >= 2)
                    for i, v in enumerate(row):
                        counts[k,i] += v
                        details[k,full,i] += v
        print(n,k,*(counts[k,i] for i in range(5 if len(argv) > 3 else 4)), 'gapped',
              *(details[k,False,i] for i in range(4)), flush=True)


if __name__ == '__main__':
    assert le(plus(star,star),zero) and le(zero,plus(star,star))
    assert game((1,), (2,), -1) == zero
    heap2 = node([zero,star],[zero,star])
    disguised = node([zero,star,black_win],[zero,star,white_win])
    assert canonical(disguised) == heap2 and nimber(heap2) == 2
    if argv[1] == '--self-check':
        # Paper position A is a positive control just beyond the six-pawn census.
        w = (3,10,25,26)  # a4 b3 d2 d3
        b = (6,14,20)     # a7 b7 c5
        assert nimber(canonical(game(w,b,-1))) == 2
        print('seven-pawn positive control A: *2')
    else:
        census(int(argv[1]), int(argv[2]))
