"""K60: own code for abstract exact over groups beside finite D-games (written for K60; no code taken from K56/K57).

Conventions (LOOPY Definitions 1.1-1.3, 4.8; K40's convention for a board component):
- A toy group is a finite move graph on boards 0..n-1.  mv[g][s] = list of (y, d): side s (0 White, 1 Black) moves
  from board g to board y, d = 1 if the move is a double step (it gives the opponent the e.p. right for one turn).
  y may be the terminal 'W' (White has won) or 'B' (Black has won): promotions (or suicides).
  ep[g][s] = extra moves of s at g, available only while s holds the e.p. right (flag f = 1).
  chk[g][s] = side s is in check at board g.  A move of s to a board where s is in check is illegal (filtered).
- Alone (P): a side with no legal move loses if in check (mate) and draws otherwise (stalemate).
- In a D-sum G (+) T: a side in check may not move in T; a move in T clears the e.p. right; a terminal anywhere ends
  the play; a side with no move anywhere loses; infinite play is a draw.
- Results are White's view: 'W', 'D', 'L'.  r is the least fixed point (retrograde analysis).
- Roots: boards 0 and 1, no flag; Black's shuttle 0 <-> 1 (d = 0).  over_D: positions 0 = omega, 1 = 0_D.
"""
from collections import deque

WT, BT = "W", "B"
ORD = {"L": 0, "D": 1, "W": 2}


def solve(n, side, opts, nomove):
    """Least fixed point on an explicit graph.  opts[i]: list of state ids or WT/BT.  nomove[i]: value if opts empty."""
    val = ["D"] * n
    pred = [[] for _ in range(n)]
    cnt = [0] * n
    q = deque()
    for i in range(n):
        o = opts[i]
        if not o:
            if nomove[i] != "D":
                val[i] = nomove[i]
                q.append(i)
            continue
        me_win = WT if side[i] == 0 else BT
        if me_win in o:
            val[i] = "W" if side[i] == 0 else "L"
            q.append(i)
            continue
        real = [y for y in o if y not in (WT, BT)]
        if not real:  # only suicides
            val[i] = "L" if side[i] == 0 else "W"
            q.append(i)
            continue
        cnt[i] = len(real)
        for y in real:
            pred[y].append(i)
    while q:
        v = q.popleft()
        good_for = 0 if val[v] == "W" else 1  # the side for whom v is a win
        for u in pred[v]:
            if val[u] != "D":
                continue
            if side[u] == good_for:
                val[u] = val[v]
                q.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0:
                    val[u] = val[v]
                    q.append(u)
    return val


class Group:
    def __init__(self, n, mv, ep, chk):
        self.n, self.mv, self.ep, self.chk = n, mv, ep, chk
        for g in range(n):
            for s in (0, 1):
                self.mv[g][s] = sorted(set((y, d) for (y, d) in mv[g][s] if y in (WT, BT) or not chk[y][s]), key=str)
                self.ep[g][s] = sorted(set((y, d) for (y, d) in ep[g][s] if y in (WT, BT) or not chk[y][s]), key=str)

    def moves(self, g, f, s):
        return self.mv[g][s] + (self.ep[g][s] if f else [])

    def key(self):
        return repr((self.mv, self.ep, self.chk))


def group_alone(G, tokens=None, sumrule=False):
    """G alone.  tokens = (X, k): side X may move elsewhere (spend a token) at most k times, not in check; spending
    clears the right.  sumrule: a side with no move loses (else P: mate loses, stalemate draws).
    Returns dict (g, f, s, l) -> value, l = tokens left."""
    X, k = tokens if tokens else (None, 0)
    idx, st = {}, []
    for l in range(k + 1):
        for g in range(G.n):
            for f in (0, 1):
                for s in (0, 1):
                    idx[(g, f, s, l)] = len(st)
                    st.append((g, f, s, l))
    side, opts, nomove = [], [], []
    for (g, f, s, l) in st:
        o = [y if y in (WT, BT) else idx[(y, d, 1 - s, l)] for (y, d) in G.moves(g, f, s)]
        if s == X and l > 0 and not G.chk[g][s]:
            o.append(idx[(g, 0, 1 - s, l - 1)])
        side.append(s)
        opts.append(o)
        lose = "L" if s == 0 else "W"
        nomove.append(lose if (sumrule or G.chk[g][s]) else "D")
    val = solve(len(st), side, opts, nomove)
    return {st[i]: val[i] for i in range(len(st))}


