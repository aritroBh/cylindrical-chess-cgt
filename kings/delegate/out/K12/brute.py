import sys, os
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K12')
from cylcgt import pawns as P
import checker as C

def mu_bfs(W,H,beta,stm,ep,Wp,Bp,p):
    # independent BFS by depth
    beta_white = beta=='W'
    omega = 'B' if beta=='W' else 'W'
    if omega=='W':
        omega_pawns_init = [tuple(x) for x in Wp]
        beta_pawns_init = [tuple(x) for x in Bp]
        promo_rank=H; start_rank=2; dstep=+1
    else:
        omega_pawns_init = [tuple(x) for x in Bp]
        beta_pawns_init = [tuple(x) for x in Wp]
        promo_rank=1; start_rank=H-1; dstep=-1
    p_t=tuple(p)
    beta_pawns_init=[q for q in beta_pawns_init if q!=p_t]
    wk=(0,1); bk=(0,H); kings={wk,bk}
    ep_avail0=False; ep_target=None; ep_captured=None
    if stm==omega and ep is not None and ep[2]==omega:
        ep_avail0=True; ep_target=tuple(ep[0]); ep_captured=tuple(ep[1])
    # BFS
    from collections import deque
    start=(tuple(sorted(omega_pawns_init)), frozenset(beta_pawns_init), ep_avail0)
    # if any immediate promotion? pawns not on promo rank by legality, but check
    q=deque()
    q.append((start,0))
    visited={start}
    # We'll search for minimal depth where a move promotes.
    # Standard BFS over states; when expanding a state at depth d, if a move promotes, answer d+1.
    while q:
        (ws,bs,epf),d = q.popleft()
        ws_set=set(ws); bs_set=set(bs)
        # generate moves
        for idx,pw in enumerate(ws):
            f,r=pw
            # single push
            nr=r+dstep
            if 1<=nr<=H:
                target=(f,nr)
                if target not in ws_set and target not in bs_set and target not in kings:
                    if nr==promo_rank:
                        return d+1
                    nws=tuple(sorted([ (f,nr) if i==idx else ws[i] for i in range(len(ws))]))
                    nstate=(nws, bs, False)
                    if nstate not in visited:
                        visited.add(nstate); q.append((nstate,d+1))
            # double
            if r==start_rank:
                n1=r+dstep; n2=r+2*dstep
                if 1<=n2<=H:
                    t1=(f,n1); t2=(f,n2)
                    if t1 not in ws_set and t1 not in bs_set and t1 not in kings and t2 not in ws_set and t2 not in bs_set and t2 not in kings:
                        if n2==promo_rank:
                            return d+1
                        nws=tuple(sorted([(f,n2) if i==idx else ws[i] for i in range(len(ws))]))
                        nstate=(nws, bs, False)
                        if nstate not in visited:
                            visited.add(nstate); q.append((nstate,d+1))
            # captures
            for df in (-1,1):
                gf=(f+df)%W
                nr=r+dstep
                if 1<=nr<=H:
                    target=(gf,nr)
                    if target in bs_set and target not in kings:
                        if nr==promo_rank:
                            return d+1
                        nws=tuple(sorted([(gf,nr) if i==idx else ws[i] for i in range(len(ws))]))
                        nbs=bs - {target}
                        nstate=(nws, frozenset(nbs), False)
                        if nstate not in visited:
                            visited.add(nstate); q.append((nstate,d+1))
            # ep
            if epf and ep_target is not None:
                cr=ep_captured[1]
                if r==cr and (abs(f-ep_target[0])%W in (1,W-1)):
                    target=ep_target
                    if target not in ws_set and target not in bs_set and target not in kings:
                        if target[1]==promo_rank:
                            return d+1
                        nws=tuple(sorted([(target[0],target[1]) if i==idx else ws[i] for i in range(len(ws))]))
                        nbs=bs - {ep_captured}
                        nstate=(nws, frozenset(nbs), False)
                        if nstate not in visited:
                            visited.add(nstate); q.append((nstate,d+1))
    return None

def check_certified_brute(W,H,Wp,Bp,ep,stm,beta):
    # reuse H1-H4 from checker, but mu via BFS
    import checker as C
    beta_white = beta=='W'
    omega='B' if beta=='W' else 'W'
    wk=(0,1); bk=(0,H)
    pos=C.make_pos(Wp,Bp,ep,W,H)
    board=P.Board(W,H,True,True)
    cands=C.passed_pawns_list(board,pos,beta,W,H)
    for p in cands:
        if not C.H1(p,beta,Wp,Bp,ep,W,H,wk,bk,pos): continue
        if not C.H2(beta,Wp,Bp,W,H): continue
        if not C.H3(omega,Wp,Bp,W,H): continue
        # H4
        if not C.H4(p,beta,Wp,Bp,W,H): continue
        # H5
        f,r=p
        if beta_white:
            d=H-r-(1 if r==2 else 0)
        else:
            d=r-1-(1 if r==H-1 else 0)
        e = d if stm==omega else d-1
        mu = mu_bfs(W,H,beta,stm,ep,Wp,Bp,p)
        if mu is None:
            h5=True
        else:
            h5 = (mu >= e+1)
        if not h5: continue
        return True
    return False