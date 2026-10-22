# Recount the paper's claims about Study2025's Dawson recurrence (31 of 301 agree; 56 wrong cylinder outcomes for n=3..300)
N=400
def mex(s):
    m=0
    while m in s: m+=1
    return m
g=[0]*(N+1); g[1]=1
for n in range(2,N+1): g[n]=mex({g[n-2]}|{g[a]^g[n-3-a] for a in range(0,n-2)})
h=[0]*(N+1)
for n in range(1,N+1): h[n]=mex({h[a]^h[n-3-a] for a in range(0,n-2)} if n>=3 else set())
print("agree at", sum(g[n]==h[n] for n in range(301)), "of 301")
print("wrong cylinder outcomes, n=3..300:", sum((g[m]==0)!=(h[m]==0) for m in range(298)))
print("g(n)!=g(n+34) for n in", [n for n in range(N-34) if g[n]!=g[n+34]])