def sum_with(G, T):
    """r(G (+) T).  T = (L, R): option lists per position (ints or WT/BT).  Returns dict (g, f, t, s) -> value."""
    LT, RT = T
    k = len(LT)
    idx, st = {}, []
    for g in range(G.n):
        for f in (0, 1):
            for t in range(k):
                for s in (0, 1):
                    idx[(g, f, t, s)] = len(st)
                    st.append((g, f, t, s))
    side, opts, nomove = [], [], []
    for (g, f, t, s) in st:
        o = [y if y in (WT, BT) else idx[(y, d, t, 1 - s)] for (y, d) in G.moves(g, f, s)]
        if not G.chk[g][s]:
            o += [y if y in (WT, BT) else idx[(g, 0, y, 1 - s)] for y in (LT[t] if s == 0 else RT[t])]
        side.append(s)
        opts.append(o)
        nomove.append("L" if s == 0 else "W")
    val = solve(len(st), side, opts, nomove)
    return {st[i]: val[i] for i in range(len(st))}


def dsum(A, B):
    """The D-sum of two D-games (no checks) as one D-game."""
    (LA, RA), (LB, RB) = A, B
    na, nb = len(LA), len(LB)
    L, R = [], []
    for a in range(na):
        for b in range(nb):
            for (src, dst, OA, OB) in ((0, L, LA, LB), (1, R, RA, RB)):
                o = [y if y in (WT, BT) else y * nb + b for y in OA[a]]
                o += [y if y in (WT, BT) else a * nb + y for y in OB[b]]
                dst.append(o)
    return (L, R)


def game_vals(T):
    """r(T) alone under the sum's rule: dict (t, s) -> value."""
    LT, RT = T
    k = len(LT)
    side, opts, nomove = [], [], []
    for t in range(k):
        for s in (0, 1):
            o = LT[t] if s == 0 else RT[t]
            opts.append([y if y in (WT, BT) else 2 * y + (1 - s) for y in o])
            side.append(s)
            nomove.append("L" if s == 0 else "W")
    val = solve(2 * k, side, opts, nomove)
    return {(t, s): val[2 * t + s] for t in range(k) for s in (0, 1)}


OVER = ([[1], []], [[0], []])    # omega: White -> 0_D, Black -> omega
UNDER = ([[0], []], [[1], []])   # mirror: White passes, Black -> 0


def over_vals(T):
    """r(over_D (+) T): dict (o, t, s) -> value, o = 0 for omega, 1 for 0_D."""
    v = game_vals(dsum(OVER, T))
    nb = len(T[0])
    return {(o, t, s): v[(o * nb + t, s)] for o in (0, 1) for t in range(nb) for s in (0, 1)}


# ---------------- Definition 4.8 (over orientation) ----------------
def exact_over(G):
    """Returns the list of freeze targets (q, d) if G is an exact over group, else None."""
    if any(G.chk[r][s] for r in (0, 1) for s in (0, 1)):
        return None
    p = group_alone(G)
    for r, o in ((0, 1), (1, 0)):
        if (o, 0) not in G.mv[r][1]:
            return None
        for (y, d) in G.mv[r][1]:
            if (y, d) == (o, 0):
                continue
            if y == BT:
                return None
            if y != WT and p[(y, d, 0, 0)] != "W":
                return None
    qs = set()
    for r in (0, 1):
        fr = []
        for (y, d) in G.mv[r][0]:
            if y == WT:
                return None          # a promotion is not a freeze to 0, and it does not lose at once
            if y == BT:
                continue
            if p[(y, d, 1, 0)] != "L":
                fr.append((y, d))
        if not fr:
            return None
        qs.update(fr)
    for (q, d) in qs:
        if q in (0, 1) or G.chk[q][0] or G.chk[q][1]:
            return None
        for f in sorted({d, 0}):
            bm = G.moves(q, f, 1)
            if not bm:
                return None
            for (y, dd) in bm:
                if y == BT or (y != WT and p[(y, dd, 0, 0)] != "W"):
                    return None
        wm = G.moves(q, 0, 0)
        if not wm:
            return None
        for (y, dd) in wm:
            if y == WT or (y != BT and p[(y, dd, 1, 0)] != "L"):
                return None
    return sorted(qs, key=str)


