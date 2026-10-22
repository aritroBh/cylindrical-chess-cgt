"""Deeper variant of hss_search.py: 7-8 ranks, 3-5 pawns a side, positions biased toward start ranks (long games, many
double steps).  Same test: HSS (+ (E) status) versus o(S) = o(W).  Usage: python3 hss_search_deep.py SECONDS SEED"""
import random, sys, time
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M
import hss_search as H

def rand_pos(rng, files, ranks):
    nw, nb = rng.randint(2, 4), rng.randint(2, 4)
    W, B = set(), set()
    fl = list(range(files))
    for _ in range(nw):
        W.add((rng.choice(fl), rng.choice([2, 2, 3, 4])))
    for _ in range(nb):
        B.add((rng.choice(fl), rng.choice([ranks - 1, ranks - 1, ranks - 2, ranks - 3])))
    if W & B or len(W) < nw - 1 or len(B) < nb - 1: return None
    return frozenset(W), frozenset(B - W)

if __name__ == "__main__":
    secs, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed); t0 = time.time(); n = 0; stat = {}
    while time.time() - t0 < secs:
        files = rng.choice([4, 5, 6, 7]); ranks = rng.choice([7, 8]); wrap = rng.random() < .4
        rule = rng.choice(["count", "mover", "opponent"]); aware = rng.random() < .75
        M.configure(files, ranks, wrap, True, rule, aware, big=70); H.tau.cache_clear()
        p = rand_pos(rng, files, ranks)
        if p is None: continue
        W, B = p
        if M.passed(W, B, None, 'W') or M.passed(W, B, None, 'B'): continue
        try:
            hss, E = H.analyse(W, B); so, wo = M.S_outcome(W, B), M.W_outcome(W, B)
        except ValueError:
            continue
        n += 1
        key = ("HSS" if hss else "notHSS", "E" if E else "notE", "agree" if so == wo else "DISAGREE")
        stat[key] = stat.get(key, 0) + 1
        if hss and so != wo:
            print("HSS-DISAGREE", files, ranks, wrap, rule, aware, "E" if E else "notE", sorted(W), sorted(B), so, wo, flush=True)
        M.W_win.cache_clear(); M.S_win.cache_clear()
        if n % 100 == 0: print(n, f"{time.time()-t0:.0f}s", stat, flush=True)
    print("FINAL", n, stat)
