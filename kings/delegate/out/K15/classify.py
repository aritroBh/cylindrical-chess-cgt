import sys, os, itertools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from cylcgt import pawns as P

def name(f,r): return f"{chr(ord('a')+f)}{r}"

class Pos:
    __slots__=('W','H','wk','bk','wp','bp')
    def __init__(self,W,H,wk,bk,wp,bp):
        self.W=W;self.H=H;self.wk=wk;self.bk=bk
        self.wp=frozenset(wp);self.bp=frozenset(bp)

def adj(f1,f2,W):
    d=(f2-f1)%W
    return d==1 or d==W-1

def pawn_attacks_square(pawns, side, sq, W, H):
    # side: color of pawn owner; sq attacked by that side's pawns?
    f,r = sq
    if side=='W':
        # white pawn attacks from (f-1,r-1),(f+1,r-1)
        for df in (-1,1):
            g=(f+df)%W  # if wrap always; but group may be on cylinder yes
            if (g, r-1) in pawns:
                return True
    else:
        for df in (-1,1):
            g=(f+df)%W
            if (g, r+1) in pawns:
                return True
    return False

def king_moves(pos, side):
    W=pos.W; H=pos.H
    if side=='W':
        king=pos.wk; own=pos.wp; opp=pos.bp; opp_king=pos.bk
    else:
        king=pos.bk; own=pos.bp; opp=pos.wp; opp_king=pos.wk
    f,r=king
    res=[]
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            nf=(f+df)%W
            nr=r+dr
            if not (1<=nr<=H): continue
            if (nf,nr)==opp_king: continue
            if (nf,nr) in own: continue
            # adjacency to opp king
            if abs(nr-opp_king[1])<=1 and ((opp_king[0]-nf)%W in (0,1,W-1)):
                # kings adjacent?
                if (opp_king[0]==nf and opp_king[1]==nr): 
                    continue
                # adjacent squares:
                dfk=(opp_king[0]-nf)%W
                if dfk==W-1: dfk=-1
                if abs(dfk)<=1 and abs(opp_king[1]-nr)<=1:
                    continue
            capturing = (nf,nr) in opp
            # attacked by opp pawns?
            opp_color = 'B' if side=='W' else 'W'
            # opponent pawns attack destination if side's king moves there? Destination attacked by OPPONENT pawns (opp_color)
            if pawn_attacks_square(opp if side=='W' else own, opp_color, (nf,nr), W, H):
                # Wait opp pawns are opponent's pawns, color opp_color. own? Let's fix below.
                pass
            # correct: destination attacked by opponent's pawns (opp)
            if pawn_attacks_square(opp, opp_color, (nf,nr), W, H):
                continue
            # build new pos
            if side=='W':
                new_wk=(nf,nr)
                new_wp=own
                new_bp = opp - {(nf,nr)} if capturing else opp
                new_bk=opp_king
                newpos=Pos(W,H,new_wk,new_bk,new_wp,new_bp)
            else:
                new_bk=(nf,nr)
                new_bp=own
                new_wp = opp - {(nf,nr)} if capturing else opp
                new_wk=opp_king
                newpos=Pos(W,H,new_wk,new_bk,new_wp,new_bp)
            res.append(((f,r),(nf,nr),newpos,capturing))
    return res

# fix pawn_attacks_square call: opp color determined by owner of opp pawns
def opp_color(side):
    return 'B' if side=='W' else 'W'

# We'll just rewrite king_moves cleanly:
def king_moves2(pos, side):
    W=pos.W; H=pos.H
    if side=='W':
        king=pos.wk; own=pos.wp; opp=pos.bp; opp_king=pos.bk
    else:
        king=pos.bk; own=pos.bp; opp=pos.wp; opp_king=pos.wk
    f,r=king
    oc = 'B' if side=='W' else 'W'  # color of opp pawns
    res=[]
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            nf=(f+df)%W
            nr=r+dr
            if not (1<=nr<=H): continue
            if (nf,nr)==opp_king: continue
            if (nf,nr) in own: continue
            # adjacency
            dfk=(opp_king[0]-nf)%W
            if dfk>W//2: dfk-=W
            drk=opp_king[1]-nr
            if abs(dfk)<=1 and abs(drk)<=1:
                continue
            if pawn_attacks_square(opp, oc, (nf,nr), W, H):
                continue
            capturing = (nf,nr) in opp
            if side=='W':
                newpos=Pos(W,H,(nf,nr),opp_king, own, (opp-{(nf,nr)} if capturing else opp))
            else:
                newpos=Pos(W,H,opp_king,(nf,nr), (opp-{(nf,nr)} if capturing else opp), own)
            res.append(((f,r),(nf,nr),newpos,capturing))
    return res

king_moves = king_moves2

def has_capture(pos, side):
    W=pos.W;H=pos.H
    # king captures
    for (u,v,np,cap) in king_moves(pos, side):
        if cap:
            return True
    # pawn captures
    if side=='W':
        pawns=pos.wp; opp=pos.bp
    else:
        pawns=pos.bp; opp=pos.wp
    d=1 if side=='W' else -1
    for (f,r) in pawns:
        r1=r+d
        if not (1<=r1<=H): continue
        for df in (-1,1):
            g=(f+df)%W
            if (g,r1) in opp:
                return True
    return False

def legal_king_move(pos, side, u, v):
    for (uu,vv,np,cap) in king_moves(pos, side):
        if uu==u and vv==v and not cap:
            return True
    return False

Fset_of = lambda F, start, W: set((start+i)%W for i in range(F))

