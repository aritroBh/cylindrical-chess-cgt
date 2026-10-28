import sys; sys.path.insert(0,'.')
from ref import *
def show(title, comps, Bs=(2,5,9)):
    d = d_results(comps); root = tuple(0 for _ in comps)
    f = lambda r: outcome(*r)
    print(title, "D:", f(d[(root,0)]), f(d[(root,1)]), "stopper-all:", [c.is_stopper() for c in comps])
    for B in Bs:
        r = cgt_results(comps, B); rt = tuple(('n',0) for _ in comps)
        print("   B=%d CGT: %s %s  dom=%s crit=%s" % (B, f(r[(rt,0)]), f(r[(rt,1)]), dominance(comps,B), criterion(comps,B)))
PL = G([['P']], [[]]); MI = G([[]], [['M']])
show("{+|}+off", [PL, OFF()]); show("{+|}+dud", [PL, DUD()]); show("{+|}+on",[PL,ON()]); show("{+|}+over",[PL,OVER()])
show("{|-}+on",[MI,ON()]); show("{|-}+off",[MI,OFF()]); show("{|-}+over",[MI,OVER()]); show("{|-}+under",[MI,UNDER()])
show("{|+}+{-|}", [G([[]],[['P']]), G([['M']],[[]])])
# tempo-regime counterexample
# K: node0: L->1, R-> M,1 ; node1 = 0.   S: a=0,b=1,c=2: a: L->c, R->b,c ; b: R->a,b ; c: L->b,c
K = G([[1],[]], [['M',1],[]])
S = G([[2],[],[1,2]], [[1,2],[0,1],[]])
print("S stopper", S.is_stopper(), "K stopper", K.is_stopper())
d = d_results([K,S]); print("D K+S:", outcome(*d[((0,0),0)]), outcome(*d[((0,0),1)]))
for nm, X in (('off',OFF()),('on',ON())):
    d = d_results([K,X]); print("K+%s"%nm, outcome(*d[((0,0),0)]), outcome(*d[((0,0),1)]))
for B in (1,2,3,14,40):
    r = cgt_results([K,S],B); rt=(('n',0),('n',0)); print(" CGT B=%d"%B, outcome(*r[(rt,0)]), outcome(*r[(rt,1)]))
# the state (K,a) was root. Also non-stopper S' and incomplete example
SX = G([[0,1],[]],[[0],[]])
show("{+|}+S'={S',0|S'}", [PL, SX]); print("  S' stopper", SX.is_stopper(), reserves(SX,4))
X1 = G([[]],[['P',0]]); X2 = G([['M',0]],[[0]])
show("{|+,0}+{-,0|0}", [X1,X2], Bs=(3,5,7))
print(reserves(X2,5), reserves(X1,5))