def bad_black_moves(G):
    """Non-shuttle Black root moves (r, y, d) whose target is a board (moves to WT are suicides, trivially fine)."""
    out = []
    for r, o in ((0, 1), (1, 0)):
        for (y, d) in G.mv[r][1]:
            if (y, d) == (o, 0) or y in (WT, BT):
                continue
            out.append((r, y, d))
    return out


MINUS1 = ([[], []], [[1], []])


def b1(G):
    sv = sum_with(G, MINUS1)
    return all(sv[(y, d, 0, 0)] == "W" for (_, y, d) in bad_black_moves(G))


# ---------------- Buchi games (for the auxiliary test) ----------------
def attractor(nodes, owner, succ, pred, target, player):
    """Nodes from which `player` can force a visit to `target` (>= 0 steps) inside the sub-arena `nodes`."""
    attr = set(target) & nodes
    cnt = {v: sum(1 for w in succ[v] if w in nodes) for v in nodes}
    q = deque(attr)
    while q:
        w = q.popleft()
        for v in pred[w]:
            if v not in nodes or v in attr:
                continue
            if owner[v] == player:
                attr.add(v)
                q.append(v)
            else:
                cnt[v] -= 1
                if cnt[v] == 0:
                    attr.add(v)
                    q.append(v)
    return attr


def buchi(owner, succ, acc):
    """Player 0 wins iff accepting nodes are visited infinitely often.  Every node must have a successor.
    Returns the set of nodes won by player 0."""
    n = len(owner)
    pred = [[] for _ in range(n)]
    for v in range(n):
        for w in succ[v]:
            pred[w].append(v)
    nodes = set(range(n))
    while True:
        r = attractor(nodes, owner, succ, pred, acc & nodes, 0)
        tr = nodes - r
        if not tr:
            return nodes
        nodes -= attractor(nodes, owner, succ, pred, tr, 1)


def aux_win(G, start_states):
    """The auxiliary game Aux(x) = x (+) under_D with White to move, scored: a finite end as usual (a terminal; a side
    with no move loses), an infinite play is a White win iff White passed (under: omega-bar -> omega-bar) infinitely
    often.  start_states: list of (g, f).  Returns dict (g, f) -> True if White wins Aux from (g, f, under, White)."""
    idx, st = {}, []
    for g in range(G.n):
        for f in (0, 1):
            for u in (0, 1):          # 0: omega-bar present, 1: frozen (0-bar)
                for s in (0, 1):
                    idx[(g, f, u, s)] = len(st)
                    st.append((g, f, u, s))
    WS, BS = len(st), len(st) + 1     # sinks
    owner = [s for (_, _, _, s) in st] + [0, 0]
    succ = [[] for _ in range(len(st) + 2)]
    acc = {WS}
    extra = []
    for i, (g, f, u, s) in enumerate(st):
        o = []
        for (y, d) in G.moves(g, f, s):
            o.append(WS if y == WT else BS if y == BT else idx[(y, d, u, 1 - s)])
        if u == 0 and not G.chk[g][s]:
            if s == 0:
                p = len(st) + 2 + len(extra)         # pass node, accepting, forced to (g, 0, 0, Black)
                extra.append(idx[(g, 0, 0, 1)])
                o.append(p)
            else:
                o.append(idx[(g, 0, 1, 0)])           # Black's freeze of under
        if not o:
            o = [BS if s == 0 else WS]
        succ[i] = o
    succ[WS] = [WS]
    succ[BS] = [BS]
    for k, tgt in enumerate(extra):
        owner.append(1)
        succ.append([tgt])
        acc.add(len(st) + 2 + k)
    win = buchi(owner, succ, acc)
    return {(g, f): idx[(g, f, 0, 0)] in win for (g, f) in start_states}
