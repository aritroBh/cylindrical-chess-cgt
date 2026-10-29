import sys,pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; prank=int(sys.argv[2]); bkname=sys.argv[3]
B=Board(spec)
sp,V=pickle.load(open('kpk_%s.pkl'%spec.replace(':','_'),'rb'))
ps=(prank-1)*B.W+4; bk=B.sq(bkname)
for stm in (1,0):
    print('pawn e%d bk %s stm %s : White K squares; D=. L=X, P=pawn, k=bk, -=illegal'%(prank,bkname,'wb'[stm]))
    for r in range(B.H-1,-1,-1):
        row=''
        for f in range(B.W):
            s=r*B.W+f
            if s==ps: row+='P ';continue
            if s==bk: row+='k ';continue
            pos=norm(B,(stm,s,bk,(),(ps,),-1))
            if not legal(B,pos): row+='- ';continue
            v=V[pos]
            row+=('. ' if v=='D' else ('X ' if v=='L' else 'W '))
        print(r+1,row)
    print('  '+' '.join('abcdefgh'[:B.W]))
