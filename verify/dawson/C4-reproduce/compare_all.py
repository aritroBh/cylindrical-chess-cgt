"""C4 verifier: compare dawson.octal.grundy, cylcgt.dawson.octal_0137 and an independent
pure-Python 'pin with neighbours' recursion up to N, and list exceptions w.r.t. the
eventual periodic value. Run from project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C4-reproduce/compare_all.py 2000
"""
import sys
from dawson.octal import grundy, find_period
from cylcgt.dawson import octal_0137

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300

def pins(N):
    g = []
    for n in range(N + 1):
        s = {g[max(i - 1, 0)] ^ g[max(n - i - 2, 0)] for i in range(n)}
        m = 0
        while m in s:
            m += 1
        g.append(m)
    return g

a, b, c = grundy("0.137", N), octal_0137(N), pins(N)
print("worker octal.grundy == cylcgt.octal_0137:", a == b)
print("worker octal.grundy == independent pins:", a == c)
exc34 = [n for n in range(N - 34 + 1) if c[n] != c[n + 34]]
print("n with g(n)!=g(n+34):", exc34)
# exceptions relative to eventual period (values at large n)
ev = {r: c[N - ((N - r) % 34)] for r in range(34)}
print("n with g(n) != eventual periodic value:", [n for n in range(N + 1) if c[n] != ev[n % 34]])
print("find_period(indep, k=3):", find_period(c, 3))
# periodicity-theorem check with an alternative, smaller n0? (is 52 the least n0?)
print("g(51), g(85):", c[51], c[85])
