"""K60 referee: own solvers for abstract exact over groups in D-sums, Aux (Buchi) and T_N.

Written from the definitions only (LOOPY Def. 1.1-1.3, 4.8, K47 convention). No code shared with K60/src or K57.

Results are ints from White's side: 0 = L, 1 = D, 2 = W.
Terminal successor codes: WINT = White wins, LOST = Black wins, DRAWT = draw (only P alone: stalemate).
"""
WINT, LOST, DRAWT = -1, -2, -3
WHITE, BLACK = 0, 1


# ---------------------------------------------------------------- generic least-fixed-point solver
def _attr(n, owner, succ, pred, me, good):
    """Set of nodes from which `me` forces reaching terminal `good` (finite play)."""
    ins = [False] * n
    cnt = [0] * n
    work = []
    for i in range(n):
        s = succ[i]
        if owner[i] == me:
            if good in s:
                ins[i] = True
                work.append(i)
        else:
            c = 0
            for j in s:
                if j != good:
                    c += 1
            cnt[i] = c
            if c == 0:
                ins[i] = True
                work.append(i)
    while work:
        j = work.pop()
        for i in pred[j]:
            if ins[i]:
                continue
            if owner[i] == me:
                ins[i] = True
                work.append(i)
            else:
                cnt[i] -= 1
                if cnt[i] == 0:
                    ins[i] = True
                    work.append(i)
    return ins


def preds(n, succ):
    pred = [[] for _ in range(n)]
    for i in range(n):
        for j in succ[i]:
            if j >= 0:
                pred[j].append(i)
    return pred


def solve(n, owner, succ):
    """Least fixed point r: every node must have >= 1 successor (stuck nodes are encoded by the caller)."""
    pred = preds(n, succ)
    w = _attr(n, owner, succ, pred, WHITE, WINT)
    l = _attr(n, owner, succ, pred, BLACK, LOST)
    return [2 if w[i] else (0 if l[i] else 1) for i in range(n)]


def buchi(n, owner, succ, acc):
    """White's winning region of the Buchi game: play reaching WINT = White win, LOST = Black win,
    infinite play = White win iff it visits nodes with acc[i] infinitely often. Every node has >= 1 successor.
    Classical nested fixed point Z = nu Z. Attr+(acc & Z)."""
    pred = preds(n, succ)
    Z = [True] * n
    it = 0
    while True:
        it += 1
        tgt = [Z[i] and acc[i] for i in range(n)]
        inY = [False] * n
        cnt = [0] * n
        work = [i for i in range(n) if tgt[i]]
        for i in range(n):
            s = succ[i]
            if owner[i] == WHITE:
                if WINT in s:
                    inY[i] = True
            else:
                cnt[i] = sum(1 for j in s if j != WINT)
                if cnt[i] == 0:
                    inY[i] = True
            if inY[i] and not tgt[i]:
                tgt[i] = True
                work.append(i)
        while work:
            j = work.pop()
            for i in pred[j]:
                if inY[i]:
                    if owner[i] == BLACK:
                        cnt[i] -= 1
                    continue
                if owner[i] == WHITE:
                    ok = True
                else:
                    cnt[i] -= 1
                    ok = cnt[i] == 0
                if ok:
                    inY[i] = True
                    if not tgt[i]:
                        tgt[i] = True
                        work.append(i)
        if inY == Z:
            return Z, it
        Z = [Z[i] and inY[i] for i in range(n)]


# ---------------------------------------------------------------- abstract groups
class Group:
    """Boards 0..nb-1. chk[g][c]: king of colour c attacked at g. mv[g][c]: list of (target, kind) for colour c to
    move at g; kind 'n' normal, 'd' double step (opponent gets the e.p. right), 'p' promotion (target ignored).
    ep[g][c]: moves available to c at g only with the e.p. right. A non-promotion move by c into a board where c is in
    check is illegal. Roots: boards 0 and 1, Black's shuttle 0 <-> 1."""

    def __init__(self, nb):
        self.nb = nb
        self.chk = [[False, False] for _ in range(nb)]
        self.mv = [[[], []] for _ in range(nb)]
        self.ep = [[[], []] for _ in range(nb)]

    def legal(self, g, e, c):
        out = []
        lst = self.mv[g][c] + (self.ep[g][c] if e else [])
        for (t, k) in lst:
            if k == 'p' or not self.chk[t][c]:
                out.append((t, k))
        return out

    def sidx(self, g, e, c):
        return (g * 2 + e) * 2 + c

    def nstates(self):
        return self.nb * 4


