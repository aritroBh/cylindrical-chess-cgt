import sys
sys.path.insert(0, '/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10r2')
from chk import *
EX = [
 (8,6,True,"Ka1 ka6 Pc4 pe3 b -"),(8,6,True,"Ka1 ka6 Pc4 pe4 b -"),(8,6,True,"Ka1 ka6 Pc4 pe3 w -"),
 (8,6,True,"Ka1 ka6 Pc3 pe3 w -"),(8,6,True,"Ka1 ka6 pc3 Pe4 w -"),(8,6,True,"Ka1 ka6 pc3 Pe3 w -"),
 (8,6,True,"Ka1 ka6 Pc2 Pd4 pd3 b -"),(8,6,True,"Ka1 ka6 Pc2 Pc3 pd3 pd4 w -"),(8,6,True,"Ka1 ka6 Pc4 Pd2 pe3 pf4 b -"),
 (7,6,True,"Ka1 ka6 Pc2 Pd3 Pf2 pe4 b -"),
 (8,6,True,"Ka1 ka6 Pc2 Pd4 Pe2 pe5 b -"),(8,6,True,"Ka1 ka6 Pc2 Pd3 Pe2 pe5 b -"),(8,6,True,"Ka1 ka6 Pc2 Pe2 Pe3 pd4 pe4 pe5 w -"),
 (8,6,True,"Ke2 ka6 Pc4 pf4 b -"),(8,6,True,"Ka1 ka6 Pc4 pf4 b -"),
 (8,6,True,"Ka1 kc5 Pc4 pf4 b -"),(8,6,True,"Kc5 ka6 Pc4 pf4 b -"),(8,6,True,"Kc6 ka6 Pc4 pf4 b -"),(8,6,True,"Ka1 kc6 Pc4 pf4 b -"),
 (8,6,True,"Ka1 ka6 Pe4 pd4 b e3"),(8,6,True,"Ka1 ka6 Pe4 pd4 b -"),
 (8,6,True,"Ka1 ka6 Pc3 Pd4 Pf2 pc4 b d3"),(8,6,True,"Ka1 ka6 Pc3 Pd4 Pf2 pc4 b -"),
 (8,6,True,"Ke1 ka6 Pa4 Pc5 Pg5 pa5 b -"),(8,6,True,"Ke1 ka6 Pa4 Pc5 pa5 b -"),
 (7,6,False,"Kb1 ka6 Pa4 Pc2 Pc5 pa5 b -"),(7,6,True,"Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5 b -"),
 (8,6,True,"Ka1 ka6 Pc2 w -"),
]
for W,H,wrap,t in EX:
    B = Bd(W,H,wrap)
    y = parse(B,t)
    out,_ = run_kp(B,[t])
    r = out.get(t)
    print(('cyl' if wrap else 'flat'),W,H,t,'| kp',r,'| legal',legal(B,y))
    for beta in 'wb':
        for p in sorted(y.wp if beta=='w' else y.bp):
            h = hyps(B,y,beta,p,full=True)
            print('    beta=%s p=%s d=%d e=%d mu=%s  H1..5=%s' % (beta,B.name(p),h['d'],h['e'],h['mu'],[h[k] for k in ('h1','h2','h3','h4','h5')]))
