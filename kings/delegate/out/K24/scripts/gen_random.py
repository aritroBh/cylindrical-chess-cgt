"""Random positions in SPEC.md format: usage gen_random.py W H N seed"""
import random, sys
W, H, N, seed = map(int, sys.argv[1:5]); ONE = len(sys.argv) > 5 and sys.argv[5] == 'one'
random.seed(seed)
def sq(s): return "abcdefgh"[s % W] + str(s // W + 1)
out = set()
while len(out) < N:
    nw = 1 if ONE else random.choice([1, 1, 2]); nb = 1 if ONE else random.choice([1, 1, 2])
    squares = random.sample(range(W * H), 2 + nw + nb)
    wk, bk = squares[:2]
    wp = squares[2:2 + nw]; bp = squares[2 + nw:]
    if any(s // W in (0, H - 1) for s in wp + bp): continue
    toks = [f"K{sq(wk)}", f"k{sq(bk)}"] + [f"P{sq(s)}" for s in wp] + [f"p{sq(s)}" for s in bp]
    out.add(" ".join(toks) + " " + random.choice("wb") + " -")
print("\n".join(sorted(out)))
