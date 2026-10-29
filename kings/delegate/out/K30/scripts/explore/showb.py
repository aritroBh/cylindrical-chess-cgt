# show for fixed White K and pawn, which Black K squares are safe (restricted strategy), side to move given
import sys,pickle
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]; rank=int(sys.argv[2]); wks=sys.argv[3]; stm=0 if sys.argv[4]=='w' else 1
B=Board(spec)
sp,V=pickle.load(open('kpkR_%s.pkl'%spec.replace(':','_'),'rb'))
ps=(rank-1)*B.W+4
wk=B.sq(wks)
for r in range(B.H-1,-1,-1):
    row=''
    for f in range(B.W):
        bk=r*B.W+f
        pos=norm(B,(stm,wk,bk,(),(ps,),-1))
        if wk==bk: ch='K'
        elif bk==ps: ch='p'
        elif not legal(B,pos): ch='.'
        else: ch={'D':'o','L':'x','W':'W'}[V[pos]] if pos in V else '?'
        row+=ch+' '
    print(r+1,row)
print('  a b c d e f g h')
