"""layers_pc.py POS capW capB typesW typesB : count the layers (white pawns, black pawns, white officer type, black officer type)
reachable from POS by pawn moves/captures/promotions (over-approximation: any capture square), per-side officer caps.
Prints number of layers by number of officers and total slots sum 2*N^(2+k)."""
import sys
W,H=7,6; N=W*H
def parse(s):
    wp=set();bp=set()
    for t in s.split():
        if t in('w','b','-'):continue
        p,sq=t[0],t[1:]
        f=ord(sq[0])-97; r=int(sq[1:])-1
        if p=='P': wp.add(r*W+f)
        if p=='p': bp.add(r*W+f)
    return frozenset(wp),frozenset(bp)
pos=sys.argv[1]; capW=int(sys.argv[2]); capB=int(sys.argv[3]); tW=sys.argv[4]; tB=sys.argv[5]
wp0,bp0=parse(pos)
def succ(wp,bp,white):
    own,en=(wp,bp) if white else (bp,wp)
    d=1 if white else -1; last=H-1 if white else 0
    out=[]
    for s in own:
        f,r=s%W,s//W
        tr=r+d
        if 0<=tr<H: out.append((s,tr*W+f,tr==last,False))
        for df in (-1,1):
            tf=f+df
            if 0<=tf<W and 0<=tr<H: out.append((s,tr*W+tf,tr==last,True))
    return out
seen=set()
fr=[(wp0,bp0,None,None)]
while fr:
    nf=[]
    for st in fr:
        if st in seen: continue
        seen.add(st)
        wp,bp,ow,ob=st
        for white in (True,False):
            for (s,q,promo,cap_) in succ(wp,bp,white):
                own,en=(wp,bp) if white else (bp,wp)
                if q in own: continue
                nown=set(own); nown.discard(s); nen=set(en)
                if cap_: nen.discard(q)
                elif q in en: continue
                if not promo: nown.add(q)
                nwp,nbp=(nown,nen) if white else (nen,nown)
                if promo:
                    if white:
                        if ow is not None and capW<=1: continue   # capped (terminal)
                        for t in tW: nf.append((frozenset(nwp),frozenset(nbp),t,ob))
                    else:
                        if ob is not None and capB<=1: continue
                        for t in tB: nf.append((frozenset(nwp),frozenset(nbp),ow,t))
                else: nf.append((frozenset(nwp),frozenset(nbp),ow,ob))
        # officers may be captured; any pawn may be captured by a king or officer
        if ow is not None: nf.append((wp,bp,None,ob))
        if ob is not None: nf.append((wp,bp,ow,None))
        for s_ in wp: nf.append((wp-{s_},bp,ow,ob))
        for s_ in bp: nf.append((wp,bp-{s_},ow,ob))
    fr=nf
by={0:0,1:0,2:0}
for (wp,bp,ow,ob) in seen:
    by[(ow is not None)+(ob is not None)]+=1
tot=sum(c*2*N**(2+k) for k,c in by.items())
print(pos,'| layers',len(seen),by,'slots',tot)
