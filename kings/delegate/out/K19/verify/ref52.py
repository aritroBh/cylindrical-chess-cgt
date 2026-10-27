from lg import *
import time
t0=time.time()
def run(W,H,FZ,sorts,Qfmt,att='b'):
    for sq in sorts:
        row={}
        for qn,q in (('queen',True),('P',False)):
            for cn,c in (('conf',True),('unconf',False)):
                for k in (0,None):
                    if (not c) and k is not None and False: continue
                    G=Game(W,H,True,att,FZ,queen=q,mate=True,confine=c)
                    row[(qn,cn,k)]=G.T(parse(Qfmt.format(sq)),k,tmax=13)
        print(W,H,sq,{f'{a}/{b}/{k}':v for (a,b,k),v in row.items()},flush=True)
run(8,8,{3,4,5},['d5','e5','f5','f7'],'K{} kd7 pe7')
run(7,6,{1,2,3},['b3','c3','d3','d5'],'K{} kb5 pc5')
print('time',time.time()-t0)
