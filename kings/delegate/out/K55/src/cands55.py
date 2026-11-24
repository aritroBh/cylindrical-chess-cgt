"""K55 part 2: which candidate games H have the results of root A / root B of Z_O on the whole battery?
usage: python3 cands55.py <za outputs...> -- <test files...>
A candidate H survives at a root if r(H + T) = r(Z_O + T) for every test T and both sides to move."""
import sys, itertools
from games55 import G, NEW_SINGLES, ATOMS, gsum, solve, readT, rsolve2
from compare55 import read_za
_i = sys.argv.index('--'); _j = sys.argv.index('--', _i + 1) if sys.argv.count('--') > 1 else len(sys.argv)
Z = {}
for _f in sys.argv[1:_i]: Z.update(read_za(_f))
_tf = sys.argv[_i + 1:_j]; _extra = sys.argv[_j + 1:]
tests = [t for _f in _tf for t in readT(_f)]
tests.sort(key=lambda t: len(t[1][0]))          # cheap tests first (early exit)
# candidates: every named single, every sum of two of (atoms and new singles), every sum of three atoms
pool = [a for a in ATOMS if a != '0'] + NEW_SINGLES
cand = {n: G[n] for n in G}
for a, b in itertools.combinations_with_replacement(pool, 2): cand[a + '+' + b] = gsum(G[a], G[b])
for c in itertools.combinations_with_replacement([a for a in ATOMS if a != '0'], 3): cand['+'.join(c)] = gsum(*[G[a] for a in c])
# extended families (added after the first look at the data): tiny-n, miny-n up to n = 20 (a stand-in for a decisive
# Black threat, larger than any integer in the battery, whose largest is 12), their sums with the short atoms, and
# one-node games {Ls | Rs} with Ls from {0, *, up, up*} and Rs from {0, *, up, up*, tiny-n, tiny-n + *, tiny-n + up} (n = 20)
from games55 import node, integer
for n in range(5, 21):
    G['tiny%d' % n] = node([G['0']], [node([G['0']], [integer(-n)])])
    cand['tiny%d' % n] = G['tiny%d' % n]
for n in (5, 8, 12, 13, 16, 20, 30):
    cand['B%d' % n] = node([G['0']], [G['tiny%d' % n]] if n <= 20 else [node([G['0']], [node([G['0']], [integer(-n)])])])
G['tiny30'] = cand['tiny30'] = node([G['0']], [node([G['0']], [integer(-30)])])
for n in (5, 8, 12, 13, 20):
    for a in ['*', 'up', 'down', 'upstar', 'downstar', 'dbl_up', 'dbl_upstar', 'up2nd', 'tiny2', 'miny2']:
        cand['tiny%d+%s' % (n, a)] = gsum(G['tiny%d' % n], G[a])
T20 = G['tiny20']; LS = {'0': G['0'], '*': G['*'], 'up': G['up'], 'upstar': G['upstar']}
RS = dict(LS); RS.update({'tiny20': T20, 'tiny20+*': gsum(T20, G['*']), 'tiny20+up': gsum(T20, G['up'])})
for k1 in range(1, 1 << len(LS)):
    ls = [x for i, x in enumerate(LS) if k1 >> i & 1]
    for k2 in range(1, 1 << len(RS)):
        rs = [x for i, x in enumerate(RS) if k2 >> i & 1]
        cand['{%s|%s}' % (','.join(ls), ','.join(rs))] = node([LS[x] for x in ls], [RS[x] for x in rs])
KEY = ['tiny5', 'tiny8', 'tiny12', 'tiny13', 'tiny20', 'tiny30', 'B5', 'B12', 'B13', 'B20', 'B30', 'tiny1', 'tiny2', 'tiny3', 'tiny4', 'dbl_upstar', 'dbl_up', 'up2nd', 'upstar', 'over', 'up', '*', 'up+up2nd', 'tiny2+*']
def mism(H, r, full):
    bad = []
    for name, T in tests:
        rr = rsolve2(H, T)
        for s, si in (('w', 0), ('b', 1)):
            if (name, r, s) in Z and rr[si] != Z[(name, r, s)][0]:
                bad.append(name + '/' + s)
                if not full: return bad
    return bad
print('battery: %d tests, %d results per root; %d candidates' % (len(tests), 2 * len(tests), len(cand)))
for r, rn in ((0, 'A (Black king d4)'), (1, 'B (Black king d5)')):
    surv = [n for n, H in cand.items() if not mism(H, r, False)]
    print('root %s: survivors %s' % (rn, ' '.join(surv) if surv else 'none'))
    for n in KEY + surv:
        if n in cand:
            b = mism(cand[n], r, True)
            print('   %-14s mismatches %3d  %s' % (n, len(b), ' '.join(b[:14])))
    # group the survivors into classes of equal short games (H1 - H2 a second-player win); loopy ones listed apart
    def short(g):
        L, R = g; n = len(L); state = [0] * n
        def dfs(v):
            state[v] = 1
            for w in L[v] + R[v]:
                if state[w] == 1 or (state[w] == 0 and not dfs(w)): return False
            state[v] = 2; return True
        return dfs(0)
    from games55 import neg
    classes = []
    for n in surv:
        H = cand[n]
        if not short(H): classes.append(['(loopy) ' + n]); continue
        for c in classes:
            if not c[0].startswith('(loopy)'):
                f = solve(gsum(H, neg(cand[c[0]])))
                if f(0, 0) == 'L' and f(0, 1) == 'W': c.append(n); break
        else: classes.append([n])
    print('   survivors in classes of equal games: ' + ' ; '.join(' = '.join(c) for c in classes))
