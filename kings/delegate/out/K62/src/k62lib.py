"""K62 toy library: abstract groups, D-sums, exactness (O0-O4), Aux (Buchi), ladders T_N.

Own code for K62 (nothing copied from K60/K61 code). Rules (K61 packet section 1):
- a group state is (g, f, s): board g, e.p. flag f (1 = the side to move holds the right), side s (0 White, 1 Black);
- moves of s at g: list `mv[g][s]` (legal with or without the right) plus `ep[g][s]` (legal only with the right);
  a move is 'P' (promotes: s wins at once) or (g2, d) (to board g2, other side to move, right iff d);
  no move into one's own check (moves to a board where the mover is in check are dropped);
- in a sum: a promotion ends the play; a side in check may not move elsewhere; a move elsewhere clears the
  mover's right; a side with no move anywhere loses; infinite play is a draw;
- P alone: a side with no move loses if in check, draws otherwise.
Values are from White's side: +1 = W, 0 = D, -1 = L.
"""
from collections import deque

W, B = 0, 1
TW, TB = -1, -2          # successor codes: terminal White win, terminal Black win


def solve(side, succ):
    """Least fixed point on an explicit graph. side[v] in {0,1}; succ[v] list of node ids or TW/TB.
    Returns list of values +1/0/-1 (White's view)."""
    n = len(side)
    val = [0] * n
    pred = [[] for _ in range(n)]
    for v in range(n):
        for w in succ[v]:
            if w >= 0:
                pred[w].append(v)
    # White wins: attractor of TW for White
    for target, mover_good in ((1, W), (-1, B)):
        good = TW if mover_good == W else TB
        cnt = [0] * n
        q = deque()
        for v in range(n):
            if val[v] != 0:
                continue
            s = succ[v]
            if side[v] == mover_good:
                if good in s:
                    val[v] = target
                    q.append(v)
            else:
                # opponent of mover_good to move: wins for mover_good if it has no move,
                # or all moves lead to mover_good's terminal
                c = 0
                for w in s:
                    if w == good:
                        continue
                    c += 1
                cnt[v] = c
                if c == 0:
                    val[v] = target
                    q.append(v)
        while q:
            w = q.popleft()
            for v in pred[w]:
                if val[v] != 0:
                    continue
                if side[v] == mover_good:
                    val[v] = target
                    q.append(v)
                else:
                    cnt[v] -= 1
                    if cnt[v] == 0:
                        val[v] = target
                        q.append(v)
    return val


class Group:
    """Abstract group. nb boards; chk[g] = (White in check, Black in check); mv/ep as in the module doc.
    roots = (A, B); shuttle moves are (B, 0) at (A, Black) and (A, 0) at (B, Black)."""

    def __init__(self, nb, names=None):
        self.nb = nb
        self.names = names or [str(i) for i in range(nb)]
        self.chk = [[False, False] for _ in range(nb)]
        self.mv = [[[], []] for _ in range(nb)]
        self.ep = [[[], []] for _ in range(nb)]
        self.roots = (0, 1)

    def idx(self, name):
        return self.names.index(name)

    def legal(self, g, f, s):
        out = []
        for m in self.mv[g][s] + (self.ep[g][s] if f else []):
            if m == 'P':
                out.append(m)
            else:
                g2, d = m
                if self.chk[g2][s]:
                    continue  # no move into own check
                out.append(m)
        return out

    def states(self):
        return [(g, f, s) for g in range(self.nb) for f in (0, 1) for s in (0, 1)]

    def has_ep_promotion(self):
        return any('P' in self.ep[g][s] for g in range(self.nb) for s in (0, 1))

    def has_checks(self):
        return any(self.chk[g][0] or self.chk[g][1] for g in range(self.nb))

    def has_ep(self):
        return any(self.ep[g][s] for g in range(self.nb) for s in (0, 1)) or any(
            m != 'P' and m[1] for g in range(self.nb) for s in (0, 1) for m in self.mv[g][s])

    # ---------- P alone ----------
    def p_values(self):
        sts = self.states()
        ix = {st: i for i, st in enumerate(sts)}
        side, succ = [], []
        for (g, f, s) in sts:
            side.append(s)
            ms = self.legal(g, f, s)
            out = []
            for m in ms:
                if m == 'P':
                    out.append(TW if s == W else TB)
                else:
                    out.append(ix[(m[0], 1 if m[1] else 0, 1 - s)])
            if not ms and not self.chk[g][s]:
                out = None  # stalemate: draw
            succ.append(out)
        # stalemate nodes: give them a self loop (draw) -> infinite play = draw
        for i, o in enumerate(succ):
            if o is None:
                succ[i] = [i]
        val = solve(side, succ)
        return {st: val[i] for i, st in enumerate(sts)}


