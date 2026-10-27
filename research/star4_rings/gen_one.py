import sys

def parse_token(tok):
    # returns (set white ranks, set black ranks)
    w=set(); b=set()
    mode=None
    for ch in tok:
        if ch=='W': mode='w'
        elif ch=='B': mode='b'
        elif ch.isdigit():
            r=int(ch)
            if mode=='w': w.add(r)
            elif mode=='b': b.add(r)
    return w,b

def make_token(wset,bset):
    t=""
    if wset: t+="W"+"".join(str(r) for r in sorted(wset))
    if bset: t+="B"+"".join(str(r) for r in sorted(bset))
    return t if t else "-"

def parse_pos(s):
    return [parse_token(t) for t in s.split()]

def fmt_pos(plist):
    return " ".join(make_token(w,b) for w,b in plist)

RANKS=range(2,8)

def has_passed(plist, side, textbook=False, ep=None):
    # ep: (file_index, holder) or None; holder 0 white may capture? We'll ignore ep for filter? Need implement for accuracy.
    n=len(plist)
    def fm(f): return (f-1)%n
    def fp(f): return (f+1)%n
    for f in range(n):
        wset,bset=plist[f]
        mine = wset if side==0 else bset
        if not mine: continue
        for r in mine:
            a=fm(f); c=fp(f)
            if side==0:
                bn = plist[a][1] | plist[f][1] | plist[c][1]
                blocked = any(rr>=r for rr in bn) # enemy at rank >= r? rg: bn >> r (ranks r+1..8)
                # Actually blocked if black pawn on rank > r (since white moves up). bn >> r means rank r+1..8.
                blocked = any(rr > r for rr in bn)
            else:
                wn = plist[a][0] | plist[f][0] | plist[c][0]
                blocked = any(rr < r for rr in wn)
            if blocked: continue
            # ep protection
            if not textbook:
                if side==0 and ep is not None and ep[0]==f and ep[1]==1 and r==4:
                    continue
                if side==1 and ep is not None and ep[0]==f and ep[1]==0 and r==5:
                    continue
            return True
    return False

def any_passed(plist):
    return has_passed(plist,0) or has_passed(plist,1)

def add_pawn_candidates(plist):
    cands=set()
    n=len(plist)
    for fi in range(n):
        wset,bset=plist[fi]
        occupied=wset|bset
        for color in (0,1):
            for r in RANKS:
                if r in occupied: continue
                new=[(set(w),set(b)) for w,b in plist]
                if color==0: new[fi][0].add(r)
                else: new[fi][1].add(r)
                # convert to tuples
                new2=[(frozenset(w),frozenset(b)) for w,b in new]
                if any_passed(new2): 
                    pass
                pos=fmt_pos(new2)
                if not any_passed(new2):
                    cands.add(pos)
    return cands

def add_pair_candidates(plist):
    cands=set()
    n=len(plist)
    for i in range(n):
        j=(i+1)%n
        # W on i, B on j
        for r1 in RANKS:
            wset_i,bset_i=plist[i]
            if r1 in (wset_i|bset_i): continue
            for r2 in RANKS:
                wset_j,bset_j=plist[j]
                if r2 in (wset_j|bset_j): continue
                new=[(set(w),set(b)) for w,b in plist]
                new[i][0].add(r1)
                new[j][1].add(r2)
                new2=[(frozenset(w),frozenset(b)) for w,b in new]
                if not any_passed(new2):
                    cands.add(fmt_pos(new2))
        # B on i, W on j
        for r1 in RANKS:
            wset_i,bset_i=plist[i]
            if r1 in (wset_i|bset_i): continue
            for r2 in RANKS:
                wset_j,bset_j=plist[j]
                if r2 in (wset_j|bset_j): continue
                new=[(set(w),set(b)) for w,b in plist]
                new[i][1].add(r1)
                new[j][0].add(r2)
                new2=[(frozenset(w),frozenset(b)) for w,b in new]
                if not any_passed(new2):
                    cands.add(fmt_pos(new2))
    return cands

def insert_file_candidates(plist):
    cands=set()
    n=len(plist)
    # possible new file tokens (as (wset,bset)) with 1 or 2 pawns
    newfiles=[]
    for r in RANKS:
        newfiles.append((frozenset([r]),frozenset()))
        newfiles.append((frozenset(),frozenset([r])))
    for r1 in RANKS:
        for r2 in RANKS:
            if r1<r2:
                newfiles.append((frozenset([r1,r2]),frozenset()))
                newfiles.append((frozenset(),frozenset([r1,r2])))
    for r1 in RANKS:
        for r2 in RANKS:
            newfiles.append((frozenset([r1]),frozenset([r2])))
    newfiles=list(set(newfiles))
    # insert one new file at any gap
    for gap in range(n+1):
        for nf in newfiles:
            new=plist[:gap]+[ (set(nf[0]),set(nf[1])) ]+plist[gap:]
            new2=[(frozenset(w),frozenset(b)) for w,b in new]
            if not any_passed(new2):
                cands.add(fmt_pos(new2))
    # insert two new files at same gap, each holding exactly one pawn (total 2 pawns)
    single_files=[(frozenset([r]),frozenset()) for r in RANKS]+[(frozenset(),frozenset([r])) for r in RANKS]
    single_files=list(set(single_files))
    for gap in range(n+1):
        for nf1 in single_files:
            for nf2 in single_files:
                new=plist[:gap]+[(set(nf1[0]),set(nf1[1])),(set(nf2[0]),set(nf2[1]))]+plist[gap:]
                new2=[(frozenset(w),frozenset(b)) for w,b in new]
                if not any_passed(new2):
                    cands.add(fmt_pos(new2))
    return cands

def star1_group_files():
    # single file W r / B r+2
    res=set()
    for r in range(2,7): # r+2 <=8? r+2<=7? allow r+2<=8? pawn rank 8 illegal? B on rank 8 is promoted? use <=7
        if r+2<=7:
            res.add((frozenset([r]),frozenset([r+2])))
    # also maybe W3 B5 etc covered by r loop
    return res

def attach_star1_candidates(plist):
    cands=set()
    n=len(plist)
    groups=star1_group_files()
    for gap in range(n+1):
        for g in groups:
            new=plist[:gap]+[(set(g[0]),set(g[1]))]+plist[gap:]
            new2=[(frozenset(w),frozenset(b)) for w,b in new]
            if not any_passed(new2):
                cands.add(fmt_pos(new2))
    return cands

if __name__=="__main__":
    seed=sys.argv[1]
    pl=parse_pos(seed)
    pl=[(set(w),set(b)) for w,b in pl]
    pl=[(frozenset(w),frozenset(b)) for w,b in pl]
    allc=set()
    allc |= add_pawn_candidates(pl)
    allc |= add_pair_candidates(pl)
    allc |= insert_file_candidates(pl)
    allc |= attach_star1_candidates(pl)
    # remove original seed
    allc.discard(seed)
    print("seed", seed)
    print("counts a/b/c/d combined:", len(allc))
    # breakdown
    print("a", len(add_pawn_candidates(pl)))
    print("b", len(add_pair_candidates(pl)))
    print("c", len(insert_file_candidates(pl)))
    print("d", len(attach_star1_candidates(pl)))
