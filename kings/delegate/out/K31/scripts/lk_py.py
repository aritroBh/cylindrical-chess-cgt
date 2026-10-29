#!/usr/bin/env python3
# K31: small independent Python implementation of LK (single or double blocked pairs, free board) with the integer
# reservoir context -n .. n, for lines (task 4).  Written from the LK definition in K20's summary.json.
import sys, itertools
from collections import deque
class LK:
    def __init__(self, W, H, cyl, pairs):
        self.W, self.H, self.cyl = W, H, cyl
        self.pw = [(f, r) for f, r in pairs]            # white pawn squares (file, rank 1-based)
        self.pb = [(f, r + 1) for f, r in pairs]
        self.full = frozenset([('P',) + p for p in self.pw] + [('p',) + p for p in self.pb])
    def fstep(self, f, d):
        g = f + d
        if self.cyl: return g % self.W
        return g if 0 <= g < self.W else None
    def adj(self, a, b):
        df = abs(a[0] - b[0])
        if self.cyl: df = min(df, self.W - df)
        return df <= 1 and abs(a[1] - b[1]) <= 1
    def attacked(self, S, sq, by):   # attacked by pawn of colour by ('P' attacks rank+1)
        for (c, f, r) in S:
            if c != by: continue
            tr = r + 1 if c == 'P' else r - 1
            if tr != sq[1]: continue
            for d in (-1, 1):
                if self.fstep(f, d) == sq[0]: return True
        return False
    def passed(self, S, p):
        c, f, r = p
        for (c2, f2, r2) in S:
            if c2 == c: continue
            df = abs(f - f2)
            if self.cyl: df = min(df, self.W - df)
            if df > 1: continue
            if c == 'P' and r2 > r: return False
            if c == 'p' and r2 < r: return False
        return True
    def legal(self, S, wk, bk):
        if wk == bk or self.adj(wk, bk): return False
        occ = {(f, r) for (c, f, r) in S}
        if wk in occ or bk in occ: return False
        if self.attacked(S, wk, 'p') or self.attacked(S, bk, 'P'): return False
        return True
    def moves(self, S, wk, bk, side):   # side 0 White, 1 Black; returns list of ('T',+/-) or ('N', S2, wk2, bk2)
        ks, os_ = (wk, bk) if side == 0 else (bk, wk)
        col = 'P' if side == 0 else 'p'; ecol = 'p' if side == 0 else 'P'
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if not df and not dr: continue
                nf = self.fstep(ks[0], df); nr = ks[1] + dr
                if nf is None or nr < 1 or nr > self.H: continue
                t = (nf, nr)
                if any(c == col and (f, r) == t for (c, f, r) in S): continue
                if t == os_ or self.adj(t, os_): continue
                S2 = S; cap = None
                for q in S:
                    if q[0] == ecol and (q[1], q[2]) == t: cap = q
                if cap: S2 = S - {cap}
                if self.attacked(S2, t, ecol): continue
                if cap:
                    wp = any(q[0] == 'P' and self.passed(S2, q) for q in S2)
                    bp = any(q[0] == 'p' and self.passed(S2, q) for q in S2)
                    if wp and not bp: out.append(('T', 1)); continue
                    if bp and not wp: out.append(('T', -1)); continue
                    if wp and bp: out.append(('T', 1 if side == 0 else -1)); continue
                out.append(('N', S2, t, bk) if side == 0 else ('N', S2, wk, t))
        return out
    def nodes(self):
        sq = [(f, r) for f in range(self.W) for r in range(1, self.H + 1)]
        res = []
        for wk in sq:
            for bk in sq:
                if self.legal(self.full, wk, bk): res.append((self.full, wk, bk))
        return res
def solve(lk, N):
    """Outcomes of x + c for the integer reservoir c in -N..N.  state = (node, c, side). returns dict state->'W','L','D' (White view) + distance."""
    nodes = lk.nodes()
    # explore reachable states of LK from all nodes (S stays full unless non-terminal capture)
    opts = {}
    stack = list(nodes); seen = set(nodes)
    while stack:
        x = stack.pop()
        S, wk, bk = x
        o = [lk.moves(S, wk, bk, s) for s in (0, 1)]
        opts[x] = o
        for s in (0, 1):
            for m in o[s]:
                if m[0] == 'N':
                    y = (m[1], m[2], m[3])
                    if y not in seen: seen.add(y); stack.append(y)
    # states (x, c, s): c>0 White spare moves (L moves), c<0 Black spare
    def succ(st):
        x, c, s = st
        res = []
        for m in opts[x][s]:
            res.append(('T', m[1]) if m[0] == 'T' else ('S', ((m[1], m[2], m[3]), c, 1 - s)))
        if s == 0 and c > 0: res.append(('S', (x, c - 1, 1)))
        if s == 1 and c < 0: res.append(('S', (x, c + 1, 0)))
        return res
    states = [(x, c, s) for x in opts for c in range(-N, N + 1) for s in (0, 1)]
    S_ = {st: succ(st) for st in states}
    rev = {st: [] for st in states}
    for st, ss in S_.items():
        for k, v in ss:
            if k == 'S': rev[v].append(st)
    win = {}   # (player) -> dict state -> distance in plies
    for player in (0, 1):
        winT = 1 if player == 0 else -1
        dist = {}; cnt = {}; q = deque()
        for st in states:
            s = st[2]; ss = S_[st]
            if s == player:
                if any(k == 'T' and v == winT for k, v in ss): dist[st] = 1; q.append(st)
            else:
                bad = any(k == 'T' and v == -winT for k, v in ss)
                c = sum(1 for k, v in ss if k == 'S')
                cnt[st] = 10**9 if bad else c
                if not bad and c == 0: dist[st] = 0; q.append(st)   # no move: loses
        while q:
            st = q.popleft(); d = dist[st]
            for p in rev[st]:
                if p in dist: continue
                if p[2] == player: dist[p] = d + 1; q.append(p)
                else:
                    cnt[p] -= 1
                    if cnt[p] == 0: dist[p] = d + 1; q.append(p)
        win[player] = dist
    return opts, S_, win
def parse(lk, t):
    wk = bk = None
    for tok in t.split():
        f = ord(tok[1]) - 97; r = int(tok[2:])
        if tok[0] == 'K': wk = (f, r)
        elif tok[0] == 'k': bk = (f, r)
    return (lk.full, wk, bk)
def name(sq): return chr(97 + sq[0]) + str(sq[1])
