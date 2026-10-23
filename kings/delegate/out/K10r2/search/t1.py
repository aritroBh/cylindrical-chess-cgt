import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sweep import *
B=Bd(6,6)
T=Tally()
t=process(B, gen_random_scenes(B,20000,1), T,'t1')
print('time',t,'gen',T.pos_generated,'tested',T.pos_tested,'inst',T.inst_cert,'viol',len(T.violations),'xs',len(T.xs),'both',len(T.both))
for k,v in sorted(T.feat.items()): print('  ',v,k)
print(T.violations[:5], T.xs[:5])
