import sys, time

def make_q(n):
    k=(n-8)//2
    toks=['W4','B7']
    for _ in range(k):
        toks += ['B4','W2']
    toks += ['W3B6','W3','W2B5','B5','W2','B4']
    assert len(toks)==n
    return toks

def make_p8():
    return ['W5','B7','W4','W4B7','B6','W3B6','W2','B4']

def parse_tokens(toks,n):
    W=0;B=0
    for fi,tok in enumerate(toks):
        i=0
        while i<len(tok):
            c=tok[i]; i+=1
            j=i
            while j<len(tok) and tok[j].isdigit(): j+=1
            rank=int(tok[i:j]); i=j
            idx=fi*8 + (rank-1)
            if c=='W': W |= (1<<idx)
            else: B |= (1<<idx)
    return W,B

def adj_files(f,n):
    return ((f-1)%n, f, (f+1)%n)

class Solver:
    def __init__(self,n,W0,B0):
        self.n=n
        self.memo={}
        self.startW=W0
        self.startB=B0

    def bits(self,mask):
        while mask:
            lsb=mask & -mask
            yield lsb.bit_length()-1
            mask ^= lsb

    def file_of(self,idx): return idx//8
    def rank0_of(self,idx): return idx%8

    def passed(self,W,B,ep_captured):
        # ep_captured: index or -1
        wp=[]
        for i in self.bits(W):
            f=self.file_of(i); r=self.rank0_of(i)
            bad=False
            for j in self.bits(B):
                gf=self.file_of(j); gr=self.rank0_of(j)
                if gf in ((f-1)%self.n, f, (f+1)%self.n) and gr > r:
                    bad=True;break
            if bad: continue
            if ep_captured==i: continue
            wp.append(i)
        bp=[]
        for j in self.bits(B):
            f=self.file_of(j); r=self.rank0_of(j)
            bad=False
            for i in self.bits(W):
                gf=self.file_of(i); gr=self.rank0_of(i)
                if gf in ((f-1)%self.n, f, (f+1)%self.n) and gr < r:
                    bad=True;break
            if bad: continue
            if ep_captured==j: continue
            bp.append(j)
        return wp,bp

    def terminal_winner(self,wp,bp,mover):
        # mover 0 white just moved, 1 black just moved
        if wp and not bp: return 0
        if bp and not wp: return 1
        if wp and bp:
            wm=min(7-r for r in [i%8 for i in wp])  # 7-r0 = moves
            # actually moves = 7 - r0; min
            wm=min(7 - (i%8) for i in wp)
            bm=min((i%8) for i in bp)
            if wm < bm: return 0
            if bm < wm: return 1
            # tie: did not just move wins
            return 1 if mover==0 else 0
        return None

    def solve(self,W,B,ep,heap,side):
        # ep: -1 none or target*1024+captured? We'll use tuple? Use int code: if none -1 else target*200+captured
        key=(W,B,ep,heap,side)
        if key in self.memo: return self.memo[key]
        ep_captured = -1 if ep==-1 else (ep % 200)
        wp,bp=self.passed(W,B,ep_captured)
        if wp or bp:
            # terminal fixed; mover unknown but for initial terminal use side? 
            # For a terminal state reached, winner fixed; race tie needs mover. We'll handle tie by 0 (shouldn't happen init)
            if wp and not bp: w=0
            elif bp and not wp: w=1
            else:
                wm=min(7-(i%8) for i in wp)
                bm=min(i%8 for i in bp)
                if wm<bm: w=0
                elif bm<wm: w=1
                else: w=0
            self.memo[key]=w
            return w
        Wset=W; Bset=B
        moves=[]
        if side==0:
            # white
            for i in self.bits(W):
                f=i//8; r=i%8
                # forward one
                if r<7:
                    ni=i+1
                    if not (W & (1<<ni)) and not (B & (1<<ni)):
                        nW = (W ^ (1<<i)) | (1<<ni)
                        nB=B
                        newep=-1
                        wp2,bp2=self.passed(nW,nB,-1)
                        if wp2 or bp2:
                            tw=self.terminal_winner(wp2,bp2,0)
                            moves.append(('t',tw))
                        else:
                            moves.append(('s',nW,nB,newep,heap,1))
                # double
                if r==1:
                    i2=i+1; i3=i+2
                    if not (W&(1<<i2)) and not (B&(1<<i2)) and not (W&(1<<i3)) and not (B&(1<<i3)):
                        nW=(W ^ (1<<i)) | (1<<i3)
                        nB=B
                        newep=i2*200 + i3  # target=i2, captured=i3
                        wp2,bp2=self.passed(nW,nB,i3)
                        if wp2 or bp2:
                            tw=self.terminal_winner(wp2,bp2,0)
                            moves.append(('t',tw))
                        else:
                            moves.append(('s',nW,nB,newep,heap,1))
                # captures
                for df in (-1,1):
                    nf=(f+df)%self.n
                    nr=r+1
                    if nr<=7:
                        ni=nf*8+nr
                        if B & (1<<ni):
                            nW=(W ^ (1<<i)) | (1<<ni)
                            nB=B ^ (1<<ni)
                            newep=-1
                            wp2,bp2=self.passed(nW,nB,-1)
                            if wp2 or bp2:
                                tw=self.terminal_winner(wp2,bp2,0)
                                moves.append(('t',tw))
                            else:
                                moves.append(('s',nW,nB,newep,heap,1))
            # en passant
            if ep!=-1:
                target=ep//200; captured=ep%200
                tf=target//8; tr=target%8
                for i in self.bits(W):
                    f=i//8; r=i%8
                    if tr==r+1 and ((tf==(f+1)%self.n) or (tf==(f-1)%self.n)):
                        if not (W&(1<<target)) and not (B&(1<<target)):
                            if B & (1<<captured):
                                nW=(W ^ (1<<i)) | (1<<target)
                                nB=B ^ (1<<captured)
                                newep=-1
                                wp2,bp2=self.passed(nW,nB,-1)
                                if wp2 or bp2:
                                    tw=self.terminal_winner(wp2,bp2,0)
                                    moves.append(('t',tw))
                                else:
                                    moves.append(('s',nW,nB,newep,heap,1))
            # heap moves
            if heap>0:
                for h2 in range(heap):
                    moves.append(('s',W,B,-1,h2,1))
        else:
            # black
            for j in self.bits(B):
                f=j//8; r=j%8
                # forward one down
                if r>0:
                    nj=j-1
                    if not (W&(1<<nj)) and not (B&(1<<nj)):
                        nB=(B ^ (1<<j)) | (1<<nj)
                        nW=W
                        newep=-1
                        wp2,bp2=self.passed(nW,nB,-1)
                        if wp2 or bp2:
                            tw=self.terminal_winner(wp2,bp2,1)
                            moves.append(('t',tw))
                        else:
                            moves.append(('s',nW,nB,newep,heap,0))
                # double
                if r==6:
                    j2=j-1; j3=j-2
                    if not (W&(1<<j2)) and not (B&(1<<j2)) and not (W&(1<<j3)) and not (B&(1<<j3)):
                        nB=(B ^ (1<<j)) | (1<<j3)
                        nW=W
                        newep=j2*200 + j3
                        wp2,bp2=self.passed(nW,nB,j3)
                        if wp2 or bp2:
                            tw=self.terminal_winner(wp2,bp2,1)
                            moves.append(('t',tw))
                        else:
                            moves.append(('s',nW,nB,newep,heap,0))
                # captures
                for df in (-1,1):
                    nf=(f+df)%self.n
                    nr=r-1
                    if nr>=0:
                        nj=nf*8+nr
                        if W & (1<<nj):
                            nB=(B ^ (1<<j)) | (1<<nj)
                            nW=W ^ (1<<nj)
                            newep=-1
                            wp2,bp2=self.passed(nW,nB,-1)
                            if wp2 or bp2:
                                tw=self.terminal_winner(wp2,bp2,1)
                                moves.append(('t',tw))
                            else:
                                moves.append(('s',nW,nB,newep,heap,0))
            # en passant for black
            if ep!=-1:
                target=ep//200; captured=ep%200
                tf=target//8; tr=target%8
                for j in self.bits(B):
                    f=j//8; r=j%8
                    if tr==r-1 and ((tf==(f+1)%self.n) or (tf==(f-1)%self.n)):
                        if not (W&(1<<target)) and not (B&(1<<target)):
                            if W & (1<<captured):
                                nB=(B ^ (1<<j)) | (1<<target)
                                nW=W ^ (1<<captured)
                                newep=-1
                                wp2,bp2=self.passed(nW,nB,-1)
                                if wp2 or bp2:
                                    tw=self.terminal_winner(wp2,bp2,1)
                                    moves.append(('t',tw))
                                else:
                                    moves.append(('s',nW,nB,newep,heap,0))
            if heap>0:
                for h2 in range(heap):
                    moves.append(('s',W,B,-1,h2,0))
        if not moves:
            w=1-side
            self.memo[key]=w
            return w
        for m in moves:
            if m[0]=='t':
                w=m[1]
            else:
                _,nW,nB,newep,nheap,nside=m
                w=self.solve(nW,nB,newep,nheap,nside)
            if w==side:
                self.memo[key]=side
                return side
        self.memo[key]=1-side
        return 1-side