def p_values(G):
    """P alone: promotion wins, mate loses, stalemate draw, infinite draw. Index sidx(g, e, c)."""
    n = G.nstates()
    owner = [0] * n
    succ = [None] * n
    for g in range(G.nb):
        for e in (0, 1):
            for c in (0, 1):
                i = G.sidx(g, e, c)
                owner[i] = c
                s = []
                for (t, k) in G.legal(g, e, c):
                    if k == 'p':
                        s.append(WINT if c == WHITE else LOST)
                    else:
                        s.append(G.sidx(t, 1 if k == 'd' else 0, 1 - c))
                if not s:
                    if G.chk[g][c]:
                        s = [LOST if c == WHITE else WINT]
                    else:
                        s = [DRAWT]
                succ[i] = s
    return solve(n, owner, succ)


def over_group():
    """over_D as a check-free group: board 0 = omega, 1 = 0_D. White omega -> 0_D, Black omega -> omega."""
    G = Group(2)
    G.mv[0][WHITE] = [(1, 'n')]
    G.mv[0][BLACK] = [(0, 'n')]
    return G


# ---------------------------------------------------------------- D-games (L, R) lists; terminals 'P' (+) and 'M' (-)
def sum_solve(G, T):
    """G (+) T under the sum's rules. Returns val[(g, e, t, c)] via index function."""
    L, R = T
    nt = len(L)
    nb = G.nb

    def idx(g, e, t, c):
        return ((g * 2 + e) * nt + t) * 2 + c

    n = nb * 2 * nt * 2
    owner = [0] * n
    succ = [None] * n
    for g in range(nb):
        for e in (0, 1):
            leg = (G.legal(g, e, 0), G.legal(g, e, 1))
            for t in range(nt):
                for c in (0, 1):
                    i = idx(g, e, t, c)
                    owner[i] = c
                    s = []
                    for (tg, k) in leg[c]:
                        if k == 'p':
                            s.append(WINT if c == WHITE else LOST)
                        else:
                            s.append(idx(tg, 1 if k == 'd' else 0, t, 1 - c))
                    if not G.chk[g][c]:
                        for o in (L[t] if c == WHITE else R[t]):
                            if o == 'P':
                                s.append(WINT)
                            elif o == 'M':
                                s.append(LOST)
                            else:
                                s.append(idx(g, 0, o, 1 - c))
                    if not s:
                        s = [LOST if c == WHITE else WINT]
                    succ[i] = s
    val = solve(n, owner, succ)
    return val, idx


def aux_solve(G, x, ex):
    """Aux(x): G (+) under_D, White to move at (x, ex, omega-bar). Buchi: infinite play is a White win iff White
    passed infinitely often. Returns (White wins?, number of iterations)."""
    nb = G.nb

    def idx(g, e, u, c):
        return ((g * 2 + e) * 2 + u) * 2 + c

    base = nb * 8
    # pass nodes: one per (g, e) with u = 1, White to move; index base + g*2 + e
    n = base + nb * 2
    owner = [0] * n
    succ = [None] * n
    acc = [False] * n
    for g in range(nb):
        for e in (0, 1):
            leg = (G.legal(g, e, 0), G.legal(g, e, 1))
            for u in (0, 1):
                for c in (0, 1):
                    i = idx(g, e, u, c)
                    owner[i] = c
                    s = []
                    for (tg, k) in leg[c]:
                        if k == 'p':
                            s.append(WINT if c == WHITE else LOST)
                        else:
                            s.append(idx(tg, 1 if k == 'd' else 0, u, 1 - c))
                    if u == 1 and not G.chk[g][c]:
                        if c == WHITE:
                            s.append(base + g * 2 + e)
                        else:
                            s.append(idx(g, 0, 0, WHITE))
                    if not s:
                        s = [LOST if c == WHITE else WINT]
                    succ[i] = s
            p = base + g * 2 + e
            owner[p] = WHITE
            succ[p] = [idx(g, 0, 1, BLACK)]
            acc[p] = True
    Z, it = buchi(n, owner, succ, acc)
    return Z[idx(x, ex, 1, WHITE)], it


# ---------------------------------------------------------------- test D-games
def T_N(N):
    """u_0..u_N = 0..N, position N+1 = '0'. White u_i -> u_{i+1}, u_N -> (+); Black u_i -> 0."""
    L = [[i + 1] for i in range(N)] + [['P'], []]
    R = [[N + 1] for _ in range(N + 1)] + [[]]
    return (L, R)


def dsum(A, B):
    """D-sum of two D-games as a D-game (terminals end everything)."""
    (LA, RA), (LB, RB) = A, B
    na, nbb = len(LA), len(LB)

    def ix(a, b):
        return a * nbb + b
    L = [None] * (na * nbb)
    R = [None] * (na * nbb)
    for a in range(na):
        for b in range(nbb):
            for (Lx, Ly, out) in ((LA, LB, L), (RA, RB, R)):
                o = []
                for y in Lx[a]:
                    o.append(y if y in ('P', 'M') else ix(y, b))
                for y in Ly[b]:
                    o.append(y if y in ('P', 'M') else ix(a, y))
                out[ix(a, b)] = o
    return (L, R)


