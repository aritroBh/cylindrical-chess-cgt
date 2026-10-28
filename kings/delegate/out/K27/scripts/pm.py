"""pm.py -- K27's own P-model engine (third implementation, written from kings/SPEC.md only).

P model on a flat W x H board (default 7 x 6): one king and a few pawns per side, no officers ever exist
because the first promotion ends the game and is a win for the promoter.  Checkmate = loss for the side to
move, stalemate = draw, e.p. on, infinite play = draw.

A position is (wk, bk, wp, bp, ep, stm) with squares s = rank*W + file (0-based), wp/bp sorted tuples,
ep = skipped square or -1, stm = 0 White / 1 Black.

Provides: parsing/printing, legal move generation (with promotion flagged), and depth-bounded forced-win search
`win(pos, n)`  (side to move forces a first promotion or a mate within n plies), with a transposition table.
"""
import sys
from functools import lru_cache

W, H = 7, 6
N = W * H


def sq(name):
    return (int(name[1:]) - 1) * W + (ord(name[0]) - 97)


def nm(s):
    return chr(97 + s % W) + str(s // W + 1)


def parse(line):
    t = line.split()
    wk = bk = -1
    wp, bp = [], []
    for tok in t[:-2]:
        c, s = tok[0], sq(tok[1:])
        if c == 'K': wk = s
        elif c == 'k': bk = s
        elif c == 'P': wp.append(s)
        elif c == 'p': bp.append(s)
    stm = 0 if t[-2] == 'w' else 1
    ep = -1 if t[-1] == '-' else sq(t[-1])
    return (wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), ep, stm)


def show(p):
    wk, bk, wp, bp, ep, stm = p
    toks = ['K' + nm(wk)] + ['P' + nm(s) for s in wp] + ['k' + nm(bk)] + ['p' + nm(s) for s in bp]
    return ' '.join(toks) + (' b ' if stm else ' w ') + (nm(ep) if ep >= 0 else '-')


def f_(s): return s % W
def r_(s): return s // W


def mk(f, r):
    if 0 <= f < W and 0 <= r < H:
        return r * W + f
    return -1


KSTEPS = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
KN = [[mk(f_(s) + a, r_(s) + b) for a, b in KSTEPS if mk(f_(s) + a, r_(s) + b) >= 0] for s in range(N)]
KADJ = [set(x) for x in KN]


def pawn_attacks(s, white):
    """squares attacked by a pawn standing on s"""
    r = r_(s) + (1 if white else -1)
    out = []
    for df in (-1, 1):
        q = mk(f_(s) + df, r)
        if q >= 0:
            out.append(q)
    return out


def attacked_by_pawns(target, pawns, white):
    return any(target in pawn_attacks(s, white) for s in pawns)


def in_check(p, side):
    wk, bk, wp, bp, ep, stm = p
    if side == 0:
        return wk in KADJ[bk] or attacked_by_pawns(wk, bp, False)
    return bk in KADJ[wk] or attacked_by_pawns(bk, wp, True)


def legal(p):
    wk, bk, wp, bp, ep, stm = p
    if wk == bk or wk in wp or wk in bp or bk in wp or bk in bp: return False
    if set(wp) & set(bp): return False
    if wk in KADJ[bk]: return False
    for s in wp:
        if r_(s) in (0, H - 1): return False
    for s in bp:
        if r_(s) in (0, H - 1): return False
    if in_check(p, 1 - stm): return False
    return True


