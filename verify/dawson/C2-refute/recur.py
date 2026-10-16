"""Independent check of claim C2 (recurrence part). Stdlib only; imports nothing from dawson/ or cylcgt/."""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300

def mex(s):
    m = 0
    while m in s: m += 1
    return m

# (A) paper's recurrence, literally: G(n) = mex{G(a)^G(b): a+b=n-3, a,b>=0}
P = []
for n in range(N + 1):
    P.append(mex({P[a] ^ P[n - 3 - a] for a in range(n - 2)}) if n >= 3 else 0)

# (B) claimed correct recurrence
C = [0, 1]
for n in range(2, N + 1):
    s = {C[n - 2]} | {C[a] ^ C[n - 3 - a] for a in range(max(0, n - 2))}
    C.append(mex(s))

# (C) generic octal-game evaluator from the code digits
def octal(code, M):
    d = [int(c) for c in code]  # d[k] for removing k tokens, k>=1 (d[0] ignored)
    g = []
    for n in range(M + 1):
        s = set()
        for k in range(1, len(d)):
            if k > n: break
            r = n - k
            if d[k] & 1 and r == 0: s.add(0)
            if d[k] & 2 and r > 0: s.add(g[r])
            if d[k] & 4 and r >= 2:
                for a in range(1, r):
                    s.add(g[a] ^ g[r - a])
        g.append(mex(s))
    return g

O137 = octal("0137", N)
O07 = octal("007", N + 1)      # Dawson's Kayles, heap n+1 <-> 0.137 heap n
O007 = octal("0007", N)        # remove exactly 3 leaving 0,1,2 heaps
print("claimed recurrence == 0.137 evaluator:", C == O137)
print("0.137(n) == 0.07(n+1):", all(O137[n] == O07[n + 1] for n in range(N + 1)))
print("paper G == 0.007:", P == O007)

agree = [n for n in range(N + 1) if P[n] == C[n]]
print("n in 0..%d with paper G == g: %d of %d" % (N, len(agree), N + 1))
print("  agreeing n:", agree)
ringP = {n: int(P[n - 3] == 0) for n in range(3, N + 1)}
ringC = {n: int(C[n - 3] == 0) for n in range(3, N + 1)}
bad = [n for n in range(3, N + 1) if ringP[n] != ringC[n]]
print("ring n in 3..%d with paper outcome != correct: %d" % (N, len(bad)))
print("  first:", bad[:12])
print("g(0..40):", C[:41])
print("G(0..40):", P[:41])
# literature check: OEIS A002187 (Sprague-Grundy values for Dawson's chess), first 87 terms as recalled
A002187 = [0,1,1,2,0,3,1,1,0,3,3,2,2,4,0,5,2,2,3,3,0,1,1,3,0,2,1,1,0,4,5,2,7,4,0,1,1,2,0,3,1,1,0,3,3,2,2,4,4,5,5,2,3,3,0,1,1,3,0,2,1,1,0,4,5,3,7,4,8,1,1,2,0,3,1,1,0,3,3,2,2,4,4,5,5,9]
print("matches recalled A002187 prefix (len %d):" % len(A002187), C[:len(A002187)] == A002187)
exc = [n for n in range(N + 1 - 34) if C[n] != C[n + 34]]
print("n with g(n)!=g(n+34), n<=%d:" % (N - 34), exc)
