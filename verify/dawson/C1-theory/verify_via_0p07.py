"""C1-theory check: verify the worker's Q32 pickle as the misere quotient of Dawson's KAYLES
(octal 0.07) heaps 1..33, deriving moves from the 0.07 rule (not from 0.137, not from the pin
model), so it also tests the identification A_32(0.137) = A_33(0.07).

0.07 heap m: remove two adjacent tokens, leaving heaps a, b >= 0 with a + b = m - 2.
A 0.07 heap 1 has no move, i.e. it IS the game 0; a 0.07 heap m >= 2 is mapped to the 0.137
strip m - 1 of the pickle (strip 2 has the same image as strip 1).

Checks: identity / commutativity / associativity (full on generators), onto, reduced,
identity not in P, P-condition for every x in Q, N-condition by an antichain fixpoint over
(x, E) with E = set of images of options, minimal E kept per x. Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C1-theory/verify_via_0p07.py dawson/quotient_Q32.pkl
"""
import pickle, sys, time

d = pickle.load(open(sys.argv[1], "rb"))
mult, P, phi = d["mult"], [bool(p) for p in d["P"]], dict(d["phi"])
N = len(mult)
H137 = max(phi)            # 32
HK = H137 + 1              # 0.07 heaps up to 33

def strip_img(s):          # image of a 0.137 strip s >= 0
    if s == 0:
        return 0
    return phi[1] if s == 2 else phi[s]

def kay_img(m):            # image of a 0.07 heap m >= 0
    return 0 if m <= 1 else strip_img(m - 1)

def kay_opts(m):           # option multisets of a 0.07 heap m
    return {tuple(sorted((a, m - 2 - a))) for a in range(0, m - 1)} if m >= 2 else set()

heaps = list(range(2, HK + 1))        # nonzero 0.07 heaps
g = {m: kay_img(m) for m in heaps}
O = {m: sorted({mult[kay_img(a)][kay_img(b)] for a, b in kay_opts(m)}) for m in heaps}

t0 = time.time()
assert all(mult[0][x] == x == mult[x][0] for x in range(N)), "identity"
assert all(mult[x][y] == mult[y][x] for x in range(N) for y in range(N)), "commutative"
# onto
seen = {0}; fr = [0]
while fr:
    nf = []
    for q in fr:
        for m in heaps:
            y = mult[q][g[m]]
            if y not in seen:
                seen.add(y); nf.append(y)
    fr = nf
print("onto:", len(seen) == N, len(seen), N)
# associativity against generators (enough once onto holds: (xy)a = x(ya) for generators a
# plus commutativity gives full associativity by induction on word length of z)
bad = sum(1 for a in set(g.values()) for x in range(N) for y in range(N)
          if mult[mult[x][y]][a] != mult[x][mult[y][a]])
print("assoc failures (generator form):", bad)
# reduced (Moore refinement w.r.t. generator action)
cls = [int(p) for p in P]; k = len(set(cls))
while True:
    sig = {}; new = []
    for x in range(N):
        new.append(sig.setdefault((cls[x],) + tuple(cls[mult[x][gv]] for gv in sorted(set(g.values()))), len(sig)))
    if len(sig) == k:
        break
    cls, k = new, len(sig)
print("reduced:", k == N, "classes", k)
print("identity in P:", P[0])
print("|Q| =", N, " |P| =", sum(P))
# P-condition
pf = [(x, m) for m in heaps for x in range(N)
      if P[mult[x][g[m]]] and any(P[mult[x][o]] for o in O[m])]
print("P-condition failures:", len(pf))
# N-condition: antichain fixpoint
Pm = sum(1 << i for i in range(N) if P[i])
Omask = {m: sum(1 << o for o in O[m]) for m in heaps}
def times(E, a):
    r = 0
    while E:
        lo = E & -E
        r |= 1 << mult[lo.bit_length() - 1][a]
        E ^= lo
    return r
anti = {}; work = []; nfail = 0; ins = 0
def insert(x, E):
    global nfail, ins
    L = anti.setdefault(x, [])
    if any(D & ~E == 0 for D in L):
        return
    L[:] = [D for D in L if E & ~D] + [E]
    ins += 1
    if not P[x] and not (E & Pm):
        nfail += 1
    work.append((x, E))
for m in heaps:
    insert(g[m], Omask[m])
gens_distinct = {}
for m in heaps:   # heaps with identical (image, option mask) act identically
    gens_distinct.setdefault((g[m], Omask[m]), m)
while work:
    x, E = work.pop()
    if E not in anti.get(x, ()):
        continue
    for (a, om) in gens_distinct:
        E2 = times(E, a) | times(om, x)
        insert(mult[x][a], E2)
print("N-condition failures:", nfail, " antichain size", sum(len(v) for v in anti.values()),
      " insertions", ins, " elements realised", len(anti))
print("single 0.07 heaps m <= %d with image in P:" % HK, [m for m in range(1, HK + 1) if P[kay_img(m)]])
print("time %.1fs" % (time.time() - t0))
