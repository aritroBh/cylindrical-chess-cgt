from lg import *
for sq in ('g4','g5','g6','h6','a6'):
    G=Game(8,8,True,'b',{7,0,1},queen=True,mate=False,confine=False)
    print('unconf',sq,[G.T(parse(f'K{sq} ka4 pa5'),k,tmax=8) for k in (0,1,4,5,6,7,None)],flush=True)
