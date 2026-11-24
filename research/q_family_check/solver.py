import sys, time

def parse_tokens(tokens, n):
    whites = []
    blacks = []
    for fi, tok in enumerate(tokens):
        # tok like W4, B7, W3B6, B4W2? We expect tokens already split by file
        i = 0
        # parse all W/B groups
        while i < len(tok):
            c = tok[i]
            i += 1
            j = i
            while j < len(tok) and tok[j].isdigit():
                j += 1
            rank = int(tok[i:j])
            i = j
            if c == 'W':
                whites.append((fi, rank))
            elif c == 'B':
                blacks.append((fi, rank))
            else:
                raise ValueError(tok)
    assert len(tokens) == n, (len(tokens), n)
    return whites, blacks

def make_q(n):
    k = (n-8)//2
    toks = ['W4','B7']
    for _ in range(k):
        toks += ['B4','W2']
    toks += ['W3B6','W3','W2B5','B5','W2','B4']
    assert len(toks)==n, (n, len(toks))
    return toks

def make_p8():
    return ['W5','B7','W4','W4B7','B6','W3B6','W2','B4']

def adj(f,n):
    return {(f-1)%n, f, (f+1)%n}

def passed(whites, blacks, n, ep):
    # returns (white_passed_list, black_passed_list)
    wp=[]
    for (f,r) in whites:
        bad=False
        for (gf,gr) in blacks:
            if gf in adj(f,n) and gr > r:
                bad=True;break
        if bad: continue
        if ep is not None and (f,r)==(ep[2],ep[3]):
            continue
        wp.append((f,r))
    bp=[]
    for (f,r) in blacks:
        bad=False
        for (gf,gr) in whites:
            if gf in adj(f,n) and gr < r:
                bad=True;break
        if bad: continue
        if ep is not None and (f,r)==(ep[2],ep[3]):
            continue
        bp.append((f,r))
    return wp,bp

