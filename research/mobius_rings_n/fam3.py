import sys,json,collections,re,itertools; sys.path.insert(0,'.')
from fam import *
H=[]
for l in open('../mobius_rings/results/hits_all.txt'):
    p=l.split(); sg=p[3]; ring=' '.join(p[4:]); H.append((sg,ring))
extra=json.load(open('extra_hits.json')) if len(sys.argv)>1 else []
for sg,r in extra: H.append((sg,r))
H=list(dict.fromkeys(H))
print(len(H),'base hits',flush=True)
blocks=[[x] for x in SINGLES]+[[x,y] for x in SINGLES for y in SINGLES]
surv=collections.defaultdict(dict)
tot=0
for bi,(sg0,ring) in enumerate(H):
    t=ring.split()
    cand=[(k,b,m) for m in (1,2) for k in range(len(t)+1) for b in blocks]
    sig=solve([' '.join(ins(t,k,b,m)) for k,b,m in cand])
    tot+=len(cand)
    for (k,b,m),s in zip(cand,sig):
        if s==sg0: surv[(ring,k,' '.join(b))][m]=s
print('solved',tot,flush=True)
out=[]
for (ring,k,b),d in surv.items():
    if not(1 in d and 2 in d): continue
    t=ring.split(); blk=b.split()
    ms=[m for m in range(1,40) if len(t)+len(blk)*m<=32]
    rings=[' '.join(ins(t,k,blk,m)) for m in ms]
    s1=solve(rings); s2=solve(rings,'bin/mob1_32'); assert s1==s2 or 'TIMEOUT' in s1+s2
    ok=all(x==d[1] for x in s1)
    out.append((ring,k,b,d[1],ms[-1],ok,sorted(set(s1))))
json.dump(out,open('results/fam_stage3.json','w'))
for o in out: print(o)
