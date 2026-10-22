import subprocess
from kpgen import Board
from lc import Cert
B=Board(7,6,True); C=Cert(B,[0,1,2])
def P(s):
    toks=s.split(); wk=bk=None; wp=set(); bp=set()
    for t in toks[:-2]:
        sq=B.sq(t[1:])
        if t[0]=='K': wk=sq
        elif t[0]=='k': bk=sq
        elif t[0]=='P': wp.add(sq)
        else: bp.add(sq)
    return (wk,bk,frozenset(wp),frozenset(bp),0 if toks[-2]=='w' else 1,-1)
exs=["Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5 b -","Kb5 kd5 Pb4 Pc5 b -","Kb5 kd5 Pb4 Pc5 pe2 b -","Kd6 kc2 pa3 Pe4 pe5 pf5 w -","Ke6 ka1 Pc4 pb3 pc5 w -","Kd6 kc2 pa3 w -","Ke6 ka1 Pc4 pb3 pc5 w -"]
out=subprocess.run(["./kp","--board","cyl:7x6","--ep","on","--promote","Q","--pmodel"],input="\n".join(exs)+"\n",capture_output=True,text=True).stdout.splitlines()
for e,o in zip(exs,out):
    Q=P(e)
    print(e,"| L1P",C.L1(Q,False,5),"L1Q",C.L1(Q,True,5),"muB",C.mu(Q,False),"muA",C.mu(Q,True),"|",o.split('|')[1] if '|' in o else o)
    T=C.L1(Q,False,5)
    if T:
        print("   L3",C.L3(Q,T,False)[:2])
