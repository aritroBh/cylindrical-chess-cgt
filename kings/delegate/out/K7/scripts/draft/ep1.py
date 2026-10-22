import subprocess,sys
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
    ep=-1 if toks[-1]=='-' else B.sq(toks[-1])
    return (wk,bk,frozenset(wp),frozenset(bp),0 if toks[-2]=='w' else 1,ep)
exs=sys.argv[1:]
out=subprocess.run(["./kp","--board","cyl:7x6","--ep","on","--promote","Q","--pmodel"],input="\n".join(exs)+"\n",capture_output=True,text=True)
print(out.stderr[:300])
for e,o in zip(exs,out.stdout.splitlines()):
    Q=P(e)
    print(e,"| L1P",C.L1(Q,False,5),"muB",C.mu(Q,False),"|",o)
    T=C.L1(Q,False,5)
    if T: print("   L3",C.L3(Q,T,False)[:2], "legal",B.legal_pos(Q))
