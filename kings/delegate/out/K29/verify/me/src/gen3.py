import itertools, random, sys
sq = [f + str(r) for f in 'ef' for r in range(2, 6)]
def subs(k):
    for c in range(k + 1): yield from itertools.combinations(sq, c)
allc = []
for W in subs(3):
    for B in subs(3):
        if set(W) & set(B): continue
        allc.append((len(W) + len(B), ['P' + s for s in W] + ['p' + s for s in B]))
print(len(allc), file=sys.stderr)
mode, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
random.seed(seed)
pool = [c for t, c in allc if (t >= 5 if mode == 'hi' else t == 4)]
for c in random.sample(pool, min(n, len(pool))): print(' '.join(c))
