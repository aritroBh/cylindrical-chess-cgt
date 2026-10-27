import subprocess, sys, os, random

KP = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K11/kp"

def rho(rank, H, beta_is_white):
    if beta_is_white:
        return rank
    else:
        return H + 1 - rank

def parse_pos(s, W, H):
    # s like "Ka1 ka6 Pc4 pe4 b -"
    toks = s.split()
    wk = bk = None
    wp = set(); bp = set()
    side = None; ep = None
    for t in toks:
        if t in ("w","b"):
            side = t; continue
        if t == "-":
            ep = None; continue
        # ep square like e3
        if len(t) in (2,3) and t[0].islower() and t[1].isdigit():
            # could be ep square
            ep = t; continue
        # piece
        kind = t[0]; sq = t[1:]
        f = ord(sq[0]) - 97; r = int(sq[1:])
        if kind == "K":
            wk = (f,r)
        elif kind == "k":
            bk = (f,r)
        elif kind == "P":
            wp.add((f,r))
        elif kind == "p":
            bp.add((f,r))
    # ep parse to square tuple
    epsq = None
    if ep and ep != "-":
        epsq = (ord(ep[0])-97, int(ep[1:]))
    # side to move as bool beta? we keep string
    return wk, bk, wp, bp, side, epsq

def in_strip(f, pf, W, wrap):
    # files f-1,f,f+1 mod W
    diffs = []
    for df in (-1,0,1):
        g = (pf+df) % W if wrap else pf+df
        if wrap or (0 <= g < W):
            if g == f:
                return True
    return False

def strip_files(pf, W, wrap):
    res = set()
    for df in (-1,0,1):
        if wrap:
            res.add((pf+df)%W)
        else:
            g = pf+df
            if 0 <= g < W:
                res.add(g)
    return res

def mod(x, W, wrap):
    if wrap:
        return x % W
    return x

def nb(f, df, W, wrap):
    g = f + df
    if wrap:
        return g % W
    if 0 <= g < W:
        return g
    return None

def passed_aware(board, wp, bp, side, ep_sq, W, H, wrap):
    # side "W" or "B" for the side whose pawns
    if side == "W":
        mine = wp; theirs = bp
        def blocked(f,r):
            files = {f} | {g for g in (nb(f,-1,W,wrap), nb(f,1,W,wrap)) if g is not None}
            return any(g in files and s > r for (g,s) in theirs)
        def ep_cap(f,r):
            if not (ep_sq is not None): return False
            # ep target square equals (f, r)? captured pawn's square
            # pos.ep[1] == square in cylcgt; ep_sq stored as target? We'll handle separately
            return False
    else:
        mine = bp; theirs = wp
        def blocked(f,r):
            files = {f} | {g for g in (nb(f,-1,W,wrap), nb(f,1,W,wrap)) if g is not None}
            return any(g in files and s < r for (g,s) in theirs)
        def ep_cap(f,r):
            return False
    for (f,r) in mine:
        if side=="W":
            files = {f} | {g for g in (nb(f,-1,W,wrap), nb(f,1,W,wrap)) if g is not None}
            blk = any(g in files and s > r for (g,s) in theirs)
        else:
            files = {f} | {g for g in (nb(f,-1,W,wrap), nb(f,1,W,wrap)) if g is not None}
            blk = any(g in files and s < r for (g,s) in theirs)
        if not blk:
            # ep capturable: if this pawn could be taken ep now
            capt = False
            if ep_sq is not None:
                # ep_sq is target square (f, r+1?) for white pawn double step; captured square (f, r?) 
                # cylcgt ep = (target_square, captured_square, side_that_may_capture)
                # We only have target? Let's store ep as target square in our pos; need captured square.
                pass
            if not capt:
                return True
    return False

# We'll simplify: checker focuses on H1-H5 and invariants; ep capturable handling for H1 uses ep info.
# We'll pass ep as (target, captured, side) tuple.

def pos_from_str(s, W, H):
    toks = s.split()
    wk=bk=None; wp=set(); bp=set(); side=None; ep=None
    for t in toks:
        if t in ("w","b"):
            side=t; continue
        if t=="-":
            ep=None; continue
        if len(t)>=2 and t[0].islower() and t[1].isdigit():
            # ep square target; but our input only gives one token for ep. cylcgt prints (ep e3) maybe.
            # kpsolve format: last token ep square or '-'. We'll treat as target only; captured = (f, r∓1)
            ep = ("target", t); continue
        kind=t[0]; sq=t[1:]
        f=ord(sq[0])-97; r=int(sq[1:])
        if kind=="K": wk=(f,r)
        elif kind=="k": bk=(f,r)
        elif kind=="P": wp.add((f,r))
        elif kind=="p": bp.add((f,r))
    return wk,bk,wp,bp,side,ep

