"""K55: small CGT games as graphs (L, R), node 0 = start, no terminals; sums; bisimulation reduction.
Used by gen55.py (the enlarged battery) and cands55.py (candidate signatures).
Notation: up = {0|*}, upstar = up + * = {0,*|0}, dbl_up = up + up = {0|up*}, dbl_upstar = dbl_up + * = {0|up},
up2nd = Conway's up-second {0|down*} (written ↑² in the brief), tiny-n = {0||0|-n}, miny-n = {n|0||0}, swa/b = the switch {a|b} (no "|" in names: it separates fields)."""
import itertools

def integer(n):
    a = abs(n); L = [[] for _ in range(a + 1)]; R = [[] for _ in range(a + 1)]
    for i in range(a):
        (L if n > 0 else R)[i].append(i + 1)
    return (L, R)

def node(Lopts, Ropts):
    """new game {Lopts | Ropts} (lists of games): disjoint union of the option graphs plus a new root 0."""
    L = [[]]; R = [[]]; roots = {}
    for side, opts in ((0, Lopts), (1, Ropts)):
        for g in opts:
            k = id(g)
            if k not in roots:
                off = len(L); roots[k] = off
                L += [[x + off for x in l] for l in g[0]]; R += [[x + off for x in r] for r in g[1]]
            (L if side == 0 else R)[0].append(roots[k])
    return reduce((L, R))

def gsum(*gs):
    sizes = [len(g[0]) for g in gs]
    states = list(itertools.product(*[range(s) for s in sizes])); idx = {s: i for i, s in enumerate(states)}
    L = [[] for _ in states]; R = [[] for _ in states]
    for s in states:
        for k, g in enumerate(gs):
            for x in g[0][s[k]]: L[idx[s]].append(idx[s[:k] + (x,) + s[k + 1:]])
            for x in g[1][s[k]]: R[idx[s]].append(idx[s[:k] + (x,) + s[k + 1:]])
    return reduce((L, R))

def neg(g):
    return (g[1], g[0])

def reduce(g):
    """keep nodes reachable from 0, then merge bisimilar nodes (same classes of Left and of Right options).
    Results r(X + T) do not change: the quotient map is a bisimulation of the move graph."""
    L, R = g; n = len(L)
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in L[v] + R[v]:
            if w not in seen: seen.add(w); st.append(w)
    order = sorted(seen); ren = {v: i for i, v in enumerate(order)}
    L = [[ren[w] for w in L[v]] for v in order]; R = [[ren[w] for w in R[v]] for v in order]; n = len(L)
    cls = [0] * n
    while True:
        sig = [(cls[v], tuple(sorted(set(cls[w] for w in L[v]))), tuple(sorted(set(cls[w] for w in R[v])))) for v in range(n)]
        ids = {}; new = []
        for s in sig:
            if s not in ids: ids[s] = len(ids)
            new.append(ids[s])
        if len(ids) == len(set(cls)): cls = new; break
        cls = new
    # renumber so that the class of node 0 is 0
    perm = {cls[0]: 0}
    for c in cls:
        if c not in perm: perm[c] = len(perm)
    m = len(perm); NL = [None] * m; NR = [None] * m
    for v in range(n):
        c = perm[cls[v]]
        if NL[c] is None:
            NL[c] = sorted(set(perm[cls[w]] for w in L[v])); NR[c] = sorted(set(perm[cls[w]] for w in R[v]))
    return (NL, NR)

def _t(x): return 'W' if x == -1 else 'B' if x == -2 else str(x)

def line(name, g):
    L, R = g
    return "%s | %d | %s" % (name, len(L), " ; ".join("%d: L=%s R=%s" % (i, ",".join(_t(x) for x in L[i]), ",".join(_t(x) for x in R[i])) for i in range(len(L))))

def readT(fn):
    out = []
    for ln in open(fn):
        if not ln.strip() or ln[0] == '#': continue
        name, n, rest = [x.strip() for x in ln.split('|', 2)]; n = int(n)
        L = [[] for _ in range(n)]; R = [[] for _ in range(n)]
        for part in rest.split(';'):
            part = part.strip(); i = int(part.split(':')[0])
            ls = part.split('L=')[1].split('R=')[0].strip(); rs = part.split('R=')[1].strip()
            cv = lambda x: -1 if x == 'W' else -2 if x == 'B' else int(x)
            L[i] = [cv(x) for x in ls.split(',') if x]; R[i] = [cv(x) for x in rs.split(',') if x]
        out.append((name, (L, R)))
    return out

