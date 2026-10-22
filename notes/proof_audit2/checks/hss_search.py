"""Adversarial search for counterexamples to
   (A) paper Theorem 10:  X HSS  and  (E)  and  BIG > moves  =>  o(S(X)) = o(W(X)),
   (B) paper Conjecture 4 read WITHOUT (E): X HSS and BIG > moves => o(S) = o(W)?
Uses the independent CGT-free implementation (indep_sum_model.py).  HSS, tau, (E) are recomputed here
from the paper's Definition 9 / condition (E):
   tau(component) contains +/- iff some position reachable (moves of either side, any order, stopping at the
   first position with a passed pawn) has a white/black passed pawn;   HSS = every non-terminal reachable
   position is pairwise safe (no two different components with opposite threats);
   (E) = no non-terminal reachable position with >= 2 components has a usable e.p. right.
Usage: python3 hss_search.py SECONDS SEED
"""
import random, sys, time
from functools import lru_cache
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M

def usable(W, B, ep):
    if not ep: return False
    side = ep[2]
    return len(M.pawn_moves(W, B, ep, side)) != len(M.pawn_moves(W, B, None, side))

def mover_free_term(W, B, ep):
    wp, bp = M.passed(W, B, ep, 'W'), M.passed(W, B, ep, 'B')
    return wp, bp

@lru_cache(maxsize=None)
def tau(W, B, ep):
    wp, bp = mover_free_term(W, B, ep)
    out = set()
    if wp: out.add(1)
    if bp: out.add(-1)
    if out: return frozenset(out)
    for side in 'WB':
        for (w2, b2, e2) in M.pawn_moves(W, B, ep, side):
            out |= tau(w2, b2, e2)
    return frozenset(out)

def reachable(W, B, ep):
    seen = {(W, B, ep)}; stack = [(W, B, ep)]
    while stack:
        x = stack.pop()
        wp, bp = mover_free_term(*x)
        if wp or bp: continue
        for side in 'WB':
            for y in M.pawn_moves(x[0], x[1], x[2], side):
                if y not in seen:
                    seen.add(y); stack.append(y)
    return seen

def analyse(W, B, ep=None):
    hss, E = True, True
    for (w, b, e) in reachable(W, B, ep):
        wp, bp = mover_free_term(w, b, e)
        if wp or bp: continue
        cs = M.comps(w, b, e)
        if len(cs) >= 2:
            if usable(w, b, e): E = False
            ts = [tau(*c) for c in cs]
            for i, a in enumerate(ts):
                for j, bb in enumerate(ts):
                    if i != j and 1 in a and -1 in bb: hss = False
    return hss, E

def rand_pos(rng, files, ranks):
    nw, nb = rng.randint(1, 4), rng.randint(1, 4)
    sq = [(f, r) for f in range(files) for r in range(2, ranks)]
    for _ in range(100):
        pick = rng.sample(sq, nw + nb)
        # bias: sometimes put pawns on start ranks to create e.p. motifs
        if rng.random() < 0.6:
            pick = [(f, 2 if (i < nw and rng.random() < .6) else (ranks - 1 if (i >= nw and rng.random() < .6) else r))
                    for i, (f, r) in enumerate(pick)]
            if len(set(pick)) < len(pick): continue
        W, B = frozenset(pick[:nw]), frozenset(pick[nw:])
        return W, B
    return None

if __name__ == "__main__":
    secs, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    t0 = time.time(); n = 0
    stat = {}
    cex = []
    while time.time() - t0 < secs:
        files = rng.choice([4, 5, 6, 7]); ranks = rng.choice([5, 6]); wrap = rng.random() < 0.4
        rule = rng.choice(["count", "mover", "opponent"]); aware = rng.random() < 0.75
        M.configure(files, ranks, wrap, True, rule, aware, big=60)
        tau.cache_clear()
        p = rand_pos(rng, files, ranks)
        if p is None: continue
        W, B = p
        wp, bp = M.passed(W, B, None, 'W'), M.passed(W, B, None, 'B')
        if wp or bp: continue
        try:
            hss, E = analyse(W, B)
            so, wo = M.S_outcome(W, B), M.W_outcome(W, B)
        except ValueError:
            continue
        n += 1
        key = ("HSS" if hss else "notHSS", "E" if E else "notE", "agree" if so == wo else "DISAGREE")
        stat[key] = stat.get(key, 0) + 1
        if hss and so != wo:
            cex.append((files, ranks, wrap, rule, aware, E, " ".join(f"{'abcdefg'[f]}{r}" for f, r in sorted(W)), " ".join(f"{'abcdefg'[f]}{r}" for f, r in sorted(B)), so, wo))
            print("HSS-DISAGREE", cex[-1], flush=True)
        M.W_win.cache_clear(); M.S_win.cache_clear()
        if n % 200 == 0:
            print(n, f"{time.time()-t0:.0f}s", stat, flush=True)
    print("FINAL n=", n, stat)
    print("HSS disagreements with (E):", [c for c in cex if c[5]])
    print("HSS disagreements without (E):", len([c for c in cex if not c[5]]))
