"""K56 referee: is Att^X_k monotone in k? Search random toy games (no checks) for a state that Y wins with
X allowed 1 (or unlimited) passes but not with 0 (or 1). Stalemate (no move, no pass) is a draw, as in P."""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from toy import pass_game, rand_game, INF
rng = random.Random(5); found = {}
for it in range(20000):
    G = rand_game(rng, rng.randint(1, 4), 0.3, 0.3)
    n = len(G[0])
    p0, p1, pi = pass_game(G, 1, 0), pass_game(G, 1, 1), pass_game(G, 1, INF)
    for g in range(n):
        for s in (0, 1):
            if p1[(g, s, 1)] == "W" and p0[(g, s, 0)] != "W": found.setdefault("Att1 not in Att0", (G, g, s))
            if pi[(g, s, INF)] == "W" and p1[(g, s, 1)] != "W": found.setdefault("Attinf not in Att1", (G, g, s))
for k, v in found.items(): print(k, "example (L, R), position, side:", v)
print("done", len(found))
