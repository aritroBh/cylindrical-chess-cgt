"""Search for positions WITHOUT a live e.p. right where the pure-game sum
identity P(X) = sum_i P(X_i) fails (lemma L1, open question 1.8).

Mode "family" (deterministic, about 4 minutes): flat boards of 6-7 files and
5-6 ranks; component A on files a,b holds the e.p. motif W a2 / B b4 plus
optionally one more pawn; file c is empty; component B gets 1-3 pawns on the
remaining files in every placement and colouring.
Mode "random" (about 10 minutes): random two-component positions with an e.p.
motif, flat and cylinder.

Run (from the project root):
    PYTHONPATH=. .venv/bin/python lemmas/search_ep_roots.py family
    PYTHONPATH=. .venv/bin/python lemmas/search_ep_roots.py random --seed 5 --n 53732
"""
import argparse
import itertools
import random
import time

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import pure, pure_sum


def family():
    n = 0
    breaks = []
    for ranks in (5, 6):
        for files in (6, 7):
            b = Board(files, ranks, False, True)
            Bsq = [(f, r) for f in range(3, files) for r in range(2, ranks)]
            for extra in [None, ("W", (1, 2)), ("B", (0, ranks - 1)), ("W", (1, 3)), ("B", (1, 5))]:
                w0, b0 = {(0, 2)}, {(1, 4)}
                if extra:
                    if extra[1] in w0 | b0:
                        continue
                    (w0 if extra[0] == "W" else b0).add(extra[1])
                for k in (1, 2, 3):
                    for sqs in itertools.combinations(Bsq, k):
                        for cols in itertools.product("WB", repeat=k):
                            w = w0 | {s for s, c in zip(sqs, cols) if c == "W"}
                            bl = b0 | {s for s, c in zip(sqs, cols) if c == "B"}
                            x = Pos(frozenset(w), frozenset(bl))
                            if len(pawns.components(b, x)) < 2:
                                continue
                            n += 1
                            if pure(b, x) is not pure_sum(b, x):
                                breaks.append((str(b), str(x)))
    return n, breaks


def rand(seed, n_target):
    rng = random.Random(seed)
    n = 0
    breaks = []
    while n < n_target:
        files = rng.choice([5, 6, 7])
        ranks = rng.choice([5, 6])
        wrap = rng.random() < 0.5
        b = Board(files, ranks, wrap, True)
        k = rng.choice([2, 3])
        Bf = list(range(k + 1, files - (1 if wrap else 0)))
        if not Bf:
            continue
        w, bl = set(), set()
        f0 = rng.randrange(k)
        f1 = f0 + 1 if f0 + 1 < k else f0 - 1
        if rng.random() < 0.5:
            w.add((f0, 2)); bl.add((f1, 4))
        else:
            bl.add((f0, ranks - 1)); w.add((f1, ranks - 3))
        Asq = [(f, r) for f in range(k) for r in range(2, ranks)]
        Bsq = [(f, r) for f in Bf for r in range(2, ranks)]
        for s in rng.sample(Asq, rng.randint(0, 2)):
            if s not in w | bl:
                (w if rng.random() < 0.5 else bl).add(s)
        for s in rng.sample(Bsq, min(len(Bsq), rng.randint(1, 3))):
            if s not in w | bl:
                (w if rng.random() < 0.5 else bl).add(s)
        if len(w | bl) > 6:
            continue
        x = Pos(frozenset(w), frozenset(bl))
        if len(pawns.components(b, x)) < 2:
            continue
        n += 1
        if pure(b, x) is not pure_sum(b, x):
            breaks.append((str(b), str(x)))
    return n, breaks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["family", "random"])
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--n", type=int, default=53732)
    a = ap.parse_args()
    t0 = time.time()
    n, br = family() if a.mode == "family" else rand(a.seed, a.n)
    print(f"{a.mode}: tested {n} positions without a live right; identity breaks: {len(br)}; {time.time() - t0:.0f} s")
    for z in br[:10]:
        print("   ", z)
