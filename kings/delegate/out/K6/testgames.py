"""Test games for K4 (rewritten; the earlier file in this directory had a wrong -1/2).

A game is an explicit graph with Left = White and Right = Black.  Node i has Left options
lopts[i] and Right options ropts[i] (lists of node indices); `start` is the node that stands for
the game.  There are no terminals: a player with no option loses (normal play), and infinite play
is a draw (decided by product.py).

Brief K4 says "17 test games" but lists 16 (0, 1, 2, -1, -2, *, up, down, 1/2, -1/2, +-1, on,
off, dud, over, under).  TESTS below holds exactly the 16 listed; the signature length follows
len(TESTS), so a 17th game would be one more line.
"""

import itertools


class Game:
    __slots__ = ('name', 'n', 'lopts', 'ropts', 'lpred', 'rpred', 'start')

    def __init__(self, name, lopts, ropts, start=0):
        self.name = name
        self.n = len(lopts)
        self.lopts = lopts
        self.ropts = ropts
        self.start = start
        self.lpred = [[] for _ in range(self.n)]
        self.rpred = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j in lopts[i]:
                self.lpred[j].append(i)
            for j in ropts[i]:
                self.rpred[j].append(i)

    def opts(self, side):
        """side 0 = Left/White, 1 = Right/Black"""
        return self.lopts if side == 0 else self.ropts

    def preds(self, side):
        return self.lpred if side == 0 else self.rpred


def from_spec(name, spec, start):
    """spec: {node name: ([left option names], [right option names])}; start: node name."""
    names = list(spec)
    idx = {nm: i for i, nm in enumerate(names)}
    lo = [[idx[x] for x in spec[nm][0]] for nm in names]
    ro = [[idx[x] for x in spec[nm][1]] for nm in names]
    return Game(name, lo, ro, idx[start])


def neg(g, name=None):
    """-g: Left and Right swap roles at every node."""
    return Game(name or '-(%s)' % g.name, [list(x) for x in g.ropts],
                [list(x) for x in g.lopts], g.start)


def plus(*games, name=None):
    """Disjunctive sum (product graph); node (i1, ..., ik) has index in row-major order."""
    acc = games[0]
    for h in games[1:]:
        lo, ro = [], []
        for i, j in itertools.product(range(acc.n), range(h.n)):
            lo.append([a * h.n + j for a in acc.lopts[i]] + [i * h.n + b for b in h.lopts[j]])
            ro.append([a * h.n + j for a in acc.ropts[i]] + [i * h.n + b for b in h.ropts[j]])
        acc = Game('', lo, ro, acc.start * h.n + h.start)
    acc.name = name or '+'.join(g.name for g in games)
    return acc


def _int(n):
    """n >= 1: {n-1 | }, chain down to 0.  n <= -1: { | n+1}."""
    spec = {'0': ([], [])}
    k = abs(n)
    for i in range(1, k + 1):
        spec[str(i)] = (['0' if i == 1 else str(i - 1)], []) if n > 0 else \
                       ([], ['0' if i == 1 else str(i - 1)])
    return spec, str(k)


def integer(n):
    """The integer n as a game (n = 0 is the game 0); used by tempo_scan.py."""
    if n == 0:
        return GAMES['0']
    spec, st = _int(n)
    return from_spec(str(n), spec, st)


def _build():
    S = {}
    S['0'] = ({'0': ([], [])}, '0')
    S['1'] = _int(1)
    S['2'] = _int(2)
    S['-1'] = _int(-1)
    S['-2'] = _int(-2)
    S['*'] = ({'*': (['0'], ['0']), '0': ([], [])}, '*')
    S['up'] = ({'up': (['0'], ['*']), '*': (['0'], ['0']), '0': ([], [])}, 'up')
    S['down'] = ({'down': (['*'], ['0']), '*': (['0'], ['0']), '0': ([], [])}, 'down')
    S['1/2'] = ({'h': (['0'], ['1']), '1': (['0'], []), '0': ([], [])}, 'h')
    S['-1/2'] = ({'h': (['-1'], ['0']), '-1': ([], ['0']), '0': ([], [])}, 'h')
    S['+-1'] = ({'pm': (['1'], ['-1']), '1': (['0'], []), '-1': ([], ['0']),
                 '0': ([], [])}, 'pm')
    S['on'] = ({'on': (['on'], [])}, 'on')
    S['off'] = ({'off': ([], ['off'])}, 'off')
    S['dud'] = ({'dud': (['dud'], ['dud'])}, 'dud')
    S['over'] = ({'over': (['0'], ['over']), '0': ([], [])}, 'over')
    S['under'] = ({'under': (['under'], ['0']), '0': ([], [])}, 'under')
    return {k: from_spec(k, spec, st) for k, (spec, st) in S.items()}


GAMES = _build()
TESTS = ['0', '1', '2', '-1', '-2', '*', 'up', 'down', '1/2', '-1/2', '+-1',
         'on', 'off', 'dud', 'over', 'under']
PRETTY = {'up': '↑', 'down': '↓', '+-1': '±1', '-1/2': '−1/2'}


def pretty(name):
    for k, v in PRETTY.items():
        name = name.replace(k, v)
    return name.replace('-', '−') if name not in PRETTY.values() else name


def _pair(nm, left, right):
    """{left | right} where left/right are game names ('' = none); copies the option graphs."""
    # build a fresh graph: root node, then disjoint copies of the option games
    lo, ro, off = [[]], [[]], 1
    starts = {}
    for side, gname in ((0, left), (1, right)):
        if not gname:
            continue
        g = GAMES[gname]
        base = off
        off += g.n
        for i in range(g.n):
            lo.append([base + a for a in g.lopts[i]])
            ro.append([base + a for a in g.ropts[i]])
        starts[side] = base + g.start
    if 0 in starts:
        lo[0].append(starts[0])
    if 1 in starts:
        ro[0].append(starts[1])
    return Game(nm, lo, ro, 0)


def candidates():
    """The 26 candidate values V as (name, Game): 16 tests, five sums with *, five {a|b}."""
    c = [(t, GAMES[t]) for t in TESTS]
    for a in ('on', 'off', '1', '-1', 'up'):
        c.append((a + '+*', plus(GAMES[a], GAMES['*'], name=a + '+*')))
    for l, r in (('on', '0'), ('0', 'off'), ('on', 'off'), ('0', 'on'), ('off', '0')):
        c.append(('{%s|%s}' % (l, r), _pair('{%s|%s}' % (l, r), l, r)))
    return c


if __name__ == '__main__':
    for nm, g in candidates():
        print(nm, g.n, g.start)
