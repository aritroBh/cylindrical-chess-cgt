"""r2_lib.py -- second referee's own library for K30 (written from kings/SPEC.md and PROOF.md text only;
no code of K30, the first referee, K24 or K7 was read).

Squares are ints f + 8*r with f = file 0..7 (a..h) and r = rank index 0..7 (rank 1..8).
Boards: 'cyl' (files glued), 'flat'.
Pieces in the families used here: White king + at most one White pawn, Black king + at most one Black pawn.
No officers (promotion is terminal in the models P, EPW, EPB).  En passant is not implemented and the code
raises if a double step would create an e.p. right (it cannot, in the families used).
"""
import sys

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def name(s):
    return 'abcdefgh'[s % 8] + str(s // 8 + 1)


def sqn(t):
    return 'abcdefgh'.index(t[0]) + 8 * (int(t[1:]) - 1)


class Board:
    def __init__(self, kind):
        assert kind in ('cyl', 'flat')
        self.kind = kind
        self.cyl = kind == 'cyl'
        self.nb = [[] for _ in range(64)]
        self.adj = [[False] * 64 for _ in range(64)]
        self.batt = [[] for _ in range(64)]   # squares attacked by a Black pawn standing here
        self.watt = [[] for _ in range(64)]   # squares attacked by a White pawn standing here
        for s in range(64):
            for df, dr in DIRS:
                t = self.at(s % 8 + df, s // 8 + dr)
                if t is not None:
                    self.nb[s].append(t)
                    self.adj[s][t] = True
            for df in (-1, 1):
                t = self.at(s % 8 + df, s // 8 - 1)
                if t is not None:
                    self.batt[s].append(t)
                t = self.at(s % 8 + df, s // 8 + 1)
                if t is not None:
                    self.watt[s].append(t)

    def at(self, f, r):
        if r < 0 or r > 7:
            return None
        if self.cyl:
            f %= 8
        elif f < 0 or f > 7:
            return None
        return f + 8 * r

    def relx(self, s, pf):
        """file offset of square s from file pf, in -4..3 (wrapped on the cylinder)."""
        d = s % 8 - pf
        if self.cyl:
            d = (d + 4) % 8 - 4
        return d


# --------------------------------------------------------------------------------------------------
# generic move generator for the family: state = (wk, bk, wp, bp, side); wp/bp = -1 when absent.
# side 0 = White to move, 1 = Black to move.  Returns (list of (label, kind, newstate)) where kind is
# 'n' (new state), 'WP' (White promotes: terminal), 'BP' (Black promotes: terminal), and the flag
# 'check' = side to move is in check.

def in_check(B, st):
    wk, bk, wp, bp, side = st
    if side == 0:
        return bp >= 0 and wk in B.batt[bp]
    return wp >= 0 and bk in B.watt[wp]


def legal_state(B, st):
    wk, bk, wp, bp, side = st
    if wk == bk or B.adj[wk][bk]:
        return False
    for p in (wp, bp):
        if p >= 0 and (p == wk or p == bk):
            return False
    if wp >= 0 and wp == bp:
        return False
    if wp >= 0 and not (1 <= wp // 8 <= 6):
        return False
    if bp >= 0 and not (1 <= bp // 8 <= 6):
        return False
    # the side not to move must not be in check
    if side == 0 and wp >= 0 and bk in B.watt[wp]:
        return False
    if side == 1 and bp >= 0 and wk in B.batt[bp]:
        return False
    return True


def gen(B, st):
    wk, bk, wp, bp, side = st
    out = []
    if side == 0:
        own_k, en_k, own_p, en_p = wk, bk, wp, bp
    else:
        own_k, en_k, own_p, en_p = bk, wk, bp, wp
    # attack test for the mover's king after the move, given the enemy pawn that remains
    def king_safe(ksq, enemy_pawn):
        if B.adj[ksq][en_k] or ksq == en_k:
            return False
        if enemy_pawn >= 0:
            att = B.batt[enemy_pawn] if side == 0 else B.watt[enemy_pawn]
            if ksq in att:
                return False
        return True

    # king moves
    for n in B.nb[own_k]:
        if n == own_p:
            continue
        if n == en_p:
            # capture of the enemy pawn
            if not king_safe(n, -1):
                continue
            new = (n, bk, wp, -1, 1) if side == 0 else (wk, n, -1, bp, 0)
            out.append((name(own_k) + name(n) + 'x', 'n', new))
        else:
            if not king_safe(n, en_p):
                continue
            new = (n, bk, wp, bp, 1) if side == 0 else (wk, n, wp, bp, 0)
            out.append((name(own_k) + name(n), 'n', new))
    # pawn moves
    if own_p >= 0:
        f, r = own_p % 8, own_p // 8
        dr = 1 if side == 0 else -1
        last = 7 if side == 0 else 0
        start = 1 if side == 0 else 6
        occupied = {wk, bk, wp, bp}
        # single step / promotion
        q = B.at(f, r + dr)
        steps = []
        if q is not None and q not in occupied:
            steps.append(q)
        for q in steps:
            if q // 8 == last:
                # promotion: own king must be safe afterwards (own pawn is gone)
                if king_safe(own_k, en_p):
                    out.append((name(own_p) + name(q) + '=', 'WP' if side == 0 else 'BP', None))
            else:
                if king_safe(own_k, en_p):
                    new = (wk, bk, q, bp, 1) if side == 0 else (wk, bk, wp, q, 0)
                    out.append((name(own_p) + name(q), 'n', new))
        # double step
        if r == start and steps:
            q2 = B.at(f, r + 2 * dr)
            if q2 is not None and q2 not in occupied:
                if king_safe(own_k, en_p):
                    # e.p. right would arise if an enemy pawn stands beside the landing square
                    if en_p >= 0 and en_p // 8 == q2 // 8 and abs(B.relx(en_p, q2 % 8)) == 1:
                        raise RuntimeError('en passant not implemented')
                    new = (wk, bk, q2, bp, 1) if side == 0 else (wk, bk, wp, q2, 0)
                    out.append((name(own_p) + name(q2), 'n', new))
        # captures
        att = B.watt[own_p] if side == 0 else B.batt[own_p]
        for t in att:
            if t == en_p:
                # capture of the enemy pawn by the pawn (never the king)
                if t // 8 == last:
                    if king_safe(own_k, -1):
                        out.append((name(own_p) + name(t) + 'x=', 'WP' if side == 0 else 'BP', None))
                else:
                    if king_safe(own_k, -1):
                        new = (wk, bk, t, -1, 1) if side == 0 else (wk, bk, -1, t, 0)
                        out.append((name(own_p) + name(t) + 'x', 'n', new))
    return out


def parse(B, line):
    t = line.split()
    assert len(t) >= 3
    wk = bk = wp = bp = -1
    for x in t[:-2]:
        s = sqn(x[1:])
        c = x[0]
        if c == 'K':
            wk = s
        elif c == 'k':
            bk = s
        elif c == 'P':
            wp = s
        elif c == 'p':
            bp = s
        else:
            raise ValueError(x)
    assert t[-1] == '-'
    return (wk, bk, wp, bp, 0 if t[-2] == 'w' else 1)


def fmt(st):
    wk, bk, wp, bp, side = st
    parts = ['K' + name(wk)]
    if wp >= 0:
        parts.append('P' + name(wp))
    parts.append('k' + name(bk))
    if bp >= 0:
        parts.append('p' + name(bp))
    return ' '.join(parts) + (' w -' if side == 0 else ' b -')


# --------------------------------------------------------------------------------------------------
# solver over the graph reachable from a set of roots.  models: 'P', 'EPW', 'EPB'.

def build(B, roots):
    ids = {}
    states = []
    succ = []      # per state: list of successor ids
    term = []      # per state: list of terminal outcomes 'W'/'B' of promotion moves
    chk = []
    stack = []
    for r in roots:
        if r not in ids:
            ids[r] = len(states)
            states.append(r)
            stack.append(r)
    done = 0
    i = 0
    while i < len(states):
        st = states[i]
        mv = gen(B, st)
        s_list = []
        t_list = []
        for lab, kind, new in mv:
            if kind == 'n':
                if new not in ids:
                    ids[new] = len(states)
                    states.append(new)
                s_list.append(ids[new])
            else:
                t_list.append('W' if kind == 'WP' else 'B')
        succ.append(s_list)
        term.append(t_list)
        chk.append(in_check(B, st))
        i += 1
    return ids, states, succ, term, chk


def solve(states, succ, term, chk, model):
    """returns (WW, BW) boolean lists: White wins / Black wins (least fixed points)."""
    n = len(states)
    pred = [[] for _ in range(n)]
    for i, sl in enumerate(succ):
        for j in sl:
            pred[j].append(i)

    def promo_owner(t):
        if model == 'P':
            return t
        return 'W' if model == 'EPW' else 'B'

    res = {}
    for c in ('W', 'B'):
        mover_is_c = [(st[4] == 0) == (c == 'W') for st in states]
        win = [False] * n
        cnt = [0] * n          # for states where the mover is not c: moves not yet known to win for c
        dead = [False] * n
        queue = []
        for i in range(n):
            tl = [promo_owner(t) for t in term[i]]
            nm = len(succ[i]) + len(tl)
            if mover_is_c[i]:
                if any(t == c for t in tl):
                    win[i] = True
                    queue.append(i)
            else:
                if nm == 0:
                    if chk[i]:           # mate of the mover: c wins
                        win[i] = True
                        queue.append(i)
                    continue
                if any(t != c for t in tl):
                    dead[i] = True
                cnt[i] = len(succ[i])    # promotions by c already count as won moves
        for i in range(n):
            if (not mover_is_c[i]) and not win[i] and not dead[i] and (len(succ[i]) + len(term[i])) > 0 and cnt[i] == 0:
                win[i] = True
                queue.append(i)
        while queue:
            j = queue.pop()
            for i in pred[j]:
                if win[i]:
                    continue
                if mover_is_c[i]:
                    win[i] = True
                    queue.append(i)
                else:
                    if dead[i]:
                        continue
                    # j counted once per move to j (a state may have two moves to the same successor? no)
                    cnt[i] -= 1
                    if cnt[i] == 0:
                        win[i] = True
                        queue.append(i)
        res[c] = win
    return res['W'], res['B']


def value(WW, BW, i):
    assert not (WW[i] and BW[i])
    return 'W' if WW[i] else ('L' if BW[i] else 'D')