# ---- named games ----
G = {}
for n in range(-6, 7): G[str(n)] = integer(n)
Z0 = G['0']
G['*'] = node([Z0], [Z0])
G['up'] = node([Z0], [G['*']]); G['down'] = neg(G['up'])
G['pm1'] = node([G['1']], [G['-1']])
G['over'] = ([[1], []], [[0], []]); G['under'] = neg(G['over'])
G['on'] = ([[0]], [[]]); G['off'] = ([[]], [[0]]); G['dud'] = ([[0]], [[0]])
G['upstar'] = node([Z0, G['*']], [Z0]); G['downstar'] = neg(G['upstar'])
G['dbl_up'] = node([Z0], [G['upstar']]); G['dbl_down'] = neg(G['dbl_up'])
G['dbl_upstar'] = node([Z0], [G['up']]); G['dbl_downstar'] = neg(G['dbl_upstar'])
G['up2nd'] = node([Z0], [G['downstar']]); G['down2nd'] = neg(G['up2nd'])
for n in range(1, 5):
    G['tiny%d' % n] = node([Z0], [node([Z0], [G[str(-n)]])]); G['miny%d' % n] = neg(G['tiny%d' % n])
    G['sw%d/-%d' % (n, n)] = node([G[str(n)]], [G[str(-n)]])
    G['sw%d/0' % n] = node([G[str(n)]], [Z0]); G['sw0/-%d' % n] = node([Z0], [G[str(-n)]])
NEW_SINGLES = ['upstar', 'downstar', 'dbl_up', 'dbl_down', 'dbl_upstar', 'dbl_downstar', 'up2nd', 'down2nd'] + \
    ['tiny%d' % n for n in range(1, 5)] + ['miny%d' % n for n in range(1, 5)] + \
    ['sw%d/-%d' % (n, n) for n in range(2, 5)] + ['sw%d/0' % n for n in range(1, 5)] + ['sw0/-%d' % n for n in range(1, 5)]
# reduced atom list for the sums of three (closed under negation; 0 included, so sums of one and two atoms appear too)
ATOMS = ['0', '*', 'up', 'down', 'tiny1', 'miny1', 'tiny2', 'miny2', 'pm1', '1', '-1', 'over', 'under']

def solve(g):
    """r(x, s) for every node of a small game (normal play, infinite play a draw); s = 0 White (Left) to move.
    Returns a function (i, s) -> 'W' | 'L' | 'D' from White's view."""
    from collections import deque
    L, R = g; n = len(L); val = {}; cnt = {}; pred = {}
    for i in range(n):
        for s, opts in ((0, L[i]), (1, R[i])):
            cnt[(i, s)] = len(opts)
            for j in opts: pred.setdefault((j, 1 - s), []).append((i, s))
    Q = deque()
    for k, c in cnt.items():
        if c == 0: val[k] = 'L' if k[1] == 0 else 'W'; Q.append(k)
    while Q:
        k = Q.popleft(); v = val[k]
        for p in pred.get(k, []):
            if p in val: continue
            win = 'W' if p[1] == 0 else 'L'
            if v == win: val[p] = win; Q.append(p)
            else:
                cnt[p] -= 1
                if cnt[p] == 0: val[p] = 'L' if p[1] == 0 else 'W'; Q.append(p)
    return lambda i, s: val.get((i, s), 'D')

def rsolve2(H, T):
    """r(H + T) at the start (both movers), product built on the fly without reduction (fast path for candidate scans).
    Returns (White-first result, Black-first result) from White's view."""
    from collections import deque
    (HL, HR), (TL, TR) = H, T; m = len(TL); n = len(HL) * m
    L = [None] * n; R = [None] * n; winL = set(); winR = set()
    for h in range(len(HL)):
        for t in range(m):
            i = h * m + t
            # terminals (-1 = White has won, -2 = Black has won, Definition 1.1) end the play; a mover with a move to
            # its own terminal wins; a move to the opponent's terminal is never better than having no move (convention N)
            L[i] = [x * m + t for x in HL[h] if x >= 0] + [h * m + y for y in TL[t] if y >= 0]
            R[i] = [x * m + t for x in HR[h] if x >= 0] + [h * m + y for y in TR[t] if y >= 0]
            if -1 in HL[h] or -1 in TL[t]: winL.add(i)
            if -2 in HR[h] or -2 in TR[t]: winR.add(i)
    val = [[0] * n, [0] * n]; cnt = [[len(L[i]) for i in range(n)], [len(R[i]) for i in range(n)]]
    pred = [[[] for _ in range(n)], [[] for _ in range(n)]]   # pred[s][j]: nodes i where mover s moves to j
    for i in range(n):
        for j in L[i]: pred[0][j].append(i)
        for j in R[i]: pred[1][j].append(i)
    Q = deque()
    for s, wins in ((0, winL), (1, winR)):
        for i in wins: val[s][i] = 1; Q.append((i, s))
    for s in (0, 1):
        for i in range(n):
            if cnt[s][i] == 0 and not val[s][i]: val[s][i] = 2; Q.append((i, s))   # 1 mover wins, 2 mover loses
    while Q:
        j, s = Q.popleft(); ps = 1 - s; v = val[s][j]
        for i in pred[ps][j]:
            if val[ps][i]: continue
            if v == 2: val[ps][i] = 1; Q.append((i, ps))
            else:
                cnt[ps][i] -= 1
                if cnt[ps][i] == 0: val[ps][i] = 2; Q.append((i, ps))
    def wv(s):
        x = val[s][0]
        return 'D' if x == 0 else ('W' if (x == 1) == (s == 0) else 'L')
    return wv(0), wv(1)
