"""Sanity check of the independent code against the project on random
positions (all rules, flat/cyl, e.p. on/off, 4-7 files, 6-8 ranks): compares
o(S) [r2_indep CGT-free] with o(pawns.value) and o(W) [r2_indep minimax] with
o(lemmas.common.W).
cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python \
  verify/lemmas/L2.2-sum_safe-counterexample-reproduce/r2_agree.py --n 300 --seed 77"""
import argparse, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import cgt, pawns
from cylcgt.pawns import Board
from lemmas.common import RULES, S, W, random_position, terminal
from r2_indep import Game
ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int); ap.add_argument("--seed", type=int)
a = ap.parse_args(); rng = random.Random(a.seed)
done = mS = mW = dis = 0; t0 = time.time()
while done < a.n:
    b = Board(rng.choice([4, 5, 6, 7]), rng.choice([6, 7, 8]), rng.random() < 0.6, rng.random() < 0.5)
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    x = None
    for _ in range(300):
        p = random_position(rng, b, nw, nb)
        if terminal(b, p) is None:
            x = p; break
    if x is None:
        continue
    rule = rng.choice(RULES)
    try:
        ps, pw = cgt.outcome(S(b, x, rule)), cgt.outcome(W(b, x, rule))
    except pawns.RaceError:
        continue
    g = Game(b.files, b.ranks, b.wrap, b.ep, rule)
    xx = (x.white, x.black, None)
    s, w = g.S_outcome(xx), g.W_outcome(xx)
    done += 1; dis += ps != pw
    if s != ps:
        mS += 1; print("S mismatch", b, x, rule, ps, s, flush=True)
    if w != pw:
        mW += 1; print("W mismatch", b, x, rule, pw, w, flush=True)
print(f"{done} positions: o(S) mismatches {mS}, o(W) mismatches {mW}; positions with o(S)!=o(W): {dis}; {time.time()-t0:.0f}s")
