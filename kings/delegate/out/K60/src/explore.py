"""K60 exploration: for exact toy groups, compare 'results of omega on the battery' with (C_B) per bad Black move and
with candidate finite tests.  usage: explore.py SEED NGROUPS NRAND [random|tempo]"""
import random
import sys
from collections import Counter
from k60lib import (aux_win, ORD, sum_with, over_vals, exact_over, bad_black_moves, b1, MINUS1, dsum, OVER, UNDER)
from k60games import named_battery, rand_T, NAMED, STAR, DOWN, random_group, tempo_group

CAND = {
    "B1": (MINUS1, "W"), "star": (STAR, "W"), "down": (DOWN, "W"),
    "underS": (UNDER, "D"), "underW": (UNDER, "W"),
    "under+over": (dsum(UNDER, OVER), "W"), "under+up": (dsum(UNDER, NAMED["up"]), "W"),
    "down+*": (dsum(DOWN, STAR), "W"), "miny1": (NAMED["miny1"], "W"),
}


def main():
    seed, ngroups, nrand = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    mode = sys.argv[4] if len(sys.argv) > 4 else "random"
    rng = random.Random(seed)
    tests = named_battery() + [("r%d" % i, rand_T(rng)) for i in range(nrand)]
    ovs = [over_vals(T) for _, T in tests]
    stats = Counter()
    conf = {c: Counter() for c in list(CAND) + ['AUX']}
    seen = set()
    tries = 0
    while stats["exact"] < ngroups and tries < 2000 * ngroups:
        tries += 1
        G = random_group(rng) if mode == "random" else tempo_group(rng)
        if G is None or G.key() in seen:
            continue
        seen.add(G.key())
        qs = exact_over(G)
        if qs is None:
            continue
        stats["exact"] += 1
        bads = bad_black_moves(G)
        cb = {bm: True for bm in bads}
        results_ok = True
        nres = 0
        for (name, T), ov in zip(tests, ovs):
            sv = sum_with(G, T)
            k = len(T[0])
            for t in range(k):
                for s in (0, 1):
                    for r in (0, 1):
                        nres += 1
                        if sv[(r, 0, t, s)] != ov[(0, t, s)]:
                            results_ok = False
                    for (q, d) in qs:
                        for f in sorted({d, 0}) if s == 1 else [0]:
                            nres += 1
                            if sv[(q, f, t, s)] != ov[(1, t, s)]:
                                stats["Q_VIOLATION"] += 1
                                print("q differs from 0_D!", name, q, f, t, s)
                    if s == 1:
                        continue
                for bm in bads:
                    (_, y, d) = bm
                    for t in range(k):
                        if ORD[sv[(y, d, t, 0)]] < ORD[ov[(0, t, 1)]]:
                            cb[bm] = False
        stats["results"] += nres
        cball = all(cb.values())
        stats["ok" if results_ok else "differs"] += 1
        if cball != results_ok:
            stats["THEOREM_A_VIOLATION"] += 1
            print("Theorem A violation", G.mv, G.ep, G.chk)
        hb1 = b1(G)
        stats["b1"] += hb1
        if hb1 and not results_ok:
            stats["LEMMA415_VIOLATION"] += 1
        if (not hb1) and results_ok:
            stats["nob1_ok"] += 1
        if any(G.chk[g][s] for g in range(G.n) for s in (0, 1)):
            stats["with_check"] += 1
        if any(d for g in range(G.n) for s in (0, 1) for (_, d) in G.mv[g][s]):
            stats["with_ep"] += 1
        aw = aux_win(G, [(y, d) for (_, y, d) in bads])
        for bm in bads:
            (_, y, d) = bm
            conf["AUX"][(cb[bm], aw[(y, d)])] += 1
            if cb[bm] != aw[(y, d)]:
                print("AUX MISMATCH", cb[bm], aw[(y, d)], bm, G.mv, G.ep, G.chk)
            for c, (T, need) in CAND.items():
                v = sum_with(G, T)[(y, d, 0, 0)]
                conf[c][(cb[bm], ORD[v] >= ORD[need])] += 1
    print("tries", tries, dict(stats))
    for c in list(CAND) + ['AUX']:
        cc = conf[c]
        print("%-12s CB&test %6d  CB&!test %6d  !CB&test %6d  !CB&!test %6d" %
              (c, cc[(True, True)], cc[(True, False)], cc[(False, True)], cc[(False, False)]))


if __name__ == "__main__":
    main()
