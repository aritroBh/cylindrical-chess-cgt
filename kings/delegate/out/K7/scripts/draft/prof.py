import time
from kpgen import Board
from lc import Cert
B=Board(7,6,True); C=Cert(B,[0,1,2])
def P(s): 
    toks=s.split()
    wk=bk=None; wp=set(); bp=set()
    for t in toks[:-2]:
        sq=B.sq(t[1:])
        if t[0]=='K': wk=sq
        elif t[0]=='k': bk=sq
        elif t[0]=='P': wp.add(sq)
        else: bp.add(sq)
    return (wk,bk,frozenset(wp),frozenset(bp),0 if toks[-2]=='w' else 1,-1)
# Z_onT1: Black Kd5 then White Kxb5 -> Q: Ka5->b5 ; black king d5
Q=P("Kb5 kd5 Pb4 Pc5 b -")
for T in range(1,7):
    t=time.time(); r=C.L1(Q,False,T); print(T,r,time.time()-t)
for s in ["Ka1 kc5 Pb2 pb4 w -","Ka1 kc5 Pb2 b -","Kb3 kc3 Pa2 pb5 w -"]:
    Q=P(s)
    for T in range(1,6):
        t=time.time(); r=C.L1(Q,False,T); print(s,T,r,round(time.time()-t,2))
