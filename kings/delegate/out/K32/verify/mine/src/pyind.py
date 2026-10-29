"""Referee-2 independent Python check (different language, naive fixpoint sweeps, exact Fractions, token-only DP for lambda/rho,
D1 recursion with its own number detection).  Own RNG and own stopper test.  Usage: pyind.py gen N COUNT SEED > graphs.txt ; pyind.py eval < graphs.txt > results.txt"""
import sys, random, math
from fractions import Fraction as F
sys.setrecursionlimit(10000)
K=3; STEP=F(1,2**K)
def is_stopper(n,L,R):
    # DFS cycle detection on (node,mover) graph
    color={}
    def succ(s):
        v,m=s
        return [(u,1-m) for u in (L[v] if m==0 else R[v])]
    def dfs(s):
        color[s]=1
        for t in succ(s):
            c=color.get(t,0)
            if c==1: return False
            if c==0 and not dfs(t): return False
        color[s]=2; return True
    for v in range(n):
        for m in (0,1):
            if color.get((v,m),0)==0 and not dfs((v,m)): return False
    return True
def gen(n,count,seed):
    rng=random.Random(seed); out=0
    while out<count:
        p=rng.choice([0.1,0.15,0.2,0.3,0.4])
        L=[[u for u in range(n) if rng.random()<p] for _ in range(n)]
        R=[[u for u in range(n) if rng.random()<p] for _ in range(n)]
        if not is_stopper(n,L,R): continue
        print(n," ".join("%d %d"%(sum(1<<u for u in L[v]),sum(1<<u for u in R[v])) for v in range(n))); out+=1
def numopts(q):
    if q.denominator==1:
        if q>0: return ([q-1],[])
        if q<0: return ([],[q+1])
        return ([],[])
    d=q.denominator; return ([q-F(1,d)],[q+F(1,d)])
def lfp(states,succ,mover_of,sigma):
    W=set(); ch=True
    while ch:
        ch=False
        for s in states:
            if s in W: continue
            ss=succ(s)
            if mover_of(s)==sigma: ok=any(t in W for t in ss)
            else: ok=all(t in W for t in ss)
            if ok: W.add(s); ch=True
    return W
def evaluate(n,L,R):
    M=n+4
    # (1) token-only lambda / rho
    T=M
    def mk(tokside):
        states=[(v,t,m) for v in range(n) for t in range(T+1) for m in (0,1)]
        def succ(s):
            v,t,m=s; res=[(u,t,1-m) for u in (L[v] if m==0 else R[v])]
            if m==tokside and t>0: res.append((v,t-1,1-m))
            return res
        return states,succ
    st,sc=mk(0); WL=lfp(st,sc,lambda s:s[2],0)
    st,sc=mk(1); WR=lfp(st,sc,lambda s:s[2],1)
    lam=[next((C for C in range(T+1) if (v,C,1) in WL),99) for v in range(n)]
    rho=[next((C for C in range(T+1) if (v,C,0) in WR),99) for v in range(n)]
    # (2) product with number games on grid
    grid=[F(p,2**K) for p in range(-M*2**K,M*2**K+1)]
    states=[(v,q,m) for v in range(n) for q in grid for m in (0,1)]
    opts={q:numopts(q) for q in grid}
    def succ(s):
        v,q,m=s
        if m==0: return [(u,q,1) for u in L[v]]+[(v,q2,1) for q2 in opts[q][0]]
        return [(u,q,0) for u in R[v]]+[(v,q2,0) for q2 in opts[q][1]]
    W1=lfp(states,succ,lambda s:s[2],0)   # Left wins
    W2=lfp(states,succ,lambda s:s[2],1)   # Right wins
    # lambda,rho again from the number product (cross-check of the token DP)
    lam2=[next((C for C in range(M+1) if (v,F(C),1) in W1),99) for v in range(n)]
    rho2=[next((C for C in range(M+1) if (v,F(-C),0) in W2),99) for v in range(n)]
    # D1
    num={}
    for v in range(n):
        xs=[-q for q in grid if (v,q,1) in W1 and (v,q,0) in W2]
        assert len(xs)<=1
        if xs: num[v]=xs[0]
    memo={}
    def stop(v,which):
        if v in num: return num[v]
        key=(v,which)
        if key in memo: return memo[key]
        if which==0:
            vals=[stop(u,1) for u in L[v]]; r=max(vals) if vals else -math.inf
        else:
            vals=[stop(u,0) for u in R[v]]; r=min(vals) if vals else math.inf
        memo[key]=r; return r
    LS=[stop(v,0) for v in range(n)]; RS=[stop(v,1) for v in range(n)]
    # D1 vs D2 consistency
    bad=0
    for v in range(n):
        for w,st in ((0,LS[v]),(1,RS[v])):
            for q in grid:
                x=-q; win=(v,q,w) in W1 if w==0 else (v,q,1) in W1
                win=((v,q,0) in W1) if w==0 else ((v,q,1) in W1)
                if st==math.inf: ok=win
                elif st==-math.inf: ok=not win
                elif x<st: ok=win
                elif x>st: ok=not win
                else: ok=True
                if not ok: bad+=1
    return lam,rho,lam2,rho2,LS,RS,bad
def relation(lam,rho,LS,RS):
    n=len(lam); viol=0; lit=0
    for v in range(n):
        for res,st,w in ((lam[v],RS[v],0),(rho[v],LS[v],1)):
            if w==0:
                if st==-math.inf: ok=(res==99)
                elif st==math.inf: ok=(res==0)
                else:
                    u=-st; lo=max(0,math.ceil(u)); hi=max(0,math.floor(u)+1); ok=(res!=99 and lo<=res<=hi)
                    if not (res!=99 and res in (math.ceil(u),math.ceil(u)+1)): lit+=1
            else:
                if st==math.inf: ok=(res==99)
                elif st==-math.inf: ok=(res==0)
                else:
                    lo=max(0,math.ceil(st)); hi=max(0,math.floor(st)+1); ok=(res!=99 and lo<=res<=hi)
                    if not (res!=99 and res in (math.ceil(st),math.ceil(st)+1)): lit+=1
            if not ok: viol+=1
    return viol,lit
def fmt(x):
    if x==math.inf: return "+inf"
    if x==-math.inf: return "-inf"
    return str(int(x*16))
if __name__=="__main__":
    if sys.argv[1]=="gen": gen(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
    else:
        gi=0; tv=tl=tb=tm=0; nodes=0
        for line in sys.stdin:
            a=list(map(int,line.split()));
            if not a: continue
            n=a[0]; L=[[u for u in range(n) if a[1+2*v]>>u&1] for v in range(n)]; R=[[u for u in range(n) if a[2+2*v]>>u&1] for v in range(n)]
            lam,rho,lam2,rho2,LS,RS,bad=evaluate(n,L,R)
            if lam!=lam2 or rho!=rho2: tm+=1
            v_,l_=relation(lam,rho,LS,RS); tv+=v_; tl+=l_; tb+=bad; nodes+=n
            for v in range(n): print("g%d %d %d %d %s %s"%(gi,v,lam[v],rho[v],fmt(LS[v]),fmt(RS[v])))
            gi+=1
        sys.stderr.write("graphs %d nodes %d corrected-violations %d literal-violations(finite stop) %d D1D2-bad %d token-vs-numbergame-mismatch graphs %d\n"%(gi,nodes,tv,tl,tb,tm))
