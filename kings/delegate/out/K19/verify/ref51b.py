from lg import *
import sys
cfgs=[dict(queen=True,mate=True,confine=True),dict(queen=True,mate=False,confine=True),dict(queen=True,mate=False,confine=False),dict(queen=False,mate=True,confine=True)]
i=int(sys.argv[1]); cfg=cfgs[i]
print(cfg,flush=True)
for sq in ('g4','g5','g6','h6','a6'):
    G=Game(8,8,True,'b',{7,0,1},**cfg)
    row=[G.T(parse(f'K{sq} ka4 pa5'),k,tmax=12) for k in list(range(0,10))+[None]]
    print(' ',sq,row,flush=True)
