"""layers_tot.py POS CAP : count the layers (white pawns, black pawns, sorted officer codes) reachable from POS under a TOTAL officer cap
(kpsolve --cap CAP semantics: a promotion that would make more than CAP officers is capped = terminal).  Over-approximation as in
layers_pc.py (any capture square, any officer or pawn may be captured).  Prints layers by number of officers and the dense slot count
sum 2*N^(2+k) (kq3's array size) for flat 7x6."""
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
pos=sys.argv[1]; CAP=int(sys.argv[2])
CAPC=[int(sys.argv[3]) if len(sys.argv)>3 else 9, int(sys.argv[4]) if len(sys.argv)>4 else 9]
PROM=[sys.argv[5] if len(sys.argv)>5 else "QRBN", sys.argv[6] if len(sys.argv)>6 else "QRBN"]
TI={"Q":0,"R":1,"B":2,"N":3}
REFINE=len(sys.argv)>7 and sys.argv[7]=="refine"; BOUND=0 if (len(sys.argv)>8 and sys.argv[8]=="A") else 1
wp0,bp0=parse(pos)
def succ(own,d,last):
    out=[]
    for s in own:
        f,r=s%W,s//W
        tr=r+d
        if 0<=tr<H: out.append((s,tr*W+f,tr==last,False))
        for df in (-1,1):
            tf=f+df
            if 0<=tf<W and 0<=tr<H: out.append((s,tr*W+tf,tr==last,True))
    return out
seen=set(); fr=[(wp0,bp0,())]
while fr:
    nf=[]
    for st in fr:
        if st in seen: continue
        seen.add(st)
        wp,bp,offs=st
        for white in (True,False):
            own,en=(wp,bp) if white else (bp,wp)
            for (s,q,promo,cap_) in succ(own,1 if white else -1,H-1 if white else 0):
                if q in own: continue
                nown=set(own); nown.discard(s); nen=set(en)
                if cap_: nen.discard(q)
                elif q in en: continue
                if not promo: nown.add(q)
                nwp,nbp=(nown,nen) if white else (nen,nown)
                if promo:
                    # a promoting capture may take an officer; over-approximate: no officer taken, and each officer taken
                    variants=[offs]+[offs[:i]+offs[i+1:] for i in range(len(offs)) if (offs[i]>>2)!=(0 if white else 1)] if cap_ else [offs]
                    for ov in variants:
                        col=0 if white else 1
                        mine=sum(1 for x in ov if (x>>2)==col)
                        if len(ov)+1>CAP or mine+1>CAPC[col]:
                            if REFINE and col==BOUND: nf.append((frozenset(nwp),frozenset(nbp),tuple(sorted(ov))))
                            continue
                        for tch in PROM[col]:
                            t=TI[tch]
                            nf.append((frozenset(nwp),frozenset(nbp),tuple(sorted(ov+((0 if white else 4)+t,)))))
                else:
                    nf.append((frozenset(nwp),frozenset(nbp),offs))
                    if cap_ and offs:   # capture on an officer's square (no pawn there): officers of the opponent colour
                        for i in range(len(offs)):
                            if (offs[i]>>2)!=(0 if white else 1): nf.append((frozenset(nwp),frozenset(nbp),offs[:i]+offs[i+1:]))
        for i in range(len(offs)): nf.append((wp,bp,offs[:i]+offs[i+1:]))
        for s_ in wp: nf.append((wp-{s_},bp,offs))
        for s_ in bp: nf.append((wp,bp-{s_},offs))
    fr=nf
by={0:0,1:0,2:0}
for (wp,bp,offs) in seen: by[len(offs)]+=1
tot=sum(c*2*N**(2+k) for k,c in by.items())
print(pos,'cap',CAP,'| layers',len(seen),by,'dense slots',tot)
