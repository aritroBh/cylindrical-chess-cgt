import sys,pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
sp,V=pickle.load(open('kpk_%s.pkl'%spec.replace(':','_'),'rb'))
for rank in range(7,1,-1):
    ps=(rank-1)*B.W+4
    for stm in (1,0):
        U=[]
        for wk in range(B.N):
            ok=True; n=0
            for bk in range(B.N):
                pos=norm(B,(stm,wk,bk,(),(ps,),-1))
                if legal(B,pos):
                    n+=1
                    if V.get(pos)!='D': ok=False;break
            if ok and n>0 and wk!=ps: U.append(B.name(wk))
        print(spec,'pawn e%d'%rank,'stm','wb'[stm],'universally safe White K:',U)