def ep_tuple(ep_raw, side_to_move):
    # convert to (target, captured, side_to_capture) if possible; if ep_raw is ("target",sq)
    if ep_raw is None: return None
    if ep_raw[0]!="target": return None
    sq=ep_raw[1]; f=ord(sq[0])-97; r=int(sq[1:])
    # determine captured square and capturing side: if target square r is one step ahead of start?
    # For a white pawn double step from rank2 to rank4, target ep square is rank3, captured rank? 
    # cylcgt ep = ((f, r1), (f, r2), other) where r1 skipped square, r2 landing. captured_square = r2 (pawn location), target = r1.
    # Our token is the skipped square? kpsolve prints ep as target? In kpsolve output move gives ep square t (skipped). Input expects ep square = skipped square.
    # So ep_raw target = skipped square. captured = pawn square (one more step in same direction). capturing side = opponent of mover.
    # We don't know mover; but side_to_move at y is the one who can capture. So capturing side = side_to_move.
    capt_side = "W" if side_to_move=="w" else "B"
    # captured square: if capturing side white, captured pawn is black pawn one rank above skipped? 
    # skipped square rank r; captured pawn at r+1 (white capturing black) or r-1 (black capturing white).
    if capt_side=="W":
        captured=(f, r+1)
    else:
        captured=(f, r-1)
    return ((f,r), captured, capt_side)

def rho_val(rank,H,beta_white):
    if beta_white: return rank
    return H+1-rank

def is_passed_aware(board_tuple, wp, bp, side, ep, W, H, wrap):
    # side "W"/"B" colour of pawns
    mine = wp if side=="W" else bp
    theirs = bp if side=="W" else wp
    for (f,r) in mine:
        files = {f} | {g for g in (nb(f,-1,W,wrap), nb(f,1,W,wrap)) if g is not None}
        if side=="W":
            blk = any(g in files and s > r for (g,s) in theirs)
        else:
            blk = any(g in files and s < r for (g,s) in theirs)
        if blk: 
            continue
        # ep capturable?
        capt = False
        if ep is not None:
            # ep = (target, captured, capt_side)
            target, captured, cside = ep
            if cside != side and captured == (f,r):
                # need adjacent capturer
                captors = theirs
                adj = [g for g in (nb(f,-1,W,wrap), nb(f,1,W,wrap)) if g is not None]
                if any((g, r) in captors for g in adj) if False else any((g, r) in captors for g in adj):
                    # Actually capturer stands on same rank as captured pawn, adjacent file.
                    capt = any((g, r) in captors for g in adj)
        if not blk and not capt:
            return True
    return False

def front_pawn(wp, bp, side, f, r, W,H,wrap):
    occ = wp | bp
    if side=="W":
        return all((f,s) not in occ for s in range(r+1, H+1))
    else:
        return all((f,s) not in occ for s in range(1, r))

def promote_dist_single(W,H,side,r,start_rank):
    if side=="W":
        return H - r - (1 if r==2 else 0)
    else:
        return r - 1 - (1 if r==H-1 else 0)

def mu_omega(wk,bk,wp,bp,p, beta_white, W,H,wrap, s_side, ep_raw, e_first):
    # delete p from wp/bp
    if beta_white:
        wp2 = set(wp); wp2.discard(p)
    else:
        bp2 = set(bp); bp2.discard(p)
    # Actually p is beta pawn; remove from beta's set
    if beta_white:
        wp2 = set(x for x in wp if x!=p)
        bp2 = set(bp)
    else:
        bp2 = set(x for x in bp if x!=p)
        wp2 = set(wp)
    # BFS: state = (frozenset wp, bp, ep_available bool) side to move omega always
    # first move may use ep if s_side=="w"? Need capturing side = omega. 
    # ep available only if omega is the side that may capture at y, i.e. side_to_move at y is omega.
    # We'll pass ep_avail = (side_to_move_str == omega_str)
    omega_is_white = not beta_white
    # side strings
    # beta_str = "W" if beta_white else "B"
    # omega_str = "B" if beta_white else "W"
    start_ep = ep_raw  # tuple or None
    # ep available if the side to move at y is omega. We'll determine outside; here assume ep_avail flag passed via ep_raw not None and s_side indicates.
    # Let's compute: if side_to_move token == omega's token then ep (if any) is for omega.
    # We'll handle by passing ep_avail boolean.
    pass