def loses_at_once(G, pv, g, f, s, m):
    """Move m of side s at (g,f): 'loses at once' = state after it, other side to move, is a win for the
    other side in P alone."""
    if m == 'P':
        return False
    st = (m[0], 1 if m[1] else 0, 1 - s)
    return pv[st] == (1 if s == B else -1)


def exactness(G):
    """Check O0-O4. Returns (ok, info) with info = dict(freezes, qstates, bad) or reason."""
    pv = G.p_values()
    A, Bb = G.roots
    info = {'freezes': [], 'qstates': set(), 'bad': []}
    for r, other in ((A, Bb), (Bb, A)):
        if G.chk[r][0] or G.chk[r][1]:
            return False, 'O0 check at root'
        bl = G.legal(r, 0, B)
        if (other, False) not in bl and (other, 0) not in bl:
            return False, 'O1 no shuttle'
        for m in bl:
            if m == 'P':
                return False, 'O1 Black root promotion'
            if m[0] == other and not m[1]:
                continue
            if not loses_at_once(G, pv, r, 0, B, m):
                return False, 'O1 bad move does not lose at once'
            info['bad'].append((r, m))
        wl = G.legal(r, 0, W)
        fr = []
        for m in wl:
            if m == 'P':
                return False, 'O2 White root promotion'
            if not loses_at_once(G, pv, r, 0, W, m):
                fr.append(m)
        if not fr:
            return False, 'O2 no freeze'
        info['freezes'] += [(r, m) for m in fr]
    for (r, m) in info['freezes']:
        q, d = m
        if G.chk[q][0] or G.chk[q][1]:
            return False, 'O0 check at q'
        for st in ((q, 1 if d else 0, B), (q, 0, W)):
            info['qstates'].add(st)
    for (q, f, s) in info['qstates']:
        ms = G.legal(q, f, s)
        if not ms:
            return False, 'O3/O4 no move at q'
        for m in ms:
            if m == 'P':
                return False, 'O3/O4 promotion at q'
            if not loses_at_once(G, pv, q, f, s, m):
                return False, 'O3/O4 q move does not lose at once'
    return True, info


def x_of(bad):
    r, m = bad
    return (m[0], 1 if m[1] else 0, W)


# ---------------- D-games ----------------
class DGame:
    """positions 0..n-1; L[i], R[i]: lists of positions or '+' (White's terminal) / '-' (Black's terminal)."""

    def __init__(self, L, R, name=''):
        self.L, self.R, self.n, self.name = L, R, len(L), name


def ladder(N):
    L = [[i + 1] for i in range(N)] + [['+'], []]
    R = [[N + 1] for _ in range(N + 1)] + [[]]
    return DGame(L, R, 'T%d' % N)


OVER = DGame([[1], []], [[0], []], 'over')      # 0 = omega, 1 = 0_D
UNDER = DGame([[0], []], [[1], []], 'under')    # 0 = omega-bar, 1 = 0-bar
MINUS1 = DGame([[], []], [[1], []], '-1')       # Black has one move elsewhere


