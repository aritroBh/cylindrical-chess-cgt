# stage: block lengths 1..3 over one-pawn-per-file hits (+ n7p8, n5p6), m=1,2 then extend to n<=32 with both solvers
import sys,json,collections,itertools; sys.path.insert(0,'.')
from fam import *
bases=json.load(open(sys.argv[1]))   # list of [name, sig, ring]
LMAX=int(sys.argv[2]); outf=sys.argv[3]
surv={}
for name,sg0,ring in bases:
    t=ring.split(); blocks=[list(b) for L in range(1,LMAX+1) for b in itertools.product(SINGLES,repeat=L)]
    cand=[(k,b,m) for m in (1,2) for k in range(len(t)+1) for b in blocks]
    sig=solve([' '.join(ins(t,k,b,m)) for k,b,m in cand])
    nto=sum(1 for s in sig if s=='TIMEOUT')
    d=collections.defaultdict(dict)
    for (k,b,m),s in zip(cand,sig):
        if s==sg0: d[(k,' '.join(b))][m]=s
    keep=[x for x,v in d.items() if len(v)==2]
    print(name,len(cand),'cands; survivors m=1,2:',len(keep),'timeouts',nto,flush=True)
    for k,b in keep:
        blk=b.split(); ms=[m for m in range(1,40) if len(t)+len(blk)*m<=32]
        rings=[' '.join(ins(t,k,blk,m)) for m in ms]
        s1=solve(rings); s2=solve(rings,'bin/mob1_32')
        ok=all(x==sg0 for x in s1) and s1==s2
        surv[(name,k,b)]=(ms[-1],ok,s1==s2,sorted(set(s1)))
        print('  ',name,'cut',k,'block',b,'maxm',ms[-1],'all_stay',ok,'solvers_agree',s1==s2,sorted(set(s1)),flush=True)
json.dump([[*k,*v] for k,v in surv.items()],open(outf,'w'))
