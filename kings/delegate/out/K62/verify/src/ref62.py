"""K62 referee: own solver for abstract over groups in D-sums (rules of the K61 packet, section 1).

Written by the K62 referee without reading the investigator's src/. Pure Python, no dependencies.

Conventions
- Sides: WHITE = 0 (Left), BLACK = 1 (Right). Values from White's side: L = 0 < D = 1 < W = 2.
- A group has boards 0..nb-1 (0 = A, 1 = B are the roots), chk[g] = [White in check, Black in check],
  mv0[(g, s)] = moves of side s at board g without a right, ep[(g, s)] = extra moves with the right
  (so a right only adds moves). A move is 'P' (promotion: a win for the mover) or (g2, dbl): to board g2,
  other side to move, holding the right iff dbl. Moves into one's own check are removed (legality).
- State index: (g, f, s) -> (g*2 + f)*2 + s.
- A D-game: n positions, L[t], R[t] lists of options: an int position, 'W' (the terminal "White has won")
  or 'B' ("Black has won").
"""
WHITE, BLACK = 0, 1
L_, D_, W_ = 0, 1, 2
TW, TB, TDRAW = -1, -2, -3


# ---------------------------------------------------------------- generic solver
def solve(n, side, succ):
    """Least-fixed-point retrograde analysis. succ[i]: node ids or TW/TB/TDRAW. No move: mover loses.
    TDRAW is a draw terminal (used only for stalemate in P alone). Infinite play is a draw."""
    val = [D_] * n
    done = [False] * n
    pred = [[] for _ in range(n)]
    cnt = [0] * n
    queue = []
    for i in range(n):
        s = succ[i]
        own = TW if side[i] == WHITE else TB
        if own in s:
            val[i] = W_ if side[i] == WHITE else L_
            done[i] = True
            queue.append(i)
            continue
        c = 0
        for j in s:
            if j >= 0:
                pred[j].append(i)
                c += 1
            elif j == TDRAW:
                c += 1  # a move that is never losing for the mover
        cnt[i] = c
        if c == 0:  # no move, or only moves to the opponent's terminal
            val[i] = L_ if side[i] == WHITE else W_
            done[i] = True
            queue.append(i)
    k = 0
    while k < len(queue):
        j = queue[k]
        k += 1
        v = val[j]
        for i in pred[j]:
            if done[i]:
                continue
            if (v == W_ and side[i] == WHITE) or (v == L_ and side[i] == BLACK):
                val[i] = v
                done[i] = True
                queue.append(i)
            else:
                cnt[i] -= 1
                if cnt[i] == 0:
                    val[i] = v
                    done[i] = True
                    queue.append(i)
    return val


# ---------------------------------------------------------------- D-games
class DG:
    def __init__(self, n, L, R, name=''):
        self.n, self.L, self.R, self.name = n, [list(x) for x in L], [list(x) for x in R], name

    def opts(self, t, s):
        return self.L[t] if s == WHITE else self.R[t]


def code(o):
    return TW if o == 'W' else TB if o == 'B' else o


def dg_values(T):
    """r(t, s) of T alone: node t*2 + s."""
    n = T.n * 2
    side = [i & 1 for i in range(n)]
    succ = []
    for t in range(T.n):
        for s in (0, 1):
            succ.append([code(o) if isinstance(o, str) else o * 2 + (1 - s) for o in T.opts(t, s)])
    return solve(n, side, succ)


def dsum(T1, T2):
    """The D-sum T1 + T2 as one D-game (positions (a, b) -> a*T2.n + b)."""
    n = T1.n * T2.n
    L, R = [], []
    for a in range(T1.n):
        for b in range(T2.n):
            for s, out in ((0, L), (1, R)):
                o = []
                for x in T1.opts(a, s):
                    o.append(x if isinstance(x, str) else x * T2.n + b)
                for y in T2.opts(b, s):
                    o.append(y if isinstance(y, str) else a * T2.n + y)
                out.append(o)
    return DG(n, L, R, T1.name + '+' + T2.name)


def over():   # 0 = omega, 1 = 0_D
    return DG(2, [[1], []], [[0], []], 'over')