def sum_solve(G, T, comp2=None):
    """Solve G (+ optional second D-game comp2) + T on all states. G may be None.
    Returns dict: (gstate or None, c2pos or None, tpos, side) -> value."""
    nodes = []
    ix = {}
    gst = [(g, f) for g in range(G.nb) for f in (0, 1)] if G is not None else [None]
    c2 = list(range(comp2.n)) if comp2 is not None else [None]
    for a in gst:
        for c in c2:
            for t in range(T.n):
                for s in (0, 1):
                    if a is not None and s != s:  # placeholder
                        pass
                    ix[(a, c, t, s)] = len(nodes)
                    nodes.append((a, c, t, s))
    side = [nd[3] for nd in nodes]
    succ = []
    for (a, c, t, s) in nodes:
        out = []
        incheck = False
        if a is not None:
            g, f = a
            incheck = G.chk[g][s]
            for m in G.legal(g, f, s):
                if m == 'P':
                    out.append(TW if s == W else TB)
                else:
                    out.append(ix[((m[0], 1 if m[1] else 0), c, t, 1 - s)])
        if not incheck:
            a0 = (a[0], 0) if a is not None else None
            if comp2 is not None:
                for o in (comp2.L[c] if s == W else comp2.R[c]):
                    if o == '+':
                        out.append(TW)
                    elif o == '-':
                        out.append(TB)
                    else:
                        out.append(ix[(a0, o, t, 1 - s)])
            for o in (T.L[t] if s == W else T.R[t]):
                if o == '+':
                    out.append(TW)
                elif o == '-':
                    out.append(TB)
                else:
                    out.append(ix[(a0, c, o, 1 - s)])
        succ.append(out)
    val = solve(side, succ)
    return {nd: val[i] for i, nd in enumerate(nodes)}


def value_G_T(G, T):
    """r(gstate + t, s): dict ((g,f), t, s) -> value."""
    v = sum_solve(G, T)
    return {(a, t, s): val for (a, c, t, s), val in v.items()}


def value_over_T(T):
    """r(omega + t, s) and r(t, s): returns (rom, rzero) dicts (t, s) -> value."""
    v = sum_solve(None, T, OVER)
    rom = {(t, s): v[(None, 0, t, s)] for t in range(T.n) for s in (0, 1)}
    rz = {(t, s): v[(None, 1, t, s)] for t in range(T.n) for s in (0, 1)}
    return rom, rz


def results_of_omega(G, info, T, vGT=None, rom=None, rz=None):
    """Full check: both roots (no right), both sides, every t: r(root+t,s) = r(omega+t,s);
    every q-state: r(q+t, s_q) = r(t, s_q). Returns list of violations."""
    if vGT is None:
        vGT = value_G_T(G, T)
    if rom is None:
        rom, rz = value_over_T(T)
    bad = []
    for r in G.roots:
        for t in range(T.n):
            for s in (0, 1):
                if vGT[((r, 0), t, s)] != rom[(t, s)]:
                    bad.append(('root', r, t, s, vGT[((r, 0), t, s)], rom[(t, s)]))
    for (q, f, s) in info['qstates']:
        for t in range(T.n):
            if vGT[((q, f), t, s)] != rz[(t, s)]:
                bad.append(('q', (q, f, s), t, vGT[((q, f), t, s)], rz[(t, s)]))
    return bad


def condC(G, x, T, vGT=None, rom=None):
    """(C) beside T at x = (g, f, W): r(x+t, W) >= r(omega+t, B) for all t. Returns list of failing t."""
    if vGT is None:
        vGT = value_G_T(G, T)
    if rom is None:
        rom, _ = value_over_T(T)
    g, f, _ = x
    return [t for t in range(T.n) if vGT[((g, f), t, W)] < rom[(t, B)]]


# ---------------- Aux: Buchi game ----------------
def aux_win(G):
    """White's winning region of Aux (G + under_D, Buchi: White wins an infinite play iff it has infinitely
    many White passes). Returns set of group states (g, f, s) with under present that White wins."""
    nodes, ix = [], {}
    for g in range(G.nb):
        for f in (0, 1):
            for s in (0, 1):
                for u in (0, 1):
                    for jp in ((0, 1) if (s == B and u == 1 and f == 0) else (0,)):
                        ix[(g, f, s, u, jp)] = len(nodes)
                        nodes.append((g, f, s, u, jp))
    SW = len(nodes); nodes.append('SW')   # White-win sink (accepting)
    SB = len(nodes); nodes.append('SB')   # Black-win sink
    owner, succ, acc = [], [], []
    for nd in nodes:
        if nd == 'SW':
            owner.append(W); succ.append([SW]); acc.append(True); continue
        if nd == 'SB':
            owner.append(W); succ.append([SB]); acc.append(False); continue
        g, f, s, u, jp = nd
        out = []
        for m in G.legal(g, f, s):
            if m == 'P':
                out.append(SW if s == W else SB)
            else:
                out.append(ix[(m[0], 1 if m[1] else 0, 1 - s, u, 0)])
        if u == 1 and not G.chk[g][s]:
            if s == W:
                out.append(ix[(g, 0, B, 1, 1)])      # White's pass
            else:
                out.append(ix[(g, 0, W, 0, 0)])      # Black's freeze of under
        if not out:
            out = [SB if s == W else SW]
        owner.append(s); succ.append(out); acc.append(jp == 1)
    win = buchi(owner, succ, acc)
    res = set()
    for i, nd in enumerate(nodes):
        if nd in ('SW', 'SB'):
            continue
        g, f, s, u, jp = nd
        if u == 1 and jp == 0 and i in win:
            res.add((g, f, s))
    return res


