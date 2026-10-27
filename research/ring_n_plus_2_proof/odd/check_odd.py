"""check_odd.py -- PROOF_odd.md: the hypotheses of T50's Lemmas 2 and 3 for the odd families R_n, Qo_n at the fixed cut
c = 6 and the base n0 = 19, checked on the ACTUAL reduced nodes with the independent Python engine
verify_compute/myeng.py (program E; the rg/cylcgt programs A, B are run by pump_verify.py / reduced_cyl.py).

  R_n  = W5 B7 (W2 B4)^((n-9)/2) W2 W3B6 W3 W2B5 B5 W2 B4      (n odd >= 11)   claimed *2
  Qo_n = W4 B7 (W2 B4)^((n-9)/2) W2 W3B6 W3 W2B5 B5 W2 B4                      claimed *3
  files: 0, 1, wall 2..n-7 (W2 on even files, B4 on odd files, W2 at BOTH ends), core n-6..n-3, then W2 (n-2), B4 (n-1).

What is checked (n = n0 and n = n0 + 2, so both the base graph and its image under ins_c are covered):
  1. reduced graph: nodes, K/T edges, no e.p. flag, zone (files on which some node differs from the start), signature h=0..4;
  2. every node: no passed pawn (either colour), no e.p. flag, and files c-4..c+5 (n0) / c-4..c+7 (n0+2) hold EXACTLY the
     pattern pawn (W2 on even files, B4 on odd files) -- the hypothesis of Lemma 3 (and the arc inside which Lemma 2's
     windows lie);
  3. Lemma 2 on every central wall pawn (files c-3..c+4 at n0, c-3..c+6 at n0+2), for both colours, with the window
     the proof uses (j-1..j+3, or j-3..j+1 when that one leaves the arc): after every move (a) the mover has no passed
     pawn, (b) the move is L or P (never T or K).  The two ends of the arc (j = c-3: window c-4..c, which contains
     the first wall file 2 beside B7; j = c+4 resp. c+6: window c+1..c+5 resp. c+3..c+7) are reported separately;
  4. Lemma 3 on the nodes: for every node p and side, the K-children of ins_c(p) are the ins_c-images of those of p and
     so are the T-children; ins_c(start_n) = start_{n+2}; and R_{n+2} = ins_c(R_n) (nodes, K-edges, T-sets);
  5. sensitivity control: for the cuts c+1..c+5 (arc reaching into the zone) Lemma 3's conclusion fails at some nodes, so
     the test in 4. can fail.
Usage (project root):  PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_2_proof/odd/check_odd.py R|Qo [n0 c]
"""
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..'))
import myeng as M          # noqa: E402
import fam                 # noqa: E402  (only to compare token lists)

W, B = M.W, M.B


