"""Referee: look for any (sortie, context) pair satisfying all hypotheses of Proposition 8.1 (P1 plain win, P2 promotion-free zero context,
P3 king clearance with a greedy winning strategy sigma), on the (1+1)-pawn roots of cyl:8x6, F_Z={a,b,c}.  Emit Q+context positions (s to move)
for kpp to check the conclusion (Black wins P)."""
import sys, re, itertools
sys.path.insert(0,'.')
from vlg import *
sys.path.insert(0,'.')
B=Board(8,6,True,[0,1,2])
W,H=8,6
# five promotion-free zero contexts (own enumeration in pf.py): recompute here
import pf_lib
ctxs=pf_lib.zero_pf_contexts()
print('zero promotion-free contexts',len(ctxs),file=sys.stderr)
def xset(wp,bp):
    seen=set(); st=[(wp,bp,-1)]; X=set()
    while st:
        s=st.pop()
        if s in seen: continue
        seen.add(s); X|=set(s[0])|set(s[1])
        for c in (0,1):
            for (a,b,e,pr) in pf_lib.moves(s[0],s[1],s[2],c): st.append((a,b,e))
    return X
nb=lambda s: set(B.kn[s])|{s}
CT=[]
for wp,bp in ctxs:
    X=xset(wp,bp); N=set()
    for x in X: N|=nb(x)
    CT.append((wp,bp,N))
G=Game(B,0,True)
def sigma_R(q,T):
    """R: squares of s's king over all s-turn nodes of lines in which sbar plays the greedy winning move (plain game)"""
    R=set(); seen=set()
    def s_node(pos,t):
        key=(pos,t)
        if key in seen: return
        seen.add(key)
        R.add(pos[0])
        lst,prom=G.s_moves(pos,0)
        if prom or lst is None: return
        for np_ in lst:
            # sbar reply: first winning move
            for kind,n2 in G.sb_moves(np_):
                if kind=='win': break
                if kind=='move' and G.Vs(n2,t-1,0):
                    s_node(n2,t-1); break
    s_node(q,T); return R
fn=sys.argv[1]
out=open(sys.argv[2],'w'); hits=0; tested=0
roots=[]
for l in open(fn):
    a=l.split(' only=')
    head=a[0].split()
    if head[0]!='Q': continue
    pos=parse(B,' '.join(head[1:]))
    if G.in_check(pos,1): continue
    roots.append(pos)
for pos in roots:
    for (npos,promo,_t) in G.moves(pos,0):
        if promo: continue
        best=None;bq=None
        for (q,qp,_t2) in G.moves(npos,1,confine=True):
            if qp: continue
            T=G.least_T(q,0,24)
            if T is not None and (best is None or T<best): best,bq=T,q
        if best is None: continue
        R=sigma_R(bq,best); tested+=1
        for wp,bp,N in CT:
            if not (R&N):
                hits+=1
                wk,bk,pw,pb,ep=bq
                s='K%s k%s %s %s %s w %s'%(name(B,wk),name(B,bk),' '.join('P'+name(B,x) for x in pw),' '.join('p'+name(B,x) for x in pb),' '.join(['P'+name(B,x) for x in wp]+['p'+name(B,x) for x in bp]),name(B,ep) if ep>=0 else '-')
                out.write(' '.join(s.split())+' | T=%d |R|=%d\n'%(best,len(R)))
out.close(); print('plain-win sorties tested',tested,'(sortie,context) pairs with P3 satisfied',hits)