def buchi(owner, succ, acc):
    """White (0) wins a play iff it visits accepting nodes infinitely often (every node has a successor).
    Nested fixed point: Win = nu Z. mu Y. (F & CPre(Z)) | CPre(Y). Returns White's winning region."""
    n = len(owner)

    def cpre(X):
        out = set()
        for v in range(n):
            if owner[v] == W:
                if any(w in X for w in succ[v]):
                    out.add(v)
            elif all(w in X for w in succ[v]):
                out.add(v)
        return out

    Z = set(range(n))
    while True:
        base = {v for v in cpre(Z) if acc[v]}
        Y = set()
        while True:
            Y2 = base | cpre(Y)
            if Y2 == Y:
                break
            Y = Y2
        if Y == Z:
            return Z
        Z = Y


# ---------------- ladders, P(x), E, S_n ----------------
def ladder_values(G, N):
    """S_N as a dict over group states (g,f,s): True iff White wins state + u_0 of T_N."""
    T = ladder(N)
    v = value_G_T(G, T)
    return {(g, f, s): v[((g, f), 0, s)] == 1 for g in range(G.nb) for f in (0, 1) for s in (0, 1)}


def nstar(G, x, cap):
    """least n <= cap with x not in S_n (None if x in S_n for all n <= cap)."""
    for n in range(cap + 1):
        if not ladder_values(G, n)[x]:
            return n
    return None


def pass_closure(G, x):
    """Z: group states reachable from x by group moves and White passes (under not yet frozen)."""
    Z = {x}
    q = deque([x])
    while q:
        g, f, s = q.popleft()
        nxt = []
        for m in G.legal(g, f, s):
            if m != 'P':
                nxt.append((m[0], 1 if m[1] else 0, 1 - s))
        if s == W and not G.chk[g][W]:
            nxt.append((g, 0, B))
        for st in nxt:
            if st not in Z:
                Z.add(st); q.append(st)
    return Z


def bound_data(G, x, cap=None):
    """Returns dict with P (boards), E (boards), Sinf (boards in P whose Black state is in S_inf),
    N* (or None), and the chain R_n."""
    Z = pass_closure(G, x)
    P = sorted({g for (g, f, s) in Z if s == W and not G.chk[g][W]})
    vm1 = value_G_T(G, MINUS1)        # F(empty): White wins beside -1 (Black has one move elsewhere)
    F0 = {(g, f, s) for g in range(G.nb) for f in (0, 1) for s in (0, 1) if vm1[((g, f), 0, s)] == 1}
    E = sorted(g for g in P if all((gg, f, s) in F0 for (gg, f, s) in Z if gg == g and s == W
                                   and not G.chk[g][W]))
    if cap is None:
        cap = 4 * G.nb + 2
    Sn = [ladder_values(G, n) for n in range(cap + 1)]
    Sinf = sorted(g for g in P if Sn[cap][(g, 0, B)])
    ns = next((n for n in range(cap + 1) if not Sn[n][x]), None)
    chain = [sorted(g for g in P if g not in E and Sn[n][(g, 0, B)]) for n in range(cap + 1)]
    return {'Z': Z, 'P': P, 'E': E, 'Sinf': Sinf, 'nstar': ns, 'chain': chain, 'Sn': Sn}
