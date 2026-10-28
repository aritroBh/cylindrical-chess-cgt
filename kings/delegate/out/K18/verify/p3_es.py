"""Referee: does hypothesis (P3) of Proposition 8.1 (king clearance) hold for ANY choice of sbar's winning strategy in K18's own ES pairs?
For each ES sortie (K18 sorties_S.json: Q after m and r), compute R under two different greedy strategies (first / last winning reply),
also adding the king square after each s move (conservative), and count pairs (sortie, zero/negative context) with R disjoint from X and its king-neighbourhood."""
import sys, json, gzip
sys.path.insert(0,'.')
from vlg import *
import pf_lib
B=Board(8,6,True,[0,1,2]); W,H=8,6
G=Game(B,0,False)   # P variant (no queen clause), no passes
S=json.load(open('../keep/sorties_S.json'))
C=json.load(open('../keep/ctxS_contexts.json'))
T=json.load(gzip.open('../keep/table_ES.json.gz','rt'))
def sq(s): return (ord(s[0])-97)+W*(int(s[1:])-1)
def nb(s): return set(B.kn[s])|{s}
def xset(c):
    wp=tuple(sorted(sq(x) for x in c['w'])); bp=tuple(sorted(sq(x) for x in c['b']))
    seen=set(); st=[(wp,bp,-1)]; X=set()
    while st:
        s=st.pop()
        if s in seen: continue
        seen.add(s); X|=set(s[0])|set(s[1])
        for col in (0,1):
            for (a,b,e,pr) in pf_lib.moves(s[0],s[1],s[2],col):
                if not pr: st.append((a,b,e))
    N=set()
    for x in X: N|=nb(x)
    return N
NX=[xset(c) for c in C]
def sigma_R(q,Tt,pick):
    R=set(); seen=set()
    def s_node(pos,t):
        key=(pos,t)
        if key in seen: return
        seen.add(key); R.add(pos[0])
        lst,prom=G.s_moves(pos,0)
        if prom or lst is None: return
        for np_ in lst:
            R.add(np_[0])
            opts=[]
            for kind,n2 in G.sb_moves(np_):
                if kind=='win': opts=None; break
                if kind=='move' and G.Vs(n2,t-1,0): opts.append(n2)
            if opts: s_node(opts[0] if pick=='first' else opts[-1],t-1)
    s_node(q,Tt); return R
Rs=[]
for i,s in enumerate(S):
    q=parse(B,' '.join(s['Q'].split()[:-2])); Tt=G.least_T(q,0,24)
    if Tt is None: Rs.append(None); print('sortie',i,'no plain win in my solver P-variant'); continue
    Rs.append((Tt,sigma_R(q,Tt,'first'),sigma_R(q,Tt,'last')))
tot=hold1=holdeither=0; ex=[]
for r in T:
    if r['cls'] not in ('zero','neg') or r['A']=='X': continue
    R=Rs[r['s']]
    if R is None: continue
    tot+=1
    h1=not (R[1]&NX[r['c']]); h2=not (R[2]&NX[r['c']])
    hold1+=h1; holdeither+=(h1 or h2)
    if h1 or h2: ex.append((r['s'],r['c'],r['cls'],r['A']))
print('ES zero/neg legal pairs',tot,'P3 holds (first-winning sigma)',hold1,'either sigma',holdeither)
print(ex[:10])
