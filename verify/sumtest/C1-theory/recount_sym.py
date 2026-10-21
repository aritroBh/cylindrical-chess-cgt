"""THEORY-lens recount of claim C1 from the worker's own data files (read-only).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C1-theory/recount_sym.py

1. Recounts the headline (cases, pairs, differing) straight from sumtest/data/*.json.gz.
2. Measures how much of the 4,967,550 is redundant:
   - symmetry orbits of the 55,195 positions (file reflection, cylinder rotation,
     colour swap W<->B with rank r -> 9-r); a symmetric image is the same test;
   - how many (position, rule) cases have the same vector with e.p. on and off;
   - how many (position, e.p.) cases have the same vector under all 3 race rules.
Writes nothing outside this directory (prints only).
"""
import gzip
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA = os.path.join(ROOT, "sumtest", "data")
BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True), "cyl5": (5, True)}
RULES = ("count", "mover", "opponent")
F = "abcdefghijklmnopqrstuvwxyz"


def L(name):
    with gzip.open(os.path.join(DATA, name), "rt") as fh:
        return json.load(fh)


def parse(text):
    w, b = text.split("/")
    sq = lambda t: (F.index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()))


def canon(W, B, n, wrap):
    """Lexicographically least image under the symmetry group of the board."""
    imgs = []
    shifts = range(n) if wrap else [0]
    for refl in (False, True):
        for s in shifts:
            def mf(f):
                g = (n - 1 - f) if refl else f
                return (g + s) % n if wrap else g
            W2 = tuple(sorted((mf(f), r) for f, r in W))
            B2 = tuple(sorted((mf(f), r) for f, r in B))
            imgs.append((W2, B2))
            # colour swap: white pawn (f,r) -> black pawn (f, 9-r) and vice versa
            imgs.append((tuple(sorted((f, 9 - r) for f, r in B2)), tuple(sorted((f, 9 - r) for f, r in W2))))
    return min(imgs)


def main():
    tot_cases = tot_pairs = 0
    diff = Counter()
    orbits_total = 0
    ep_same = ep_cases = 0
    rule_same = rule_cases = 0
    for b, (n, wrap) in BOARDS.items():
        cy = {(r, e): L(f"cylcgt__{b}__{r}__{'ep' if e else 'noep'}.json.gz")["outcomes"]
              for r in RULES for e in (True, False)}
        keys = set(cy[("count", True)])
        orbs = {canon(*parse(k), n, wrap) for k in keys}
        orbits_total += len(orbs)
        print(f"{b}: positions {len(keys)}, symmetry orbits {len(orbs)}")
        for r in RULES:
            for e in (True, False):
                assert set(cy[(r, e)]) == keys
                variants = ["plain__whole", "plain__comp", "plain-global__whole"] if e else ["off__whole", "off__comp"]
                for var in variants:
                    m = L(f"mine__{b}__{r}__{var}.json.gz")["outcomes"]
                    assert set(m) == keys
                    d = sum(m[k] != cy[(r, e)][k] for k in keys)
                    dp = sum(x != y for k in keys for x, y in zip(m[k], cy[(r, e)][k]))
                    diff[var] += dp
                    if var in ("plain__whole", "off__whole"):
                        tot_cases += len(keys)
                        tot_pairs += sum(len(m[k]) for k in keys)
                    if d:
                        print("  DIFF", b, r, e, var, d, dp)
            for k in keys:
                ep_cases += 1
                ep_same += cy[(r, True)][k] == cy[(r, False)][k]
        for e in (True, False):
            for k in keys:
                rule_cases += 1
                rule_same += len({cy[(r, e)][k] for r in RULES}) == 1
    print(f"headline: cases {tot_cases}, pairs {tot_pairs}, differing pairs per variant {dict(diff)}")
    print(f"symmetry orbits over all boards: {orbits_total} (of 55,195 positions)")
    print(f"(position, rule) cases with identical cylcgt vector e.p. on vs off: {ep_same}/{ep_cases}")
    print(f"(position, e.p.) cases with identical cylcgt vector under all 3 rules: {rule_same}/{rule_cases}")


if __name__ == "__main__":
    main()
