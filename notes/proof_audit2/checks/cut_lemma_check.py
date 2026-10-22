"""Paper Theorem 2 (cut lemma), tested with the independent minimax (outcomes of S and W, all race rules, e.p. settings):
a pawn position on cyl(n) with an empty file e has the same outcome as the relabelled position on flat(n-1).
Run: python3 notes/proof_audit2/checks/cut_lemma_check.py [N] [seed]
"""
import random, sys
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
bad = 0; n_done = 0
while n_done < N:
    n = rng.choice([3, 4, 5, 6, 7]); ranks = rng.choice([5, 6, 7]); ep = rng.random() < .6
    rule = rng.choice(["count", "mover", "opponent"]); aware = rng.random() < .7
    e = rng.randrange(n)
    files = [f for f in range(n) if f != e]
    nw, nb = rng.randint(1, 3), rng.randint(1, 3)
    sq = [(f, r) for f in files for r in range(2, ranks)]
    if nw + nb > len(sq): continue
    pick = rng.sample(sq, nw + nb)
    W, B = frozenset(pick[:nw]), frozenset(pick[nw:])
    relabel = {f: (f - e - 1) % n for f in files}          # files e+1, e+2, ..., e-1  ->  0 .. n-2
    W2 = frozenset((relabel[f], r) for f, r in W); B2 = frozenset((relabel[f], r) for f, r in B)
    res = []
    for (nf, wrap, w, b) in ((n, True, W, B), (n - 1, False, W2, B2)):
        M.configure(nf, ranks, wrap, ep, rule, aware, big=40)
        if M.passed(w, b, None, 'W') and M.passed(w, b, None, 'B'): res = None; break
        try:
            res.append((M.S_outcome(w, b), M.W_outcome(w, b)))
        except ValueError:
            res = None; break
    if res is None: continue
    n_done += 1
    if res[0] != res[1]:
        bad += 1; print("MISMATCH", n, e, sorted(W), sorted(B), rule, aware, ep, res)
print(f"cut-lemma outcome checks: {n_done}, mismatches {bad}")
