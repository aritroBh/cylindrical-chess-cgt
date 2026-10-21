"""Exact environment for (normal-play) Dawson's chess as sums of strips.

A position is a multiset of strip lengths (positive ints). Each strip of length k
has Grundy value g(k) (octal 0.137). The value of a sum is the nim-sum of the
component Grundy values; first player (side to move) wins iff nim-sum != 0.

Ring (cylinder) components: a full 3xn ring has value 0/1 = (g(n-3)==0)?1:0
i.e. first player wins iff g(n-3)==0. Represented as ('ring', n).

This module reuses dawson/octal.py read-only for g(n).
"""
import random
import sys

sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from dawson.octal import grundy as _grundy

G_MAX = 200
_G = _grundy("0.137", G_MAX)


def g(n):
    """Grundy value of a flat strip of length n (n>=0). g(0)=0."""
    if n < 0:
        raise ValueError(n)
    if n > G_MAX:
        # extend on demand
        global _G
        _G = _grundy("0.137", n)
    return _G[n]


def ring_value(n):
    """Outcome (0/1 win for first player) of a full 3xn cylinder ring, n>=3."""
    if n < 3:
        return 0
    return 1 if g(n - 3) == 0 else 0


def nimsum(lengths):
    x = 0
    for L in lengths:
        x ^= g(L)
    return x


def outcome(lengths, rings=None):
    """First-player win (1) / loss (0) for a position given flat strip lengths and rings."""
    x = nimsum(lengths)
    for n in (rings or []):
        # ring contributes a nimber 0 or *? Ring value is 0 or 1 as a number (not nimber).
        # In CGT a ring is a number 0 or 1; for outcome of a sum of numbers+ nimbers we
        # cannot simply XOR. For this ML task we restrict to strip sums (flat) primarily.
        # Rings are recorded but not mixed here; handle separately if needed.
        pass
    # For pure strip sums:
    return 1 if x != 0 else 0


def outcome_strips(lengths):
    return 1 if nimsum(lengths) != 0 else 0


def random_composition(total, m):
    """Return m positive ints summing to total."""
    if m < 1 or m > total:
        raise ValueError((total, m))
    cuts = sorted(random.sample(range(1, total), m - 1))
    parts = []
    prev = 0
    for c in cuts + [total]:
        parts.append(c - prev)
        prev = c
    return parts


def gen_positions(total_min, total_max, n_per_total, rng_seed=0):
    """Generate list of (lengths_tuple, label) for totals in [total_min,total_max]."""
    random.seed(rng_seed)
    data = []
    for T in range(total_min, total_max + 1):
        if T == 0:
            data.append(((), 0))
            continue
        for _ in range(n_per_total):
            m = random.randint(1, min(T, 12))
            # sometimes allow more strips
            if random.random() < 0.3:
                m = random.randint(1, T)
            if m > T:
                m = T
            lengths = tuple(sorted(random_composition(T, m)))
            data.append((lengths, outcome_strips(lengths)))
    return data


if __name__ == "__main__":
    # quick sanity
    for n in range(0, 20):
        print(n, g(n))
    print("outcome [1,2,3]:", outcome_strips([1, 2, 3]), "nimsum", nimsum([1, 2, 3]))
