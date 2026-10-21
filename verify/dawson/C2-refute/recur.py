"""Independent check of claim C2 (does not import any worker code).
g137: Dawson's chess as octal 0.137 (pin form: remove a pin plus its surviving neighbours).
k07 : Dawson's Kayles 0.07 (remove two adjacent pins); g137(n) should equal k07(n+1).
P   : the 2025 paper's recurrence P(n) = mex{P(a)^P(b) : a+b=n-3, a,b>=0} (empty set -> 0).
P2  : same recurrence but seeded with the true values for n=0,1,2 (alternative reading).
"""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
def mex(s):
    m = 0
    while m in s: m += 1
    return m
# direct pin-row definition of 0.137: remove pin i together with pins i-1, i+1 that exist
g = []
for n in range(N + 1):
    opts = set()
    for i in range(n):           # remove pin i
        left = max(i - 1, 0)      # pins 0..i-2 survive on the left
        right = n - min(i + 2, n) # pins i+2..n-1 survive on the right
        opts.add(g[left] ^ g[right])
    g.append(mex(opts))
k = []
for n in range(N + 2):
    k.append(mex({k[a] ^ k[n - 2 - a] for a in range(0, n - 1)}))
assert all(g[n] == k[n + 1] for n in range(N + 1)), "0.137 vs 0.07 disagree"
P = []
for n in range(N + 1):
    P.append(mex({P[a] ^ P[n - 3 - a] for a in range(0, n - 2)}))
P2 = [0, 1, 1]
for n in range(3, N + 1):
    P2.append(mex({P2[a] ^ P2[n - 3 - a] for a in range(0, n - 2)}))
print("g(0..40) =", g[:41])
print("P(0..40) =", P[:41])
agree = [n for n in range(N + 1) if P[n] == g[n]]
print(f"paper P == g at {len(agree)} of {N+1} values n=0..{N}; agree at {agree[:40]}")
agree2 = [n for n in range(N + 1) if P2[n] == g[n]]
print(f"[alt seed P2(0..2)=0,1,1] P2 == g at {len(agree2)} of {N+1}")
# ring: first player wins iff value(n-3)==0, n>=3
ringmis = [n for n in range(3, N + 1) if (P[n-3] == 0) != (g[n-3] == 0)]
print(f"ring outcome mismatches n=3..{N}: {len(ringmis)}; first {ringmis[:12]}")
ringmis2 = [n for n in range(3, N + 1) if (P2[n-3] == 0) != (g[n-3] == 0)]
print(f"[alt seed] ring mismatches n=3..{N}: {len(ringmis2)}; first {ringmis2[:12]}")
# Ring Grundy values as numbers (0/1) mismatch count is identical to outcome mismatch count
print("true ring wins n<=100:", [n for n in range(3, 101) if g[n-3] == 0])
print("paper ring wins n<=100:", [n for n in range(3, 101) if P[n-3] == 0])
# does the 'omitted options' description explain it? recurrence with a,b>=-1, value(-1)=0
h = {-1: 0}
for n in range(N + 1):
    h[n] = mex({h[a] ^ h[n - 3 - a] for a in range(-1, n - 1)})
print("recurrence with a,b>=-1 (h(-1)=0) equals g:", all(h[n] == g[n] for n in range(N + 1)))
r = [0, 1]
for n in range(2, N + 1):
    r.append(mex({r[n-2]} | {r[a] ^ r[n-3-a] for a in range(0, n - 2)}))
print("claimed corrected recurrence equals g:", r == g)
