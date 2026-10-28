#!/usr/bin/env python3
"""pyp.py (K16): an independent pure-Python solver for the P model with real kings (first promotion wins),
own move generator (no code shared with kpsolve.c / kp_p.c / chk.c / cylcgt), per position.
Rules (SPEC.md + P model): kings and pawns only; promotion wins at once for the promoter; checkmate = loss of the
side to move, stalemate = draw, infinite play = draw (least fixed point).  e.p. as in SPEC.
usage: pyp.py BOARD 'position line' ...   (prints 'pos | W/D/L' from White's point of view)
Also: strategy_check(board, pos, beta, p) -> failure kind of the strategy 'beta pushes p every move'.
"""
import sys
from collections import deque


class Board:
    def __init__(self, spec):
        kind, dims = spec.split(":")
        self.W, self.H = map(int, dims.split("x"))
        self.wrap = kind == "cyl"

    def sq(self, f, r):
        return r * self.W + f

    def fr(self, s):
        return s % self.W, s // self.W

    def nf(self, f, d):
        g = f + d
        if self.wrap:
            return g % self.W
        return g if 0 <= g < self.W else None

    def kdist(self, a, b):
        fa, ra = self.fr(a)
        fb, rb = self.fr(b)
        df = abs(fa - fb)
        if self.wrap:
            df = min(df, self.W - df)
        return max(df, abs(ra - rb))

    def king_steps(self, s):
        f, r = self.fr(s)
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                g = self.nf(f, df)
                rr = r + dr
                if g is None or rr < 0 or rr >= self.H:
                    continue
                t = rr * self.W + g
                if t != s and t not in out:
                    out.append(t)
        return out

    def pawn_att(self, colour, s):
        """squares attacked by a pawn of `colour` (0 white, 1 black) on s"""
        f, r = self.fr(s)
        rr = r + (1 if colour == 0 else -1)
        if rr < 0 or rr >= self.H:
            return []
        out = []
        for d in (-1, 1):
            g = self.nf(f, d)
            if g is not None:
                out.append(rr * self.W + g)
        return out


def parse(B, line):
    toks = line.split()
    wk = bk = None
    wp = set()
    bp = set()
    stm = None
    ep = -1
    i = 0
    while i < len(toks):
        t = toks[i]
        if stm is None and t in ("w", "b"):
            stm = 0 if t == "w" else 1
            ep_tok = toks[i + 1]
            if ep_tok != "-":
                ep = B.sq(ord(ep_tok[0]) - 97, int(ep_tok[1:]) - 1)
            break
        s = B.sq(ord(t[1]) - 97, int(t[2:]) - 1)
        if t[0] == "K":
            wk = s
        elif t[0] == "k":
            bk = s
        elif t[0] == "P":
            wp.add(s)
        elif t[0] == "p":
            bp.add(s)
        i += 1
    return (wk, bk, frozenset(wp), frozenset(bp), stm, ep)


def attacked_by_pawns(B, colour, pawns, target):
    for s in pawns:
        if target in B.pawn_att(colour, s):
            return True
    return False


def in_check(B, st, colour):
    wk, bk, wp, bp, stm, ep = st
    if colour == 0:
        return attacked_by_pawns(B, 1, bp, wk)
    return attacked_by_pawns(B, 0, wp, bk)