def under():  # 0 = omega-bar, 1 = 0-bar
    return DG(2, [[0], []], [[1], []], 'under')


def ladder(N):  # u_0..u_N = 0..N, z = N+1
    L = [[i + 1] for i in range(N)] + [['W'], []]
    R = [[N + 1] for _ in range(N + 1)] + [[]]
    return DG(N + 2, L, R, 'T%d' % N)


def minus1():  # y = 0, z = 1; R(y) = {z}
    return DG(2, [[], []], [[1], []], '-1')


def chain(N):  # C_N: positions 0..N, L(i) = {i-1}, R(i) = {0} (i >= 1)
    L = [[]] + [[i - 1] for i in range(1, N + 1)]
    R = [[]] + [[0] for i in range(1, N + 1)]
    return DG(N + 1, L, R, 'C%d' % N)


# ---------------------------------------------------------------- groups
class Group:
    def __init__(self, nb, chk=None, mv0=None, ep=None, name='', filter_check=True):
        self.nb, self.name = nb, name
        self.chk = chk or [[False, False] for _ in range(nb)]
        mv0 = mv0 or {}
        ep = ep or {}
        self.mv = {}
        for g in range(nb):
            for s in (0, 1):
                base = [m for m in mv0.get((g, s), []) if not (filter_check and m != 'P' and self.chk[m[0]][s])]
                extra = [m for m in ep.get((g, s), []) if not (filter_check and m != 'P' and self.chk[m[0]][s])]
                self.mv[(g, 0, s)] = list(base)
                self.mv[(g, 1, s)] = list(base) + list(extra)
        self.ns = 4 * nb

    @staticmethod
    def si(g, f, s):
        return (g * 2 + f) * 2 + s

    @staticmethod
    def unsi(i):
        return i >> 2, (i >> 1) & 1, i & 1

    def succ_state(self, m, s):
        g2, dbl = m
        return self.si(g2, 1 if dbl else 0, 1 - s)

    def ep_only(self, g, s):
        """Moves legal only with the right (the e.p. moves)."""
        return self.mv[(g, 1, s)][len(self.mv[(g, 0, s)]):]


def p_values(G):
    """P alone: no move = mate (loss) if in check, else stalemate (draw). Node = state index."""
    n = G.ns
    side, succ = [], []
    for i in range(n):
        g, f, s = G.unsi(i)
        side.append(s)
        mv = G.mv[(g, f, s)]
        if not mv:
            succ.append([] if G.chk[g][s] else [TDRAW])
        else:
            succ.append([(TW if s == WHITE else TB) if m == 'P' else G.succ_state(m, s) for m in mv])
    return solve(n, side, succ)


def sum_values(G, T):
    """G + T with the sum's rules. Node = state*T.n + t. Returns val list."""
    n = G.ns * T.n
    side = [0] * n
    succ = [None] * n
    for i in range(G.ns):
        g, f, s = G.unsi(i)
        own = TW if s == WHITE else TB
        gm = [own if m == 'P' else G.succ_state(m, s) for m in G.mv[(g, f, s)]]
        free = not G.chk[g][s]
        after = G.si(g, 0, 1 - s)  # a move elsewhere clears the mover's right
        for t in range(T.n):
            node = i * T.n + t
            side[node] = s
            lst = [x if x < 0 else x * T.n + t for x in gm]
            if free:
                for o in T.opts(t, s):
                    lst.append(code(o) if isinstance(o, str) else after * T.n + o)
            succ[node] = lst
    return solve(n, side, succ)