def opponent_frozen(pos, T, Fset):
    W=pos.W; H=pos.H
    S = 'W' if T=='B' else 'B'
    for (u,v,np,cap) in king_moves(pos, T):
        if v[0] not in Fset:
            continue
        if cap:
            return False  # captures our pawn: decisive, not frozen
        # reversible king move => opponent has a shuttle/escape
        if legal_king_move(np, T, v, u):
            return False
    # decisive pawn move by opponent
    if side_has_decisive_pawn_move(pos, T, W, H):
        return False
    return True

def has_safe_shuttle(pos, side, Fset):
    T = 'B' if side=='W' else 'W'
    if not opponent_frozen(pos, T, Fset):
        return False
    for (u,v,np,cap) in king_moves(pos, side):
        if cap: continue
        if u[0] not in Fset or v[0] not in Fset: continue
        # reverse
        if not legal_king_move(np, side, v, u):
            continue
        if not opponent_frozen(np, T, Fset):
            continue
        return True
    return False

def creates_passer(pos, side, W, H):
    # after a move? This function checks a position already; we'll check moves separately.
    return False

def side_has_decisive_pawn_move(pos, side, W, H):
    # exists a legal pawn move by side such that after it, side has a passed pawn (cylcgt) and no? 
    board = P.Board(W, H, True, True)
    # generate pawn moves manually
    if side=='W':
        pawns=pos.wp; opp=pos.bp; own_king=pos.wk
    else:
        pawns=pos.bp; opp=pos.wp; own_king=pos.bk
    d=1 if side=='W' else -1
    start=2 if side=='W' else H-1
    occ=pos.wp | pos.bp
    for (f,r) in pawns:
        rest = pawns - {(f,r)}
        # single step
        r1=r+d
        if 1<=r1<=H and (f,r1) not in occ:
            new_mine = rest | {(f,r1)}
            if side=='W':
                npos = P.Pos(frozenset(new_mine), frozenset(opp))
            else:
                npos = P.Pos(frozenset(opp), frozenset(new_mine))
            if P.passed(board, npos, side) and not P.passed(board, npos, 'B' if side=='W' else 'W'):
                return True
        # double step
        r2=r+2*d
        if r==start and 1<=r2<=H and (f,r1) not in occ and (f,r2) not in occ:
            new_mine = rest | {(f,r2)}
            if side=='W':
                npos = P.Pos(frozenset(new_mine), frozenset(opp))
            else:
                npos = P.Pos(frozenset(opp), frozenset(new_mine))
            if P.passed(board, npos, side) and not P.passed(board, npos, 'B' if side=='W' else 'W'):
                return True
        # captures
        for df in (-1,1):
            g=(f+df)%W
            r1=r+d
            if not (1<=r1<=H): continue
            t=(g,r1)
            if t in opp:
                new_mine = rest | {t}
                new_opp = opp - {t}
                if side=='W':
                    npos = P.Pos(frozenset(new_mine), frozenset(new_opp))
                else:
                    npos = P.Pos(frozenset(new_opp), frozenset(new_mine))
                if P.passed(board, npos, side) and not P.passed(board, npos, 'B' if side=='W' else 'W'):
                    return True
    return False

def root_no_passer(W,H,wp,bp):
    board=P.Board(W,H,True,True)
    pos=P.Pos(frozenset(wp), frozenset(bp))
    return (not P.passed(board,pos,'W')) and (not P.passed(board,pos,'B'))

def classify(W,H,wk,bk,wp,bp):
    pos=Pos(W,H,wk,bk,wp,bp)
    Fset=set(range(W))  # group may be subset; but for shuttle inside group we need group files. We'll pass Fset separately.
    return pos

def classify_with_files(W,H,wk,bk,wp,bp, group_files):
    Fset=set(group_files)
    pos=Pos(W,H,wk,bk,wp,bp)
    ws=has_safe_shuttle(pos,'W',Fset)
    bs=has_safe_shuttle(pos,'B',Fset)
    # decisive pawn moves
    wdec=side_has_decisive_pawn_move(pos,'W',W,H)
    bdec=side_has_decisive_pawn_move(pos,'B',W,H)
    if ws and not bs:
        if bdec:
            return 'other'  # black has decisive, not pure on?
        return 'on'
    if bs and not ws:
        if wdec:
            # over? white has decisive move; check if it leads to frozen
            # count white moves to frozen
            cnt=0
            # king moves
            for (u,v,np,cap) in king_moves(pos,'W'):
                if cap: continue
                if u[0] not in Fset or v[0] not in Fset: 
                    # could be decisive pawn? handled separately
                    pass
                # check if after move black no shuttle and frozen-ish
                if not has_safe_shuttle(np,'B',Fset) and not side_has_decisive_pawn_move(np,'B',W,H):
                    # also white no shuttle? 
                    if not has_safe_shuttle(np,'W',Fset):
                        cnt+=1
            # pawn moves that create frozen?
            # We'll also count pawn moves that remove black shuttle: hard; skip for now
            if cnt==1:
                return 'over'
            return 'other'
        return 'off'
    if ws and bs:
        return 'dud'
    # neither shuttle
    if wdec or bdec:
        return 'other'
    return 'frozen'

if __name__=='__main__':
    # quick test known Z_onT1
    W,H=7,6
    wk=(0,5); bk=(2,6)
    wp=[(1,4),(2,5)]
    bp=[(1,5)]
    files=[0,1,2]
    print('Z_onT1', classify_with_files(W,H,wk,bk,wp,bp,files))
