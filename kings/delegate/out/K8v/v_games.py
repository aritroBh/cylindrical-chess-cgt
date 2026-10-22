"""Auditor B: independent test-game definitions (written from the K4 brief text, not from the
builder's testgames.py) and an independent naive-Kleene solver for pure sums.

A game is a dict  name -> (left option names, right option names); `root` is its start.
Sum = product graph.  Outcome of a graph under normal play + infinite = draw is the least fixed
point:  state (node, mover) is a mover-WIN if some option leads to a mover-LOSS state, a
mover-LOSS if all options lead to mover-WIN states (including the case of no option).
"""
import itertools


def G(root, **kw):
    return (root, kw)

def integer(n):
    if n == 0:
        return G('0', **{'0': ([], [])})
    d = {'0': ([], [])}
    for i in range(1, abs(n) + 1):
        prev = str(i - 1)
        d[str(i)] = ([prev], []) if n > 0 else ([], [prev])
    return G(str(abs(n)), **d)

GAMES = {
    '0':    integer(0),
    '1':    integer(1),
    '2':    integer(2),
    '-1':   integer(-1),
    '-2':   integer(-2),
    '*':    G('s', s=(['z'], ['z']), z=([], [])),
    'up':   G('u', u=(['z'], ['s']), s=(['z'], ['z']), z=([], [])),
    'down': G('d', d=(['s'], ['z']), s=(['z'], ['z']), z=([], [])),
    '1/2':  G('h', h=(['z'], ['o']), o=(['z'], []), z=([], [])),
    '-1/2': G('h', h=(['m'], ['z']), m=([], ['z']), z=([], [])),
    '+-1':  G('p', p=(['o'], ['m']), o=(['z'], []), m=([], ['z']), z=([], [])),
    'on':   G('a', a=(['a'], [])),
    'off':  G('a', a=([], ['a'])),
    'dud':  G('a', a=(['a'], ['a'])),
    'over': G('v', v=(['z'], ['v']), z=([], [])),
    'under': G('v', v=(['v'], ['z']), z=([], [])),
}
TESTS = ['0', '1', '2', '-1', '-2', '*', 'up', 'down', '1/2', '-1/2', '+-1', 'on', 'off', 'dud', 'over', 'under']


def neg(g):
    root, d = g
    return (root, {k: (list(r), list(l)) for k, (l, r) in d.items()})


def plus(*gs):
    """product graph; node names are tuples"""
    roots = tuple(g[0] for g in gs)
    d = {}
    for combo in itertools.product(*[list(g[1]) for g in gs]):
        L, R = [], []
        for i, g in enumerate(gs):
            l, r = g[1][combo[i]]
            for x in l:
                L.append(combo[:i] + (x,) + combo[i + 1:])
            for x in r:
                R.append(combo[:i] + (x,) + combo[i + 1:])
        d[combo] = (L, R)
    return (roots, d)


def brace(left, right):
    """{left | right}: left/right are games or None"""
    d = {'ROOT': ([], [])}
    cnt = 0
    for side, g in ((0, left), (1, right)):
        if g is None:
            continue
        cnt += 1
        tag = 'c%d' % cnt
        for k, (l, r) in g[1].items():
            d[(tag, k)] = ([(tag, x) for x in l], [(tag, x) for x in r])
        d['ROOT'][side].append((tag, g[0]))
    return ('ROOT', d)


def outcome(g):
    """(result with White to move, result with Black to move) in 'W','D','L' from White's view"""
    root, d = g
    # state (node, mover)  mover 0 = Left/White
    win = {}
    changed = True
    states = [(k, s) for k in d for s in (0, 1)]
    while changed:
        changed = False
        for (k, s) in states:
            if (k, s) in win:
                continue
            opts = d[k][s]
            nxt = [(o, 1 - s) for o in opts]
            if any(win.get(x) is False for x in nxt):
                win[(k, s)] = True; changed = True
            elif all(win.get(x) is True for x in nxt):
                win[(k, s)] = False; changed = True
    out = []
    for s in (0, 1):
        w = win.get((root, s))
        out.append('D' if w is None else ('W' if (w == (s == 0)) else 'L'))
    return tuple(out)


def candidates():
    c = [(t, GAMES[t]) for t in TESTS]
    star = GAMES['*']
    for a in ('on', 'off', '1', '-1', 'up'):
        c.append((a + '+*', plus(GAMES[a], star)))
    pr = [('on', '0'), ('0', 'off'), ('on', 'off'), ('0', 'on'), ('off', '0')]
    for l, r in pr:
        c.append(('{%s|%s}' % (l, r), brace(GAMES[l], GAMES[r])))
    return c


def signature(V):
    s = ''
    for t in TESTS:
        a, b = outcome(plus(V, GAMES[t]))
        s += a + b
    return s


if __name__ == '__main__':
    facts = [
        ('1+(-1)', ['1', '-1'], ('L', 'W')), ('*+*', ['*', '*'], ('L', 'W')),
        ('up+down', ['up', 'down'], ('L', 'W')), ('1/2+1/2+(-1)', ['1/2', '1/2', '-1'], ('L', 'W')),
        ('on+(-2)', ['on', '-2'], ('W', 'W')), ('on+off', ['on', 'off'], ('D', 'D')),
        ('dud+1', ['dud', '1'], ('D', 'D')), ('over+(-1/2)', ['over', '-1/2'], ('L', 'L')),
        ('over', ['over'], ('W', 'W')), ('up+*', ['up', '*'], ('W', 'L')),
        # extra sanity facts (standard CGT), not in the brief
        ('up', ['up'], ('W', 'W')), ('*', ['*'], ('W', 'W')) ,
        ('+-1 + +-1', ['+-1', '+-1'], ('L', 'W')), ('1/2+1/2+(-1)+(1/2)', ['1/2', '1/2', '-1', '1/2'], ('W', 'W')),
        ('2+(-1)', ['2', '-1'], ('W', 'W')), ('under', ['under'], ('L', 'L')),
        ('on+on', ['on', 'on'], ('W', 'W')), ('off+(+2)', ['off', '2'], ('L', 'L')),
        ('up+up+*', ['up', 'up', '*'], ('W', 'W')),
    ]
    bad = 0
    for name, parts, exp in facts:
        got = outcome(plus(*[GAMES[p] for p in parts]) if len(parts) > 1 else GAMES[parts[0]])
        ok = got == exp
        bad += not ok
        print('%-4s %-22s expected %s got %s' % ('PASS' if ok else 'FAIL', name, exp, got))
    # over+under, and on + off + *
    print('over+under ->', outcome(plus(GAMES['over'], GAMES['under'])))
    print('FAILS:', bad)
