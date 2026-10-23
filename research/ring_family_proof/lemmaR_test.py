"""Check of the reduction lemma (Lemma R): deleting terminal-loss and poisoned moves does not change the outcome of
G + *h.  For random positions (n = 3..8 files, 4..12 pawns) compare
   (a) the outcome string of G + *h, h = 0..4, from the full search `rg solve` (no deletion at all), with
   (b) the same string computed on the reduced graph `rg reduce` + graph.solve.
Usage: python lemmaR_test.py [N] [seed]
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph
from lemmaL_test import classify_many

def rand_tokens(rng):
    n = rng.randrange(3, 9)
    npawn = rng.randrange(4, 13)
    cells = {}
    for _ in range(npawn):
        f = rng.randrange(n); r = rng.randrange(2, 8)
        cells[(f, r)] = "W" if rng.random() < 0.5 else "B"
    toks = []
    for f in range(n):
        w = tuple(sorted(r for (g, r), c in cells.items() if g == f and c == "W"))
        b = tuple(sorted(r for (g, r), c in cells.items() if g == f and c == "B"))
        toks.append(fam.join_file((w, b)))
    return toks

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    cases = []
    while len(cases) < N:
        t = rand_tokens(rng)
        cases.append(t)
    blocks = classify_many([" ".join(t) for t in cases])
    keep = [t for t, b in zip(cases, blocks) if b["passed"] == "PASSED 0 0"]
    # structured positions: random walks (any non-terminal move, e.p. flags allowed) from small family members
    walk = []
    for _ in range(300):
        famname = rng.choice(["odd", "even", "F"])
        n = rng.choice({"odd": [5, 7, 9], "even": [6, 8, 10], "F": [5, 7, 8, 9]}[famname])
        walk.append(fam.FAMILIES[famname](n))
    for step in range(rng.randrange(1, 12) + 10):
        bl = classify_many([" ".join(t) for t in walk])
        for i, b in enumerate(bl):
            cand = [child for side, code, mv, child in b["mv"] if code in "KP"]
            if cand:
                walk[i] = rng.choice(cand).split()
                if step % 4 == 0 and not any(x.startswith("ep") for x in walk[i]): keep.append(list(walk[i]))
    keep = [t for t in keep if not any(x.startswith("ep") for x in t) or True]
    bad = 0; sigs = {}
    for t in keep:
        full = fam.run_rg("solve", " ".join(t) + "\n", extra=("4",)).split()[0]
        g = graph.build(t)
        red = graph.solve(g, 4)
        sigs[full] = sigs.get(full, 0) + 1
        if full != red:
            bad += 1
            if bad <= 5: print("MISMATCH", " ".join(t), full, red)
    print(f"Lemma R check: {len(keep)} non-terminal random positions, outcome strings of G+*h (h=0..4) full vs reduced: mismatches {bad}; "
          f"{len(sigs)} distinct strings, e.g. {sorted(sigs.items(), key=lambda x: -x[1])[:6]}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