# This is getting complex. Let me instead write a more direct checker focusing on invariants + kpsolve outcomes,
# and a BFS mu for H5.

def beta_str(beta_white): return "W" if beta_white else "B"
def omega_str(beta_white): return "B" if beta_white else "W"

def ep_avail_at_y(side_to_move_token, beta_white):
    # side_to_move_token "w"/"b"; omega token is "b" if beta_white else "w"
    omega_token = "b" if beta_white else "w"
    return side_to_move_token == omega_token

def rho_of(rank, H, beta_white):
    return rank if beta_white else H+1-rank

def mu_omega_bfs(wk,bk,wp,bp,p,beta_white,W,H,wrap, side_to_move_token, ep_raw):
    # remove p
    if beta_white:
        wp = set(x for x in wp if x != p)
    else:
        bp = set(x for x in bp if x != p)
    omega_white = not beta_white
    # ep available for first omega move?
    ep_avail = ep_avail_at_y(side_to_move_token, beta_white)
    # ep tuple
    ep_tuple = None
    if ep_raw is not None and ep_avail:
        ep_tuple = ep_raw  # (target,captured,capt_side) should be for omega; check
    # BFS
    from collections import deque
    start = (frozenset(wp), frozenset(bp), True if ep_tuple is not None else False)
    # store ep_tuple separately for first move
    # We'll encode state as (wp, bp, ep_flag) where ep_flag True means the original ep right still usable
    # and if True, ep_tuple is the original.
    # moves for omega
    def omega_pawn_moves(wp, bp, ep_flag):
        # returns list of (new_wp,new_bp,new_ep_flag, promoted bool)
        res = []
        occ = wp | bp
        # omega colour
        if omega_white:
            mine = wp; theirs = bp; d = 1; start_rank = 2
        else:
            mine = bp; theirs = wp; d = -1; start_rank = H-1
        # We need move omega pawns; but wp/bp sets include both. We'll work with mine set reference.
        # Determine which set is mine
        if omega_white:
            cur_mine = set(wp); cur_theirs = set(bp)
        else:
            cur_mine = set(bp); cur_theirs = set(wp)
        occ = cur_mine | cur_theirs
        for (f,r) in list(cur_mine):
            rest = cur_mine - {(f,r)}
            r1 = r + d
            if 1 <= r1 <= H:
                # push
                if (f, r1) not in occ:
                    nm = rest | {(f,r1)}
                    # promotion?
                    promoted = (r1 == (H if omega_white else 1))
                    # build new sets
                    if omega_white:
                        nwp = nm; nbp = cur_theirs
                    else:
                        nwp = cur_theirs; nbp = nm
                    res.append((nwp,nbp,False,promoted))
                    # double step
                    r2 = r + 2*d
                    if r == start_rank and 1 <= r2 <= H and (r2 == (H if omega_white else 1)) is False and (f,r2) not in occ and (f,r1) not in occ:
                        # double step not promoting usually; but could promote on 4-rank? handle promoted if r2 last
                        prom2 = (r2 == (H if omega_white else 1))
                        nm2 = rest | {(f,r2)}
                        if omega_white:
                            nwp2=nm2; nbp2=cur_theirs
                        else:
                            nwp2=cur_theirs; nbp2=nm2
                        # ep: if capturable by beta? not needed for promotion distance; but state ep not usable later (beta doesn't move) so ep_flag False
                        res.append((nwp2,nbp2,False,prom2))
                    elif r == start_rank and 1<=r2<=H and (f,r2) not in occ and (f,r1) not in occ:
                        prom2 = (r2 == (H if omega_white else 1))
                        nm2 = rest | {(f,r2)}
                        if omega_white:
                            nwp2=nm2; nbp2=cur_theirs
                        else:
                            nwp2=cur_theirs; nbp2=nm2
                        res.append((nwp2,nbp2,False,prom2))
                # captures
                for df in (-1,1):
                    g = (f+df) % W if wrap else f+df
                    if not wrap and (g<0 or g>=W): continue
                    t_sq = (g, r1)
                    if t_sq in cur_theirs:
                        nm = rest | {t_sq}
                        cur_theirs2 = cur_theirs - {t_sq}
                        prom = (r1 == (H if omega_white else 1))
                        if omega_white:
                            nwp=nm; nbp=cur_theirs2
                        else:
                            nwp=cur_theirs2; nbp=nm
                        res.append((nwp,nbp,False,prom))
                    # ep capture
                    if ep_flag and ep_tuple is not None:
                        tgt, capt, cside = ep_tuple
                        if cside == ("W" if omega_white else "B"):
                            # target square should be t_sq
                            if tgt == t_sq and capt in cur_theirs:
                                # landing t_sq, remove captured
                                nm = rest | {tgt}
                                cur_theirs2 = cur_theirs - {capt}
                                prom = (tgt[1] == (H if omega_white else 1))
                                if omega_white:
                                    nwp=nm; nbp=cur_theirs2
                                else:
                                    nwp=cur_theirs2; nbp=nm
                                res.append((nwp,nbp,False,prom))
        # dedup
        uniq = []
        seen = set()
        for (a,b,c,d) in res:
            key = (frozenset(a), frozenset(b))
            if key in seen: continue
            seen.add(key)
            uniq.append((a,b,c,d))
        return uniq

    # BFS
    # state key: (frozenset wp, frozenset bp, ep_flag)
    q = deque()
    q.append((frozenset(wp), frozenset(bp), ep_avail))
    dist = { (frozenset(wp), frozenset(bp), ep_avail): 0 }
    while q:
        wpf, bpf, ef = q.popleft()
        d0 = dist[(wpf,bpf,ef)]
        # check if any omega pawn promoted already? state before move; if promoted we would have returned.
        moves = omega_pawn_moves(set(wpf), set(bpf), ef)
        # ep_tuple available only if ef and original
        # Need pass ep_tuple to moves; closure above uses ep_tuple global? We'll restructure: pass ep_tuple
        # We'll just use global et
        for (nwp, nbp, nef, prom) in moves:
            if prom:
                return d0 + 1
            key = (frozenset(nwp), frozenset(nbp), nef)
            if key not in dist:
                dist[key] = d0+1
                q.append(key)
    return float('inf')

