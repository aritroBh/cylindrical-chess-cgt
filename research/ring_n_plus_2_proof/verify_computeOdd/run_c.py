"""run_c.py -- (c) the insertion isomorphism ins_c : R_n -> R_{n+2} (and Qo) at the note's fixed cut c = 6, plus Lemmas 2 and 3 on
the actual nodes, all with oddeng.py (this directory).

  python run_c.py FAM LO HI [CUT] [LEMMA_N_MAX]
For every odd n = LO..HI (default cut 6):
  * ins_c(start_n) = start_{n+2};  nodes of G_n map ONTO the nodes of G_{n+2} (bijectively);  for every node and side the
    K-children map onto the K-children and the T-children onto the T-children of the image;   (the L/P counts per side may differ);
  * the same for EVERY cut c = 0..n-2, listing the cuts at which the isomorphism holds (information: the note claims c = 6 only
    needs 6 <= c <= n-13);
  * Lemma 3 recomputed directly (not through the explored graph) on ins_c(p) for every node p and both sides (n <= LEMMA_N_MAX);
  * Lemma 2 (a),(b) on every wall pawn q of the mover with pattern windows, with the windows used in the note, and in general;
  * sensitivity control: cuts c = 7..11 at n = LO.
"""
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oddeng as O          # noqa: E402

WH, BL = O.WH, O.BL


def image(nd, c):
    assert nd[1] is None
    return (O.ins(nd[0], c), None)


def iso(G0, G1, c):
    """returns dict of counters; ok iff every violation count is 0."""
    r = dict(start=int(image(G0.start, c) != G1.start), nodes0=len(G0.order), nodes1=len(G1.order))
    imgs = [image(nd, c) for nd in G0.order]
    r['onto'] = int(set(imgs) != set(G1.order))
    r['injective'] = int(len(set(imgs)) != len(imgs))
    kbad = tbad = lpdiff = 0
    for nd, im in zip(G0.order, imgs):
        if im not in G1.info:
            kbad += 1
            continue
        for s in (WH, BL):
            T0, K0, nl0, np0 = G0.info[nd][s]
            T1, K1, nl1, np1 = G1.info[im][s]
            if {image(x, c) for x in K0} != set(K1):
                kbad += 1
            if {image(x, c) for x in T0} != set(T1):
                tbad += 1
            if (nl0 + np0) != (nl1 + np1):
                lpdiff += 1
    r['K'], r['T'], r['LPcount_differs'] = kbad, tbad, lpdiff
    r['ok'] = not (r['start'] or r['onto'] or r['injective'] or kbad or tbad)
    return r


def lemma3_direct(G, c):
    """for every node p and side: K- and T-children of ins_c(p) (classified afresh) are the images of those of p."""
    bad = pairs = 0
    for nd in G.order:
        for s in (WH, BL):
            T0, K0, _, _ = G.info[nd][s]
            K1, T1 = set(), set()
            for k, ch in O.classify(O.ins(nd[0], c), None, s):
                if k == 'K':
                    K1.add(ch)
                elif k == 'T':
                    T1.add(ch)
            pairs += 1
            if K1 != {image(x, c) for x in K0} or T1 != {image(x, c) for x in T0}:
                bad += 1
    return bad, pairs


def pattern_file(n, j):
    """the start content of wall file j (2 <= j <= n-7): W2 on even files, B4 on odd files."""
    return O.tok_to_file('W2') if j % 2 == 0 else O.tok_to_file('B4')


def lemma2(G, n, c, arc_hi):
    """Lemma 2(a),(b) for the mover Z (= side to move, no flag) and a pawn q of Z on file j, files j-1,j,j+1 pattern files and the window
    j-1..j+3 (or j-3..j+1) consisting of pattern files.  Two reports: 'note' = central files c-3..arc_hi-1 with the windows of the note,
    'general' = every wall file 3..n-8 whose window lies inside the wall files 2..n-7 and consists of exact pattern files in the node."""
    res = {}
    for label in ('note', 'general'):
        qpos = Counter()
        cls = Counter()
        failures_a = failures_b = 0
        for pos, flag in G.order:
            assert flag is None
            for Z in (WH, BL):
                if label == 'note':
                    js = range(c - 3, arc_hi)
                else:
                    js = range(3, n - 7)
                for j in js:
                    own = (pos[j] >> (8 * Z)) & 255
                    if not own:
                        continue
                    if label == 'note':
                        a, b = (j - 1, j + 3) if j + 3 <= arc_hi else (j - 3, j + 1)
                        wins = [(a, b)]
                    else:
                        wins = [w for w in ((j - 1, j + 3), (j - 3, j + 1)) if w[0] >= 2 and w[1] <= n - 7]
                    okw = [w for w in wins if all(pos[x] == pattern_file(n, x) for x in range(w[0], w[1] + 1))]
                    if not okw:
                        continue
                    assert pos[j] == pattern_file(n, j)
                    r = own.bit_length()
                    assert own == 1 << (r - 1)
                    qpos[j] += 1
                    for ch in O.gen(pos, None, Z, only=(j, r)):
                        if O.passed(ch[0], ch[1], Z):
                            failures_a += 1
                        k = O.kind_of(ch, Z)
                        cls[(j, k)] += 1
                        if k not in 'LP':
                            failures_b += 1
        res[label] = (sum(qpos.values()), sum(cls.values()), failures_a, failures_b, dict(sorted(cls.items())))
    return res