# ---------------------------------------------------------------- Aux (Buchi)
def aux_graph(G):
    """Aux on G + under_D. Nodes: state*2 + u (u = 0: omega-bar, 1: 0-bar), then pass nodes, then sinks."""
    ns = G.ns
    base = ns * 2
    npass = ns
    WS, LS = base + npass, base + npass + 1
    n = LS + 1
    side = [0] * n
    succ = [None] * n
    acc = set()
    for i in range(ns):
        g, f, s = G.unsi(i)
        own_sink = WS if s == WHITE else LS
        opp_sink = LS if s == WHITE else WS
        gm = [own_sink if m == 'P' else G.succ_state(m, s) for m in G.mv[(g, f, s)]]
        free = not G.chk[g][s]
        for u in (0, 1):
            node = i * 2 + u
            side[node] = s
            lst = [x if x in (WS, LS) else x * 2 + u for x in gm]
            if u == 0 and free:
                if s == WHITE:
                    lst.append(base + i)  # pass node
                else:
                    lst.append(G.si(g, 0, WHITE) * 2 + 1)  # freeze of under
            if not lst:
                lst = [opp_sink]
            succ[node] = lst
        pn = base + i
        side[pn] = WHITE
        succ[pn] = [G.si(g, 0, BLACK) * 2 + 0]
        acc.add(pn)
    side[WS], succ[WS] = WHITE, [WS]
    side[LS], succ[LS] = WHITE, [LS]
    acc.add(WS)
    return n, side, succ, acc


def _attr(n, side, succ, target, player, arena=None):
    """Attractor of target for player within arena (None = all)."""
    inA = [arena is None or (v in arena) for v in range(n)] if arena is not None else [True] * n
    pred = [[] for _ in range(n)]
    cnt = [0] * n
    for v in range(n):
        if not inA[v]:
            continue
        c = 0
        for w in succ[v]:
            if inA[w]:
                pred[w].append(v)
                c += 1
        cnt[v] = c
    res = [False] * n
    q = []
    for v in target:
        if inA[v] and not res[v]:
            res[v] = True
            q.append(v)
    k = 0
    while k < len(q):
        w = q[k]
        k += 1
        for v in pred[w]:
            if res[v]:
                continue
            if side[v] == player:
                res[v] = True
                q.append(v)
            else:
                cnt[v] -= 1
                if cnt[v] == 0:
                    res[v] = True
                    q.append(v)
    return set(v for v in range(n) if res[v])


def buchi_numu(n, side, succ, acc):
    """White's winning region by nu Z. mu Y. (CPre(Y) or (Acc and CPre(Z)))."""
    Z = set(range(n))
    while True:
        A = set()
        for v in acc:
            if side[v] == WHITE:
                if any(w in Z for w in succ[v]):
                    A.add(v)
            elif all(w in Z for w in succ[v]):
                A.add(v)
        Y = _attr(n, side, succ, A, WHITE)
        if Y == Z:
            return Z
        Z = Y


def buchi_classic(n, side, succ, acc):
    """Classical algorithm: repeatedly remove Black's attractor of the nodes that cannot reach Acc."""
    arena = set(range(n))
    while True:
        R = _attr(n, side, succ, acc & arena, WHITE, arena)
        trap = arena - R
        if not trap:
            return arena
        Bw = _attr(n, side, succ, trap, BLACK, arena)
        arena = arena - Bw


def aux_wins(G, both=True):
    """Set of White-to-move... all states sigma (index) such that White wins Aux from (sigma, omega-bar)."""
    n, side, succ, acc = aux_graph(G)
    W1 = buchi_numu(n, side, succ, acc)
    res1 = set(i for i in range(G.ns) if i * 2 in W1)
    if both:
        W2 = buchi_classic(n, side, succ, acc)
        res2 = set(i for i in range(G.ns) if i * 2 in W2)
        assert res1 == res2, ('Buchi solvers disagree', G.name)
    return res1


def surv_under(G):
    """r(sigma + omega-bar, side of sigma) in the ordinary D-sum with under_D (infinite play a draw)."""
    v = sum_values(G, under())
    return {i: v[i * 2] for i in range(G.ns)}


