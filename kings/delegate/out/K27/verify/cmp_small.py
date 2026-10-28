import sys
inp=sys.argv[1]; kpf=sys.argv[2]; Af=sys.argv[3]; Bf=sys.argv[4]
inpl=[l.strip() for l in open(inp) if l.strip()]
kp={}
for l in open(kpf):
    p,r=l.strip().split(' | '); kp[p]=r.split()
A={};B={}
for l in open(Af): p,r=l.strip().split(' | '); A[p]=r
for l in open(Bf): p,r=l.strip().split(' | '); B[p]=r
cmp=bad=skip=missing=0
from collections import Counter
c=Counter()
for p in inpl:
    t=p.split()
    if any((x[0]=='P' and x[2]=='2') or (x[0]=='p' and x[2]=='5') for x in t[:-2]): skip+=1; continue
    if p not in kp: missing+=1; continue
    cmp+=1; c[tuple(kp[p])]+=1
    if kp[p]!=[A[p],B[p]]: bad+=1; print('DIFF',p,'kp',kp[p],'own',A[p],B[p])
print('compared',cmp,'bad',bad,'skipped(double-step possible)',skip,'missing(kp not finished)',missing, dict(c))