class Solver:
    def __init__(self,n,whites,blacks):
        self.n=n
        self.memo={}
        self.initW=tuple(sorted(whites))
        self.initB=tuple(sorted(blacks))

    def occ(self, W,B,f,r):
        return (f,r) in W or (f,r) in B

    def solve(self, W, B, ep, heap, side):
        # W,B tuples sorted
        key=(W,B,ep,heap,side)
        if key in self.memo:
            return self.memo[key]
        # terminal check
        wp,bp = passed(W,B,self.n,ep)
        if wp or bp:
            # terminal fixed
            if wp and not bp:
                w=0
            elif bp and not wp:
                w=1
            else:
                wm=min(8-r for (_,r) in wp)
                bm=min(r-1 for (_,r) in bp)
                if wm < bm:
                    w=0
                elif bm < wm:
                    w=1
                else:
                    # unknown mover; shouldn't happen for non-start terminal; default side? 
                    w=0
            self.memo[key]=w
            return w
        # generate moves
        moves=[]
        Wset=set(W); Bset=set(B)
        if side==0:
            # white board moves
            for (f,r) in W:
                # forward one
                if r+1<=8 and not self.occ(Wset,Bset,f,r+1):
                    nW=list(W); nW.remove((f,r)); nW.append((f,r+1)); nW=sorted(nW)
                    nB=B
                    newep=None
                    # terminal?
                    wp2,bp2=passed(tuple(nW),nB,self.n,newep)
                    if wp2 or bp2:
                        # determine winner with mover=white(0)
                        if wp2 and not bp2: tw=0
                        elif bp2 and not wp2: tw=1
                        else:
                            wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                            if wm<bm: tw=0
                            elif bm<wm: tw=1
                            else: tw=1 # tie, did not just move (black) wins
                        moves.append(('term',tw))
                    else:
                        moves.append(('state',(tuple(nW),nB,newep,heap,1)))
                # double step
                if r==2:
                    if not self.occ(Wset,Bset,f,3) and not self.occ(Wset,Bset,f,4):
                        nW=list(W); nW.remove((f,2)); nW.append((f,4)); nW=sorted(nW)
                        nB=B
                        newep=(f,3,f,4)
                        wp2,bp2=passed(tuple(nW),nB,self.n,newep)
                        if wp2 or bp2:
                            if wp2 and not bp2: tw=0
                            elif bp2 and not wp2: tw=1
                            else:
                                wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                                if wm<bm: tw=0
                                elif bm<wm: tw=1
                                else: tw=1
                            moves.append(('term',tw))
                        else:
                            moves.append(('state',(tuple(nW),nB,newep,heap,1)))
                # captures
                for df in (-1,1):
                    f2=(f+df)%self.n
                    r2=r+1
                    if r2<=8 and (f2,r2) in Bset:
                        nW=list(W); nW.remove((f,r)); nW.append((f2,r2)); nW=sorted(nW)
                        nB=[p for p in B if p!=(f2,r2)]
                        nB=sorted(nB)
                        newep=None
                        wp2,bp2=passed(tuple(nW),tuple(nB),self.n,newep)
                        if wp2 or bp2:
                            if wp2 and not bp2: tw=0
                            elif bp2 and not wp2: tw=1
                            else:
                                wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                                if wm<bm: tw=0
                                elif bm<wm: tw=1
                                else: tw=1
                            moves.append(('term',tw))
                        else:
                            moves.append(('state',(tuple(nW),tuple(nB),newep,heap,1)))
            # en passant (white captures black's double step)
            if ep is not None:
                tf,tr,cf,cr = ep
                for (f,r) in W:
                    if tr==r+1 and ((tf==(f+1)%self.n) or (tf==(f-1)%self.n)):
                        if not self.occ(Wset,Bset,tf,tr):
                            # captured pawn must exist
                            if (cf,cr) in Bset:
                                nW=list(W); nW.remove((f,r)); nW.append((tf,tr)); nW=sorted(nW)
                                nB=[p for p in B if p!=(cf,cr)]
                                nB=sorted(nB)
                                newep=None
                                wp2,bp2=passed(tuple(nW),tuple(nB),self.n,newep)
                                if wp2 or bp2:
                                    if wp2 and not bp2: tw=0
                                    elif bp2 and not wp2: tw=1
                                    else:
                                        wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                                        if wm<bm: tw=0
                                        elif bm<wm: tw=1
                                        else: tw=1
                                    moves.append(('term',tw))
                                else:
                                    moves.append(('state',(tuple(nW),tuple(nB),newep,heap,1)))
            # heap moves
            if heap>0:
                for h2 in range(heap):
                    moves.append(('state',(W,B,None,h2,1)))
        else:
            # black board moves
            for (f,r) in B:
                # forward one (down)
                if r-1>=1 and not self.occ(Wset,Bset,f,r-1):
                    nB=list(B); nB.remove((f,r)); nB.append((f,r-1)); nB=sorted(nB)
                    nW=W
                    newep=None
                    wp2,bp2=passed(nW,tuple(nB),self.n,newep)
                    if wp2 or bp2:
                        if wp2 and not bp2: tw=0
                        elif bp2 and not wp2: tw=1
                        else:
                            wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                            if wm<bm: tw=0
                            elif bm<wm: tw=1
                            else: tw=0 # tie, did not just move (white) wins
                        moves.append(('term',tw))
                    else:
                        moves.append(('state',(nW,tuple(nB),newep,heap,0)))
                # double step
                if r==7:
                    if not self.occ(Wset,Bset,f,6) and not self.occ(Wset,Bset,f,5):
                        nB=list(B); nB.remove((f,7)); nB.append((f,5)); nB=sorted(nB)
                        nW=W
                        newep=(f,6,f,5)
                        wp2,bp2=passed(nW,tuple(nB),self.n,newep)
                        if wp2 or bp2:
                            if wp2 and not bp2: tw=0
                            elif bp2 and not wp2: tw=1
                            else:
                                wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                                if wm<bm: tw=0
                                elif bm<wm: tw=1
                                else: tw=0
                            moves.append(('term',tw))
                        else:
                            moves.append(('state',(nW,tuple(nB),newep,heap,0)))
                # captures
                for df in (-1,1):
                    f2=(f+df)%self.n
                    r2=r-1
                    if r2>=1 and (f2,r2) in Wset:
                        nB=list(B); nB.remove((f,r)); nB.append((f2,r2)); nB=sorted(nB)
                        nW=[p for p in W if p!=(f2,r2)]
                        nW=sorted(nW)
                        newep=None
                        wp2,bp2=passed(tuple(nW),tuple(nB),self.n,newep)
                        if wp2 or bp2:
                            if wp2 and not bp2: tw=0
                            elif bp2 and not wp2: tw=1
                            else:
                                wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                                if wm<bm: tw=0
                                elif bm<wm: tw=1
                                else: tw=0
                            moves.append(('term',tw))
                        else:
                            moves.append(('state',(tuple(nW),tuple(nB),newep,heap,0)))
            # en passant (black captures white's double step)
            if ep is not None:
                tf,tr,cf,cr = ep
                for (f,r) in B:
                    if tr==r-1 and ((tf==(f+1)%self.n) or (tf==(f-1)%self.n)):
                        if not self.occ(Wset,Bset,tf,tr):
                            if (cf,cr) in Wset:
                                nB=list(B); nB.remove((f,r)); nB.append((tf,tr)); nB=sorted(nB)
                                nW=[p for p in W if p!=(cf,cr)]
                                nW=sorted(nW)
                                newep=None
                                wp2,bp2=passed(tuple(nW),tuple(nB),self.n,newep)
                                if wp2 or bp2:
                                    if wp2 and not bp2: tw=0
                                    elif bp2 and not wp2: tw=1
                                    else:
                                        wm=min(8-r for (_,r) in wp2); bm=min(r-1 for (_,r) in bp2)
                                        if wm<bm: tw=0
                                        elif bm<wm: tw=1
                                        else: tw=0
                                    moves.append(('term',tw))
                                else:
                                    moves.append(('state',(tuple(nW),tuple(nB),newep,heap,0)))
            # heap moves
            if heap>0:
                for h2 in range(heap):
                    moves.append(('state',(W,B,None,h2,0)))
        if not moves:
            # no legal move: side to move loses
            winner = 1-side
            self.memo[key]=winner
            return winner
        # minimax: current side wins if any move leads to win for side
        for m in moves:
            if m[0]=='term':
                w=m[1]
            else:
                st=m[1]
                w=self.solve(st[0],st[1],st[2],st[3],st[4])
            if w==side:
                self.memo[key]=side
                return side
        self.memo[key]=1-side
        return 1-side

