# Independent check of Dawson's chess Grundy values (octal game 0.137) and of the 3xn cylinder ring rule.
import sys, functools
N=400
# (1) octal game 0.137 straight from the octal code, NOT the paper's formula
# digits 1,3,7: remove k tokens (k=1,2,3) from a heap; code digit bit0 = may leave 0 heaps, bit1 = may leave 1 heap, bit2 = may leave 2 heaps
code={1:1,2:3,3:7}
g=[0]*(N+1)
for n in range(1,N+1):
    opts=set()
    for k,d in code.items():
        if k>n: continue
        r=n-k
        if d&1 and r==0: opts.add(0)
        if d&2 and r>0: opts.add(g[r])
        if d&4 and r>=2:
            for a in range(1,r//2+1): opts.add(g[a]^g[r-a])
    m=0
    while m in opts: m+=1
    g[n]=m
print("g[0..40]=",g[:41])
# paper formula
h=[0]*(N+1); h[1]=1
for n in range(2,N+1):
    s={h[n-2]}
    for a in range(0,n-2):
        b=n-3-a
        if b>=0: s.add(h[a]^h[b])
    m=0
    while m in s: m+=1
    h[n]=m
print("octal==paper formula up to",N,":",g==h)
# period and last exception
for p in range(1,100):
    ex=[n for n in range(N+1-p) if g[n]!=g[n+p]]
    if ex and max(ex)< N-3*p-1 or not ex:
        pass
cand=[]
for p in range(1,100):
    ex=[n for n in range(0,N-p+1) if g[n]!=g[n+p]]
    # period p from some point on
    last=max(ex) if ex else -1
    if last < N-p-100:
        cand.append((p,last+1))
print("(period, preperiod end) candidates (smallest first):",cand[:3])
p=34
ex=[n for n in range(0,N-p+1) if g[n]!=g[n+p]]
print("period 34: last n with g(n)!=g(n+34):",max(ex)," -> last exceptional index (value not matching the periodic part) =",max(ex)+34 if False else max(ex))
zeros=[n for n in range(0,70) if g[n]==0]
print("zeros g(m)=0 for m<70:",zeros)
print("cylinder first-player-win n=m+3:",[m+3 for m in zeros])
