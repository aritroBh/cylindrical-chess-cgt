#!/usr/bin/env python3
"""Referee's own implementation (written from the rules in LOOPY, not from K16 scripts).
P model: first promotion wins at once for the promoter; king: one step, not adjacent to the other king, not
attacked by a pawn, may capture a pawn; checkmate = side to move loses; stalemate = draw; infinite play = draw.
Squares are (f, r) with r = 0..H-1; White pawns move r+1, start r=1, promote at r=H-1; Black move r-1, start r=H-2, promote r=0.
"""
import sys, random, itertools
from functools import lru_cache

class B:
    def __init__(s, kind, W, H):
        s.W, s.H, s.wrap = W, H, (kind == 'cyl')
    def nb(s, sq):
        f, r = sq
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0: continue
                rr = r + dr
                if rr < 0 or rr >= s.H: continue
                ff = f + df
                if s.wrap: ff %= s.W
                elif ff < 0 or ff >= s.W: continue
                out.append((ff, rr))
        return list(dict.fromkeys(out))
    def ff(s, f, df):
        g = f + df
        if s.wrap: return g % s.W
        return g if 0 <= g < s.W else None
    def dist(s, a, b):
        df = abs(a[0] - b[0])
        if s.wrap: df = min(df, s.W - df)
        return max(df, abs(a[1] - b[1]))
    def adjfiles(s, f):
        out = []
        for df in (-1, 1):
            g = s.ff(f, df)
            if g is not None and g != f: out.append(g)
        return list(dict.fromkeys(out))

# position: (wk, bk, wp(frozenset), bp(frozenset), stm 0=w 1=b, ep square or None)
def parse(b, line):
    t = line.split()
    wk = bk = None; wp = set(); bp = set()
    for x in t[:-2]:
        f = ord(x[1]) - 97; r = int(x[2:]) - 1
        c = x[0]
        if c == 'K': wk = (f, r)
        elif c == 'k': bk = (f, r)
        elif c == 'P': wp.add((f, r))
        elif c == 'p': bp.add((f, r))
    stm = 0 if t[-2] == 'w' else 1
    ep = None if t[-1] == '-' else (ord(t[-1][0]) - 97, int(t[-1][1:]) - 1)
    return (wk, bk, frozenset(wp), frozenset(bp), stm, ep)

def fmt(pos):
    wk, bk, wp, bp, stm, ep = pos
    sq = lambda s: chr(97 + s[0]) + str(s[1] + 1)
    parts = ['K' + sq(wk), 'k' + sq(bk)] + ['P' + sq(x) for x in sorted(wp)] + ['p' + sq(x) for x in sorted(bp)]
    return ' '.join(parts) + (' w ' if stm == 0 else ' b ') + ('-' if ep is None else sq(ep))

def pawn_attacks_sq(b, color, psq):
    f, r = psq
    rr = r + (1 if color == 0 else -1)
    if rr < 0 or rr >= b.H: return []
    out = []
    for df in (-1, 1):
        g = b.ff(f, df)
        if g is not None: out.append((g, rr))
    return list(dict.fromkeys(out))

def attacked_by_pawns(b, sq, attacker_color, pawns):
    # is sq attacked by a pawn of attacker_color in pawns
    f, r = sq
    pr = r - 1 if attacker_color == 0 else r + 1  # rank where an attacker would stand
    if pr < 0 or pr >= b.H: return False
    for df in (-1, 1):
        g = b.ff(f, df)
        if g is not None and (g, pr) in pawns: return True
    return False

def in_check(b, pos, color):
    wk, bk, wp, bp, stm, ep = pos
    if color == 0: return attacked_by_pawns(b, wk, 1, bp)
    return attacked_by_pawns(b, bk, 0, wp)

def legal_pos(b, pos):
    wk, bk, wp, bp, stm, ep = pos
    if wk == bk or b.dist(wk, bk) < 2: return False
    for (f, r) in wp | bp:
        if r == 0 or r == b.H - 1: return False
    if wk in wp or wk in bp or bk in wp or bk in bp: return False
    if wp & bp: return False
    if in_check(b, pos, 1 - stm): return False
    return True

