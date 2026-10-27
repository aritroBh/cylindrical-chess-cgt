#!/usr/bin/env python3
"""Referee's own solver (written from kings/SPEC.md, not from K24's mine.c nor kpsolve.c) for king + pawn positions in
three promotion models:
  p  : first promotion ends the game, win for the promoter
  ww : every promotion (either side) is a WHITE win
  bb : every promotion (either side) is a BLACK win
Checkmate wins, stalemate and infinite play draw.  Pieces: two kings and pawns only (no officers ever exist).
Position = (stm, wk, bk, wpawns(tuple sorted), bpawns(tuple sorted), ep) ; ep = target square or -1 (normalised:
kept only if an enemy pawn can capture on it).
Usage: psolve.py BOARD(cyl:8x8) MODEL [--moves] < positions     (positions in SPEC format)
"""
import sys
from collections import deque

def setup(board):
    global W, H, WRAP
    kind, dims = board.split(":")
    W, H = map(int, dims.split("x"))
    WRAP = (kind == "cyl")
    KN.clear()

def sq(f, r):
    return r * W + f

def nbr(s, df, dr):
    f, r = s % W + df, s // W + dr
    if r < 0 or r >= H:
        return -1
    if WRAP:
        f %= W
    elif f < 0 or f >= W:
        return -1
    return r * W + f

KN = {}
def king_nb(s):
    if s not in KN:
        KN[s] = tuple(x for x in (nbr(s, a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)) if x >= 0)
    return KN[s]

def adj(a, b):
    return a == b or b in king_nb(a)

def pawn_att(c, s):
    """squares attacked by a pawn of colour c standing on s"""
    d = 1 if c == 0 else -1
    out = []
    for df in (-1, 1):
        t = nbr(s, df, d)
        if t >= 0:
            out.append(t)
    return out

def king_attacked(pos, c):
    """is the king of colour c attacked by an enemy pawn?"""
    ks = pos[1 + c]
    for p in pos[3 + (1 - c)]:
        if ks in pawn_att(1 - c, p):
            return True
    return False

def ep_usable(c_mover, target, pawns_of_mover):
    """can a pawn of colour c_mover capture e.p. onto target?"""
    d = 1 if c_mover == 0 else -1
    for df in (-1, 1):
        s = nbr(target, df, -d)
        if s >= 0 and s in pawns_of_mover:
            return True
    return False

def moves(pos):
    """list of (kind, newpos|None, promoter) ; kind 'm' normal move to newpos, 'p' promotion (terminal)"""
    stm, wk, bk, wp, bp, ep = pos
    c = stm
    out = []
    kings = [wk, bk]
    pawns = [list(wp), list(bp)]
    own_p, en_p = pawns[c], pawns[1 - c]
    allp = set(wp) | set(bp)
    def mk(newk, newown, newen, newep):
        k2 = kings[:]
        k2[c] = newk
        if c == 0:
            return (1, k2[0], k2[1], tuple(sorted(newown)), tuple(sorted(newen)), newep)
        return (0, k2[0], k2[1], tuple(sorted(newen)), tuple(sorted(newown)), newep)
    def legal_after(newpos):
        if adj(newpos[1], newpos[2]):
            return False
        # side that moved is c; newpos[0] = opponent to move
        return not king_attacked(newpos, c)
    # king moves
    for t in king_nb(kings[c]):
        if t in own_p:
            continue
        newen = [x for x in en_p if x != t]
        np_ = mk(t, own_p, newen, -1)
        if legal_after(np_):
            out.append(('m', np_, c))
    # pawn moves
    d = 1 if c == 0 else -1
    last = H - 1 if c == 0 else 0
    start = 1 if c == 0 else H - 2
    for p in own_p:
        rest = [x for x in own_p if x != p]
        # pushes
        t = nbr(p, 0, d)
        if t >= 0 and t not in allp and t != wk and t != bk:
            if t // W == last:
                np_ = mk(kings[c], rest + [t], en_p, -1)  # king-safety check does not depend on the new piece
                if legal_after(np_):
                    out.append(('p', None, c))
            else:
                np_ = mk(kings[c], rest + [t], en_p, -1)
                if legal_after(np_):
                    t2 = nbr(t, 0, d)
                    out.append(('m', np_, c))
                if p // W == start:
                    t2 = nbr(t, 0, d)
                    if t2 >= 0 and t2 not in allp and t2 != wk and t2 != bk:
                        e = t if ep_usable(1 - c, t, en_p) else -1
                        np2 = mk(kings[c], rest + [t2], en_p, e)
                        if legal_after(np2):
                            out.append(('m', np2, c))
        # captures
        for df in (-1, 1):
            t = nbr(p, df, d)
            if t < 0:
                continue
            if t in en_p:
                newen = [x for x in en_p if x != t]
                if t // W == last:
                    np_ = mk(kings[c], rest, newen, -1)
                    if legal_after(np_):
                        out.append(('p', None, c))
                else:
                    np_ = mk(kings[c], rest + [t], newen, -1)
                    if legal_after(np_):
                        out.append(('m', np_, c))
            elif t == ep:
                victim = nbr(t, 0, -d)
                if victim in en_p:
                    newen = [x for x in en_p if x != victim]
                    np_ = mk(kings[c], rest + [t], newen, -1)
                    if legal_after(np_):
                        out.append(('m', np_, c))
    return out

