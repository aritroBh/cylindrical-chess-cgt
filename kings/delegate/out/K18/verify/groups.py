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
R=list(roots())
print('roots',len(R),file=sys.stderr)
if sample:
    random.Random(seed).shuffle(R); R=R[:sample]
seen={}
import collections
for qc in (True,False):
    n=0
    for pos in R:
        c=classify(pos,qc)
        if c is None: continue
        only=any(cl=='PLAIN-ONLY' for _,cl in c); esc=any(cl=='ESC' for _,cl in c)
        tag=('Q' if qc else 'P')
        print(tag,fmt(B,pos),'only=%d esc=%d'%(sum(cl=='PLAIN-ONLY' for _,cl in c),sum(cl=='ESC' for _,cl in c)),'NOESC' if not esc else 'ESCAPE',' '.join('[%s %s]'%(fmt(B,np_).split()[0],cl) for np_,cl in c) if only else '', flush=True) if only else None
