import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from pawnlevel import make_solver, start, g137, PROMO
n = int(sys.argv[1])
t = time.time()
s = make_solver(n, True)
w = s(start('x' * n), 1)
print(f"ring n={n}: White-first wins = {w}; predicted g(n-3)==0 -> {g137(n)[n-3]==0}; "
      f"cache {s.cache_info().currsize}; promotions {PROMO[0]}; {time.time()-t:.1f}s", flush=True)
