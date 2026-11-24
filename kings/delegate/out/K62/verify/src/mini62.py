"""K62 referee: minimise the hill-climbing examples (greedy deletion of moves keeping exactness and N*),
and print them. Usage: .venv/bin/python kings/delegate/out/K62/verify/src/mini62.py"""
from ref62 import Group, exact, x_of, sum_values, ladder, W_, aux_wins
from chk62 import analyse, INF

F, T = False, True
# the two examples printed by `chk62.py climb 7 50 lit3` and `... m2ep4` (logs/climb.log), as state -> moves
LIT3 = {(0, 0, 0): [(2, F), (2, F)], (0, 1, 0): [(2, F), (2, F), 'P', (2, T)], (0, 0, 1): [(1, F)],
        (0, 1, 1): [(1, F), (1, T)], (1, 0, 0): [(2, F), (1, T), (1, T)],
        (1, 1, 0): [(2, F), (1, T), (1, T), 'P', (2, F), (0, T)],
        (1, 0, 1): [(0, F), (0, F), (0, F), (1, T), (2, T)],
        (1, 1, 1): [(0, F), (0, F), (0, F), (1, T), (2, T), 'P', (0, T)], (2, 0, 0): [(1, T)],
        (2, 1, 0): [(1, T), (1, F), (2, F), (2, T)], (2, 0, 1): [(1, T)], (2, 1, 1): [(1, T), (0, T), (2, F)]}
M2EP4 = {(0, 0, 0): [(2, T), (3, T)], (0, 1, 0): [(2, T), (3, T)], (0, 0, 1): [(1, F)], (0, 1, 1): [(1, F), (3, F)],
         (1, 0, 0): [(2, F)], (1, 1, 0): [(2, F), (0, T), (3, F)], (1, 0, 1): [(0, F), (0, T), (3, F)],
         (1, 1, 1): [(0, F), (0, T), (3, F)], (2, 0, 0): [(3, F)], (2, 1, 0): [(3, F), (1, F)], (2, 0, 1): [(3, T)],
         (2, 1, 1): [(3, T), (3, F)], (3, 0, 0): [(2, F)], (3, 1, 0): [(2, F), 'P', (1, T), (1, F)],
         (3, 0, 1): ['P', (2, F), (1, T), (0, F)], (3, 1, 1): ['P', (2, F), (1, T), (0, F), 'P']}


def build(nb, st):
    mv0, ep = {}, {}
    for g in range(nb):
        for s in (0, 1):
            base = st.get((g, 0, s), [])
            full = st.get((g, 1, s), [])
            assert full[:len(base)] == base
            mv0[(g, s)] = list(base)
            ep[(g, s)] = list(full[len(base):])
    return mv0, ep


def best(G, reading, m2):
    res, _ = analyse(G, reading, m2)
    if res is None:
        return -1, None
    assert not res['viol'], res['viol']
    fin = [r for r in res['rows'] if r['Nstar'] < INF]
    if not fin:
        return 0, None
    r = max(fin, key=lambda r: r['Nstar'])
    return r['Nstar'], r


def minimise(nb, st, reading, m2):
    mv0, ep = build(nb, st)
    G = Group(nb, None, mv0, ep)
    target, _ = best(G, reading, m2)
    changed = True
    while changed:
        changed = False
        for d in (ep, mv0):
            for key in sorted(d):
                i = 0
                while i < len(d[key]):
                    if d is mv0 and key[1] == 1 and key[0] in (0, 1) and i == 0:
                        i += 1
                        continue  # keep the shuttle
                    trial = {k: list(v) for k, v in d.items()}
                    trial[key].pop(i)
                    H = Group(nb, None, trial if d is mv0 else mv0, trial if d is ep else ep)
                    if best(H, reading, m2)[0] >= target:
                        d[key] = trial[key]
                        changed = True
                    else:
                        i += 1
    G = Group(nb, None, mv0, ep)
    n, row = best(G, reading, m2)
    return G, n, row


NAMES = {0: 'A', 1: 'B', 2: 'q'}


def show(G, label, reading, m2):
    ok, info = exact(G, reading, m2)
    n, row = best(G, reading, m2)
    nm = lambda g: NAMES.get(g, 'g%d' % g)
    print('%s: %d boards, exact (%s, %s): %s, N* = %d at %s -> %s, value beside T_N*: %s'
          % (label, G.nb, reading, 'M2' if m2 else 'M1', ok, n, nm(row['r']), row['m'], 'W' if row['vN'] == W_ else 'not W'))
    for s, sn in ((1, 'Black'), (0, 'White')):
        parts = []
        for g in range(G.nb):
            base = G.mv[(g, 0, s)]
            extra = G.ep_only(g, s)
            f = lambda m: 'promotes' if m == 'P' else ('=>' if m[1] else '->') + nm(m[0])
            if base or extra:
                parts.append('%s: %s%s' % (nm(g), ', '.join(f(m) for m in base) or '-',
                                           (' | with right: ' + ', '.join(f(m) for m in extra)) if extra else ''))
        print('   %s  %s' % (sn, '; '.join(parts)))
    for N in range(0, n + 2):
        T = ladder(N)
        v = sum_values(G, T)
        print('   beside T_%d: x + u_0 = %s; roots (Black to move) = %s, %s' % (
            N, 'WDL'[2 - v[row['x'] * T.n]], 'WDL'[2 - v[G.si(0, 0, 1) * T.n]], 'WDL'[2 - v[G.si(1, 0, 1) * T.n]]))
    for rd in ('strict', 'literal'):
        for mm in (False, True):
            print('   exact %s %s: %s' % (rd, 'M2' if mm else 'M1', exact(G, rd, mm)[0]))


G, n, row = minimise(3, LIT3, 'literal', False)
show(G, 'literal-reading example (from lit3)', 'literal', False)
G, n, row = minimise(4, M2EP4, 'strict', True)
show(G, 'M2 e.p. example (from m2ep4)', 'strict', True)
