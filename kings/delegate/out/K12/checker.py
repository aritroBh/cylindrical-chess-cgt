import json, os, sys
from functools import lru_cache

sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import pawns as P

def board(W,H): return P.Board(W,H,True,True)

def rho(r, beta_white, H):
    return r if beta_white else H+1-r

def cyclic_dist(a,b,W):
    d=abs(a-b); return min(d, W-d)

def king_dist(f1,r1,f2,r2,W):
    return max(cyclic_dist(f1,f2,W), abs(r1-r2))

def passed_pawns_list(board, pos, side, W, H):
    mine = pos.white if side=='W' else pos.black
    theirs = pos.black if side=='W' else pos.white
    res=[]
    for (f,r) in mine:
        files = {f} | {g for g in (board.nb(f,-1), board.nb(f,1)) if g is not None}
        if side=='W':
            blocked = any(g in files and s > r for (g,s) in theirs)
        else:
            blocked = any(g in files and s < r for (g,s) in theirs)
        if blocked: continue
        if P.ep_capturable(board, pos, side, (f,r)): continue
        res.append((f,r))
    return res

def has_passed(board,pos,side,W,H):
    return len(passed_pawns_list(board,pos,side,W,H))>0

def ep_tuple(ep):
    if ep is None: return None
    return (tuple(ep[0]), tuple(ep[1]), ep[2])

def make_pos(Wp,Bp,ep,W,H):
    epo=None
    if ep is not None:
        epo=(tuple(ep[0]), tuple(ep[1]), ep[2])
    return P.Pos(frozenset(tuple(x) for x in Wp), frozenset(tuple(x) for x in Bp), epo)

def H1(p, beta, Wp, Bp, ep, W, H, wk, bk, pos):
    # p tuple (f,r) of beta
    beta_white = beta=='W'
    omega = 'B' if beta=='W' else 'W'
    # beta pawns set
    beta_pawns = Wp if beta=='W' else Bp
    omega_pawns = Bp if beta=='W' else Wp
    beta_set = set(tuple(x) for x in beta_pawns)
    omega_set = set(tuple(x) for x in omega_pawns)
    board = P.Board(W,H,True,True)
    poso = make_pos(Wp,Bp,ep,W,H)
    # p passed?
    if p not in passed_pawns_list(board, poso, beta, W, H):
        return False
    f,r = p
    pr = rho(r, beta_white, H)
    # front pawn of file: no piece ahead on same file
    if beta_white:
        ranks_ahead = range(r+1, H+1)
    else:
        ranks_ahead = range(1, r)
    for rr in ranks_ahead:
        sq=(f,rr)
        if sq in beta_set or sq in omega_set: return False
        if sq==wk or sq==bk: return False
    # path squares empty (same as above) yes
    # no king on path already.
    return True

def H2(beta, Wp, Bp, W, H):
    beta_white = beta=='W'
    beta_king_file = 0  # a
    adj = {(W-1)%W, 0, 1%W}  # files adjacent to a-file
    # Actually adjacent files to file 0: W-1 and 1
    adj = { (W-1)%W, 1%W }
    allp = set(tuple(x) for x in Wp) | set(tuple(x) for x in Bp)
    for (f,r) in allp:
        if f in adj:
            return False
    return True

def H3(omega, Wp, Bp, W, H):
    # omega king position
    if omega=='W':
        ok=(0,1)
    else:
        ok=(0,H)
    beta_king = (0,H) if omega=='W' else (0,1)
    allp = set(tuple(x) for x in Wp) | set(tuple(x) for x in Bp)
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            # neighbor with wrap
            tf = (ok[0]+df)%W
            tr = ok[1]+dr
            if tr<1 or tr>H: continue
            t=(tf,tr)
            # not adjacent to beta king
            if king_dist(t[0],t[1],beta_king[0],beta_king[1],W) < 2:
                continue
            # no pawn on file of t or adjacent files
            files = {(tf-1)%W, tf, (tf+1)%W}
            bad=False
            for (f,r) in allp:
                if f in files:
                    bad=True; break
            if not bad:
                return True
    return False

