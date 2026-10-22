"""Validate notes/proof_audit2/checks/indep_sum_model.py against the repository engines
(cylcgt.pawns.value for S, lemmas.common.alt_outcome for W) on random small positions.
Run from the project root:  PYTHONPATH=. .venv/bin/python notes/proof_audit2/checks/crossvalidate.py N SEED
"""
import random, sys
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common as C

N = int(sys.argv[1]); seed = int(sys.argv[2])
rng = random.Random(seed)
bad = 0; done = 0; tested_S = tested_W = 0
while done < N:
    files = rng.choice([3, 4, 5, 6]); ranks = rng.choice([5, 6, 7]); wrap = rng.random() < 0.5
    ep = rng.random() < 0.6
    rule = rng.choice(["count", "mover", "opponent"]); aware = rng.random() < 0.7
    b = Board(files, ranks, wrap, ep)
    nw, nb_ = rng.randint(1, 4), rng.randint(1, 4)
    x = None
    for _ in range(200):
        lo, hi = 2, ranks - 1
        sq = [(f, r) for f in range(files) for r in range(lo, hi + 1)]
        if nw + nb_ > len(sq): break
        pick = rng.sample(sq, nw + nb_)
        p = Pos(frozenset(pick[:nw]), frozenset(pick[nw:]))
        if C.terminal(b, p) is None:
            x = p; break
    if x is None: continue
    pawns.PASSED_RESPECTS_EP = aware
    pawns.RACE_RULE = rule; pawns._value.cache_clear(); C._W_memo.clear(); C.alt_winner.cache_clear()
    try:
        so_repo = cgt.outcome(C.S(b, x, rule))
        wo_repo = C.alt_outcome(b, x, rule)
    except pawns.RaceError:
        continue
    M.configure(files, ranks, wrap, ep, rule, aware, big=60)
    so = M.S_outcome(x.white, x.black); wo = M.W_outcome(x.white, x.black)
    done += 1
    if so != so_repo or wo != wo_repo:
        bad += 1
        print("MISMATCH", b, rule, aware, x, "S repo/mine", so_repo, so, "W repo/mine", wo_repo, wo, flush=True)
print(f"done={done} mismatches={bad}")