# ---------------------------------------------------------------- exactness
def exact(G, reading='literal', m2=False):
    """Check (O0)-(O4) of the K61 packet 1.5 with roots 0 = A, 1 = B and the Black shuttle.
    reading 'literal': promotions only constrained at the named states (Definition 4.8 as written);
    'strict': no promotion at any state of a root board or q-board.
    Returns (ok, info) with info = dict(freezes, qboards, qstates, bad)."""
    P = p_values(G)
    si = G.si
    info = {'why': ''}

    def fail(w):
        info['why'] = w
        return False, info

    def loses_at_once(m, s):
        if m == 'P':
            return False
        v = P[G.succ_state(m, s)]
        return v == (L_ if s == WHITE else W_)

    A, B = 0, 1
    for r, o in ((A, B), (B, A)):
        if (o, False) not in G.mv[(r, 0, BLACK)]:
            return fail('no shuttle')
    freezes = []
    for r in (A, B):
        mvW = G.mv[(r, 0, WHITE)]
        if any(m == 'P' for m in mvW):
            return fail('O2 white root promotion')
        fz = [m for m in mvW if not loses_at_once(m, WHITE)]
        if not fz:
            return fail('O2 no freeze')
        freezes += [(r, m) for m in fz]
    qboards = sorted(set(m[0] for r, m in freezes))
    qstates = set()
    for r, m in freezes:
        qstates.add(si(m[0], 1 if m[1] else 0, BLACK))
        qstates.add(si(m[0], 0, WHITE))
    # O0
    for g in [A, B] + qboards:
        if G.chk[g][0] or G.chk[g][1]:
            return fail('O0 check')
    # O1
    bad = []
    for r, o in ((A, B), (B, A)):
        lst = list(G.mv[(r, 0, BLACK)])
        lst.remove((o, False))  # the shuttle (one copy)
        for m in lst:
            if not loses_at_once(m, BLACK):
                return fail('O1')
            bad.append((r, m))
    # O3, O4
    for q in qstates:
        g, f, s = G.unsi(q)
        mv = G.mv[(g, f, s)]
        if not mv:
            return fail('O3/O4 no move')
        if not all(loses_at_once(m, s) for m in mv):
            return fail('O3/O4')
    if reading == 'strict':
        for g in [A, B] + qboards:
            for f in (0, 1):
                for s in (0, 1):
                    if 'P' in G.mv[(g, f, s)]:
                        return fail('strict promotion')
    if m2:
        for (g, f, s), mv in G.mv.items():
            tg = [m for m in mv if m != 'P']
            if any(m[0] == g for m in tg):
                return fail('M2 same board')
            if len(set(tg)) != len(tg):
                return fail('M2 duplicate')
            if m2 == 'board' and len(set(m[0] for m in tg)) != len(tg):
                return fail('M2b two moves to one board')
    info.update(freezes=freezes, qboards=qboards, qstates=qstates, bad=bad, P=P)
    return True, info


def x_of(G, r, m):
    """x_m: the state after the bad Black move m at root r (White to move)."""
    return G.succ_state(m, BLACK)


# ---------------------------------------------------------------- ladder sets, Z, P, E
def S_sets(G, nmax):
    """S[n] = set of states sigma with sigma + u_0 of T_n a White win, n = 0..nmax."""
    out = []
    for n in range(nmax + 1):
        T = ladder(n)
        v = sum_values(G, T)
        out.append(frozenset(i for i in range(G.ns) if v[i * T.n] == W_))
    return out


def Zset(G, x):
    seen = {x}
    st = [x]
    while st:
        i = st.pop()
        g, f, s = G.unsi(i)
        nxt = [G.succ_state(m, s) for m in G.mv[(g, f, s)] if m != 'P']
        if s == WHITE and not G.chk[g][WHITE]:
            nxt.append(G.si(g, 0, BLACK))
        for j in nxt:
            if j not in seen:
                seen.add(j)
                st.append(j)
    return seen


def PE(G, x, F0):
    """P(x), E(x) of the investigator's Theorem 4.20, computed from my own definitions.
    F0 = set of states sigma with sigma + y of -1 a White win."""
    Z = Zset(G, x)
    P, E = set(), set()
    whites = {}
    for i in Z:
        g, f, s = G.unsi(i)
        if s == WHITE and not G.chk[g][WHITE]:
            P.add(g)
            whites.setdefault(g, []).append(i)
    for g in P:
        if all(i in F0 for i in whites[g]):
            E.add(g)
    return Z, P, E


def F0_set(G):
    T = minus1()
    v = sum_values(G, T)
    return frozenset(i for i in range(G.ns) if v[i * T.n] == W_)


def white_ep_promotes(G):
    return any('P' in G.ep_only(g, WHITE) for g in range(G.nb))
