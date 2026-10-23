# test: Remark (count rule) dp(omega) >= mu_omega unless a king stands on the passer's path;
# Corollary 2.11b layout; dp vs cylcgt promote_distance; Corollary 2.11a credit consistency
import sys,os,random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
from sweep import *
from cylcgt import pawns as cp
def to_cyl(B,y):
    f=lambda s:(s[0],s[1])
    return cp.Pos(frozenset(y.wp),frozenset(y.bp),None) if y.ep is None else None
def cyl_pos(B,y):
    ep=None
    if y.ep is not None:
        v=ep_victim(B,y); mover=other(y.stm)
        ep=(y.ep,v,'W' if y.stm=='w' else 'B')
    return cp.Pos(frozenset(y.wp),frozenset(y.bp),ep)
def front_passers(B,y,color):
    mine=y.wp if color=='w' else y.bp; theirs=y.bp if color=='w' else y.wp
    out=[]
    for (f,r) in mine:
        st={f}|set(B.adjfiles(f))
        if color=='w':
            if any(q[0] in st and q[1]>r for q in theirs): continue
            if any(q[0]==f and q[1]>r for q in list(mine)+list(theirs)): continue
        else:
            if any(q[0] in st and q[1]<r for q in theirs): continue
            if any(q[0]==f and q[1]<r for q in list(mine)+list(theirs)): continue
        if y.ep is not None and y.stm!=color and ep_victim(B,y)==(f,r) and any((g,r) in theirs for g in B.adjfiles(f)): continue
        d=(B.H-r-(1 if r==2 else 0)) if color=='w' else (r-1-(1 if r==B.H-1 else 0))
        out.append(((f,r),d))
    return out
def my_passed_front_dp(B,y,color):
    """promote distance of color's fastest passer (own implementation, e.p. aware, front pawn of file)"""
    mine=y.wp if color=='w' else y.bp; theirs=y.bp if color=='w' else y.wp
    best=10**6
    for (f,r) in mine:
        st={f}|set(B.adjfiles(f))
        if color=='w':
            if any(q[0] in st and q[1]>r for q in theirs): continue
            if any(q[0]==f and q[1]>r for q in list(mine)+list(theirs)): continue
        else:
            if any(q[0] in st and q[1]<r for q in theirs): continue
            if any(q[0]==f and q[1]<r for q in list(mine)+list(theirs)): continue
        if y.ep is not None and y.stm!=color and ep_victim(B,y)==(f,r) and any((g,r) in theirs for g in B.adjfiles(f)): continue
        d=(B.H-r-(1 if r==2 else 0)) if color=='w' else (r-1-(1 if r==B.H-1 else 0))
        best=min(best,d)
    return best
rnd=random.Random(5)
nchk=0; nmis=0; nrem=0; nremv=0; viol=[]
for (W,H) in [(6,6),(7,6),(8,6),(6,7),(5,6)]:
    B=Bd(W,H)
    for y in gen_uniform(B,60000,rnd.randrange(10**9),maxper=3):
        if not legal(B,y): continue
        cpos=cyl_pos(B,y); cb=cp.Board(W,H,True,True)
        for col,C in (('w','W'),('b','B')):
            a=my_passed_front_dp(B,y,col); b=cp.promote_distance(cb,cpos,C)
            nchk+=1
            if a!=b: nmis+=1; viol.append(('dp-mismatch',W,H,y.text(B),col,a,b))
        # remark: for omega with a passer, mu_omega(y;p) <= dp(omega) unless a king is on the passer's path
        for beta in 'wb':
            om=other(beta)
            dpo=my_passed_front_dp(B,y,om)
            if dpo>=10**6: continue
            # does a king stand on the path of some fastest passer?  (any passer attaining dpo)
            for p in (y.wp if beta=='w' else y.bp):
                mu=mu_search(B,y,beta,p,dpo)
                nrem+=1
                if mu>dpo:
                    # find kings on path of omega passers
                    kingpath=True
                    for (sq,dd) in front_passers(B,y,om):
                        if dd!=dpo: continue
                        f,r=sq
                        rng=range(r+1,B.H+1) if om=='w' else range(r-1,0,-1)
                        if not any((f,rr) in (y.wk,y.bk) for rr in rng): kingpath=False
                    nremv+=1
                    if not kingpath: viol.append(('remark',W,H,y.text(B),beta,B.name(p),dpo,mu))
print('dp compared',nchk,'mismatch',nmis,'remark instances',nrem,'with mu>dp',nremv)
print('violations:',[v for v in viol][:10], len(viol))
