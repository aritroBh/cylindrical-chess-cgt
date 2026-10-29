#!/usr/bin/env python3
"""mini.py BOARD "<group>" : referee-2 third, own solver of the P model for a BARE group (kings + pawns): exact loss depth of the side
to move, in plies, by depth-bounded search (a promotion ends the game and wins for the promoter; stalemate draw; mate loss; e.p. on).
Written from SPEC.md and the P-model sentence only; shares nothing with kpsolve/ref3/grp.  Prints: loss depth (plies) for w and b, and for each
legal move m of the loser the exact depth d(m) of the opponent's win after m and T_P(m) = (d+1)/2."""
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)
board = sys.argv[1]; Wd, Hd = [int(x) for x in board.split(':')[1].split('x')]; cyl = board.startswith('cyl')
def sq(tok): return ((ord(tok[1]) - 97), int(tok[2:]) - 1)
def fw(f, df):
    f += df
    if cyl: return f % Wd
    return f if 0 <= f < Wd else None
def parse(s):
    wk = bk = None; wp = []; bp = []
    for t in s.split():
        x = sq(t)
        if t[0] == 'K': wk = x
        elif t[0] == 'k': bk = x
        elif t[0] == 'P': wp.append(x)
        elif t[0] == 'p': bp.append(x)
    return wk, bk, frozenset(wp), frozenset(bp)
def adjk(a, b):
    df = abs(a[0] - b[0])
    if cyl: df = min(df, Wd - df)
    return max(df, abs(a[1] - b[1])) <= 1
def pawn_att(c, pawns, s):  # is square s attacked by a pawn of colour c (0 white) in set pawns
    d = 1 if c == 0 else -1
    for df in (-1, 1):
        f = fw(s[0], -df)
        if f is not None and (f, s[1] - d) in pawns: return True
    return False
def attacked(c, ks, pawns, s):  # by pawns of colour c or by that colour's king ks
    return pawn_att(c, pawns, s) or adjk(ks, s)
def moves(stm, wk, bk, wp, bp, ep):
    """yield ('promo',) or (wk,bk,wp,bp,ep') legal moves of stm"""
    out = []
    own_k, en_k = (wk, bk) if stm == 0 else (bk, wk)
    own_p, en_p = (wp, bp) if stm == 0 else (bp, wp)
    d = 1 if stm == 0 else -1
    last = Hd - 1 if stm == 0 else 0
    second = 1 if stm == 0 else Hd - 2
    def legal(nk, nown, nen):  # own king nk not attacked by enemy pawns nor adjacent to enemy king
        return not pawn_att(1 - stm, nen, nk) and not adjk(nk, en_k)
    # king moves
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0: continue
            f = fw(own_k[0], df); r = own_k[1] + dr
            if f is None or not 0 <= r < Hd: continue
            t = (f, r)
            if t in own_p: continue
            nen = en_p - {t}
            if not legal(t, own_p, nen): continue
            out.append((t, own_p, nen, None))
    # pawn moves
    for p in own_p:
        f, r = p
        t = (f, r + d)
        if t not in own_p and t not in en_p and t != own_k and t != en_k:
            if r + d == last:
                if legal(own_k, own_p, en_p): out.append('promo')
            else:
                np_ = (own_p - {p}) | {t}
                if legal(own_k, np_, en_p): out.append((own_k, np_, en_p, None))
                if r == second:
                    t2 = (f, r + 2 * d)
                    if t2 not in own_p and t2 not in en_p and t2 != en_k and t2 != own_k:
                        np2 = (own_p - {p}) | {t2}
                        if legal(own_k, np2, en_p): out.append((own_k, np2, en_p, (f, r + d)))
        for df in (-1, 1):
            g = fw(f, df)
            if g is None: continue
            t = (g, r + d)
            if t in en_p:
                if r + d == last:
                    if legal(own_k, own_p, en_p - {t}): out.append('promo')  # capture-promotion
                else:
                    np_ = (own_p - {p}) | {t}; nen = en_p - {t}
                    if legal(own_k, np_, nen): out.append((own_k, np_, nen, None))
            elif ep is not None and t == ep:
                cap = (g, r)  # the double-stepped enemy pawn stands beside p
                if cap in en_p:
                    np_ = (own_p - {p}) | {t}; nen = en_p - {cap}
                    if legal(own_k, np_, nen): out.append((own_k, np_, nen, None))
    res = []
    for m in out:
        if m == 'promo': res.append('promo'); continue
        nk, nown, nen, nep = m
        if stm == 0: res.append((1, nk, bk, nown, nen, nep))
        else: res.append((0, wk, nk, nen, nown, nep))
    return res
def incheck(stm, wk, bk, wp, bp):
    return pawn_att(1 - stm, bp if stm == 0 else wp, wk if stm == 0 else bk)
@lru_cache(maxsize=None)
def lost_d(stm, wk, bk, wp, bp, ep):
    """exact loss depth (plies, counting the mover's own move) of the side to move, or None if it does not lose / draw. computed by increasing bound"""
    for n in range(2, 60, 2):
        if lost(stm, wk, bk, wp, bp, ep, n): return n
    return None
@lru_cache(maxsize=None)
def win(stm, wk, bk, wp, bp, ep, n):  # side to move wins within n plies (n odd >=1)
    if n < 1: return False
    for m in moves(stm, wk, bk, wp, bp, ep):
        if m == 'promo': return True
        if n >= 3 and lost(*m, n - 1): return True
    return False
@lru_cache(maxsize=None)
def lost(stm, wk, bk, wp, bp, ep, n):  # side to move is lost within n plies (n even >=2)
    if n < 2: return False
    ms = moves(stm, wk, bk, wp, bp, ep)
    if not ms: return incheck(stm, wk, bk, wp, bp)
    for m in ms:
        if m == 'promo': return False
        if not win(*m, n - 1): return False
    return True
if __name__ == '__main__':
    g = sys.argv[2]
    wk, bk, wp, bp = parse(g)
    for stm, nm in ((0, 'w'), (1, 'b')):
        # bounded search up to 40 plies
        d = None
        for n in range(2, 41, 2):
            if lost(stm, wk, bk, wp, bp, None, n): d = n; break
        line = '%s to move: loss depth %s plies (T_P=%s)' % (nm, d, (d // 2) if d else None)
        # per move
        if d:
            per = []
            for m in moves(stm, wk, bk, wp, bp, None):
                if m == 'promo': per.append('promo'); continue
                dd = None
                for n in range(1, 40, 2):
                    if win(*m, n): dd = n; break
                per.append(dd)
            line += ' | per-move d(m): ' + ','.join(str(x) for x in per)
        print(g, '|', line, flush=True)
