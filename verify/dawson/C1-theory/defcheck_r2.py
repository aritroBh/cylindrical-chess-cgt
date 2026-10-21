"""C1-theory, round 2: definition-level checks of the worker's Q_32 pickle.

Differs from verify_via_0p07.py (round 1) in method:
  * reducedness is tested straight from the definition: x != y must have different
    Z(x) = {z in Q : x*z in P}  (no Moore refinement);
  * the N-condition is tested by a plain breadth-first search over ALL reachable pairs
    (Phi(G), {Phi(G') : G' an option of G}) with no subsumption/antichain pruning
    (capped; if the cap is hit the check is reported as incomplete);
  * moves are generated from the pin description of 0.137 written out by hand here
    (remove 1 pin from a strip of 1; remove 2 adjacent pins from an end; remove 3 adjacent
    pins anywhere), not from dawson/octal.py.
Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C1-theory/defcheck_r2.py dawson/quotient_Q32.pkl 4000000
"""
import pickle
import sys
import time
from collections import deque

d = pickle.load(open(sys.argv[1], "rb"))
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 4_000_000
mult, P, phi = d["mult"], [bool(p) for p in d["P"]], dict(d["phi"])
N = len(mult)
n = max(phi)
t0 = time.time()


def img_strip(s):
    if s == 0:
        return 0
    return phi[1] if s == 2 else phi[s]


def pin_options(s):
    """0.137 options of a strip of s pins, as multisets of remaining strip lengths."""
    out = set()
    if s == 1:
        out.add(())
    if s >= 2:                       # take two adjacent pins at an end (digit 3: 0 or 1 heap left)
        out.add(tuple(x for x in (s - 2,) if x > 0))
    if s >= 3:                       # take three adjacent pins, starting at position i
        for i in range(0, s - 2):
            a, b = i, s - 3 - i
            out.add(tuple(sorted(x for x in (a, b) if x > 0)))
    return out


strips = list(range(1, n + 1))
g = {s: img_strip(s) for s in strips}
O = {s: {mult[img_strip(t[0]) if len(t) > 0 else 0][img_strip(t[1]) if len(t) > 1 else 0]
         for t in pin_options(s)} for s in strips}

# --- basic monoid facts
assert all(mult[0][x] == x for x in range(N)), "identity"
assert all(mult[x][y] == mult[y][x] for x in range(N) for y in range(N)), "commutativity"
print("identity in P:", P[0], "| |Q| =", N, "| |P| =", sum(P))

# --- onto
seen = {0}
fr = [0]
while fr:
    nf = []
    for q in fr:
        for s in strips:
            y = mult[q][g[s]]
            if y not in seen:
                seen.add(y)
                nf.append(y)
    fr = nf
print("onto:", len(seen) == N)

# --- reduced, from the definition
Z = []
for x in range(N):
    m = 0
    row = mult[x]
    for z in range(N):
        if P[row[z]]:
            m |= 1 << z
    Z.append(m)
print("reduced (all Z(x) distinct):", len(set(Z)) == N, "| distinct Z:", len(set(Z)))

# --- P-condition over all x in Q (Fact C.1 form)
pf = sum(1 for s in strips for x in range(N)
         if P[mult[x][g[s]]] and any(P[mult[x][o]] for o in O[s]))
print("P-condition failures:", pf)

# --- N-condition by plain BFS over reachable (a, E), no subsumption
Pm = sum(1 << i for i in range(N) if P[i])
Om = {s: sum(1 << o for o in O[s]) for s in strips}
acts = {}
for s in strips:                       # strips with equal (image, option-mask) act identically
    acts.setdefault((g[s], Om[s]), s)
acts = list(acts)
cache = {}


def times(E, a):
    k = (E, a)
    r = cache.get(k)
    if r is not None:
        return r
    r = 0
    e = E
    while e:
        lo = e & -e
        r |= 1 << mult[lo.bit_length() - 1][a]
        e ^= lo
    if len(cache) < 3_000_000:
        cache[k] = r
    return r


start = (0, 0)                         # the empty position: terminal, misere N, excluded
visited = {start}
dq = deque([start])
nfail = 0
first = None
complete = True
while dq:
    a, E = dq.popleft()
    for (h, om) in acts:
        st = (mult[a][h], times(E, h) | times(om, a))
        if st in visited:
            continue
        visited.add(st)
        if not P[st[0]] and (st[1] & Pm) == 0:
            nfail += 1
            if first is None:
                first = st[0]
        if len(visited) >= CAP:
            complete = False
            dq.clear()
            break
        dq.append(st)
print("N-condition BFS: reachable pairs", len(visited), "| complete:", complete,
      "| failures:", nfail, first)
print("time %.1fs" % (time.time() - t0))
