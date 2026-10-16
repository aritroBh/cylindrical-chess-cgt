"""Verifier: random differential test, indep.py versus cylcgt/lemmas.common, of
o(S) and o(W) on random non-terminal positions (4-8 files, 6-8 ranks, flat and
cylinder, e.p. on/off, all three race rules). Also counts single-component
positions where o(S) != o(W) (sum_safe is True on every single component).
Run from project root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python \
      verify/lemmas/L2.2-sum_safe-counterexample-reproduce/diff_random.py --n 400 --seed 101
"""
import argparse, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import S, W, random_position, terminal

ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=400); ap.add_argument("--seed", type=int, default=101)
a = ap.parse_args()
rng = random.Random(a.seed)
t0 = time.time(); done = 0; mism = 0; single_bad = []; ss_true = 0
while done < a.n:
    n, m = rng.choice([4, 5, 6, 7, 8]), rng.choice([6, 7, 8])
    b = Board(n, m, rng.random() < 0.6, rng.random() < 0.5)
    x = random_position(rng, b, rng.randint(1, 4), rng.randint(1, 4))
    if terminal(b, x) is not None:
        continue
    rule = rng.choice(["count", "mover", "opponent"])
    oS, oW = cgt.outcome(S(b, x, rule)), cgt.outcome(W(b, x, rule))
    bd = indep.Bd(n, m, b.wrap, b.ep); p = (x.white, x.black, None)
    iS, iW = indep.s_outcome(bd, p, rule), indep.w_outcome(bd, p, rule)
    done += 1
    if (oS, oW) != (iS, iW):
        mism += 1
        print("MISMATCH", b, x, rule, oS, iS, oW, iW, flush=True)
    if pawns.sum_safe(b, x):
        ss_true += 1
    if len(pawns.components(b, x)) == 1 and oS != oW:
        single_bad.append((str(b), str(x), rule, oS, oW))
    if done % 100 == 0:
        indep.clear(); print(f"  {done} done, {time.time()-t0:.0f}s", flush=True)
print(f"seed {a.seed}: {done} positions, implementation mismatches {mism}, sum_safe True {ss_true}, "
      f"single-component o(S)!=o(W): {len(single_bad)}")
for r in single_bad:
    print("   ", r)