def in_check(pos, c):
    return king_attacked(pos, c)

def legal_position(pos):
    stm, wk, bk, wp, bp, ep = pos
    allsq = [wk, bk] + list(wp) + list(bp)
    if len(set(allsq)) != len(allsq):
        return False
    if adj(wk, bk):
        return False
    for p in wp:
        if p // W == 0 or p // W == H - 1:
            return False
    for p in bp:
        if p // W == 0 or p // W == H - 1:
            return False
    if king_attacked(pos, 1 - stm):
        return False
    return True

def solve(starts, model):
    idx = {}
    nodes = []
    succ = []      # per node: list of child indices
    tw = []        # per node: has a terminal winning move for mover
    tl = []        # per node: number of terminal losing moves
    queue = deque()
    def get(pos):
        if pos in idx:
            return idx[pos]
        i = len(nodes)
        idx[pos] = i
        nodes.append(pos)
        succ.append(None)
        tw.append(False)
        tl.append(0)
        queue.append(i)
        return i
    for s in starts:
        get(s)
    while queue:
        i = queue.popleft()
        pos = nodes[i]
        mv = moves(pos)
        ch = []
        for kind, np_, c in mv:
            if kind == 'p':
                if model == 'p':
                    winner = c
                elif model == 'ww':
                    winner = 0
                else:
                    winner = 1
                if winner == pos[0]:
                    tw[i] = True
                else:
                    tl[i] += 1
            else:
                ch.append(get(np_))
        succ[i] = (len(mv), ch)
    n = len(nodes)
    val = [0] * n   # 0 draw/unknown, 1 win for mover, -1 loss for mover
    preds = [[] for _ in range(n)]
    cnt = [0] * n
    q = deque()
    for i in range(n):
        nm, ch = succ[i]
        for j in ch:
            preds[j].append(i)
        cnt[i] = len(ch)
        if nm == 0:
            if in_check(nodes[i], nodes[i][0]):
                val[i] = -1
                q.append(i)
        elif tw[i]:
            val[i] = 1
            q.append(i)
        elif cnt[i] == 0:
            val[i] = -1
            q.append(i)
    while q:
        j = q.popleft()
        for i in preds[j]:
            if val[i] != 0:
                continue
            if val[j] == -1:
                val[i] = 1
                q.append(i)
            else:
                cnt[i] -= 1
                if cnt[i] == 0:
                    val[i] = -1
                    q.append(i)
    return idx, nodes, val, succ

def parse(line):
    toks = line.split()
    eps = toks[-1]
    stm = 0 if toks[-2] == 'w' else 1
    wk = bk = -1
    wp, bp = [], []
    for t in toks[:-2]:
        f = ord(t[1]) - ord('a')
        r = int(t[2:]) - 1
        s = sq(f, r)
        ch = t[0]
        if ch == 'K': wk = s
        elif ch == 'k': bk = s
        elif ch == 'P': wp.append(s)
        elif ch == 'p': bp.append(s)
    ep = -1
    if eps != '-':
        ep = sq(ord(eps[0]) - ord('a'), int(eps[1:]) - 1)
    return (stm, wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), ep)

def name(s):
    return "abcdefgh"[s % W] + str(s // W + 1)

def wpov(v, stm):
    # value from White's view
    if v == 0: return 'D'
    return 'W' if (v == 1) == (stm == 0) else 'L'

if __name__ == '__main__':
    setup(sys.argv[1])
    model = sys.argv[2]
    show = '--moves' in sys.argv
    lines = [l.strip() for l in sys.stdin if l.strip() and not l.startswith('#')]
    starts = []
    for l in lines:
        p = parse(l)
        starts.append(p)
    ok = [p for p in starts if legal_position(p)]
    idx, nodes, val, succ = solve(ok, model)
    sys.stderr.write(f"[psolve {sys.argv[1]} {model}: {len(nodes)} positions]\n")
    for l, p in zip(lines, starts):
        if not legal_position(p):
            print(l, '| X'); continue
        i = idx[p]
        r = wpov(val[i], p[0])
        s = f"{l} | {r}"
        if show:
            # value after each move
            parts = []
            for kind, np_, c in moves(p):
                if kind == 'p':
                    winner = c if model == 'p' else (0 if model == 'ww' else 1)
                    parts.append(f"promo:{'W' if winner == 0 else 'L'}")
                else:
                    parts.append(f"{name(p[1 + c])}>{name(np_[1 + c])}:{wpov(val[idx[np_]], np_[0])}" if True else "")
            s += " | " + " ".join(parts)
        print(s)
