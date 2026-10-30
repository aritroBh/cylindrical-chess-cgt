import itertools, json, os
from cylcgt import pawns as P

OUT = os.path.dirname(os.path.abspath(__file__))

def board(W,H): return P.Board(W,H,True,True)

def rho(f,r,beta_white,H):
    return r if beta_white else H+1-r

def is_white_beta(beta): return beta=='W'

def king_dist(f1,r1,f2,r2,W):
    df = abs(f1-f2)
    df = min(df, W-df)
    dr = abs(r1-r2)
    return max(df,dr)

def adj_files(f,W):
    return {(f-1)%W, f, (f+1)%W}

def passed_pawn_list(board, pos, side, H):
    # return list of pawns (f,r) of side that are passed in cylcgt e.p.-aware sense
    mine = pos.white if side=='W' else pos.black
    theirs = pos.black if side=='W' else pos.white
    res=[]
    for (f,r) in mine:
        files = {f} | {g for g in (board.nb(f,-1), board.nb(f,1)) if g is not None}
        if side=='W':
            blocked = any(g in files and s > r for (g,s) in theirs)
        else:
            blocked = any(g in files and s < r for (g,s) in theirs)
        if blocked:
            continue
        # ep capturable
        if P.ep_capturable(board, pos, side, (f,r)):
            continue
        res.append((f,r))
    return res

def has_passed_side(board,pos,side,H):
    return len(passed_pawn_list(board,pos,side,H))>0

def legality(board, pos, stm, W,H):
    # side not to move not in check; kings fixed; pawns valid
    wk=(0,1); bk=(0,H)
    # pawns on valid ranks
    for (f,r) in pos.white | pos.black:
        if r<2 or r>H-1: return False
    # no overlap
    if pos.white & pos.black: return False
    if wk in pos.white or wk in pos.black or bk in pos.white or bk in pos.black: return False
    if wk==bk: return False
    # kings adjacent?
    if king_dist(wk[0],wk[1],bk[0],bk[1],W)<=1: return False
    # side not to move not in check by enemy pawns
    notm = 'B' if stm=='W' else 'W'
    king = wk if notm=='W' else bk
    enemy = pos.black if notm=='W' else pos.white
    # enemy pawns attack king
    for (f,r) in enemy:
        # pawn attacks diagonally toward its promotion side
        if notm=='W':
            # enemy black pawns attack downward? Actually black pawns move down, attack down-left/down-right from their square? 
            # A black pawn on (f,r) attacks (f±1, r-1). King in check if king == one of those.
            for df in (-1,1):
                g = (f+df)%W if board.wrap else f+df
                if 0<=g<W and r-1>=1 and (g,r-1)==king:
                    return False
        else:
            for df in (-1,1):
                g = (f+df)%W if board.wrap else f+df
                if 0<=g<W and r+1<=H and (g,r+1)==king:
                    return False
    # also if king adjacent to enemy king? already.
    return True

def ep_variants_for_config(Wp, Bp, stm, W, H):
    # yield ep tuple or None already handled separately; this yields possible ep (target,captured,stm) with capturer=stm
    opp = 'B' if stm=='W' else 'W'
    opp_pawns = Wp if opp=='W' else Bp
    stm_pawns = Bp if opp=='W' else Wp  # wait stm pawns are opposite opp
    # Actually if stm='W', capturer white; mover black. stm_pawns = white pawns = Wp.
    stm_pawns = Wp if stm=='W' else Bp
    mover_pawns = Bp if stm=='W' else Wp
    # landing rank for mover double step
    if opp=='W':
        landing_rank = 4
        skipped_rank = 3
        origin_rank = 2
        dstep = +2  # not needed
    else:
        landing_rank = H-3
        skipped_rank = H-2
        origin_rank = H-1
    if landing_rank < 2 or landing_rank > H-1:
        return []
    variants=[]
    # for each mover pawn at landing rank
    for (f,r) in mover_pawns:
        if r != landing_rank:
            continue
        origin = (f, origin_rank)
        skipped = (f, skipped_rank)
        # origin and skipped must be empty in current config
        allp = set(Wp)|set(Bp)
        if origin in allp or skipped in allp:
            continue
        # kings not on origin/skipped
        if origin==(0,1) or origin==(0,H) or skipped==(0,1) or skipped==(0,H):
            continue
        # capturer adjacent at landing rank
        capturers=0
        for df in (-1,1):
            g = (f+df)%W  # wrap cylinder
            if (g, landing_rank) in stm_pawns:
                capturers+=1
        if capturers==0:
            continue
        # legality of double step: mover king not in check after move (same as base) handled by caller
        variants.append((skipped, (f,landing_rank), stm))
    # dedup by target file? multiple pawns? landing ranks same file unique; dedup
    uniq=[]
    seen=set()
    for v in variants:
        if v[0] not in seen:
            seen.add(v[0]); uniq.append(v)
    return uniq