def H4(p, beta, Wp, Bp, W, H):
    beta_white = beta=='W'
    beta_pawns = Wp if beta=='W' else Bp
    other_beta = [q for q in beta_pawns if tuple(q)!=tuple(p)]
    f0,r0 = p
    pr0 = rho(r0, beta_white, H)
    adj_files = {(f0-1)%W, (f0+1)%W}
    for q in other_beta:
        fq,rq = q
        if fq not in adj_files:
            continue
        prq = rho(rq, beta_white, H)
        if prq > pr0 + 1:
            return False
    return True

def mu_omega(W,H,beta,stm,ep, Wp,Bp,p, wk,bk):
    # beta: 'W'/'B'; stm side to move at y; ep tuple or None
    beta_white = beta=='W'
    omega = 'B' if beta=='W' else 'W'
    # omega moves toward promotion rank: if beta white, omega black moves down to rank1; if beta black, omega white moves up to rank H
    # p removed from beta pawns
    omega_pawns_init = list(Bp if omega=='B' else Wp)  # omega pawns are black if omega B else white
    # Actually omega side pieces: if omega=='W' -> white pawns Wp; if 'B' -> black pawns Bp
    if omega=='W':
        omega_pawns_init = [tuple(x) for x in Wp]
        beta_pawns_init = [tuple(x) for x in Bp]
    else:
        omega_pawns_init = [tuple(x) for x in Bp]
        beta_pawns_init = [tuple(x) for x in Wp]
    # remove p from beta pawns
    p_t = tuple(p)
    beta_pawns_init = [q for q in beta_pawns_init if q != p_t]
    # promotion rank for omega
    if omega=='W':
        promo_rank = H  # white promotes to H
        start_rank = 2
        dstep = +1
    else:
        promo_rank = 1
        start_rank = H-1
        dstep = -1
    # ep availability for omega: if stm==omega and ep capturer is omega
    ep_avail0 = False
    ep_target = None
    ep_captured = None
    if stm==omega and ep is not None:
        # ep tuple (target,captured,capturer)
        if ep[2]==omega:
            ep_avail0 = True
            ep_target = tuple(ep[0])
            ep_captured = tuple(ep[1])
    # kings
    wk_t = (0,1) if True else None
    # fixed kings:
    white_king = (0,1)
    black_king = (0,H)
    king_squares = {white_king, black_king}

    from functools import lru_cache

    # state: (tuple sorted omega, frozenset beta, ep_avail bool)
    memo={}
    def key(ws, bs, epf):
        return (tuple(sorted(ws)), frozenset(bs), epf)

    def search(ws, bs, epf):
        ws = tuple(sorted(ws))
        bs = frozenset(bs)
        k = (ws, bs, epf)
        if k in memo:
            return memo[k]
        # if any omega already promoted? none
        # generate moves
        best = None  # min moves
        bs_set = set(bs)
        ws_set = set(ws)
        # For each pawn
        for idx,pw in enumerate(ws):
            f,r = pw
            # single push
            nr = r + dstep
            if 1 <= nr <= H:
                target=(f,nr)
                if target not in ws_set and target not in bs_set and target not in king_squares:
                    # promotion?
                    if nr == promo_rank:
                        # terminal
                        if best is None or 1 < best:
                            best = 1
                    else:
                        nws = list(ws); nws[idx]=(f,nr)
                        # remove none
                        val = search(nws, bs, False)
                        if val != float('inf'):
                            cand = 1 + val
                            if best is None or cand < best:
                                best = cand
            # double push
            if r == start_rank:
                n1 = r + dstep
                n2 = r + 2*dstep
                if 1 <= n2 <= H:
                    t1=(f,n1); t2=(f,n2)
                    if t1 not in ws_set and t1 not in bs_set and t1 not in king_squares and t2 not in ws_set and t2 not in bs_set and t2 not in king_squares:
                        if n2 == promo_rank:
                            if best is None or 1<best:
                                best=1
                        else:
                            nws=list(ws); nws[idx]=(f,n2)
                            val=search(nws, bs, False)
                            if val!=float('inf'):
                                cand=1+val
                                if best is None or cand<best: best=cand
            # captures
            for df in (-1,1):
                gf = (f+df)%W  # wrap
                nr = r + dstep
                if 1 <= nr <= H:
                    target=(gf,nr)
                    if target in bs_set and target not in king_squares:
                        # promotion?
                        if nr == promo_rank:
                            if best is None or 1<best: best=1
                        else:
                            nws=list(ws); nws[idx]=(gf,nr)
                            nbs=[q for q in bs if q!=target]
                            val=search(nws, nbs, False)
                            if val!=float('inf'):
                                cand=1+val
                                if best is None or cand<best: best=cand
            # e.p. capture
            if epf and ep_target is not None:
                # capturer must be at landing rank? ep target skipped square; capturer at adjacent file and landing rank
                # landing rank = ep_captured rank
                cr = ep_captured[1]
                if r == cr:
                    # adjacent file to ep_target file
                    if cyclic_dist(f, ep_target[0], W)==1:
                        target = ep_target
                        if target not in ws_set and target not in bs_set and target not in king_squares:
                            # e.p. capture removes ep_captured
                            nws=list(ws); nws[idx]=target
                            nbs=[q for q in bs if q!=ep_captured]
                            # does not promote (ep target not promo rank usually)
                            if target[1]==promo_rank:
                                if best is None or 1<best: best=1
                            else:
                                val=search(nws, nbs, False)
                                if val!=float('inf'):
                                    cand=1+val
                                    if best is None or cand<best: best=cand
        if best is None:
            best = float('inf')
        memo[k]=best
        return best

    val = search(omega_pawns_init, beta_pawns_init, ep_avail0)
    if val == float('inf'):
        return None  # infinity
    return val