# We need make omega_pawn_moves use ep_tuple. Let's instead inline ep_tuple global.
ET_GLOBAL = None

def omega_pawn_moves2(wp_set, bp_set, ep_flag, omega_white, W, H, wrap, ep_tuple):
    res = []
    if omega_white:
        mine = set(wp_set); theirs = set(bp_set); d = 1; start_rank = 2; last = H
    else:
        mine = set(bp_set); theirs = set(wp_set); d = -1; start_rank = H-1; last = 1
    occ = mine | theirs
    for (f,r) in list(mine):
        rest = mine - {(f,r)}
        r1 = r + d
        if 1 <= r1 <= H:
            if (f, r1) not in occ:
                nm = rest | {(f,r1)}
                prom = (r1 == last)
                if omega_white:
                    nwp = nm; nbp = theirs
                else:
                    nwp = theirs; nbp = nm
                res.append((nwp,nbp,False,prom))
                r2 = r + 2*d
                if r == start_rank and 1 <= r2 <= H and (f,r2) not in occ and (f,r1) not in occ:
                    prom2 = (r2 == last)
                    nm2 = rest | {(f,r2)}
                    if omega_white:
                        nwp2 = nm2; nbp2 = theirs
                    else:
                        nwp2 = theirs; nbp2 = nm2
                    res.append((nwp2,nbp2,False,prom2))
            for df in (-1,1):
                g = (f+df)%W if wrap else f+df
                if (not wrap) and (g<0 or g>=W): continue
                t_sq = (g, r1)
                if t_sq in theirs:
                    nm = rest | {t_sq}
                    theirs2 = theirs - {t_sq}
                    prom = (r1 == last)
                    if omega_white:
                        nwp = nm; nbp = theirs2
                    else:
                        nwp = theirs2; nbp = nm
                    res.append((nwp,nbp,False,prom))
                if ep_flag and ep_tuple is not None:
                    tgt, capt, cside = ep_tuple
                    omega_side = "W" if omega_white else "B"
                    if cside == omega_side and tgt == t_sq and capt in theirs:
                        nm = rest | {tgt}
                        theirs2 = theirs - {capt}
                        prom = (tgt[1] == last)
                        if omega_white:
                            nwp = nm; nbp = theirs2
                        else:
                            nwp = theirs2; nbp = nm
                        res.append((nwp,nbp,False,prom))
    # dedup
    uniq=[]; seen=set()
    for (a,b,c,d) in res:
        key=(frozenset(a),frozenset(b))
        if key in seen: continue
        seen.add(key); uniq.append((a,b,c,d))
    return uniq