def tokens(famname, n):
    assert n % 2 == 1 and n >= 9
    head = {'R': 'W5', 'Qo': 'W4'}[famname]
    return [head, 'B7'] + ['W2', 'B4'] * ((n - 9) // 2) + ['W2', 'W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']


def start_pos(famname, n):
    t = tokens(famname, n)
    assert t == (fam.R(n) if famname == 'R' else fam.Qo(n))
    return tuple(M.parse_file(x) for x in t)


def kind(child, side):
    """T / L / P / K of the move of `side` to child = (pos, ep)."""
    v = M.verdict(child[0], child[1], side)
    if v == side:
        return 'T'
    if v == 1 - side:
        return 'L'
    for rp, re_ in M.gen_moves(child[0], child[1], 1 - side):
        if M.verdict(rp, re_, 1 - side) == 1 - side:
            return 'P'
    return 'K'


def graph_checks(G, famname, n, c, arc_hi, pattern):
    st = G.stats()
    exp_zone = ([0, 1] if famname == 'Qo' else []) + list(range(n - 7, n - 2)) + [n - 1]
    assert st['flagged'] == 0 and st['zone'] == exp_zone, st
    sig = G.signature(range(5))
    assert sig == ('NNPNN' if famname == 'R' else 'NNNPN'), sig
    p0 = G.start[0]
    assert p0[2] == pattern[2] and p0[n - 7] == pattern[n - 7] and pattern[2] == pattern[n - 7] == M.parse_file('W2')
    for pos, ep in G.order:
        assert ep is None
        assert not M.passed_pawns(pos, ep, W) and not M.passed_pawns(pos, ep, B)
        assert all(pos[j] == pattern[j] for j in range(c - 4, arc_hi + 1))
        assert all(pos[j] == p0[j] for j in range(n) if j not in exp_zone)
    print(f'{famname}_{n}: nodes={st["nodes"]} K={st["K"]} T={st["T"]} flagged=0 zone={st["zone"]} sig(h=0..4)={sig};'
          f' no passed pawn, no flag; files {c-4}..{arc_hi} are exact pattern files in every node; the start has W2 on'
          f' file 2 and on file n-7={n-7} (W2 at both wall ends)', flush=True)
    return st


def lemma2(G, n, c, arc_hi, pattern):
    lo = c - 4
    windows = {}
    for j in range(c - 3, arc_hi):
        windows[j] = (j - 1, j + 3) if j + 3 <= arc_hi else (j - 3, j + 1)
        assert windows[j][0] >= lo and windows[j][1] <= arc_hi
    cls = Counter()
    npos = Counter()
    for pos, ep in G.order:
        for side in (W, B):
            for j in windows:
                if not pos[j][side]:
                    continue
                assert pos[j] == pattern[j]
                ranks = list(M.bits(pos[j][side]))
                assert len(ranks) == 1
                npos[j] += 1
                for child in M.gen_moves(pos, ep, side, only=(j, ranks[0])):
                    assert not M.passed_pawns(child[0], child[1], side), ('Lemma 2(a)', j, side)
                    k = kind(child, side)
                    assert k in 'LP', ('Lemma 2(b)', j, side, k)
                    cls[(j, k)] += 1
    print(f'  Lemma 2 at n={n}: central files {c-3}..{arc_hi-1}; windows {windows}')
    print(f'    q-positions={sum(npos.values())} moves={sum(cls.values())}; (a) failures 0; (b) T/K moves 0;'
          f' by (file, class) {dict(sorted(cls.items()))}')
    ends = {j: windows[j] for j in (c - 3, arc_hi - 1)}
    print(f'    arc ends: j={c-3} window {windows[c-3]} (left wall end: file 2 is W2, file 1 is B7);'
          f' j={arc_hi-1} window {windows[arc_hi-1]}')
    # information only: the moves of the wall-end pawns (not covered by Lemma 2: file 1 resp. n-6 is no pattern file)
    info = Counter()
    for pos, ep in G.order:
        for j in (2, n - 7):
            if pos[j][W] and pos[j] == pattern[j]:
                for child in M.gen_moves(pos, ep, W, only=(j, 2)):
                    info[(j, kind(child, W))] += 1
    print(f'    (info) moves of the wall-end W2 pawns, file 2 and file n-7={n-7}, by (file, class): {dict(sorted(info.items()))}',
          flush=True)


def ins_image(item, c):
    pos, ep = item
    assert ep is None
    return (M.ins(pos, c), None)


def lemma3_and_pump(G, G2, c):
    n = len(G.start[0])
    assert M.ins(G.start[0], c) == G2.start[0], 'ins(start_n) != start_{n+2}'
    nodes = set(G.order)
    nodes2 = set(G2.order)
    img = {nd: ins_image(nd, c) for nd in G.order}
    assert set(img.values()) == nodes2 and len(set(img.values())) == len(nodes), 'node sets differ'
    cmp_ = 0
    for nd in G.order:
        for side in (W, B):
            T, K, _, _ = G.info[nd][side]
            T2, K2, _, _ = G2.info[img[nd]][side]
            assert T2 == frozenset(ins_image(x, c) for x in T), ('T-children', nd, side)
            assert K2 == frozenset(ins_image(x, c) for x in K), ('K-children', nd, side)
            # Lemma 3 itself, on ins_c(p) computed independently of G2's exploration
            cl = M.classify(img[nd][0], None, side)
            assert frozenset((p, e) for k, p, e in cl if k == 'K') == K2
            assert frozenset((p, e) for k, p, e in cl if k == 'T') == T2
            cmp_ += 1
    print(f'  ins_{c}(start_{n}) = start_{n+2}; graph_{n+2} = ins_{c}(graph_{n}): {len(nodes)} nodes onto {len(nodes2)} nodes, K- and T-children'
          f' equal for all {cmp_} (node, side) pairs; Lemma 3 recomputed on every ins_{c}(p): 0 mismatches', flush=True)


def control(G, c):
    """sensitivity control: number of (node, side) pairs at which Lemma 3's conclusion fails for the cut c (no asserts)."""
    bad = pairs = 0
    for nd in G.order:
        for side in (W, B):
            T, K, _, _ = G.info[nd][side]
            cl = M.classify(M.ins(nd[0], c), None, side)
            Kh = frozenset((p, e) for k, p, e in cl if k == 'K')
            Th = frozenset((p, e) for k, p, e in cl if k == 'T')
            pairs += 1
            if Kh != frozenset(ins_image(x, c) for x in K) or Th != frozenset(ins_image(x, c) for x in T):
                bad += 1
    return bad, pairs


def main():
    famname = sys.argv[1]
    n0 = int(sys.argv[2]) if len(sys.argv) > 2 else 19
    c = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    t0 = time.time()
    chain = []
    for step in range(3):                      # n0, n0+2, n0+4: two insertion steps
        n = n0 + 2 * step
        chain.append((n, M.Graph(start_pos(famname, n))))
    for step, (n, G) in enumerate(chain):
        pattern = {j: M.parse_file('W2' if j % 2 == 0 else 'B4') for j in range(2, n - 6)}
        arc_hi = c + 5 + 2 * step if step < 2 else None
        if step < 2:
            graph_checks(G, famname, n, c, arc_hi, pattern)
            lemma2(G, n, c, arc_hi, pattern)
        else:
            graph_checks(G, famname, n, c, c + 5 + 2 * step, pattern)
    for step in range(2):
        lemma3_and_pump(chain[step][1], chain[step + 1][1], c)
    for cc in range(c + 1, c + 6):             # arcs cc-4..cc+5 that reach into the zone (file 12 and beyond at n0 = 19)
        bad, pairs = control(chain[0][1], cc)
        print(f'  control, cut c={cc} (arc {cc-4}..{cc+5}, reaches the zone {cc+5 >= n0 - 7}): Lemma 3 conclusion fails at {bad} of {pairs} (node, side) pairs', flush=True)
    print(f'{famname}: ALL CHECKS PASSED ({time.time() - t0:.0f}s)')


if __name__ == '__main__':
    main()
