import sys,pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; rank=int(sys.argv[2]); bks=sys.argv[3]; stm=0 if sys.argv[4]=='w' else 1
B=Board(spec)
sp,V=pickle.load(open(('kpkR_%s.pkl' if len(sys.argv)>5 else 'kpk_%s.pkl')%spec.replace(':','_'),'rb'))
ps=(rank-1)*B.W+4
bk=B.sq(bks)
for r in range(B.H-1,-1,-1):
    row=''
    for f in range(B.W):
        wk=r*B.W+f
        pos=norm(B,(stm,wk,bk,(),(ps,),-1))
        if wk==bk: ch='k'
        elif wk==ps: ch='p'
        elif not legal(B,pos): ch='.'
        else: ch={'D':'D','L':'x','W':'W'}[V[pos]] if pos in V else '?'
        row+=ch+' '
    print(r+1,row)
print('  a b c d e f g h')
