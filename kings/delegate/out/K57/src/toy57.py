"""K57: test Lemma 2 (criterion B1) on the K56 referee's abstract toy groups (src/toy_k56ref.py, copied unchanged).
For every random exact over group (Definition 4.8 on the toy): B1 = every non-shuttle Black root move y leaves a position
that White wins beside -1 with White to move (sum rules, no move loses).  Then r(G (+) T) against over for random T.
Prediction of Lemma 2: groups with B1 never differ.  usage: python3 toy57.py SEED NGROUPS NTESTS"""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import toy_k56ref as K
MINUS1 = ([[], []], [[1], []])  # Black has one move elsewhere
def b1(G):
    L, R = G
    sv = K.sum_values(G, MINUS1)
    for r, other in ((0, 1), (1, 0)):
        for y in R[r]:
            if y == other or y == K.WT: continue
            if y == K.BT: return False
            if sv[(y, 0, 0)] != 'W': return False
    return True
def main():
    seed, ngroups, ntests = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    tests = [K.rand_game(rng, rng.randint(1, 4), rng.choice([0.2, 0.35, 0.5]), rng.choice([0.0, 0.15, 0.3])) for _ in range(ntests)]
    over_vals = [K.sum_values(K.OVER, T) for T in tests]
    st = dict(exact=0, b1=0, b1_diff_groups=0, nb1=0, nb1_diff_groups=0, results_b1=0, tempo=0, tempo_not_b1=0)
    seen = set(); tried = 0
    while st['exact'] < ngroups and tried < 400 * ngroups:
        tried += 1
        G = K.rand_group_repaired(rng) if rng.random() < 0.9 else K.rand_group(rng)
        if G is None or repr(G) in seen: continue
        seen.add(repr(G))
        qs = K.exact_over(G)
        if qs is None: continue
        st['exact'] += 1
        ok = b1(G); te = K.tempo_exact(G, qs)
        st['tempo'] += te; st['tempo_not_b1'] += te and not ok
        diff = 0; nres = 0
        for T, ov in zip(tests, over_vals):
            sv = K.sum_values(G, T)
            for t in range(len(T[0])):
                for s in (0, 1):
                    for g in (0, 1):
                        nres += 1; diff += sv[(g, t, s)] != ov[(0, t, s)]
                    for q in qs:
                        nres += 1; diff += sv[(q, t, s)] != ov[(1, t, s)]
        if ok:
            st['b1'] += 1; st['results_b1'] += nres; st['b1_diff_groups'] += diff > 0
            if diff: print('COUNTEREXAMPLE to Lemma 2:', G, qs)
        else:
            st['nb1'] += 1; st['nb1_diff_groups'] += diff > 0
    print(st)
if __name__ == '__main__':
    main()
