import sys
sys.path.insert(0,'..'); sys.argv=['x','1','1','7','6','cyl','z','4','ctx']
exec(open('ept2.py').read().split("rows = []")[0])
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
for s in ["Kd6 kc4 Pe3 pa4 pe4 pf3 w f4","Kb6 kb4 Pe3 pf3 pe4 pa5 w f4","Kd6 kb5 pa4 Pe3 pe4 pf3 w f4"]:
    Q=P(s)
    T=C.L1(Q,False,6); TS=C.L1(Q,True,6)
    print(s,"legal",B.legal_pos(Q),"T",T,"Tsafe",TS,"mu_noep",C.mu(Q,False),"mu_ep",mu_ep(Q),"L3",C.L3(Q,T,False)[:2])
