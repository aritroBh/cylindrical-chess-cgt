import sys, collections, pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
E=4
def Uset(rank):   # rank of pawn (1-based): White K squares e(rank-1), e(rank-2); for rank 3 only e2
    if rank>=4: return {(rank-2-1)*B.W+E,(rank-1-1)*B.W+E}
    if rank==3: return {(2-1)*B.W+E}
    return set()
def flt(B,p,m):
    lab,k,np_=m
    if k=='p': return True
    bp=np_[4]
    if not bp: return True    # captured the pawn
    rank=B.r(bp[0])+1
    return np_[1] in Uset(rank)
roots=[]
for r in range(1,B.H-1):
    ps=r*B.W+E
    for wk in range(B.N):
        for bk in range(B.N):
            for stm in (0,1):
                pos=norm(B,(stm,wk,bk,(),(ps,),-1))
                if legal(B,pos): roots.append(pos)
idx,pl,val,mv=solve(B,'P',roots,wfilter=flt)
V={p:val[i] for p,i in idx.items()}
bad=0; tot=0
for rank in range(2,8):
    ps=(rank-1)*B.W+E
    for wk in Uset(rank):
        for bk in range(B.N):
            pos=norm(B,(1,wk,bk,(),(ps,),-1))
            if legal(B,pos):
                tot+=1
                if V[pos]!='D':
                    bad+=1
                    if bad<=40: print('UNSAFE',fmt(B,pos))
print(spec,'Black-to-move positions with White K in U_r:',tot,'unsafe under rule:',bad)
pickle.dump((spec,V),open('kpkU_%s.pkl'%spec.replace(':','_'),'wb'))