def mu_omega(wk,bk,wp,bp,p,beta_white,W,H,wrap,side_to_move_token,ep_raw):
    if beta_white:
        wp = set(x for x in wp if x != p)
    else:
        bp = set(x for x in bp if x != p)
    omega_white = not beta_white
    ep_avail = ep_avail_at_y(side_to_move_token, beta_white)
    ep_tuple = None
    if ep_raw is not None and ep_avail:
        # ep_raw is (target,captured,capt_side) maybe; our pos ep stored as tuple? We'll pass already tuple
        ep_tuple = ep_raw
    from collections import deque
    start_key = (frozenset(wp), frozenset(bp), ep_avail)
    q = deque([start_key])
    dist = {start_key: 0}
    while q:
        wpf,bpf,ef = q.popleft()
        d0 = dist[(wpf,bpf,ef)]
        moves = omega_pawn_moves2(set(wpf), set(bpf), ef, omega_white, W, H, wrap, ep_tuple)
        for (nwp,nbp,nef,prom) in moves:
            if prom:
                return d0+1
            key = (frozenset(nwp), frozenset(nbp), False)
            if key not in dist:
                dist[key] = d0+1
                q.append(key)
    return float('inf')

# ---- invariants ----

def rho_pawn(f,r,beta_white,W,H,wrap):
    return r if beta_white else H+1-r

def strip_files_list(pf,W,wrap):
    res=[]
    for df in (-1,0,1):
        if wrap:
            res.append((pf+df)%W)
        else:
            g=pf+df
            if 0<=g<W: res.append(g)
    return res

