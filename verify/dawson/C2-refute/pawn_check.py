import sys, time
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from pawns3 import make, board, strips_board, FLAGS
MAXB = int(sys.argv[1]) if len(sys.argv) > 1 else 14
SUMB = int(sys.argv[2]) if len(sys.argv) > 2 else MAXB + 2

def mex(s):
    m = 0
    while m in s: m += 1
    return m
g = [0, 1]
for n in range(2, 40):
    g.append(mex({g[n-2]} | {g[a] ^ g[n-3-a] for a in range(n-2)}))
G = []
for n in range(40):
    G.append(mex({G[a] ^ G[n-3-a] for a in range(n-2)}) if n >= 3 else 0)

t0 = time.time()
# 1. paper's literal 1xn rule: remove a pawn whose neighbours (if any) are empty
for n in range(1, 8):
    row = [1]*n
    mv = [i for i in range(n) if all(row[j] == 0 for j in (i-1, i+1) if 0 <= j < n)]
    print("paper 1x%d rule: legal first moves = %d" % (n, len(mv)))

# 2. flat single strips, both colours to move
for n in range(1, MAXB + 1):
    w = make(n, False); b = board(n, set(range(n)))
    ow, ob = w(b, 1), w(b, 2)
    print("flat 3x%-2d first player wins: W-first %s B-first %s | g=%d pred %s | paperG=%d pred %s"
          % (n, ow, ob, g[n], g[n] != 0, G[n], G[n] != 0))
# 3. cylinders
for n in range(3, MAXB + 1):
    w = make(n, True); b = board(n, set(range(n)))
    ow, ob = w(b, 1), w(b, 2)
    print("cyl  3x%-2d first player wins: W-first %s B-first %s | correct pred %s | paper pred %s"
          % (n, ow, ob, g[n-3] == 0, G[n-3] == 0))
# 4. pin down g(n) exactly via sums: strip n + strip k is a 2nd-player win iff g(n) == g(k)
refs = {0: 0, 1: 1, 3: 2, 5: 3, 13: 4, 15: 5}
mism = 0
for n in range(1, MAXB + 1):
    found = []; tested = []
    for k, v in refs.items():
        lens = [n] if k == 0 else [n, k]
        nb, b = strips_board(lens)
        if nb > SUMB: continue
        tested.append(v)
        P = not make(nb, False)(b, 1)
        if P: found.append(v)
    ok = (g[n] in found) if found else None
    if ok is False: mism += 1
    print("sum test n=%-2d: refs tested v=%s ; P-position only for v=%s ; g(n)=%d"
          % (n, tested, found, g[n]))
print("sum-test mismatches:", mism)
print("flags:", FLAGS, "time %.1fs" % (time.time() - t0))