def moves(B, st):
    """list of (kind, next_state) ; kind 'promo' = immediate win for mover; else 'move'."""
    wk, bk, wp, bp, stm, ep = st
    W, H = B.W, B.H
    us = stm
    res = []
    own_k, opp_k = (wk, bk) if us == 0 else (bk, wk)
    own_p, opp_p = (wp, bp) if us == 0 else (bp, wp)

    def make(nk, nown, nopp, nep):
        if us == 0:
            return (nk, bk, frozenset(nown), frozenset(nopp), 1, nep)
        return (wk, nk, frozenset(nopp), frozenset(nown), 0, nep)

    def legal(ns):
        return not in_check(B, ns, us)

    # king moves
    for t in B.king_steps(own_k):
        if t in own_p or t == opp_k or B.kdist(t, opp_k) <= 1:
            continue
        nopp = set(opp_p)
        nopp.discard(t)
        ns = make(t, own_p, nopp, -1)
        if legal(ns):
            res.append(("move", ns))
    # pawns
    d = 1 if us == 0 else -1
    start = 1 if us == 0 else H - 2
    last = H - 1 if us == 0 else 0
    occ = set(wp) | set(bp) | {wk, bk}
    for s in sorted(own_p):
        f, r = B.fr(s)
        t = s + d * W
        if t not in occ:
            nown = set(own_p)
            nown.discard(s)
            if t // W == last:
                nown.add(t)
                ns = make(own_k, nown, opp_p, -1)
                if legal(ns):
                    res.append(("promo", ns))
            else:
                nown.add(t)
                ns = make(own_k, nown, opp_p, -1)
                if legal(ns):
                    res.append(("move", ns))
                t2 = t + d * W
                if r == start and t2 not in occ and t2 // W != last:
                    nown2 = set(own_p)
                    nown2.discard(s)
                    nown2.add(t2)
                    ns2 = make(own_k, nown2, opp_p, -1)
                    if legal(ns2):
                        # genuine e.p. right only if an enemy pawn attacks the skipped square t
                        capt = any(t in B.pawn_att(1 - us, q) for q in opp_p)
                        ns2 = make(own_k, nown2, opp_p, t if capt else -1)
                        res.append(("move", ns2))
        for c in B.pawn_att(us, s):
            victim = None
            if c in opp_p:
                victim = c
            elif c == ep:
                victim = c - d * W
            if victim is None:
                continue
            nown = set(own_p)
            nown.discard(s)
            nopp = set(opp_p)
            nopp.discard(victim)
            if c // W == last:
                nown.add(c)
                ns = make(own_k, nown, nopp, -1)
                if legal(ns):
                    res.append(("promo", ns))
            else:
                nown.add(c)
                ns = make(own_k, nown, nopp, -1)
                if legal(ns):
                    res.append(("move", ns))
    return res


def solve(B, root, limit=3_000_000):
    """value from White's point of view: 'W', 'D', 'L' (P model)."""
    # states: ('S', st); results from side-to-move's POV: 1 win, -1 loss, 0 draw
    idx = {root: 0}
    order = [root]
    succ = []
    term = []  # None, or 'W' (stm has an immediate win), or 'M' mate, 'S' stalemate
    q = deque([root])
    i = 0
    while i < len(order):
        st = order[i]
        mv = moves(B, st)
        has_promo = any(k == "promo" for k, _ in mv)
        if has_promo:
            succ.append([])
            term.append("win")
        elif not mv:
            succ.append([])
            term.append("mate" if in_check(B, st, st[4]) else "stale")
        else:
            lst = []
            for k, ns in mv:
                if ns not in idx:
                    idx[ns] = len(order)
                    order.append(ns)
                lst.append(idx[ns])
            succ.append(lst)
            term.append(None)
        i += 1
        if len(order) > limit:
            raise RuntimeError("too many states")
    n = len(order)
    val = [0] * n  # 0 unknown/draw, 1 win, -1 loss
    cnt = [0] * n
    pred = [[] for _ in range(n)]
    queue = deque()
    for u in range(n):
        if term[u] == "win":
            val[u] = 1
            queue.append(u)
        elif term[u] == "mate":
            val[u] = -1
            queue.append(u)
        elif term[u] == "stale":
            val[u] = 0
        else:
            cnt[u] = len(succ[u])
            for v in succ[u]:
                pred[v].append(u)
    done = [False] * n
    while queue:
        v = queue.popleft()
        if done[v]:
            continue
        done[v] = True
        for u in pred[v]:
            if val[u] != 0 or term[u] is not None:
                continue
            if val[v] == -1:
                val[u] = 1
                queue.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0:
                    val[u] = -1
                    queue.append(u)
    v = val[0]
    if v == 0:
        return "D"
    white_wins = (v == 1) == (root[4] == 0)
    return "W" if white_wins else "L"


def solve_line(spec, line):
    B = Board(spec)
    return solve(B, parse(B, line))


if __name__ == "__main__":
    spec = sys.argv[1]
    B = Board(spec)
    for line in sys.argv[2:]:
        print(line, "|", solve(B, parse(B, line)))
