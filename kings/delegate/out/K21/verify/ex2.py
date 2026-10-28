import sys; sys.path.insert(0,'.')
from ex import show
from ref import *
print("-----")
SM = G([['M']],[[]])   # {-|}  Left suicide
SP = G([[]],[['P']])   # {|+}  Right suicide
show("{-|}+on", [SM, ON()]); show("{-|}+dud", [SM, DUD()]); show("{|+}+off", [SP, OFF()]); show("{|+}+dud",[SP,DUD()])
# simpler tempo-regime counterexample found by my random search: K={+,0|0}, S={0|off}
K = G([[1,'P'],[]],[[1],[]]); S = G([[2],[],[]],[[1],[1],[]])
d = d_results([K,S]); print("K={+,0|0}, S={0|off}: stopper", S.is_stopper(), "D:", outcome(*d[((0,0),0)]), outcome(*d[((0,0),1)]))
dOn = d_results([K,ON()]); dOff = d_results([K,OFF()])
print("  K+on", outcome(*dOn[((0,0),0)]), outcome(*dOn[((0,0),1)]), " K+off", outcome(*dOff[((0,0),0)]), outcome(*dOff[((0,0),1)]))
for B in (1,2,5,14):

    rt=(('n',0),('n',0)); r = cgt_results([K,S],B); print('  CGT B=%d'%B, outcome(*r[(rt,0)]), outcome(*r[(rt,1)]))
