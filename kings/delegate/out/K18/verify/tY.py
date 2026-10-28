import sys; sys.path.insert(0,'.')
from vlg import *
B=Board(8,6,True,[0,1,2])
Y=parse(B,'Ka1 Pa2 kc1 pa3')
for k in (0,1,2,None):
    res,G=sortie_table(B,Y,0,k)
    print('k',k,[(fmt(B,p).split()[0],T) for p,T in res])
