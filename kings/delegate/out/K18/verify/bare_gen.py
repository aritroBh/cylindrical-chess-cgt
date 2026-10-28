"""Referee: positions after each White sortie m at roots (cyl:8x6, F_Z={a,b,c}); tag whether Black wins the plain / pass local game
(my own solver vlg.py, queen clause).  Writes 'pos | plain pass' lines.  usage: bare_gen.py MAXW MAXB sample seed out"""
import sys, itertools, random
sys.path.insert(0,'.')
from vlg import *
W,H=8,6
B=Board(W,H,True,[0,1,2])
fz=sorted(B.fzsq)
maxw,maxb=int(sys.argv[1]),int(sys.argv[2]); sample=int(sys.argv[3]); seed=int(sys.argv[4]); out=open(sys.argv[5],'w')
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
roots=[]
for nw in range(maxw+1):
  for nb in range(maxb+1):
    for wp in itertools.combinations(pawn_sq,nw):
      for bp in itertools.combinations(pawn_sq,nb):
        if set(wp)&set(bp) or has_passer(wp,bp): continue
        for wk in fz:
          for bk in fz:
            if wk==bk or bk in B.kn[wk] or {wk,bk}&(set(wp)|set(bp)): continue
            roots.append((wk,bk,wp,bp,-1))
random.Random(seed).shuffle(roots)
if sample: roots=roots[:sample]
g0=Game(B,0,True); gi=Game(B,0,True)
def punished(npos,k,g):
    for (qpos,qp,_t) in g.moves(npos,1,confine=True):
        if qp: continue
        if g.least_T(qpos,k,24) is not None: return True
    return False
def sqn(s): return name(B,s)
n=0
for pos in roots:
    mv=g0.moves(pos,0)
    if any(p for (_,p,_) in mv): continue
    for (npos,promo,_t) in mv:
        if any(k=='win' for k,_ in g0.sb_moves(npos)): continue   # immediate promotion by Black: not a local-game question
        a=punished(npos,0,g0); b=punished(npos,None,gi)
        wk,bk,wp,bp,ep=npos
        s='K%s k%s %s %s b %s'%(sqn(wk),sqn(bk),' '.join('P'+sqn(x) for x in wp),' '.join('p'+sqn(x) for x in bp),sqn(ep) if ep>=0 else '-')
        s=' '.join(s.split())
        out.write('%s | %d %d\n'%(s,a,b)); n+=1
out.close(); print('positions',n)
