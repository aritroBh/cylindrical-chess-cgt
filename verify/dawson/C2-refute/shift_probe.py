"""Could the paper's G be the right sequence under a different indexing? Compare G(n) with g(n+s)."""
def mex(s):
    m = 0
    while m in s: m += 1
    return m
N = 400
g = [0, 1]
for n in range(2, N + 1):
    g.append(mex({g[n-2]} | {g[a] ^ g[n-3-a] for a in range(n-2)}))
G = []
for n in range(N + 1):
    G.append(mex({G[a] ^ G[n-3-a] for a in range(n-2)}) if n >= 3 else 0)
for s in range(-6, 7):
    rng = [n for n in range(0, 301) if 0 <= n + s <= N]
    agree = sum(G[n] == g[n + s] for n in rng)
    print("shift %+d: G(n)==g(n%+d) on %d of %d n in 0..300" % (s, s, agree, len(rng)))
# zero sets (the only thing the ring outcome uses)
print("G zeros <=100:", [n for n in range(101) if G[n] == 0])
print("g zeros <=100:", [n for n in range(101) if g[n] == 0])
