import sys, collections, pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
E=4
def flt(B,p,m):
    lab,k,np_=m
    if k=='p': return True
    wk=np_[1]
    if abs(((wk%B.W)-E+B.W//2)%B.W-B.W//2)>1 if B.cyl else abs((wk%B.W)-E)>1: return False
    bp=np_[4]
    if not bp: return True
    d=B.r(bp[0])-B.r(wk)
    return 1<=d<=2
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
pickle.dump((spec,V),open('kpkR_%s.pkl'%spec.replace(':','_'),'wb'))
print(spec,'safe positions',sum(1 for r in roots if V[r]=='D'),'of',len(roots))
