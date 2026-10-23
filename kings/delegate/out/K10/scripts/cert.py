"""Own checker for Proposition 2.11 (final form). Uses cylcgt only for passed/promote_distance/moves.
Positions: board Board(W,H,True,True); pos Pos(white,black,ep); kings wk,bk squares (file,rank), rank 1..H."""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt.pawns import Board, Pos, passed, promote_distance, moves, ep_capturable, name
import cylcgt.pawns as cp

import os
NTH = int(os.environ.get('NTH','1'))
def opp(c): return 'B' if c == 'W' else 'W'

def kdist(bd, a, b):
    df = abs(a[0]-b[0]); df = min(df, bd.files-df)
    return max(df, abs(a[1]-b[1]))

def cyc_adj(bd, f):
    return {(f-1) % bd.files, (f+1) % bd.files}

def pawn_passed(bd, pos, side, sq):
    mine, theirs = (pos.white, pos.black) if side == 'W' else (pos.black, pos.white)
    f, r = sq
    files = {f} | {g for g in (bd.nb(f,-1), bd.nb(f,1)) if g is not None}
    if side == 'W': blocked = any(g in files and s > r for g, s in theirs)
    else: blocked = any(g in files and s < r for g, s in theirs)
    return (not blocked) and not ep_capturable(bd, pos, side, sq)

def dist_to_promote(bd, side, sq):
    r = sq[1]
    if side == 'W': return bd.ranks - r - (1 if r == 2 else 0)
    return r - 1 - (1 if r == bd.ranks - 1 else 0)

def omega_mu(bd, om, bo, kings, omside, ep_first, cap):
    """least number of omega-only moves (<= cap) after which some omega pawn is on its last rank; None if > cap.
    om: omega pawns, bo: beta pawns other than p (static, capturable), kings: set of squares (obstacles),
    ep_first: (target, captured) usable as first move or None."""
    d = -1 if omside == 'B' else 1  # direction of omega... White +1, Black -1
    d = 1 if omside == 'W' else -1
    start = 2 if omside == 'W' else bd.ranks - 1
    last = bd.ranks if omside == 'W' else 1
    seen = {(om, bo, ep_first)}
    frontier = [(om, bo, ep_first)]
    for k in range(1, cap + 1):
        nxt = []
        for om_, bo_, ep_ in frontier:
            occ = om_ | bo_ | kings
            for (f, r) in om_:
                rest = om_ - {(f, r)}
                r1 = r + d
                if (f, r1) not in occ:
                    if r1 == last: return k
                    s = (rest | {(f, r1)}, bo_, None)
                    if s not in seen: seen.add(s); nxt.append(s)
                    r2 = r + 2*d
                    if r == start and (f, r2) not in occ:
                        s = (rest | {(f, r2)}, bo_, None)
                        if s not in seen: seen.add(s); nxt.append(s)
                for df in (-1, 1):
                    g = bd.nb(f, df)
                    if g is None: continue
                    t = (g, r1)
                    if t in bo_:
                        if r1 == last: return k
                        s = (rest | {t}, bo_ - {t}, None)
                        if s not in seen: seen.add(s); nxt.append(s)
                    elif ep_ and ep_[0] == t:
                        s = (rest | {t}, bo_ - {ep_[1]}, None)
                        if s not in seen: seen.add(s); nxt.append(s)
        frontier = nxt
        if not frontier: break
    return None

def check(bd, pos, wk, bk, stm, beta, *, use=('P1','front','kpath','K1','K2','N','M'), detail=False):
    """Does Proposition 2.11 (all hypotheses in `use`) hold for some pawn p of beta?  Returns (ok, info)."""
    om_side = opp(beta)
    mine, theirs = (pos.white, pos.black) if beta == 'W' else (pos.black, pos.white)
    bk_, ok_ = (wk, bk) if beta == 'W' else (bk, wk)   # beta king, omega king
    H = bd.ranks
    last = H if beta == 'W' else 1
    sgn = 1 if beta == 'W' else -1
    best = None
    for p in mine:
        f, r = p
        info = {}
        if 'P1' in use and not pawn_passed(bd, pos, beta, p): continue
        if 'front' in use:
            if any(q[0] == f and (q[1]-r)*sgn > 0 for q in mine): continue
        if 'kpath' in use:
            if any(k[0] == f and (k[1]-r)*sgn > 0 for k in (wk, bk)): continue
        d = dist_to_promote(bd, beta, p)
        e = d - (1 if stm == beta else 0)
        if 'K1' in use:
            adj = cyc_adj(bd, bk_[0])
            if any(q[0] in adj for q in pos.white | pos.black): continue
        if 'K2' in use:
            okK = False
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df == 0 and dr == 0: continue
                    g = (ok_[0]+df) % bd.files
                    rr = ok_[1]+dr
                    if not (1 <= rr <= H): continue
                    t = (g, rr)
                    if kdist(bd, t, bk_) < 2: continue
                    fs = {t[0]} | cyc_adj(bd, t[0])
                    if any(q[0] in fs for q in pos.white | pos.black): continue
                    okK = True
            if not okK: continue
        if 'N' in use:
            adj = cyc_adj(bd, f)
            bad = False
            for q in mine:
                if q != p and q[0] in adj and (q[1]-r)*sgn > NTH: bad = True
            if bad: continue
        if 'M' in use:
            om = theirs
            bo = mine - {p}
            ep_first = None
            if pos.ep and stm == om_side and pos.ep[2] == om_side:
                ep_first = (pos.ep[0], pos.ep[1])
            mu = omega_mu(bd, frozenset(om), frozenset(bo), frozenset([wk, bk]), om_side, ep_first, e)
            if mu is not None: continue   # omega promotes within e moves
        return True, {'p': p, 'd': d, 'e': e}
    return False, None
