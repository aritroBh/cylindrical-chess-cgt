"""Referee: enumerate context pawn sets on files e,f,g of cyl:8x6 (<=2+2 pawns, ranks 2..5, a legal pawn move for each side),
decide promotion-free (any order, either colour, e.p. included) and the normal-play class of the pawn-only frozen game."""
import itertools, sys
from functools import lru_cache
W,H=8,6
FILES=(4,5,6)
sqs=[r*W+f for r in range(1,H-1) for f in FILES]
def moves(wp,bp,ep,c):
    """c=0 white to move. returns list of (wp',bp',ep',promo)"""
    out=[]
    mp,op=(wp,bp) if c==0 else (bp,wp)
    dr=1 if c==0 else -1; last=H-1 if c==0 else 0; start=1 if c==0 else H-2
    occ=set(wp)|set(bp)
    for p in mp:
        f,r=p%W,p//W
        nr=r+dr
        others=tuple(x for x in mp if x!=p)
        cands=[]
        t=nr*W+f
        if t not in occ:
            cands.append((t,None,-1))
            if r==start:
                t2=(nr+dr)*W+f
                if t2 not in occ: cands.append((t2,None,t))
        for df in (-1,1):
            g=(f+df)%W
            t=nr*W+g
            if t in op: cands.append((t,t,-1))
            elif t==ep:
                cp=r*W+g
                if cp in op: cands.append((t,cp,-1))
        for (t,cap,nep) in cands:
            nop=tuple(x for x in op if x!=cap) if cap is not None else op
            promo=(t//W==last)
            nmp=others if promo else tuple(sorted(others+(t,)))
            if c==0: out.append((nmp,nop,-1 if promo else nep,promo))
            else: out.append((nop,nmp,-1 if promo else nep,promo))
    return out
def promo_free(wp,bp):
    seen=set(); st=[(wp,bp,-1)]
    while st:
        s=st.pop()
        if s in seen: continue
        seen.add(s)
        for c in (0,1):
            for (a,b,e,pr) in moves(s[0],s[1],s[2],c):
                if pr: return False
                st.append((a,b,e))
    return True
@lru_cache(None)
def first_wins(wp,bp,ep,c):
    """normal play, promotion-free only: player c to move wins iff some move leads to position where opponent loses; no move -> loses"""
    for (a,b,e,pr) in moves(wp,bp,ep,c):
        assert not pr
        if not first_wins(a,b,e,1-c): return True
    return False
res={}
import collections
cnt=collections.Counter(); tot=0; legal=0
for nw in range(3):
    for nb in range(3):
        for wp in itertools.combinations(sqs,nw):
            for bp in itertools.combinations(sqs,nb):
                if set(wp)&set(bp): continue
                if not moves(wp,bp,-1,0) or not moves(wp,bp,-1,1): continue
                legal+=1
                if promo_free(wp,bp):
                    wm=first_wins(wp,bp,-1,0); bm=first_wins(wp,bp,-1,1)
                    cls={(False,False):'zero',(True,False):'positive',(False,True):'negative',(True,True):'fuzzy'}[(wm,bm)]
                    cnt[cls]+=1
print('legal contexts (<=2+2, a legal pawn move for each side):',legal)
print('promotion-free by class:',dict(cnt))