def certified_root(W,H,Wp,Bp,ep,stm):
    board = P.Board(W,H,True,True)
    # beta determination done by caller; but certified checks existence of beta pawn p satisfying.
    # We'll pass beta and Wp/Bp.
    # Need beta credited side determined by caller. Here infer? We'll require caller passes beta.
    return None

def check_certified(W,H,Wp,Bp,ep,stm,beta, drop_h4=False, weaken_h5=False):
    beta_white = beta=='W'
    # beta pawns
    beta_pawns = Wp if beta=='W' else Bp
    omega = 'B' if beta=='W' else 'W'
    wk=(0,1); bk=(0,H)
    # candidate p: passed pawns of beta
    pos = make_pos(Wp,Bp,ep,W,H)
    board = P.Board(W,H,True,True)
    cands = passed_pawns_list(board, pos, beta, W, H)
    for p in cands:
        # H1
        if not H1(p, beta, Wp, Bp, ep, W, H, wk, bk, pos):
            continue
        if not H2(beta, Wp, Bp, W, H):
            continue
        if not H3(omega, Wp, Bp, W, H):
            continue
        if not drop_h4:
            if not H4(p, beta, Wp, Bp, W, H):
                continue
        # H5
        d = None
        # promote distance for p
        # use cylcgt promote_distance? It computes min over passed pawns; for single p maybe. Compute formula.
        f,r = p
        pr = rho(r, beta_white, H)
        if beta_white:
            # d = H - r - (1 if r==2 else 0)
            d = H - r - (1 if r==2 else 0)
        else:
            d = r - 1 - (1 if r==H-1 else 0)
        if stm==omega:
            e = d
        else:
            e = d-1
        mu = mu_omega(W,H,beta,stm,ep,Wp,Bp,p,wk,bk)
        if mu is None:
            mu_inf = True
        else:
            mu_inf = False
        if mu_inf:
            h5 = True
        else:
            thr = e if weaken_h5 else e+1
            h5 = (mu >= thr)
        if not h5:
            continue
        return True
    return False
