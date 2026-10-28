"""Deletion sensitivity check for Proposition 3.2' (d).
Run from project root with .venv/bin/python kings/delegate/out/K34/blind_deletions.py.
"""
import random
from blind_check import attractor, gen, SEED, INSTANCES


def z_exact():
    return [([2 * (1-a) + b, 'BOT'], [2*a + (1-b), 'TOP'])
            for a in range(2) for b in range(2)]


def main():
    base = z_exact()
    base0 = attractor([( [], [] )], base)
    for idx, turn in [(z, t) for z in range(4) for t in (0, 1)]:
        z = [ (list(l), list(r)) for l, r in base ]
        z[idx][turn].remove((2 * (1-idx//2) + idx%2) if turn == 0 else (2*(idx//2) + (1-idx%2)))
        # The removed edge is the shuttle arrow for this state and side.
        out = attractor([([], [])], z)
        assert any(out[(0, s, t)] != base0[(0, s, t)]
                   for s in range(4) for t in (0, 1)), (idx, turn, out, base0)
    print('PASS G=0: each of 8 individual shuttle-arrow deletions changes at least one of the 8 state/turn outcomes')

    rng = random.Random(SEED)
    counts = [0] * 8
    for _ in range(INSTANCES):
        G, _ = gen(rng)
        base = z_exact()
        original = attractor(G, base)
        for k, (idx, turn) in enumerate((z, t) for z in range(4) for t in (0, 1)):
            z = [(list(l), list(r)) for l, r in base]
            if turn == 0:
                target = 2 * (1-idx//2) + idx%2
            else:
                target = 2 * (idx//2) + (1-idx%2)
            z[idx][turn].remove(target)
            altered = attractor(G, z)
            if any(altered[(x, idx, t)] != original[(x, idx, t)]
                   for x in range(len(G)) for t in (0, 1)):
                counts[k] += 1
    print(f'COMPUTED-1 seed={SEED} instances={INSTANCES} changed-instance-counts-per-deleted-arrow={counts}')

if __name__ == '__main__':
    main()
