import sys, collections, pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
E=4
def T(rank):
    out=set()
    for d,offs in [(1,[0]),(2,[-1,0,1])]:
        rr=rank-d
        if 1<=rr<=B.H:
            for o in offs:
                f=E+o
                if B.cyl: f%=B.W
                elif not (0<=f<B.W): continue
                out.add((rr-1)*B.W+f)
    return out
def flt(B,p,m):
    lab,k,np_=m
    if k=='p': return True
    bp=np_[4]
    if not bp: return True
    rank=B.r(bp[0])+1
    return np_[1] in T(rank)
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
pickle.dump((spec,V),open('kpkT_%s.pkl'%spec.replace(':','_'),'wb'))
for rank in range(7,1,-1):
    ps=(rank-1)*B.W+E
    for wk in sorted(T(rank)):
        print('pawn e%d White K %s (Black to move): Black K squares where S4 FAILS:'%(rank,B.name(wk)))
        bad=[B.name(bk) for bk in range(B.N) if legal(B,norm(B,(1,wk,bk,(),(ps,),-1))) and V[norm(B,(1,wk,bk,(),(ps,),-1))]!='D']
        print('   ',' '.join(bad))
