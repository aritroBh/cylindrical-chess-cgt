import sys
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
# all positions: Black pawn e-file ranks 2..7 (idx r=1..6 -> rank 2..7), no white pawn
E=4
roots=[]
for r in range(1,B.H-1):
    ps=r*B.W+E
    for wk in range(B.N):
        for bk in range(B.N):
            for stm in (0,1):
                pos=(stm,wk,bk,(),(ps,),-1)
                pos=norm(B,pos)
                if legal(B,pos): roots.append(pos)
print(len(roots),'legal roots')
index,plist,val,moves=solve(B,'P',roots)
import collections
print(len(plist),'positions')
cnt=collections.Counter()
for r in roots:
    cnt[(r[0],val[index[r]])]+=1
print(cnt)
import pickle
pickle.dump((spec,{p:val[i] for p,i in index.items()}),open('kpk_%s.pkl'%spec.replace(':','_'),'wb'))
