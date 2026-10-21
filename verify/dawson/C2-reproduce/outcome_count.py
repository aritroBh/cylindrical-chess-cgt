# Verifier side count: n <= 300 where the paper's G gives the wrong flat-board outcome.
def mex(s):
    m = 0
    while m in s: m += 1
    return m
N = 300
g = [0]*(N+1)
for n in range(1, N+1):
    g[n] = mex({g[max(i-1,0)] ^ g[max(n-i-2,0)] for i in range(n)})
G = [0]*(N+1)
for n in range(3, N+1):
    G[n] = mex({G[a] ^ G[n-3-a] for a in range(n-2)})
bad = [n for n in range(N+1) if (g[n]==0) != (G[n]==0)]
print("flat outcome mismatches n=0..300:", len(bad), "first:", bad[:12])
