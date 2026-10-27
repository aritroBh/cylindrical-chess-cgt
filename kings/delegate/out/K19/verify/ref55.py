from lg import *
import sys
q = sys.argv[1]=='q'
for sq in ('c5','d3','d4','d5'):
    G=Game(8,6,True,'w',{0,1,2},queen=q,mate=True,confine=True)
    st=parse(f'Kb3 Pb2 k{sq}')
    row=[G.T(st,k,tmax=20 if k is None else 18) for k in list(range(0,7))+[8,None]]
    print(sq,'queen' if q else 'P','k=0..6,8,inf',row,flush=True)