def make_pos(Wp, Bp, ep):
    return P.Pos(frozenset(Wp), frozenset(Bp), ep)

def gen_board(W,H,K):
    avail = [(f,r) for f in range(2,W-1) for r in range(2,H)]
    # combinations of white and black disjoint
    roots=[]
    # precompute combos by size
    combos_by_size = {k: list(itertools.combinations(avail,k)) for k in range(K+1)}
    # iterate
    total_configs=0
    for kw in range(K+1):
        for kb in range(K+1):
            for wc in combos_by_size[kw]:
                wset=set(wc)
                rem=[s for s in avail if s not in wset]
                # black combos from rem
                for bc in itertools.combinations(rem,kb):
                    bset=set(bc)
                    total_configs+=1
    # too many? We'll just iterate and process roots directly
    return avail

def process_board(W,H,K):
    avail = [(f,r) for f in range(2,W-1) for r in range(2,H)]
    board = P.Board(W,H,True,True)
    roots_out=[]  # list of dicts
    # iterate configs
    for kw in range(K+1):
        for kb in range(K+1):
            for wc in itertools.combinations(avail,kw):
                wset=set(wc)
                rem=[s for s in avail if s not in wset]
                for bc in itertools.combinations(rem,kb):
                    bset=set(bc)
                    Wp=list(wset); Bp=list(bset)
                    for stm in ('W','B'):
                        # base no ep
                        pos0 = P.Pos(frozenset(Wp), frozenset(Bp), None)
                        if not legality(board, pos0, stm, W, H):
                            continue
                        # has passer?
                        wp = has_passed_side(board,pos0,'W',H)
                        bp = has_passed_side(board,pos0,'B',H)
                        if not (wp or bp):
                            # still ep variants might create passer; handle below
                            pass
                        # base root if has passer
                        if wp or bp:
                            roots_out.append((W,H,Wp,Bp,None,stm))
                        # ep variants
                        variants = ep_variants_for_config(Wp,Bp,stm,W,H)
                        for (skipped, captured, capside) in variants:
                            ep = (skipped, captured, capside)
                            pos1 = P.Pos(frozenset(Wp), frozenset(Bp), ep)
                            if not legality(board, pos1, stm, W, H):
                                continue
                            wp1 = has_passed_side(board,pos1,'W',H)
                            bp1 = has_passed_side(board,pos1,'B',H)
                            if wp1 or bp1:
                                roots_out.append((W,H,Wp,Bp,ep,stm))
    # dedup
    seen=set()
    uniq=[]
    for r in roots_out:
        Wp,Bp,ep,stm = r[2],r[3],r[4],r[5]
        key=(frozenset(Wp),frozenset(Bp), ep, stm)
        if key in seen: continue
        seen.add(key); uniq.append(r)
    return uniq, board

if __name__=='__main__':
    specs = [(6,6,3),(7,6,3),(8,6,2)]
    # maybe 7x6 3 may be large; we'll run and see
    allroots=[]
    for (W,H,K) in specs:
        uniq,board = process_board(W,H,K)
        print(W,H,K,'roots',len(uniq))
        for r in uniq:
            allroots.append(r)
    # save
    with open(os.path.join(OUT,'roots.json'),'w') as f:
        # convert ep tuple with tuples to lists
        serial=[]
        for (W,H,Wp,Bp,ep,stm) in allroots:
            serial.append({'W':W,'H':H,'Wp':Wp,'Bp':Bp,'ep': (list(ep[0]),list(ep[1]),ep[2]) if ep else None,'stm':stm})
        json.dump(serial,f)
    print('total',len(allroots))
