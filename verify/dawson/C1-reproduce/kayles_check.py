"""Check the indexing claim 'strips <= 32 of 0.137 = Dawson's Kayles (0.07) heaps <= 33' and the
quotient's predictions against a direct misere solver for Dawson's Kayles, written from the
0.07 rule only (a move removes two adjacent pins from a row of pins).
Run from project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/kayles_check.py verify/dawson/C1-reproduce/quotient_Q32.pkl 44
"""
import pickle, sys
from functools import lru_cache
sys.setrecursionlimit(100000)
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from indep_verify import strip_options

def kayles_opts(m):            # row of m pins, remove pins j, j+1 (1 <= j < m)
    return {tuple(sorted(x for x in (j - 1, m - j - 1) if x > 0)) for j in range(1, m)}

# 1. 0.137 strip n has the same options as 0.07 heap n+1, under heap -> heap+1 (0.07 heaps 0, 1 are null)
for n in range(1, 60):
    a = {tuple(sorted(x + 1 for x in t)) for t in strip_options(n)}
    b = {tuple(sorted(x for x in t if x >= 2)) for t in kayles_opts(n + 1)}
    a = {tuple(x for x in t if x >= 2) for t in a}
    assert a == b, (n, a, b)
print("0.137 strip n  ==  0.07 heap n+1 (option sets agree under the shift) for n = 1..59")

def canon(t):
    return tuple(sorted(x for x in t if x >= 2))   # 0.07 heaps of size 0, 1 have no move

@lru_cache(maxsize=None)
def misereP(pos):              # pos: sorted tuple of 0.07 heaps (>= 2)
    if not pos:
        return False           # no move: player to move wins in misere
    seen = set()
    for i, m in enumerate(pos):
        if m in seen: continue
        seen.add(m)
        rest = pos[:i] + pos[i + 1:]
        for t in kayles_opts(m):
            if misereP(canon(rest + t)):
                return False
    return True

def parts(total, maxp):
    if total == 0:
        yield (); return
    for k in range(min(total, maxp), 1, -1):
        for r in parts(total - k, k):
            yield r + (k,)

d = pickle.load(open(sys.argv[1], "rb"))
mult, P, phi = d["mult"], d["P"], dict(d["phi"]); phi[2] = phi[1]
T = int(sys.argv[2])
checked = bad = 0
for t in range(T + 1):                      # t = total of 0.07 heap sizes
    for lam in parts(t, 33):
        x = 0
        for m in lam:
            x = mult[x][phi[m - 1]]         # 0.07 heap m = 0.137 strip m - 1 (m - 1 >= 1)
        checked += 1
        if bool(P[x]) != misereP(tuple(sorted(lam))):
            bad += 1
print(f"Dawson's Kayles positions with heaps 2..33, total pins <= {T}: {checked} checked against the "
      f"quotient, disagreements: {bad}")
print("single 0.07 heaps m <= 34 that are misere P:", [m for m in range(2, 35) if misereP((m,))])
