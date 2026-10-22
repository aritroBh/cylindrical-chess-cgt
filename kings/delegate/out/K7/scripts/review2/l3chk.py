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
Q=P("Kd6 kc4 Pe3 pa4 pe4 pf3 w f4")
print(C.L3s(Q,3,False))