def check_hypotheses(wk,bk,wp,bp,side_token,beta_white,p,W,H,wrap,ep_raw):
    # returns (ok, reason)
    beta_is_white = beta_white
    # p must be beta pawn
    if beta_white:
        if p not in wp: return False,"p not in wp"
    else:
        if p not in bp: return False,"p not in bp"
    pf,pr = p
    # H1: p passed aware + all squares ahead empty + no king on path
    # passed
    # build ep tuple
    ep_tuple = None
    if ep_raw is not None:
        # ep_raw may be tuple already
        ep_tuple = ep_raw
    # passed for beta side
    if beta_white:
        mine=wp; theirs=bp
    else:
        mine=bp; theirs=wp
    # passed aware for single pawn p? Need check p specifically passed and front.
    # Use cylcgt-like: for p, no enemy on adjacent files ahead; not ep capturable.
    # adjacent files
    adj_files = {pf} | {g for g in (nb(pf,-1,W,wrap), nb(pf,1,W,wrap)) if g is not None}
    ahead_ranks = (range(pr+1, H+1) if beta_white else range(1, pr))
    blocked = False
    for (g,s) in theirs:
        if g in adj_files:
            if beta_white and s > pr: blocked=True
            if (not beta_white) and s < pr: blocked=True
    # front pawn
    occ = wp | bp
    if beta_white:
        front = all((pf,s) not in occ for s in range(pr+1,H+1))
    else:
        front = all((pf,s) not in occ for s in range(1,pr))
    if blocked or not front:
        return False,"H1 blocked/not front"
    # ep capturable for p
    ep_capt = False
    if ep_tuple is not None:
        target, captured, cside = ep_tuple
        if cside != ("W" if beta_white else "B") and captured == p:
            adj = [g for g in (nb(pf,-1,W,wrap), nb(pf,1,W,wrap)) if g is not None]
            captors = theirs
            if any((g, pr) in captors for g in adj):
                ep_capt = True
    if ep_capt:
        return False,"H1 ep capturable"
    # no king on path
    path_sqs = [(pf,s) for s in (range(pr+1,H+1) if beta_white else range(pr-1,0,-1))]
    # promotion square included: last rank
    if beta_white:
        path_sqs = [(pf,s) for s in range(pr+1, H+1)]
    else:
        path_sqs = [(pf,s) for s in range(pr-1, 0, -1)]
    for sq in path_sqs:
        if wk == sq or bk == sq:
            return False,"H1 king on path"
    # H2: no pawn of either colour on file adjacent to beta king file
    bking = wk if beta_white else bk
    bkf = bking[0]
    adj_king_files = set()
    for df in (-1,1):
        g = nb(bkf, df, W, wrap)
        if g is not None: adj_king_files.add(g)
    for (f,r) in (wp | bp):
        if f in adj_king_files:
            return False,"H2"
    # H3: omega king has neighbour t not adjacent to beta king, no pawn on file t or adjacent
    oking = bk if beta_white else wk
    # neighbours of oking
    of, orr = oking
    # king moves
    cand_ts = []
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            f2 = nb(of, df, W, wrap) if df!=0 else of
            # if wrap, file wrap; rank
            if wrap:
                f2 = (of+df)%W
            else:
                f2 = of+df
                if f2<0 or f2>=W: continue
            r2 = orr+dr
            if r2<1 or r2>H: continue
            # king distance to beta king >=2
            # cyclic file distance
            def king_dist(fa,ra,fb,rb):
                dfd = abs(fa-fb)
                if wrap:
                    dfd = min(dfd, W-dfd)
                return max(dfd, abs(ra-rb))
            if king_dist(f2,r2, bking[0], bking[1]) >= 2:
                cand_ts.append((f2,r2))
    h3_ok = False
    for (tf,tr) in cand_ts:
        # no pawn of either colour on file tf or adjacent
        files_to_check = {tf} | {g for g in (nb(tf,-1,W,wrap), nb(tf,1,W,wrap)) if g is not None}
        bad = False
        for (f,r) in (wp | bp):
            if f in files_to_check:
                bad=True; break
        # also t not occupied by king? t square not adjacent to beta king already; occupancy by pawn checked. King occupancy? t could be occupied by a king? neighbour of omega king cannot be occupied by beta king due dist>=2? maybe. skip.
        if not bad:
            h3_ok = True; break
    if not h3_ok:
        return False,"H3"
    # H4: beta pawns (other than p) on file adjacent to p file have rho <= rho(p)+1
    rp = rho_of(pr, H, beta_white)
    for (f,r) in (wp if beta_white else bp):
        if (f,r)==p: continue
        if f in {g for g in (nb(pf,-1,W,wrap), nb(pf,1,W,wrap)) if g is not None} or f==pf:
            # adjacent files only? "on a file adjacent" means neighbouring files, not same file. But p's own file other pawns? H4 says adjacent to p's file. Use adjacent only.
            if f == pf: 
                continue
            rpv = rho_of(r,H,beta_white)
            if rpv > rp + 1:
                return False,"H4"
    # Actually H4 only adjacent files:
    for (f,r) in (wp if beta_white else bp):
        if (f,r)==p: continue
        adj_pf = {g for g in (nb(pf,-1,W,wrap), nb(pf,1,W,wrap)) if g is not None}
        if f in adj_pf:
            rpv = rho_of(r,H,beta_white)
            if rpv > rp + 1:
                return False,"H4"
    # H5
    d = promote_dist_single(W,H, "W" if beta_white else "B", pr, 2 if beta_white else H-1)
    # e
    side_to_move_is_beta = (side_token == ("w" if beta_white else "b"))
    if side_to_move_is_beta:
        e = d - 1
    else:
        e = d
    mu = mu_omega(wk,bk,wp,bp,p,beta_white,W,H,wrap,side_token,ep_tuple)
    if not (mu >= e + 1):
        return False,"H5"
    return True,"ok"

def beta_push_pos(wk,bk,wp,bp,p,beta_white,W,H,wrap):
    # return new position after pushing p
    pf,pr = p
    if beta_white:
        start_rank = 2
        if pr == start_rank:
            newp = (pf, pr+2)
        else:
            newp = (pf, pr+1)
        wp2 = set(x for x in wp if x != p) | {newp}
        return wk,bk,wp2,bp,newp
    else:
        start_rank = H-1
        if pr == start_rank:
            newp = (pf, pr-2)
        else:
            newp = (pf, pr-1)
        bp2 = set(x for x in bp if x != p) | {newp}
        return wk,bk,wp,bp2,newp

def rho_of_rank(r,H,beta_white):
    return r if beta_white else H+1-r

