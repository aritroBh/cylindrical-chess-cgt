"""Verifier A, module 2: explicit loopy game graphs (Left = White = side 0, Right = Black = side 1).

A Game is (lo, ro): lo[v] / ro[v] are the Left / Right option lists of node v; node 0 is the root.
"""

# name -> (left option names, right option names), written from the task statement
DEFS = {
    '0': ([], []),
    '1': (['0'], []), '2': (['1'], []),
    '-1': ([], ['0']), '-2': ([], ['-1']),
    '*': (['0'], ['0']),
    'up': (['0'], ['*']), 'down': (['*'], ['0']),
    '1/2': (['0'], ['1']), '-1/2': (['-1'], ['0']),
    '+-1': (['1'], ['-1']),
    'on': (['on'], []), 'off': ([], ['off']), 'dud': (['dud'], ['dud']),
    'over': (['0'], ['over']), 'under': (['under'], ['0']),
    # candidate-only, not test games
    '{on|0}': (['on'], ['0']), '{0|off}': (['0'], ['off']), '{on|off}': (['on'], ['off']),
    '{0|on}': (['0'], ['on']), '{off|0}': (['off'], ['0']),
}
TESTS = ['0', '1', '2', '-1', '-2', '*', 'up', 'down', '1/2', '-1/2', '+-1',
         'on', 'off', 'dud', 'over', 'under']
SUM_CANDS = [('on+*', 'on', '*'), ('off+*', 'off', '*'), ('1+*', '1', '*'),
             ('-1+*', '-1', '*'), ('up+*', 'up', '*')]
EXTRA_CANDS = ['{on|0}', '{0|off}', '{on|off}', '{0|on}', '{off|0}']


def named(name):
    """Compile a named game into (lo, ro) with the root at node 0 (reachable nodes only)."""
    order, idx = [], {}

    def visit(n):
        if n in idx:
            return
        idx[n] = len(order)
        order.append(n)
        for m in DEFS[n][0] + DEFS[n][1]:
            visit(m)
    visit(name)
    lo = [[idx[m] for m in DEFS[n][0]] for n in order]
    ro = [[idx[m] for m in DEFS[n][1]] for n in order]
    return lo, ro


def add(a, b):
    """Disjunctive sum: product graph on reachable pairs, root (0, 0) is node 0."""
    (alo, aro), (blo, bro) = a, b
    idx, order = {(0, 0): 0}, [(0, 0)]
    lo, ro = [], []
    i = 0
    while i < len(order):
        u, v = order[i]
        i += 1
        L, R = [], []
        for lst, ao, bo in ((L, alo, blo), (R, aro, bro)):
            for u2 in ao[u]:
                lst.append((u2, v))
            for v2 in bo[v]:
                lst.append((u, v2))
        outl = []
        for lst in (L, R):
            o = []
            for key in lst:
                if key not in idx:
                    idx[key] = len(order)
                    order.append(key)
                o.append(idx[key])
            outl.append(sorted(set(o)))
        lo.append(outl[0])
        ro.append(outl[1])
    return lo, ro


def neg(g):
    lo, ro = g
    return ro, lo


def all_candidates():
    """Return ordered dict name -> game for the 16 test games, 5 sums and 5 extra candidates."""
    out = {}
    for t in TESTS:
        out[t] = named(t)
    for name, x, y in SUM_CANDS:
        out[name] = add(named(x), named(y))
    for name in EXTRA_CANDS:
        out[name] = named(name)
    return out
