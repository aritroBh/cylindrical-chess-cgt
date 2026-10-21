"""Independent check of claim C4 (adversarial verifier). Does not import worker code.

(1) g(n) for 0.137 from the hand-written rule:
      g(0)=0, g(1)=1 (remove a lone pin),
      n>=2: options g(n-2) [end pin + its neighbour; n=2 -> empty]
            and g(a)^g(b), a+b=n-3, a,b>=0 [interior pin + both neighbours]
(2) g for 0.07 (Dawson's Kayles): options g(a)^g(b), a+b=n-2.
(3) brute-force Sprague-Grundy on actual rows of pins (bitmask game, the
    "remove a pin together with its surviving neighbours" rule), n<=20,
    with sums handled by computing the Grundy value of the whole bitmask
    position, not by nim-adding.
(4) period / exception analysis, Guy-Smith certificate bound, least period.
"""
import sys
from functools import lru_cache

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300

def mex(s):
    m = 0
    while m in s:
        m += 1
    return m

g = [0] * (N + 1)
for n in range(1, N + 1):
    opts = set()
    if n == 1:
        opts.add(0)
    if n >= 2:
        opts.add(g[n - 2])
    if n >= 3:
        for a in range(0, n - 2):
            opts.add(g[a] ^ g[n - 3 - a])
    g[n] = mex(opts)

k07 = [0] * (N + 2)
for n in range(2, N + 2):
    k07[n] = mex({k07[a] ^ k07[n - 2 - a] for a in range(0, n - 1)})

# (3) bitmask brute force: position = set of live pins on a line of length L;
# pins i and i+1 are neighbours iff both live (a dead pin breaks adjacency).
@lru_cache(maxsize=None)
def sg_mask(mask):
    opts = set()
    m = mask
    i = 0
    while m >> i:
        if (mask >> i) & 1:
            nm = mask & ~(1 << i)
            if i > 0 and (mask >> (i - 1)) & 1:
                nm &= ~(1 << (i - 1))
            if (mask >> (i + 1)) & 1:
                nm &= ~(1 << (i + 1))
            opts.add(sg_mask(nm))
        i += 1
    return mex(opts)

BF = 20
bf = [sg_mask((1 << n) - 1) for n in range(BF + 1)]
bf_ok = all(bf[n] == g[n] for n in range(BF + 1))
# also some sums (two strips separated by one dead pin), to confirm nim-addition
sum_ok = True
for a in range(0, 10):
    for b in range(0, 10):
        mask = ((1 << a) - 1) | (((1 << b) - 1) << (a + 1))
        if sg_mask(mask) != g[a] ^ g[b]:
            sum_ok = False

print("g_0.137(0..%d):" % N)
for s in range(0, N + 1, 34):
    print("  n=%3d..%3d: %s" % (s, min(s + 33, N), " ".join(str(x) for x in g[s:s + 34])))
print("max g(n), n<=%d: %d" % (N, max(g)))
print("brute-force pin rows == recurrence for n<=%d: %s" % (BF, bf_ok))
print("brute-force two-strip sums == nim-sum for a,b<10: %s" % sum_ok)
print("g_0.137(n) == g_0.07(n+1) for n<=%d: %s" % (N, all(g[n] == k07[n + 1] for n in range(N + 1))))

p = 34
exc = [n for n in range(0, N - p + 1) if g[n] != g[n + p]]
print("n with g(n) != g(n+34), n+34<=%d: %s" % (N, exc))
# eventual-value definition: g(n) != g(n + 34*m) for the largest m with n+34m <= N
eventual = {r: g[N - ((N - r) % p)] for r in range(p)}
exc2 = [n for n in range(0, N + 1) if g[n] != eventual[n % p]]
print("n with g(n) != eventual periodic value: %s" % exc2)
n0 = exc[-1] + 1 if exc else 0
k = 3
bound = 2 * n0 + p + k
need = all(g[n] == g[n + p] for n in range(n0, bound))
print("Guy-Smith: n0=%d p=%d k=%d -> need g(n+p)=g(n) for %d<=n<%d (i.e. data to n+p=%d): %s"
      % (n0, p, k, n0, bound, bound - 1 + p, need))
print("data actually cover n0<=n<=%d" % (N - p))
# least eventual period: smallest q with g(n)=g(n+q) for all n in [n_q, N-q] where
# a Guy-Smith certificate fits in the data
for q in range(1, 34):
    ex = [n for n in range(0, N - q + 1) if g[n] != g[n + q]]
    last = ex[-1] if ex else -1
    print("  q=%2d: last n with g(n)!=g(n+q) is %d" % (q, last)) if q in (1, 2, 17) else None
cands = []
for q in range(1, 34):
    ex = [n for n in range(0, N - q + 1) if g[n] != g[n + q]]
    if not ex or ex[-1] < (N - q) - 60:
        cands.append(q)
print("periods q<34 holding on a tail of length >=60: %s" % cands)
zeros = [n for n in range(0, 201) if g[n] == 0]
print("g(n)=0, n<=200: %s" % zeros)
print("block 52..85: %s" % " ".join(str(x) for x in g[52:86]))
