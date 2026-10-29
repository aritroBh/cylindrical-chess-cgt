# Independent Python re-implementation (referee K32): token-count recursion for lambda/rho, Fraction number games for the stops.
import sys, functools
from fractions import Fraction as F
INF=float('inf')
def parse(f):
    gs=[]; cur=None
    for ln in open(f):
        ln=ln.split()
        if ln[0]=='G':
            n=int(ln[1]); v=list(map(int,ln[2:])); Lm=v[0::2]; Rm=v[1::2]
            cur=dict(n=n,L=[[j for j in range(n) if Lm[i]>>j&1] for i in range(n)],R=[[j for j in range(n) if Rm[i]>>j&1] for i in range(n)],res=[])
            gs.append(cur)
        else:
            d=dict(x.split('=') for x in ln[1:]); cur['res'].append(d)
    return gs
def numopts(v):
    # canonical form of a dyadic Fraction: (left option or None, right option or None)
    if v==0: return None,None
    if v.denominator==1:
        return (v-1,None) if v>0 else (None,v+1)
    d=v.denominator; return v-F(1,d), v+F(1,d)
def mk(g):
    L,R=g['L'],g['R']
    @functools.lru_cache(None)
    def win(y,v,mover):   # winner 'L'/'R' of y + v (v a Fraction), mover = 'L' or 'R'
        l,r=numopts(v)
        if mover=='L':
            opts=[win(j,v,'R') for j in L[y]]+([win(y,l,'R')] if l is not None else [])
            return 'L' if 'L' in opts else 'R'
        opts=[win(j,v,'L') for j in R[y]]+([win(y,r,'L')] if r is not None else [])
        return 'R' if 'R' in opts else 'L'
    @functools.lru_cache(None)
    def tok(y,c,mover):   # independent token-count version: y plus c Left tokens; winner
        if mover=='L':
            opts=[tok(j,c,'R') for j in L[y]]+([tok(y,c-1,'R')] if c>0 else [])
            return 'L' if 'L' in opts else 'R'
        opts=[tok(j,c,'L') for j in R[y]]
        return 'R' if 'R' in opts else 'L'
    @functools.lru_cache(None)
    def rtok(y,c,mover):  # y plus c Right tokens
        if mover=='L':
            opts=[rtok(j,c,'R') for j in L[y]]
            return 'L' if 'L' in opts else 'R'
        opts=[rtok(j,c,'L') for j in R[y]]+([rtok(y,c-1,'L')] if c>0 else [])
        return 'R' if 'R' in opts else 'L'
    return win,tok,rtok
def run(g,K=5):
    n=g['n']; win,tok,rtok=mk(g)
    xs=[F(p,2**K) for p in range(-(n+1)*2**K,(n+1)*2**K+1)]
    def isnum(y):
        for x in xs:
            if win(y,-x,'R')=='L' and win(y,-x,'L')=='R': return x
        return None
    nm=[isnum(y) for y in range(n)]
    memo={}
    def st(y,m):
        if (y,m) in memo: return memo[(y,m)]
        if nm[y] is not None: r=nm[y]
        elif m=='L': r=max([st(j,'R') for j in g['L'][y]],default=-INF)
        else: r=min([st(j,'L') for j in g['R'][y]],default=INF)
        memo[(y,m)]=r; return r
    out=[]
    for y in range(n):
        lam=next((c for c in range(0,n+3) if tok(y,c,'R')=='L'),None)
        rho=next((c for c in range(0,n+3) if rtok(y,c,'L')=='R'),None)
        # cross-check the two reserve methods
        lam2=next((c for c in range(0,n+3) if win(y,F(c),'R')=='L'),None)
        rho2=next((c for c in range(0,n+3) if win(y,F(-c),'L')=='R'),None)
        assert lam==lam2 and rho==rho2,(g,y)
        out.append((lam,rho,st(y,'L'),st(y,'R')))
    return out
def fmt(v):
    return '+inf' if v==INF else '-inf' if v==-INF else str(v)
if __name__=='__main__':
    gs=parse(sys.argv[1]); bad=0; tot=0; lit=0; corr=0
    import math
    for g in gs:
        out=run(g)
        for y,(lam,rho,LS,RS) in enumerate(out):
            d=g['res'][y]; tot+=1
            c_lam=-1 if lam is None else lam; c_rho=-1 if rho is None else rho
            def cf(s):
                if s.endswith('inf'): return F(INF) if False else (INF if s[0]=='+' else -INF)
                a,b=s.split('/'); return F(int(a),int(b))
            ok=(int(d['lam'])==c_lam and int(d['rho'])==c_rho and cf(d['LS'])==LS and cf(d['RS'])==RS)
            if not ok: bad+=1; print('MISMATCH',g['n'],y,d,(lam,rho,LS,RS))
            # corrected relation (own derivation of the check)
            if (lam is None)!=(RS==-INF): corr+=1
            elif lam is not None and RS!=INF:
                u=-RS; lo=max(0,math.ceil(u)); hi=max(0,math.floor(u)+1)
                if not lo<=lam<=hi: corr+=1
                if not (lam==math.ceil(u) or lam==math.ceil(u)+1): lit+=1
                assert (lam==math.ceil(u) or lam==math.ceil(u)+1)==(RS<2)
            elif lam is not None and RS==INF and lam!=0: corr+=1
            if (rho is None)!=(LS==INF): corr+=1
            elif rho is not None and LS!=-INF:
                u=LS; lo=max(0,math.ceil(u)); hi=max(0,math.floor(u)+1)
                if not lo<=rho<=hi: corr+=1
            elif rho is not None and LS==-INF and rho!=0: corr+=1
    print('graphs',len(gs),'nodes',tot,'mismatches vs C',bad,'corrected violations (python)',corr,'literal lam violations',lit)
