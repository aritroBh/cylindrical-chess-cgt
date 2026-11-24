"""K57 referee: cross-check of toyref.py's sum solver against the K56 referee's toy.py (sum_values) on groups without
checks and e.p. rights, and of toyref's over_vals against toy.py's sum_values(OVER, T)."""
import random
import sys
sys.path.insert(0, sys.argv[1])  # directory of the K56 referee's toy.py
import toy  # noqa: E402
import toyref  # noqa: E402

rng = random.Random(5)
n_cmp = n_diff = 0
for it in range(3000):
    n = rng.randint(2, 7)
    L, R = toy.rand_game(rng, n, rng.choice([0.2, 0.35]), 0.25)
    T = toy.rand_game(rng, rng.randint(1, 4), rng.choice([0.2, 0.4]), rng.choice([0.0, 0.3]))
    a = toy.sum_values((L, R), T)
    G = toyref.Group(n, [[[(y, 0) for y in L[g]], [(y, 0) for y in R[g]]] for g in range(n)], [[[], []] for _ in range(n)],
                     [[False, False] for _ in range(n)])
    b = toyref.sum_vals(G, T)
    for (g, t, s), v in a.items():
        n_cmp += 1
        n_diff += v != b[(g, 0, t, s)]
    ov = toyref.over_vals(T)
    oa = toy.sum_values(toy.OVER, T)
    for (o, t, s), v in oa.items():
        n_cmp += 1
        n_diff += v != ov[(o, t, s)]
print(f"xval: {n_cmp} values compared, {n_diff} differ")