def moves(b, pos):
    """legal moves: list of (newpos, promo_flag). promo_flag True = mover wins at once."""
    wk, bk, wp, bp, stm, ep = pos
    out = []
    H = b.H
    us = stm
    own = wp if us == 0 else bp
    opp = bp if us == 0 else wp
    ksq = wk if us == 0 else bk
    oksq = bk if us == 0 else wk
    dr = 1 if us == 0 else -1
    start = 1 if us == 0 else H - 2
    last = H - 1 if us == 0 else 0
    occ = set(wp) | set(bp) | {wk, bk}
    def mk(nwk, nbk, nwp, nbp, nep):
        return (nwk, nbk, frozenset(nwp), frozenset(nbp), 1 - us, nep)
    def ok(np_):
        # mover's king must not be attacked afterwards
        return not in_check(b, np_, us)
    for p in own:
        f, r = p
        # push
        t = (f, r + dr)
        if t not in occ:
            if r + dr == last:
                np_ = mk(wk, bk, (wp - {p}) | {t} if us == 0 else wp, (bp - {p}) | {t} if us == 1 else bp, None)
                # a promoting pawn: king safety is judged with the pawn removed (officer would be on t; any officer type is
                # allowed, so promotion is available if some promotion keeps the king safe; a promoted piece cannot expose own king
                # beyond what the pawn move did: pawn leaving p). King safety only depends on pawns of opp.
                npos = mk(wk, bk, wp - {p} if us == 0 else wp, bp - {p} if us == 1 else bp, None)
                if not in_check(b, npos, us):
                    out.append((npos, True))
            else:
                nown = (own - {p}) | {t}
                nwp = nown if us == 0 else wp; nbp = nown if us == 1 else bp
                nep = None
                if r == start:
                    t2 = (f, r + 2 * dr)
                    if t2 not in occ:
                        nown2 = (own - {p}) | {t2}
                        nwp2 = nown2 if us == 0 else wp; nbp2 = nown2 if us == 1 else bp
                        # ep square recorded only if an enemy pawn could capture
                        cap = False
                        for g in b.adjfiles(f):
                            if (g, r + 2 * dr) in opp: cap = True
                        np2 = mk(wk, bk, nwp2, nbp2, t if cap else None)
                        if ok(np2): out.append((np2, False))
                np_ = mk(wk, bk, nwp, nbp, None)
                if ok(np_): out.append((np_, False))
        # captures
        for df in (-1, 1):
            g = b.ff(f, df)
            if g is None: continue
            t = (g, r + dr)
            if t in opp:
                nown = (own - {p}) | {t}
                nopp = opp - {t}
                if r + dr == last:
                    npos = mk(wk, bk, wp - {p} if us == 0 else nopp, nopp if us == 0 else bp - {p}, None)
                    # careful: build explicitly
                    if us == 0:
                        npos = mk(wk, bk, wp - {p}, nopp, None)
                    else:
                        npos = mk(wk, bk, nopp, bp - {p}, None)
                    if not in_check(b, npos, us): out.append((npos, True))
                else:
                    if us == 0: np_ = mk(wk, bk, nown, nopp, None)
                    else: np_ = mk(wk, bk, nopp, nown, None)
                    if ok(np_): out.append((np_, False))
            elif ep is not None and t == ep:
                victim = (g, r)
                if victim in opp:
                    nown = (own - {p}) | {t}
                    nopp = opp - {victim}
                    if us == 0: np_ = mk(wk, bk, nown, nopp, None)
                    else: np_ = mk(wk, bk, nopp, nown, None)
                    if ok(np_): out.append((np_, False))
    # king moves
    for t in b.nb(ksq):
        if t in own or t == oksq or b.dist(t, oksq) < 2: continue
        if us == 0:
            nbp = bp - {t}
            np_ = mk(t, bk, wp, nbp, None)
        else:
            nwp = wp - {t}
            np_ = mk(wk, t, nwp, bp, None)
        if ok(np_): out.append((np_, False))
    return out

def solve(b, root, limit=3_000_000):
    """value for the side to move at root: 'W','L','D'. Own retrograde solver."""
    idx = {}; plist = []; kids = []; winnow = []
    stack = [root]; idx[root] = 0; plist.append(root)
    i = 0
    while i < len(plist):
        pos = plist[i]
        mv = moves(b, pos)
        win = any(f for (_, f) in mv)
        ch = []
        if not win:
            for (np_, f) in mv:
                if np_ not in idx:
                    idx[np_] = len(plist); plist.append(np_)
                    if len(plist) > limit: raise RuntimeError('too big')
                ch.append(idx[np_])
        kids.append(ch); winnow.append(win)
        i += 1
    n = len(plist)
    val = [0] * n  # 0 unknown 1 win 2 loss
    cnt = [len(k) for k in kids]
    parents = [[] for _ in range(n)]
    for s, ch in enumerate(kids):
        for c in ch: parents[c].append(s)
    q = []
    for s in range(n):
        if winnow[s]:
            val[s] = 1; q.append(s)
        elif cnt[s] == 0:
            # no legal move: checkmate loses, stalemate draws
            if in_check(b, plist[s], plist[s][4]):
                val[s] = 2; q.append(s)
    while q:
        c = q.pop()
        for s in parents[c]:
            if val[s] != 0: continue
            if val[c] == 2:
                val[s] = 1; q.append(s)
            else:
                cnt[s] -= 1
                if cnt[s] == 0:
                    val[s] = 2; q.append(s)
    v = val[0]
    return {0: 'D', 1: 'W', 2: 'L'}[v]

def white_view(pos, v):
    if pos[4] == 0: return v
    return {'W': 'L', 'L': 'W', 'D': 'D'}[v]

if __name__ == '__main__':
    kind, W, H = sys.argv[1].split(':')[0], *map(int, sys.argv[1].split(':')[1].split('x'))
    b = B(kind, W, H)
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        pos = parse(b, line)
        v = white_view(pos, solve(b, pos))
        print(line, '|', v)
