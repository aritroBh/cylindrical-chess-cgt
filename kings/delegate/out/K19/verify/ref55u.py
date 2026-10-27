from lg import *
for sq in ('c5','d4','d5','d3'):
    G=Game(8,6,True,'w',{0,1,2},queen=True,mate=True,confine=False)
    print('unconf',sq,[G.T(parse(f'Kb3 Pb2 k{sq}'),k,tmax=12) for k in (0,2,None)],flush=True)
