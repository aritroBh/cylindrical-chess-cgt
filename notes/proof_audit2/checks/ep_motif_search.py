"""Targeted search for a counterexample to paper Conjecture 4 / Theorem 10 when (E) is dropped:
HSS positions, BIG larger than every move count, with an e.p. motif (a pawn on its start rank facing an enemy pawn on the
double-step landing rank, next to another component).  Reports positions with HSS and o(S) != o(W).
Usage: python3 ep_motif_search.py SECONDS SEED
"""
import random, sys, time
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
import hss_search as H

def gen(rng, files, ranks):
    # e.p. motif with a blocker so that the position after the double step is NOT terminal:
    #  W double-steps (f,2)->(f,4) next to B (f+1,4); a second white pawn on (f+2,3) keeps B (f+1,4) from being passed.
    #  (mirror images, and the colour-reversed motif)
    f = rng.randrange(0, files - 2)
    t = rng.randrange(4)
    if t == 0:   Wm = {(f, 2), (f + 2, 3)}; Bm = {(f + 1, 4)}
    elif t == 1: Wm = {(f + 2, 2), (f, 3)}; Bm = {(f + 1, 4)}
    elif t == 2: Bm = {(f, ranks - 1), (f + 2, ranks - 2)}; Wm = {(f + 1, ranks - 3)}
    else:        Bm = {(f + 2, ranks - 1), (f, ranks - 2)}; Wm = {(f + 1, ranks - 3)}
    if rng.random() < .5:   # optionally an extra random pawn inside the motif files
        g = rng.choice([f, f + 1, f + 2]); r = rng.randint(2, ranks - 1)
        if (g, r) not in Wm | Bm: (Wm if rng.random() < .5 else Bm).add((g, r))
    used = {g for g, _ in Wm | Bm}
    forb = set(used) | {g + d for g in used for d in (-1, 1)}
    # optionally a second motif pawn pair member
    W, B = set(Wm), set(Bm)
    free_files = [g for g in range(files) if g not in forb]
    rng.shuffle(free_files)
    # other components: facing pairs on one file (W below B), which can never create a passed pawn: pure tempo
    # (so that the position has a chance to be HSS); non-adjacent files only
    taken = set()
    for g in free_files:
        if g in taken or len(taken) >= 6: continue
        if rng.random() < .55:
            lo = rng.randint(2, ranks - 2); hi = rng.randint(lo + 1, ranks - 1)
            W.add((g, lo)); B.add((g, hi))
            taken |= {g - 1, g, g + 1}
    # sometimes add one more pawn on a motif-adjacent file to enrich
    return frozenset(W), frozenset(B)

if __name__ == "__main__":
    secs, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed); t0 = time.time(); n = 0; stat = {}
    while time.time() - t0 < secs:
        files = rng.choice([6, 7, 8]); ranks = rng.choice([6, 7]); rule = rng.choice(["count", "mover", "opponent"])
        aware = rng.random() < 0.75
        M.configure(files, ranks, False, True, rule, aware, big=60); H.tau.cache_clear()
        W, B = gen(rng, files, ranks)
        if M.passed(W, B, None, 'W') or M.passed(W, B, None, 'B'): continue
        try:
            hss, E = H.analyse(W, B); so, wo = M.S_outcome(W, B), M.W_outcome(W, B)
        except ValueError:
            continue
        n += 1
        key = ("HSS" if hss else "notHSS", "E" if E else "notE", "agree" if so == wo else "DISAGREE")
        stat[key] = stat.get(key, 0) + 1
        if hss and so != wo:
            print("HSS-DISAGREE", files, ranks, rule, aware, "E" if E else "notE",
                  " ".join(f"{'abcdefgh'[f]}{r}" for f, r in sorted(W)), "/", " ".join(f"{'abcdefgh'[f]}{r}" for f, r in sorted(B)),
                  "S", so, "W", wo, flush=True)
        M.W_win.cache_clear(); M.S_win.cache_clear()
        if n % 500 == 0: print(n, f"{time.time()-t0:.0f}s", stat, flush=True)
    print("FINAL", n, stat)