def moves(p):
    """list of (label, newpos or 'PROMO') for all legal moves of the side to move.
    label like 'Kb2-c3', 'b4-b5', 'b4xc5', 'b4-b5=Q' (promotion; newpos 'PROMO')"""
    wk, bk, wp, bp, ep, stm = p
    out = []
    white = stm == 0
    own_k, en_k = (wk, bk) if white else (bk, wk)
    own_p, en_p = (wp, bp) if white else (bp, wp)
    occ = set(wp) | set(bp) | {wk, bk}

    def mkpos(nok, nown, nen, nep):
        if white:
            q = (nok, en_k, tuple(sorted(nown)), tuple(sorted(nen)), nep, 1)
        else:
            q = (en_k, nok, tuple(sorted(nen)), tuple(sorted(nown)), nep, 0)
        return q

    # king moves
    for t in KN[own_k]:
        if t in own_p or t == en_k: continue
        if t in KADJ[en_k]: continue
        nen = [s for s in en_p if s != t]
        # attacked by enemy pawns (after capture)?
        if attacked_by_pawns(t, nen, not white): continue
        cap = 'x' if t in en_p else '-'
        out.append(('K' + nm(own_k) + cap + nm(t), mkpos(t, own_p, nen, -1)))
    # pawn moves
    d = 1 if white else -1
    last = H - 1 if white else 0
    second = 1 if white else H - 2
    for s in own_p:
        rest = [x for x in own_p if x != s]
        # single / double
        t = mk(f_(s), r_(s) + d)
        if t >= 0 and t not in occ:
            if r_(t) == last:
                if self_safe(p, white, s, t, rest, en_p, None):
                    out.append((nm(s) + '-' + nm(t) + '=Q', 'PROMO'))
            else:
                if self_safe(p, white, s, t, rest + [t], en_p, None):
                    out.append((nm(s) + '-' + nm(t), mkpos(own_k, rest + [t], en_p, -1)))
                if r_(s) == second:
                    t2 = mk(f_(s), r_(s) + 2 * d)
                    if t2 >= 0 and t2 not in occ and r_(t2) != last:
                        if self_safe(p, white, s, t2, rest + [t2], en_p, None):
                            out.append((nm(s) + '-' + nm(t2), mkpos(own_k, rest + [t2], en_p, t)))
        for df in (-1, 1):
            t = mk(f_(s) + df, r_(s) + d)
            if t < 0: continue
            if t in en_p:
                nen = [x for x in en_p if x != t]
                if r_(t) == last:
                    if self_safe(p, white, s, t, rest, nen, None):
                        out.append((nm(s) + 'x' + nm(t) + '=Q', 'PROMO'))
                else:
                    if self_safe(p, white, s, t, rest + [t], nen, None):
                        out.append((nm(s) + 'x' + nm(t), mkpos(own_k, rest + [t], nen, -1)))
            elif t == ep and ep >= 0:
                cs = mk(f_(t), r_(t) - d)  # captured pawn square
                if cs in en_p:
                    nen = [x for x in en_p if x != cs]
                    if self_safe(p, white, s, t, rest + [t], nen, None):
                        out.append((nm(s) + 'x' + nm(t) + 'ep', mkpos(own_k, rest + [t], nen, -1)))
    return out


def self_safe(p, white, s, t, nown, nen, _):
    """own king not attacked after the pawn move (pawn leaves s, arrives t, enemy pawn set nen)"""
    wk, bk = p[0], p[1]
    ok = wk if white else bk
    return not attacked_by_pawns(ok, nen, not white) and ok not in KADJ[bk if white else wk]


# ---------------------------------------------------------------- forced-win search
INF = 10 ** 9
winmin = {}     # pos -> minimal proven n such that side to move wins within n plies
nowin = {}      # pos -> largest n proven such that side to move cannot be proven (exactly: cannot win within n)


def win(p, n):
    """True iff the side to move can force a first promotion (own) or mate within n plies of play
    (n counts plies from p, own move first)."""
    if n <= 0: return False
    wm = winmin.get(p)
    if wm is not None and wm <= n: return True
    if nowin.get(p, 0) >= n: return False
    ms = moves(p)
    res = False
    for lab, q in ms:
        if q == 'PROMO':
            res = True; break
    if not res and n >= 3:
        for lab, q in ms:
            if lose(q, n - 1):
                res = True; break
    if res:
        winmin[p] = min(n, winmin.get(p, INF))
    else:
        nowin[p] = max(n, nowin.get(p, 0))
    return res


def lose(p, n):
    """side to move at p loses (is mated or every move lets the opponent win) within n plies (n>=0 counted
    from p; a mated position is lost in 0 plies)."""
    ms = moves(p)
    if not ms:
        return in_check(p, p[5])
    if n < 2: return False
    for lab, q in ms:
        if q == 'PROMO': return False
        if not win(q, n - 1): return False
    return True


def dtw(p, cap=40):
    """minimal n such that side to move wins within n plies, or None up to cap"""
    for n in range(1, cap + 1, 2):
        if win(p, n): return n
    return None
