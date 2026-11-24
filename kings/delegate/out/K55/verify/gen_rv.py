"""K55 referee: test games as graphs, sums, negatives; r(over + T) by a small sweep. Own code.
A game is (L, R) lists of option lists; node 0 is the start. Writes rv55 test files (tab separated).
usage: gen_rv.py <set name> <out file>"""
import sys

def num(n):            # integer n (n moves for Left if n > 0, for Right if n < 0)
    k = abs(n); L = [[] for _ in range(k + 1)]; R = [[] for _ in range(k + 1)]
    for i in range(k):
        (L if n > 0 else R)[i].append(i + 1)
    return (L, R)
def mk(spec):          # spec: list of (Lopts, Ropts) per node
    return ([list(a) for a, b in spec], [list(b) for a, b in spec])
ZERO = num(0)
STAR = mk([([1], [1]), ([], [])])
UP = mk([([1], [2]), ([], []), ([1], [1])])            # {0 | *}
DOWN = mk([([2], [1]), ([], []), ([1], [1])])          # {* | 0}
OVER = mk([([1], [0]), ([], [])])                       # {0 | over}
UNDER = mk([([0], [1]), ([], [])])                      # {under | 0}
ON = mk([([0], [])]); OFF = mk([([], [0])]); DUD = mk([([0], [0])])
PM1 = mk([([1], [2]), ([3], []), ([], [3]), ([], [])])  # {1 | -1}
def neg(g): return (g[1], g[0])
def add(*gs):
    """sum of graphs, reachable part only"""
    gs = list(gs); start = tuple(0 for _ in gs); idx = {start: 0}; order = [start]; L = []; R = []
    i = 0
    while i < len(order):
        st = order[i]; i += 1; l = []; r = []
        for k, g in enumerate(gs):
            for side, out in ((0, l), (1, r)):
                for o in g[side][st[k]]:
                    nx = st[:k] + (o,) + st[k + 1:]
                    if nx not in idx: idx[nx] = len(order); order.append(nx)
                    out.append(idx[nx])
        L.append(l); R.append(r)
    return (L, R)
def tiny(n):           # {0 || 0 | -n}: 0 tiny, 1 = {0 | -n}, 2 = 0, 3.. = -n chain
    # chain: node 3 is -n, node 3+i moves (Right) to 3+i+1, node 3+n is 0
    L = [[2], [2], []] + [[] for _ in range(n + 1)]
    R = [[1], [3], []] + [[3 + i + 1] for i in range(n)] + [[]]
    return (L, R)
def miny(n): return neg(tiny(n))
def solve(g):
    """values of every (node, mover): 1 White (Left) wins, 2 Black wins, 0 draw; no move loses"""
    n = len(g[0]); v = {}
    ch = True
    while ch:
        ch = False
        for x in range(n):
            for s in (0, 1):
                if (x, s) in v: continue
                me = 1 if s == 0 else 2; opp = 3 - me; opts = g[s][x]
                res = [v.get((y, 1 - s), 0) for y in opts]
                if me in res: v[(x, s)] = me; ch = True
                elif all(r == opp for r in res): v[(x, s)] = opp; ch = True
    return lambda x, s: v.get((x, s), 0)
def res(g):            # (White first, Black first) from White's view
    f = solve(g); c = {1: 'W', 2: 'L', 0: 'D'}; return c[f(0, 0)] + c[f(0, 1)]
SETS = {}
SETS['main'] = [('0', ZERO), ('*', STAR), ('up', UP), ('down', DOWN), ('down+*', add(DOWN, STAR)), ('up+*', add(UP, STAR)),
    ('under', UNDER), ('under+*', add(UNDER, STAR)), ('over', OVER), ('over+*', add(OVER, STAR)), ('down+down', add(DOWN, DOWN)),
    ('under+up', add(UNDER, UP)), ('under+down', add(UNDER, DOWN)), ('under+under', add(UNDER, UNDER)), ('1+pm1', add(num(1), PM1)),
    ('pm1', PM1), ('1', num(1)), ('-1', num(-1)), ('on', ON), ('off', OFF), ('dud', DUD), ('over+down', add(OVER, DOWN)),
    ('miny2', miny(2)), ('tiny2', tiny(2)), ('dblup*', add(UP, UP, STAR)), ('dbldown*', add(DOWN, DOWN, STAR))]
SETS['tempo'] = [('-%d' % n, num(-n)) for n in range(1, 7)] + [('off', OFF), ('*', STAR), ('0', ZERO)]
if __name__ == '__main__':
    name, out = sys.argv[1], sys.argv[2]
    with open(out, 'w') as f:
        for nm, g in SETS[name]:
            cells = [nm, str(len(g[0]))]
            for x in range(len(g[0])):
                cells.append(','.join(map(str, g[0][x])) or '-'); cells.append(','.join(map(str, g[1][x])) or '-')
            f.write('\t'.join(cells) + '\n')
    with open(out + '.over', 'w') as f:
        for nm, g in SETS[name]:
            f.write('%s | over+T %s | T %s\n' % (nm, res(add(OVER, g)), res(g)))
