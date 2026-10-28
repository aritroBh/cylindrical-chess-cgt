"""Deterministic small random check of Proposition 3.2' (a).
Run from project root with .venv/bin/python kings/delegate/out/K34/blind_check.py.
"""
import random

SEED = 340027
INSTANCES = 1000

# Each G position stores (Left options, Right options); targets are integers
# or terminal strings TOP/BOT. Empty lists model no move.
def attractor(G, Z=None, start_z=None):
    """Return terminal result (W/L/D) for every (x,z,turn) in sum arena."""
    nz = 1 if Z is None else len(Z)
    nodes = [(x, z, t) for x in range(len(G)) for z in range(nz) for t in (0, 1)]
    edges = {}
    for x, z, t in nodes:
        opts = []
        for v in G[x][t]:
            opts.append((v, None) if isinstance(v, str) else ((v, z), None))
        if Z is None:
            opts.append(((x, z), None))  # dud pass
        else:
            for v in Z[z][t]:
                opts.append((v, None) if isinstance(v, str) else ((x, v), None))
        edges[(x, z, t)] = opts
    white, black = set(), set()
    changed = True
    while changed:
        changed = False
        nw, nb = set(white), set(black)
        for u, opts in edges.items():
            t = u[2]
            # Immediate terminals resolve the whole sum.
            if t == 0:
                if any(v == 'TOP' or (v not in ('TOP', 'BOT') and v in white) for v, _ in opts):
                    nw.add(u)
                if all(v == 'BOT' or (v not in ('TOP', 'BOT') and v in black) for v, _ in opts):
                    nb.add(u)
            else:
                if all(v == 'TOP' or (v not in ('TOP', 'BOT') and v in white) for v, _ in opts):
                    nw.add(u)
                if any(v == 'BOT' or (v not in ('TOP', 'BOT') and v in black) for v, _ in opts):
                    nb.add(u)
        if nw != white or nb != black:
            changed = True
            white, black = nw, nb
    return {u: ('W' if u in white else 'L' if u in black else 'D') for u in nodes}


def gen(rng):
    n = rng.randint(1, 5)
    G = []
    choices = list(range(n)) + ['TOP', 'BOT']
    for _ in range(n):
        sides = []
        for _t in (0, 1):
            sides.append([rng.choice(choices) for _ in range(rng.randint(0, 3))])
        G.append(tuple(sides))
    # Exact four state two-shuttle Z; every non-shuttle option is suicide.
    Z = []
    for a in range(2):
        for b in range(2):
            left = [2 * (1-a) + b, 'BOT']
            right = [2 * a + (1-b), 'TOP']
            Z.append((left, right))
    return G, Z


def main():
    rng = random.Random(SEED)
    for i in range(INSTANCES):
        G, Z = gen(rng)
        exact = attractor(G, Z)
        dud = attractor(G)
        for x in range(len(G)):
            for z in range(4):
                for t in (0, 1):
                    assert exact[(x, z, t)] == dud[(x, 0, t)], (i, G, exact, dud)
    print(f'PASS instances={INSTANCES} seed={SEED} generator=n1..5; each G side has 0..3 IID options uniformly from positions plus TOP/BOT; Z is exact 4-cycle shuttles plus one suicide per side/state; compared all x, 4 states, 2 turns')

if __name__ == '__main__':
    main()