def classify(n,toks):
    W0,B0=parse_tokens(toks,n)
    res={}
    for h in range(5):
        sol=Solver(n,W0,B0)
        t0=time.time()
        wf=sol.solve(W0,B0,-1,h,0)
        bf=sol.solve(W0,B0,-1,h,1)
        cls='N' if (wf==0 and bf==1) else ('P' if (wf==1 and bf==0) else ('L' if (wf==0 and bf==0) else 'R'))
        dt=time.time()-t0
        print(f"n={n} h={h}: {cls} states={len(sol.memo)} time={dt:.3f}", flush=True)
        res[h]=(cls,len(sol.memo),dt)
    return res

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='q':
        n=int(sys.argv[2]); toks=make_q(n)
    elif mode=='p8':
        n=8; toks=make_p8()
    elif mode=='qmod':
        n=int(sys.argv[2]); toks=make_q(n)
    else:
        n=int(sys.argv[2]); toks=sys.argv[3:]
    W0,B0=parse_tokens(toks,n)
    if mode=='qmod':
        # move black pawn file1 rank7->6: clear bit (1,6 0-based? rank7 index6) set rank6 index5
        B0 = B0 & ~(1<<(1*8+6))
        B0 |= (1<<(1*8+5))
    print("whites mask bits:", bin(W0))
    print("blacks mask bits:", bin(B0))
    t0=time.time()
    res=classify(n,toks if mode!='qmod' else toks)
    # if qmod, recompute with modified B0? classify uses parse; need adjust. We'll handle separately below.
    print("total time:", time.time()-t0)