def main():
    fam = sys.argv[1]
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    c = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    lemma_nmax = int(sys.argv[5]) if len(sys.argv) > 5 else 23
    G = {}
    t0 = time.time()
    for n in range(lo, hi + 3, 2):
        G[n] = O.Graph(O.start(fam, n))
        st = G[n].stats()
        print(f'{fam}_{n}: graph built: nodes={st["nodes"]} K={st["K"]} T={st["T"]} flagged={st["flagged"]} zone={st["zone"]} ({time.time() - t0:.0f}s)', flush=True)
    # ---- isomorphism at the fixed cut
    print(f'--- {fam}: ins_{c} : G_n -> G_(n+2) at the fixed cut c={c}', flush=True)
    for n in range(lo, hi + 1, 2):
        r = iso(G[n], G[n + 2], c)
        print(f'  n={n}->{n + 2} cut {c}: start->start {not r["start"]}, nodes onto {not r["onto"]} (injective {not r["injective"]}; {r["nodes0"]} -> {r["nodes1"]}), '
              f'K-children violations {r["K"]}, T-children violations {r["T"]}  => {"ISOMORPHIC" if r["ok"] else "NOT ISOMORPHIC"}'
              f'   (side-moves with a different L+P count: {r["LPcount_differs"]})', flush=True)
    # ---- all cuts
    print(f'--- {fam}: all cuts c=0..n-2 at which ins_c : G_n -> G_(n+2) is an isomorphism (note: admissible 6 <= c <= n-13)', flush=True)
    for n in range(lo, hi + 1, 2):
        okc = [cc for cc in range(0, n - 1) if iso(G[n], G[n + 2], cc)['ok']]
        adm = list(range(6, n - 12))
        print(f'  n={n}: iso holds for c in {okc};  note\'s admissible cuts {adm}: all iso = {all(x in okc for x in adm)}', flush=True)
    # ---- Lemma 3 direct, Lemma 2
    print(f'--- {fam}: Lemma 3 recomputed on ins_{c}(p) for every node p and both sides', flush=True)
    for n in range(lo, min(hi, lemma_nmax) + 1, 2):
        bad, pairs = lemma3_direct(G[n], c)
        print(f'  n={n}: (node, side) pairs {pairs}, mismatches {bad}', flush=True)
    print(f'--- {fam}: Lemma 2 (a) no passed pawn for the mover after the move, (b) every move L or P', flush=True)
    for n in range(lo, min(hi, lemma_nmax) + 1, 2):
        arc_hi = c + 5 + (n - 19)          # arc c-4..c+5 at n0=19, c-4..c+7 at 21, ... (grows by two files per insertion)
        arc_hi = min(arc_hi, n - 8)
        r = lemma2(G[n], n, c, arc_hi)
        for label in ('note', 'general'):
            q, m, fa, fb, cl = r[label]
            print(f'  n={n} [{label}] q-positions {q}, moves {m}, (a) failures {fa}, (b) T/K moves {fb}; by (file, class) {cl}', flush=True)
    # ---- control
    print(f'--- {fam}: sensitivity control at n={lo}: Lemma 3 recomputed for cuts whose arc reaches the zone', flush=True)
    for cc in range(c + 1, c + 6):
        bad, pairs = lemma3_direct(G[lo], cc)
        print(f'  n={lo} cut c={cc} (arc {cc - 4}..{cc + 5}): Lemma 3 fails at {bad} of {pairs} (node, side) pairs', flush=True)
    print(f'{fam}: DONE ({time.time() - t0:.0f}s)', flush=True)


if __name__ == '__main__':
    main()
