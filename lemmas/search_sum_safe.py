"""Search for counterexamples to cylcgt.pawns.sum_safe as a correctness test
(lemma L2): random single-component 8x8 positions (cylinder 70%, flat 30%,
e.p. on/off at random), race rule "count", for which sum_safe() is True but
the outcome of the sum model S differs from the exact whole-board outcome.

The exact outcome is taken from crosscheck/minimax.py (Codex's independent
implementation) and compared with lemmas.common.W.

Run (from the project root; about 20 minutes per run):
    PYTHONPATH=. .venv/bin/python lemmas/search_sum_safe.py --seed 11 --n 489
    PYTHONPATH=. .venv/bin/python lemmas/search_sum_safe.py --seed 13 --n 763
"""
import argparse
import random
import time

from cylcgt import cgt, pawns
from cylcgt.pawns import Board
from crosscheck import minimax as mm
from lemmas.common import S, W, random_position, terminal

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=11)
ap.add_argument("--n", type=int, default=489, help="number of single-component positions tried")
a = ap.parse_args()
rng = random.Random(a.seed)
t0 = time.time()
found = []
tried = 0
while tried < a.n:
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
    tried += 1
    try:
        s = S(b, x, "count")
    except pawns.RaceError:
        continue
    if not pawns.sum_safe(b, x):
        continue
    exact = mm.outcome_class(mm.Board(8, 8, wrap, ep), mm.Position(x.white, x.black, None))
    if cgt.outcome(s) != exact:
        found.append((str(b), str(x), cgt.outcome(s), exact, cgt.outcome(W(b, x, "count"))))
        print("counterexample (board, position, o(S), crosscheck, o(W)):", found[-1], flush=True)
print(f"seed {a.seed}: tried {tried} single components, {len(found)} counterexamples, {time.time() - t0:.0f} s")
