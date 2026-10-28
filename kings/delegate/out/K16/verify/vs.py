import sys, random
sys.path.insert(0,'.')
from cert import *
V='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/viol_small/'
random.seed(5)
tot=0; res=[]
for fn,kind,W,H in [('cyl_6x6_20.viol','cyl',6,6),('cyl_7x6_20.viol','cyl',7,6),('cyl_8x6_20.viol','cyl',8,6),('flat_6x6_11.viol','flat',6,6),('flat_6x6_20.viol','flat',6,6),('flat_7x6_11.viol','flat',7,6),('flat_7x6_20.viol','flat',7,6)]:
    lines=[l.split('|')[0].strip() for l in open(V+fn) if l.strip()]
    sample = lines if len(lines)<=6 else random.sample(lines,6)
    b=B(kind,W,H)
    for l in sample:
        pos=parse(b,l)
        v=white_view(pos,solve(b,pos))
        cs=[]
        for p in pos[2]:
            c=cert_static(b,pos,0,p)
            if c: cs.append((p,ns_sim(b,pos,0,p)[1]))
        print(fn,l,'| mine:',v,'| certified p (with NS kind):',cs,flush=True)
