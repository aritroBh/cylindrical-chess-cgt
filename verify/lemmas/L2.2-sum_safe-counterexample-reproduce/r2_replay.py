"""Replay the exact position sequence of lemmas/search_sum_safe.py (same RNG
calls; generation uses the project's random_position/terminal/components so
the sequence is identical), then evaluate every tried position with the
INDEPENDENT code r2_indep.py (CGT-free sum model + own whole-board minimax).
Sharded: --shard k --nshards K evaluates tried-indices i with i % K == k.

cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python \
  verify/lemmas/L2.2-sum_safe-counterexample-reproduce/r2_replay.py --seed 13 --n 763 --shard 0 --nshards 1
"""
import argparse, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import pawns
from cylcgt.pawns import Board
from lemmas.common import random_position, terminal
from r2_indep import Game, show

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int); ap.add_argument("--n", type=int)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
a = ap.parse_args()
rng = random.Random(a.seed)
seq = []
while len(seq) < a.n:
    wrap = rng.random() < 0.7
    ep = rng.random() < 0.5
    b = Board(8, 8, wrap, ep)
    nw, nb = rng.randint(2, 4), rng.randint(2, 4)
    x = None
    for _ in range(300):
        p = random_position(rng, b, nw, nb)
        if terminal(b, p) is None and len(pawns.components(b, p)) == 1:
            x = p
            break
    if x is None:
        continue
    seq.append((wrap, ep, (x.white, x.black, None)))
t0 = time.time()
games = {}
found = []
done = 0
for i, (wrap, ep, x) in enumerate(seq):
    if i % a.nshards != a.shard:
        continue
    g = games.setdefault((wrap, ep), Game(8, 8, wrap, ep, "count"))
    s, w = g.S_outcome(x), g.W_outcome(x)
    done += 1
    if s != w:
        found.append((i, wrap, ep, show(x), s, w))
        print("counterexample (index, wrap, ep, position, o(S), o(W)):", found[-1], flush=True)
    if len(g.thr.cache_info()._asdict()) and g.thr.cache_info().currsize > 3_000_000:
        games.clear()
print(f"seed {a.seed} n {a.n} shard {a.shard}/{a.nshards}: evaluated {done}, counterexamples {len(found)}, {time.time()-t0:.0f}s", flush=True)