def simulate_invariants(wk,bk,wp,bp,side_token,beta_white,p,W,H,wrap,ep_raw, max_depth=10):
    # DFS over omega moves; beta pushes p each beta turn.
    # returns (ok, reason)
    ep_tuple = ep_raw if (isinstance(ep_raw, tuple) and len(ep_raw)==3) else None
    # state: (wk,bk,wp,bp,p,side_token, ep_tuple, remaining_beta_pushes?, omega_moves_made)
    # We'll just recurse with a depth limit on omega moves (e+1)
    # Determine e,d
    pr = p[1]
    d = promote_dist_single(W,H, "W" if beta_white else "B", pr, 2 if beta_white else H-1)
    side_to_move_is_beta = (side_token == ("w" if beta_white else "b"))
    e = d-1 if side_to_move_is_beta else d
    # current invariant check function
    def inv_check(wk,bk,wp,bp,p,side_token):
        pf,prc = p
        rp = rho_of_rank(prc,H,beta_white)
        strip = set(strip_files_list(pf,W,wrap))
        # I1: file pf ahead of p empty
        occ = wp | bp
        if beta_white:
            ahead = [(pf,s) for s in range(prc+1, H+1)]
        else:
            ahead = [(pf,s) for s in range(prc-1, 0, -1)]
        for sq in ahead:
            if sq in occ:
                return False,"I1"
        # omega pawns in strip
        omega_set = bp if beta_white else wp
        if side_token == ("w" if beta_white else "b"):
            # beta to move: J_beta: rho <= rp+1
            for (f,r) in omega_set:
                if f in strip:
                    if rho_of_rank(r,H,beta_white) > rp + 1:
                        return False,"Jbeta"
        else:
            # omega to move: J_omega: rho <= rp
            for (f,r) in omega_set:
                if f in strip:
                    if rho_of_rank(r,H,beta_white) > rp:
                        return False,"Jomega"
            # p not ep capturable
            # check if any omega pawn adjacent can capture ep
            if ep_tuple is not None:
                target, captured, cside = ep_tuple
                if captured == p and cside != ("W" if beta_white else "B"):
                    adj = [g for g in (nb(pf,-1,W,wrap), nb(pf,1,W,wrap)) if g is not None]
                    captors = omega_set
                    if any((g, prc) in captors for g in adj):
                        return False,"ep capturable"
        return True,"ok"
    # initial
    ok,reason = inv_check(wk,bk,wp,bp,p,side_token)
    if not ok:
        return False, "initial "+reason
    # remaining beta pushes
    remaining = d  # number of pushes needed
    # if beta to move now, first push counts; if omega to move, omega moves first then beta pushes
    # We'll DFS
    from functools import lru_cache
    # state for visited? We'll just brute force with depth limit
    sys.setrecursionlimit(10000)
    results = {"ok": True, "reason": None}
    def dfs(wk,bk,wp,bp,p,side_token,ep_tuple, pushes_done, omega_moves_done):
        nonlocal results
        if pushes_done >= d:
            # beta promoted already? Actually pushes_done counts completed pushes; if d pushes done, promoted. Should not reach here before check.
            return
        if side_token == ("w" if beta_white else "b"):
            # beta turn: push p
            pf,prc = p
            if beta_white:
                start_rank = 2
                newp = (pf, prc+2) if prc==start_rank else (pf, prc+1)
            else:
                start_rank = H-1
                newp = (pf, prc-2) if prc==start_rank else (pf, prc-1)
            # legality: square empty
            occ = wp | bp
            # check path empty already I1; new square empty?
            if newp in occ:
                results["ok"]=False; results["reason"]="push blocked"; return
            # apply
            if beta_white:
                wp2 = set(x for x in wp if x!=p) | {newp}
                bp2 = set(bp)
            else:
                bp2 = set(x for x in bp if x!=p) | {newp}
                wp2 = set(wp)
            pushes_done2 = pushes_done + 1
            if pushes_done2 >= d:
                # promoted; done (success)
                return
            # after beta push, ep right? single step gives none; double step gives ep right for omega for next move only
            new_ep = None
            if beta_white:
                if prc == 2:  # double step
                    new_ep = ((pf, prc+1), (pf, prc+2), "B")
            else:
                if prc == H-1:
                    new_ep = ((pf, prc-1), (pf, prc-2), "W")
            # omega to move next
            # invariant at node with omega to move after beta push
            side2 = "b" if beta_white else "w"
            ok,rr = inv_check(wk,bk,wp2,bp2,newp,side2)
            if not ok:
                results["ok"]=False; results["reason"]="after push "+rr; return
            dfs(wk,bk,wp2,bp2,newp,side2,new_ep,pushes_done2,omega_moves_done)
        else:
            # omega turn: generate all omega pawn moves
            omega_white = not beta_white
            moves = omega_pawn_moves2(set(wp), set(bp), ep_tuple is not None, omega_white, W, H, wrap, ep_tuple)
            # also if no moves? omega has king move but loses; ignore (terminal). For invariant, if no pawn moves, omega must move king and lose; play ends. We can stop.
            if not moves:
                return
            for (nwp,nbp,nef,prom) in moves:
                if prom:
                    # omega promotes -> H5 violated (shouldn't happen if certified)
                    results["ok"]=False; results["reason"]="omega promotes"; return
                # p still present? p is beta pawn; ensure not captured
                if beta_white:
                    if p not in nbp and p not in nwp:
                        # p captured? p in wp originally; if missing from wp2? 
                        pass
                    if p not in set(nwp if False else (nwp if beta_white else nbp)):
                        # p should remain in beta set
                        pass
                # check p present
                beta_set = nwp if beta_white else nbp
                if p not in beta_set:
                    results["ok"]=False; results["reason"]="p captured"; return
                # new ep: after omega move, ep_tuple no longer usable (beta didn't move) but if omega double stepped, ep right for beta; irrelevant for omega moves. Set None for next? 
                # Actually if omega double steps, beta gets ep right, but beta's strategy pushes p not capture; but for invariant J, p not ep capturable? We handle via ep_tuple maybe. We'll set new_ep = None for omega move? 
                # The ep right from y only usable first omega move; after any omega move, no. Also omega's own double step gives beta ep right, not relevant. So new_ep=None.
                new_ep = None
                side2 = "w" if beta_white else "b"
                ok,rr = inv_check(wk,bk,nwp,nbp,p,side2)
                # wait p unchanged
                if not ok:
                    results["ok"]=False; results["reason"]="after omega move "+rr; return
                # recurse
                dfs(wk,bk,nwp,nbp,p,side2,new_ep,pushes_done,omega_moves_done+1)
                if not results["ok"]:
                    return
    # determine initial side token already
    dfs(wk,bk,set(wp),set(bp),p,side_token,ep_tuple,0,0)
    return results["ok"], results["reason"]

