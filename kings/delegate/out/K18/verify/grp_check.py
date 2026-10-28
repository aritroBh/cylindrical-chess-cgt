"""Referee's own group search (cyl:8x6, F_Z={a,b,c}): classify roots with my own local-game solver (vlg.py).
usage: groups.py MAXW MAXB [sample_n seed]"""
import sys, itertools, random
sys.path.insert(0,'.')
from vlg import *
W,H=8,6
B=Board(W,H,True,[0,1,2])
fz=sorted(B.fzsq)
maxw,maxb=int(sys.argv[1]),int(sys.argv[2])
sample=int(sys.argv[3]) if len(sys.argv)>3 else 0
seed=int(sys.argv[4]) if len(sys.argv)>4 else 1
pawn_sq=[r*W+f for r in range(1,H-1) for f in range(3)]
def adj(f,g): return ((g-f)%W) in (0,1,W-1)
def has_passer(wp,bp):
    for p in wp:
        f,r=p%W,p//W
        if not any(adj(f,q%W) and q//W>r for q in bp): return True
    for q in bp:
        g,s=q%W,q//W
        if not any(adj(p%W,g) and p//W<s for p in wp): return True
    return False
def roots():
    for nw in range(maxw+1):
        for nb in range(maxb+1):
            for wp in itertools.combinations(pawn_sq,nw):
                for bp in itertools.combinations(pawn_sq,nb):
                    if set(wp)&set(bp): continue
                    if has_passer(wp,bp): continue
                    for wk in fz:
                        for bk in fz:
                            if wk==bk or bk in B.kn[wk]: continue
                            if wk in wp or wk in bp or bk in wp or bk in bp: continue
                            pos=(wk,bk,wp,bp,-1)
                            yield pos
G={}
def game(k,qc):
    key=(k,qc)
    if key not in G: G[key]=Game(B,0,qc)
    return G[key]
def classify(pos,qc):
    """returns None if white can promote at once; else (list of (move, cls)), anyOnly, escape"""
    g0=game(0,qc); gi=game(None,qc)
    mv=g0.moves(pos,0)
    if any(p for (_,p,_) in mv): return None
    out=[]
    for (npos,promo,_t) in mv:
        imm=False
        bestp=bests=None
        for kind,np2 in game(0,qc).sb_moves(npos):
            if kind=='win': imm=True
        if imm:
            out.append((npos,'IMM')); continue
        plain=passp=False
        for (qpos,qpromo,_t2) in g0.moves(npos,1,confine=True):
            if qpromo: continue
            if not plain and g0.least_T(qpos,0,24) is not None: plain=True
            if not passp and gi.least_T(qpos,None,24) is not None: passp=True
            if plain and passp: break
        cls='both' if plain and passp else 'PLAIN-ONLY' if plain else 'pass-only' if passp else 'ESC'
        out.append((npos,cls))
    return out
def canon(pos):
    wk,bk,wp,bp,_=pos
    m=lambda s:(s//W)*W+(2-s%W)
    a=(wk,bk,wp,bp); b=(m(wk),m(bk),tuple(sorted(map(m,wp))),tuple(sorted(map(m,bp))))
    return min(a,b)

import gzip, random, time
def sq2(x): return x
theirs={}
for l in gzip.open('../keep/search_c8x6_f3_22.out.gz','rt'):
    if l[0]=='#': continue
    p=[x.strip() for x in l.split('|')]
    if p[0]!='Q': continue
    toks=p[1].split()
    theirs[frozenset(toks[:-2])]=(p[3],p[4])
def keyof(pos):
    return frozenset(fmt(B,pos).split())
def mirk(fs): return frozenset(x[0]+chr(97+(2-(ord(x[1])-97)))+x[2:] for x in fs)
R=list(roots()); R=[p for p in R if len(p[2])==2 and len(p[3])==2]
random.Random(11).shuffle(R)
random.seed(5)
# stratified: roots in theirs (NOESC), in theirs (ESCAPE), not in theirs
pos_no=[];pos_esc=[];neg=[]
for p in R:
    k=keyof(p)
    t=theirs.get(k) or theirs.get(mirk(k))
    if t is None:
        if len(neg)<20: neg.append(p)
    elif t[0]=='NOESC':
        if len(pos_no)<30: pos_no.append(p)
    else:
        if len(pos_esc)<15: pos_esc.append(p)
    if len(neg)>=20 and len(pos_no)>=30 and len(pos_esc)>=15: break
bad=0; t0=time.time()
for lab,L in (('NOESC',pos_no),('ESCAPE',pos_esc),('none',neg)):
    for p in L:
        c=classify(p,True)
        if c is None: mine='IMMWIN'
        else:
            only=any(cl=='PLAIN-ONLY' for _,cl in c); esc=any(cl=='ESC' for _,cl in c)
            mine='none' if not only else ('ESCAPE' if esc else 'NOESC')
        if mine!=lab:
            bad+=1; print('DIFF',fmt(B,p),'theirs',lab,'mine',mine,flush=True)
    print(lab,len(L),'checked, time',round(time.time()-t0),flush=True)
print('differences',bad)
