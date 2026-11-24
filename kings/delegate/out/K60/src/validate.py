"""K60 validation on abstract exact toy groups (own code).
Checks, per exact group and per bad Black root move m (x = position after m, White to move):
  TA   : G has the results of omega on the battery  <=>  (C_B) holds on the battery for every m
  B=>A : (B1) at m  =>  Aux(x) is a White win
  A=>C : Aux(x) White win  =>  (C_B) on the battery at m
  C=>A : (C_B) on the battery at m  =>  Aux(x) White win      (needs T_N in the battery; T_{4n} is added per group)
  TN   : r(x (+) T_N, White first) = W  <=>  Aux(x) White win,  N = 4n (n boards)
Also: (C_W) (comparison with omega (+) t White to move) failures among groups with the results of omega;
the smallest N with x (+) T_N agreeing with Aux; k*down agreement for k = 1..4.
usage: validate.py SEED NRANDOM NTEMPO NRANDT"""
import random
import sys
from collections import Counter
from k60lib import ORD, sum_with, over_vals, exact_over, bad_black_moves, b1, aux_win
from k60games import (named_battery, rand_T, random_group, tempo_group, T_N, k_down,
                      example_nob1, example_cw, example_k58)


def check_group(G, tests, ovs, st, tag):
    qs = exact_over(G)
    if qs is None:
        return False
    st["exact"] += 1
    st["exact_" + tag] += 1
    bads = bad_black_moves(G)
    n = G.n
    TNbig = T_N(4 * n)
    ovN = over_vals(TNbig)
    assert ovN[(0, 0, 1)] == "W"
    cb = {bm: True for bm in bads}
    cw = {bm: True for bm in bads}
    ok = True
    for (name, T), ov in list(zip(tests, ovs)) + [(("T_4n", TNbig), ovN)]:
        sv = sum_with(G, T)
        for t in range(len(T[0])):
            for s in (0, 1):
                for r in (0, 1):
                    st["results"] += 1
                    if sv[(r, 0, t, s)] != ov[(0, t, s)]:
                        ok = False
                for (q, d) in qs:
                    for f in (sorted({d, 0}) if s == 1 else [0]):
                        st["results"] += 1
                        if sv[(q, f, t, s)] != ov[(1, t, s)]:
                            st["VIOL_q_not_0D"] += 1
                            print("VIOL q", tag, name, G.mv, G.ep, G.chk)
            for (_, y, d) in bads:
                if ORD[sv[(y, d, t, 0)]] < ORD[ov[(0, t, 1)]]:
                    cb[(_, y, d)] = False
                if ORD[sv[(y, d, t, 0)]] < ORD[ov[(0, t, 0)]]:
                    cw[(_, y, d)] = False
    aw = aux_win(G, [(y, d) for (_, y, d) in bads])
    hb1 = b1(G)
    st["ok" if ok else "differs"] += 1
    if ok != all(cb.values()):
        st["VIOL_TA"] += 1
        print("VIOL TA", tag, G.mv, G.ep, G.chk)
    if hb1:
        st["b1"] += 1
        if not ok:
            st["VIOL_L415"] += 1
            print("VIOL L4.15", tag, G.mv, G.ep, G.chk)
    elif ok:
        st["nob1_but_omega"] += 1
    if ok and not all(cw.values()):
        st["omega_but_CW_fails"] += 1
    if any(G.chk[g][s] for g in range(n) for s in (0, 1)):
        st["groups_with_check"] += 1
    if any(d for g in range(n) for s in (0, 1) for (_, d) in G.mv[g][s]):
        st["groups_with_doublestep"] += 1
    if any(G.ep[g][s] for g in range(n) for s in (0, 1)):
        st["groups_with_ep_moves"] += 1
    sB1 = sum_with(G, ([[], []], [[1], []]))
    for bm in bads:
        (_, y, d) = bm
        st["badmoves"] += 1
        a = aw[(y, d)]
        st["aux_win" if a else "aux_loss"] += 1
        b = sB1[(y, d, 0, 0)] == "W"
        if b and not a:
            st["VIOL_B1_implies_aux"] += 1
            print("VIOL B1=>Aux", tag, bm, G.mv, G.ep, G.chk)
        if not b and a:
            st["aux_win_without_B1"] += 1
        if a and not cb[bm]:
            st["VIOL_aux_implies_CB"] += 1
            print("VIOL Aux=>CB", tag, bm, G.mv, G.ep, G.chk)
        if cb[bm] and not a:
            st["VIOL_CB_implies_aux"] += 1
            print("VIOL CB=>Aux", tag, bm, G.mv, G.ep, G.chk)
        tn = sum_with(G, TNbig)[(y, d, 0, 0)] == "W"
        if tn != a:
            st["VIOL_TN_vs_aux"] += 1
            print("VIOL TN", tag, bm, G.mv, G.ep, G.chk)
        first = None
        for N in range(0, 4 * n + 1):
            if (sum_with(G, T_N(N))[(y, d, 0, 0)] == "W") == a:
                if first is None:
                    first = N
            else:
                first = None
        st["TN_first_agree_N=%s" % first] += 1
        for k in range(1, 5):
            kd = sum_with(G, k_down(k))[(y, d, 0, 0)] == "W"
            st["kdown%d_%s" % (k, "agree" if kd == a else "differ")] += 1
    return True


def main():
    seed, nrand, ntempo, nT = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    tests = named_battery() + [("r%d" % i, rand_T(rng)) for i in range(nT)]
    ovs = [over_vals(T) for _, T in tests]
    st = Counter()
    for nm, G in (("nob1", example_nob1()), ("cw", example_cw()), ("k58", example_k58())):
        before = dict(st)
        check_group(G, tests, ovs, st, "hand")
        print("hand example", nm, {k: st[k] - before.get(k, 0) for k in st if st[k] != before.get(k, 0)})
    seen = set()
    for tag, gen, want in (("random", random_group, nrand), ("tempo", tempo_group, ntempo)):
        got = tries = 0
        while got < want and tries < 5000 * want:
            tries += 1
            G = gen(rng)
            if G is None or G.key() in seen:
                continue
            seen.add(G.key())
            if check_group(G, tests, ovs, st, tag):
                got += 1
    print("tests", len(tests) + 1, "per group (battery + T_4n)")
    for k in sorted(st):
        print("%-34s %d" % (k, st[k]))


if __name__ == "__main__":
    main()
