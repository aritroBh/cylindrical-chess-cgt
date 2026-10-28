"""Referee: budget vectors T_k (k=0..6, inf) per sortie for (1+1)-pawn roots, own solver; compare multiset of vectors per root with K18's searchk output."""
import sys, gzip, re, random
sys.path.insert(0,'.')
from vlg import *
B=Board(8,6,True,[0,1,2])
random.seed(3)
theirs={}
for l in gzip.open('../keep/searchk_c8x6_f3_22.out.gz','rt'):
    if l[0]=='#': continue
    p=[x.strip() for x in l.split('|')]
    if p[0]!='Q': continue
    toks=p[1].split()[:-2]
    if sum(1 for x in toks if x[0]=='P')!=1 or sum(1 for x in toks if x[0]=='p')!=1: continue
    vecs=[]
    for m in re.findall(r'\[([^\]]*)\]',p[4]):
        mm=re.search(r'k=(\S+)',m)
        if mm: vecs.append(tuple(None if x=='-' else int(x) for x in mm.group(1).split(',')))
    theirs[' '.join(toks)]=(p[3],sorted(vecs,key=lambda v:[(-1 if x is None else x) for x in v]))
roots=[r for r,(f,_) in theirs.items() if f=='NOESC']
oth=[r for r,(f,_) in theirs.items() if f!='NOESC']; random.shuffle(oth)
roots+=oth[:30]
print('roots to check',len(roots),'of',len(theirs),flush=True)
games={k:Game(B,0,True) for k in list(range(7))+[None]}
bad=0
for r in roots:
    pos=parse(B,r.replace(' ','  ').replace('  ',' '))
    vecs=[]
    g=games[0]
    for (npos,promo,_t) in g.moves(pos,0):
        if promo: continue
        v=[]
        for k in list(range(7))+[None]:
            gk=games[k]; best=None
            for (qpos,qp,_t2) in gk.moves(npos,1,confine=True):
                if qp: continue
                T=gk.least_T(qpos,k,30)
                if T is not None and (best is None or T<best): best=T
            v.append(best)
        # moves with an immediate safe promotion for Black are listed by K18 w/o k vector? keep only if no 'win'
        vecs.append(tuple(v))
    vecs=sorted(vecs,key=lambda v:[(-1 if x is None else x) for x in v])
    tv=theirs[r][1]
    # their list only has moves for which k= was printed; compare as multiset restricted to my vecs
    ok = vecs==tv
    if not ok:
        bad+=1
        print('DIFF',r,theirs[r][0],'\n  mine',vecs,'\n  theirs',tv,flush=True)
print('checked',len(roots),'differences',bad)
