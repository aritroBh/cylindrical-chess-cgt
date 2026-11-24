"""K56: random small D-games as test games T (K47/K55 line format).  usage: gen56.py <count> <seed> <terminals 0|1> <prefix>
Each game has 2 to 5 nodes; every option list draws from the nodes (loops allowed) and, if terminals are on, from W and B."""
import random, sys
cnt, seed, term, pre = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(seed)
for g in range(cnt):
    n = rng.randint(2, 5)
    items = []
    for i in range(n):
        def opts():
            pool = list(range(n)) + (['W', 'B'] if term else [])
            k = rng.choice([0, 0, 1, 1, 1, 2, 2, 3])
            return sorted(set(rng.choice(pool) for _ in range(k)), key=str)
        items.append('%d: L=%s R=%s' % (i, ','.join(map(str, opts())), ','.join(map(str, opts()))))
    print('%s%d | %d | %s' % (pre, g, n, ' ; '.join(items)))
