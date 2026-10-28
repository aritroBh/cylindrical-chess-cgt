"""layers_estimate.py POS CAP : over-approximate the layers (white pawns, black pawns, officer multiset) kpsolve visits from POS and the
number of states sum 2*N^(2+k) (k officers), to extrapolate cap 2 from the measured cap 1 (layers, states)."""
import sys, itertools
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
W,H=7,6; N=42
pos=pm.parse(sys.argv[1]); cap=int(sys.argv[2])
wp0,bp0=frozenset(pos[2]),frozenset(pos[3])
KINDS=[(t,c) for c in (0,1) for t in 'QRBN']
def pawn_succ(wp,bp,white):
    own,en=(wp,bp) if white else (bp,wp)
    d=1 if white else -1; last=H-1 if white else 0; second=1 if white else H-2
    out=[]
    for s in own:
        f,r=s%W,s//W
        for t in [(f,r+d)]+([(f,r+2*d)] if r==second else []):
            tf,tr=t
            if 0<=tr<H:
                q=tr*W+tf
                out.append((s,q,tr==last,False))
        for df in (-1,1):
            tf,tr=f+df,r+d
            if 0<=tf<W and 0<=tr<H:
                q=tr*W+tf
                if q in en or True:   # over-approx: any square (captures of pieces too)
                    out.append((s,q,tr==last,True))
    return out
seen=set(); fr=[(wp0,bp0,())]
while fr:
    nf=[]
    for (wp,bp,off) in fr:
        if (wp,bp,off) in seen: continue
        seen.add((wp,bp,off))
        for white in (True,False):
            for (s,q,promo,cap_) in pawn_succ(wp,bp,white):
                own,en=(wp,bp) if white else (bp,wp)
                if q in own: continue
                nown=set(own); nown.discard(s)
                nen=set(en)
                if cap_ : nen.discard(q)
                elif q in en: continue
                if not promo: nown.add(q)
                nwp,nbp=(nown,nen) if white else (nen,nown)
                if promo:
                    for t in 'QRBN':
                        no=tuple(sorted(off+((t,0 if white else 1),)))
                        if len(no)<=cap: nf.append((frozenset(nwp),frozenset(nbp),no))
                else:
                    nf.append((frozenset(nwp),frozenset(nbp),off))
        # officers can be lost
        for i in range(len(off)):
            nf.append((wp,bp,off[:i]+off[i+1:]))
    fr=nf
tot=0
for (wp,bp,off) in seen:
    tot+=2*N**(2+len(off))
print('layers',len(seen),'states(upper-bound)',tot)
