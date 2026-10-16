"""Re-generate the exact random sample of lemmas/test_L2_big.py (run(n, seed)),
then classify every position twice:
  project: lemmas.common S/W/hereditarily_safe + pawns.sum_safe (the code under test)
  indep:   verify/.../indep_hss.py (own move generator, own sum minimax, own HSS, own (E))
and report every per-position disagreement.

Usage (from project root):
  PYTHONPATH=. .venv/bin/python verify/lemmas/L2.1-HSS-theorem-reproduce/compare_sample.py --n 1500 --seed 1 [--no-project]
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import indep_hss as I  # noqa: E402

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board  # noqa: E402
from lemmas.common import RULES, random_position, terminal  # noqa: E402


def sample(n, seed):
    """Exact replica of the RNG use in lemmas/test_L2_big.py: run()."""
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        files = rng.choice([4, 5, 6, 7, 8])
        ranks = rng.choice([6, 7, 8])
        b = Board(files, ranks, rng.random() < 0.6, rng.random() < 0.5)
        x = None
        nw, nb = rng.randint(1, 4), rng.randint(1, 4)
        for _ in range(300):
            p = random_position(rng, b, nw, nb)
            if terminal(b, p) is None:
                x = p
                break
        if x is None:
            continue
        rule = rng.choice(RULES)
        out.append((b, x, rule))   # RaceError cannot occur at a non-terminal root
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--no-project", action="store_true")
    a = ap.parse_args()
    smp = sample(a.n, a.seed)
    st = Counter()
    mism = []
    t0 = time.time()
    for i, (b, x, rule) in enumerate(smp):
        B = (b.files, b.ranks, b.wrap, b.ep)
        X = (x.white, x.black, None)
        so_i = I.s_outcome(B, X, rule)
        wo_i = I.w_outcome(B, X, rule)
        h_i = I.hss(B, X)
        e_i = I.cond_E(B, X)
        multi = len(I.comps(B, X)) > 1
        st[("HSS" if h_i else "notHSS", "E" if e_i else "notE", "agree" if so_i == wo_i else "DISAGREE")] += 1
        st["multi" if multi else "single"] += 1
        if b.ep:
            st["ep_on"] += 1
        if h_i and so_i != wo_i:
            mism.append(("INDEP HSS COUNTEREXAMPLE", str(b), I.show(X), rule, so_i, wo_i, e_i))
        if not a.no_project:
            from lemmas.common import S, W, hereditarily_safe
            so_p = cgt.outcome(S(b, x, rule))
            wo_p = cgt.outcome(W(b, x, rule))
            h_p = hereditarily_safe(b, x)
            if (so_p, wo_p, h_p) != (so_i, wo_i, h_i):
                mism.append(("PROJECT!=INDEP", str(b), I.show(X), rule, (so_p, wo_p, h_p), (so_i, wo_i, h_i)))
        if (i + 1) % 250 == 0:
            print(f"  {i+1} done, {time.time()-t0:.0f}s", flush=True)
    print(f"sample n={a.n} seed={a.seed}")
    for k in sorted(st, key=str):
        print("   ", k, st[k])
    print("mismatches / counterexamples:", len(mism))
    for m in mism:
        print("   ", m)


if __name__ == "__main__":
    main()