def run_kp(pos_str, board, W, H, wrap):
    # board string like cyl:8x6
    inp = pos_str + "\n"
    cmd = [KP, "--board", board, "--frozen", "--cap", "1", "--threads", "2"]
    p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    line = p.stdout.strip().splitlines()[-1]
    # format: pos | A B
    parts = line.split("|")
    res = parts[1].strip()
    return res

def main():
    # Test a set of positions
    tests = [
        # certified wins
        ("Ka1 ka6 Pc4 pe4 b -", "cyl:8x6", True),
        ("Ka1 ka6 Pc4 pe3 b -", "cyl:8x6", True),
        ("Ka1 ka6 Pc3 pe3 w -", "cyl:8x6", True),
    ]
    for pos, board, _ in tests:
        # parse
        toks = pos.split()
        # identify beta: White if p uppercase? We'll just test beta=White for these
        wk,bk,wp,bp,side,ep_raw = pos_from_str(pos, 8, 6)
        # ep tuple
        side_token = side
        ep_tuple = None
        if ep_raw is not None:
            # ep_raw ("target", sq)
            sq = ep_raw[1]
            f = ord(sq[0])-97; r = int(sq[1:])
            capt_side = side_token  # side to move captures
            if capt_side == "w":
                captured = (f, r+1)
            else:
                captured = (f, r-1)
            ep_tuple = ((f,r), captured, "W" if capt_side=="w" else "B")
        # choose p: first beta pawn with passed? We'll try Pc4 etc. For these tests p = c4 (2,4)
        # beta_white True
        beta_white = True
        # find a certified p: choose p manually
        p = (2,4) if "Pc4" in pos else (2,3)
        okh, reasonh = check_hypotheses(wk,bk,wp,bp,side_token,beta_white,p,8,6,True,ep_tuple)
        oki, reasoni = simulate_invariants(wk,bk,wp,bp,side_token,beta_white,p,8,6,True,ep_tuple)
        kp = run_kp(pos, board, 8, 6, True)
        print(f"{pos} | hyp={okh}({reasonh}) inv={oki}({reasoni}) kp={kp}")

if __name__ == "__main__":
    main()