def classify(n, whites, blacks):
    res={}
    for h in range(5):
        sol=Solver(n,whites,blacks)
        wf=sol.solve(tuple(sorted(whites)),tuple(sorted(blacks)),None,h,0)
        bf=sol.solve(tuple(sorted(whites)),tuple(sorted(blacks)),None,h,1)
        if wf==0 and bf==1:
            cls='N'
        elif wf==1 and bf==0:
            cls='P'
        elif wf==0 and bf==0:
            cls='L'
        else:
            cls='R'
        res[h]=(cls,wf,bf,sol.memo.__len__())
        print(f"n={n} h={h}: {cls} (white-first winner={'W' if wf==0 else 'B'}, black-first winner={'B' if bf==1 else 'W'}) states={len(sol.memo)}", flush=True)
    return res

if __name__=='__main__':
    import argparse
    # command: python solver.py q 8  (or p8, control)
    mode=sys.argv[1]
    if mode=='q':
        n=int(sys.argv[2])
        toks=make_q(n)
    elif mode=='qmod':
        n=int(sys.argv[2])
        toks=make_q(n)
        # move black pawn file1 rank7->6
        # parse then modify
    elif mode=='p8':
        n=8
        toks=make_p8()
    else:
        # custom tokens
        n=int(sys.argv[2])
        toks=sys.argv[3:]
    whites,blacks=parse_tokens(toks,n)
    if mode=='qmod':
        # change file1 black rank7 to 6
        blacks=[(f,r-1) if (f==1 and r==7) else (f,r) for (f,r) in blacks]
    print("tokens:", toks)
    print("whites:", whites)
    print("blacks:", blacks)
    t0=time.time()
    res=classify(n,whites,blacks)
    print("time:", time.time()-t0)