def chainW(n):
    return ([[i + 1] for i in range(n)] + [[]], [[] for _ in range(n + 1)])


def chainB(n):
    return ([[] for _ in range(n + 1)], [[i + 1] for i in range(n)] + [[]])


NAMED = {
    'zero': ([[]], [[]]),
    'one': chainW(1), 'two': chainW(2), 'm1': chainB(1), 'm2': chainB(2), 'm3': chainB(3),
    'star': ([[1], []], [[1], []]),
    'up': ([[1], [], [1]], [[2], [], [1]]),
    'down': ([[2], [], [1]], [[1], [], [1]]),
    'on': ([[0]], [[]]), 'off': ([[]], [[0]]), 'dud': ([[0]], [[0]]),
    'over': ([[1], []], [[0], []]), 'under': ([[0], []], [[1], []]),
    'pm1': ([[1], [2], [], [], []], [[3], [], [], [4], []]),
    'hot': ([['P']], [['M']]),
    'Wthreat': ([[1], ['P']], [[], []]), 'Bthreat': ([[], []], [[1], ['M']]),
    'g2t0': ([[1], ['P']], [['M'], []]),            # K60's t0 of Prop. A2
    'Wwaste_Bthr': ([[0], []], [[1], ['M']]),       # White may pass forever, Black threatens
    'Bwaste_Wthr': ([[1], ['P']], [[0], []]),
    'suicideW': ([['M'], []], [[1], []]),
    'onW_offB': ([[0], [1]], [[1], [0]]),
}


def random_dgame(rng, maxpos=5, pterm=0.15, maxopt=2):
    k = rng.randint(1, maxpos)
    L, R = [], []
    for _ in range(k):
        for side in (L, R):
            o = []
            for _ in range(rng.randint(0, maxopt)):
                r = rng.random()
                if r < pterm:
                    o.append('P' if rng.random() < 0.55 or side is L else 'M')
                elif r < 2 * pterm:
                    o.append('M' if side is R or rng.random() < 0.3 else 'P')
                else:
                    o.append(rng.randrange(k))
            side.append(o)
    return (L, R)


# ---------------------------------------------------------------- second Buchi solver (Zielonka, for cross-checks)
def zielonka_aux(G, x, ex):
    """Same game as aux_solve, solved as a parity game (priority 2 on pass nodes, 1 elsewhere; terminals as sinks)
    with Zielonka's recursive algorithm. Independent of buchi()."""
    nb = G.nb
    nodes = {}
    owner, prio, succ = [], [], []

    def node(key, o, p):
        if key not in nodes:
            nodes[key] = len(owner)
            owner.append(o); prio.append(p); succ.append([])
        return nodes[key]
    WS = node('WS', WHITE, 2)
    LS = node('LS', WHITE, 1)
    succ[WS].append(WS); succ[LS].append(LS)
    for g in range(nb):
        for e in (0, 1):
            for u in (0, 1):
                for c in (0, 1):
                    node((g, e, u, c), c, 1)
            node(('pass', g, e), WHITE, 2)
    for g in range(nb):
        for e in (0, 1):
            for u in (0, 1):
                for c in (0, 1):
                    i = nodes[(g, e, u, c)]
                    for (tg, k) in G.legal(g, e, c):
                        if k == 'p':
                            succ[i].append(WS if c == WHITE else LS)
                        else:
                            succ[i].append(nodes[(tg, 1 if k == 'd' else 0, u, 1 - c)])
                    if u == 1 and not G.chk[g][c]:
                        succ[i].append(nodes[('pass', g, e)] if c == WHITE else nodes[(g, 0, 0, WHITE)])
                    if not succ[i]:
                        succ[i].append(LS if c == WHITE else WS)
            succ[nodes[('pass', g, e)]].append(nodes[(g, 0, 1, BLACK)])
    n = len(owner)

    def attr(V, A, pl):
        A = set(A)
        changed = True
        while changed:
            changed = False
            for i in V:
                if i in A:
                    continue
                ss = [j for j in succ[i] if j in V]
                if owner[i] == pl:
                    if any(j in A for j in ss):
                        A.add(i); changed = True
                else:
                    if ss and all(j in A for j in ss):
                        A.add(i); changed = True
        return A

    def zl(V):
        if not V:
            return set(), set()
        p = max(prio[i] for i in V)
        pl = WHITE if p % 2 == 0 else BLACK
        U = {i for i in V if prio[i] == p}
        A = attr(V, U, pl)
        W0, W1 = zl(V - A)
        Wopp = W1 if pl == WHITE else W0
        if not Wopp:
            return (set(V), set()) if pl == WHITE else (set(), set(V))
        B = attr(V, Wopp, 1 - pl)
        X0, X1 = zl(V - B)
        if pl == WHITE:
            return X0, X1 | B
        return X0 | B, X1
    W0, _ = zl(set(range(n)))
    return nodes[(x, ex, 1, WHITE)] in W0
