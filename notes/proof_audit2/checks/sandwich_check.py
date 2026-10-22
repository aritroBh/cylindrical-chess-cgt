"""Paper Lemma 18 (sandwich): random model trees (internal nodes = positions with Left/Right options, leaves = end positions).
Leaf values: +BIG, -BIG (known), or unknown; the 'true' unknown leaf is any game t with -2BIG <= t <= 2BIG
(here: +-BIG, 0, *, up, a switch, 2BIG, -2BIG, 1/2 ...).  Check O^- <= O <= O^+ with the repo CGT engine.
Run: PYTHONPATH=. .venv/bin/python notes/proof_audit2/checks/sandwich_check.py [N]
"""
import random, sys
from cylcgt import cgt
BIG = 8
rng = random.Random(5)
def leaf_pool():
    star = cgt.make([cgt.integer(0)], [cgt.integer(0)])
    up = cgt.make([cgt.integer(0)], [star])
    sw = cgt.make([cgt.integer(3)], [cgt.integer(-3)])
    return [cgt.integer(BIG), cgt.integer(-BIG), cgt.integer(0), star, up, sw, cgt.integer(2*BIG), cgt.integer(-2*BIG),
            cgt.number(__import__('fractions').Fraction(1, 2)), cgt.integer(1), cgt.integer(-3)]
POOL = leaf_pool()
def tree(depth):
    """returns a nested structure: ('leaf', id) or ('node', [children L], [children R])"""
    if depth == 0 or rng.random() < .25:
        return ('leaf', rng.randrange(1000))
    nl, nr = rng.randint(0, 3), rng.randint(0, 3)
    return ('node', [tree(depth - 1) for _ in range(nl)], [tree(depth - 1) for _ in range(nr)])
def val(t, leafval):
    if t[0] == 'leaf': return leafval(t[1])
    return cgt.make([val(c, leafval) for c in t[1]], [val(c, leafval) for c in t[2]])
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
bad = 0
for _ in range(N):
    t = tree(4)
    ids = set()
    def collect(x):
        if x[0] == 'leaf': ids.add(x[1])
        else:
            for c in x[1] + x[2]: collect(c)
    collect(t)
    kind = {i: rng.choice(['known+', 'known-', 'unknown', 'unknown']) for i in ids}
    truth = {i: (cgt.integer(BIG) if kind[i] == 'known+' else cgt.integer(-BIG) if kind[i] == 'known-' else rng.choice(POOL)) for i in ids}
    lo = lambda i: truth[i] if kind[i].startswith('known') else cgt.integer(-2 * BIG)
    hi = lambda i: truth[i] if kind[i].startswith('known') else cgt.integer(2 * BIG)
    O, Om, Op = val(t, lambda i: truth[i]), val(t, lo), val(t, hi)
    if not (cgt.le(Om, O) and cgt.le(O, Op)):
        bad += 1; print("VIOLATION")
print("trees:", N, "violations:", bad)
