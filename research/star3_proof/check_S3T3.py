"""check_S3T3.py -- hypotheses of T50's Lemmas 2 and 3 for the *3 families T3_n (even n>=12) and S3_n (odd n>=13)
(whole-board game on C_n).  n+1 pawns.

  T3_n = (B4 W2)^((n-10)/2) B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2     even n >= 12, n+1 pawns   claimed *3
  S3_n = B4 B6 W3 (W2 B4)^((n-11)/2) W6B7 W3 B7 B6 W3 W2 B6 W2   odd  n >= 13, n+1 pawns   claimed *3

  files 0-based, file 0 first.
  Zone (pump): T3 {n-10, n-9} U {n-7..n-2}; S3 {0,1,2} U {n-10,n-9} U {n-7..n-1}.

Usage (project root):
  PYTHONPATH=. nice -n 15 .venv/bin/python research/star3_proof/check_S3T3.py T3 [n0 c]   (defaults n0=20, c=4)
  PYTHONPATH=. nice -n 15 .venv/bin/python research/star3_proof/check_S3T3.py S3 [n0 c]   (defaults n0=25, c=7)
"""
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof'))
import myeng as M          # noqa: E402
import fam                 # noqa: E402

W, B = M.W, M.B


def family(arg):
    a = arg.upper().strip('_-')
    if a in ('T3', 'T'):
        return 'T3'
    if a in ('S3', 'S'):
        return 'S3'
    raise SystemExit('first argument must be T3 or S3')


def tokens(famname, n):
    if famname == 'T3':
        assert n % 2 == 0 and n >= 12
        t = fam.T3(n)
    else:
        assert n % 2 == 1 and n >= 13
        t = fam.S3(n)
    assert t == (fam.T3(n) if famname == 'T3' else fam.S3(n)), 'token mismatch with fam'
    assert M.npawns(tuple(M.parse_file(x) for x in t)) == n + 1, (famname, n, M.npawns(tuple(M.parse_file(x) for x in t)))
    return list(t)


def start_pos(famname, n):
    return tuple(M.parse_file(x) for x in tokens(famname, n))


def kind(child, side):
    v = M.verdict(child[0], child[1], side)
    if v == side:
        return 'T'
    if v == 1 - side:
        return 'L'
    for rp, re_ in M.gen_moves(child[0], child[1], 1 - side):
        if M.verdict(rp, re_, 1 - side) == 1 - side:
            return 'P'
    return 'K'


def expected_zone(famname, n):
    if famname == 'T3':
        return [n - 10, n - 9] + list(range(n - 7, n - 1))   # {n-10,n-9} U {n-7..n-2}
    return [0, 1, 2, n - 10, n - 9] + list(range(n - 7, n))  # {0,1,2} U {n-10,n-9} U {n-7..n-1}


def graph_checks(G, famname, n, c, arc_hi):
    st = G.stats()
    exp_zone = expected_zone(famname, n)
    assert st['flagged'] == 0, st
    assert st['zone'] == exp_zone, (st['zone'], exp_zone)
    sig = G.signature(range(6))
    assert sig == 'NNNPNN', (n, sig)
    p0 = G.start[0]
    for pos, ep in G.order:
        assert ep is None
        assert not M.passed_pawns(pos, ep, W) and not M.passed_pawns(pos, ep, B)
        assert all(pos[j] == p0[j] for j in range(c - 4, arc_hi + 1))
        assert all(pos[j] == p0[j] for j in range(n) if j not in exp_zone)
    print(f'{famname}_{n}: nodes={st["nodes"]} K={st["K"]} T={st["T"]} flagged=0 zone={st["zone"]} sig(h=0..5)={sig};'
          f' no passed pawn, no flag; files {c-4}..{arc_hi} are exact pattern files in every node', flush=True)
    return st, p0


def lemma2(G, famname, n, c, arc_hi, pattern):
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
    print(f'    arc ends: j={c-3} window {windows[c-3]} (left end); j={arc_hi-1} window {windows[arc_hi-1]} (right end)',
          flush=True)
    if famname == 'T3':
        lastwall = n - 11
    else:
        lastwall = n - 9
    info = Counter()
    for pos, ep in G.order:
        if 0 <= lastwall < n and pos[lastwall][W]:
            ranks = list(M.bits(pos[lastwall][W]))
            if len(ranks) == 1:
                for child in M.gen_moves(pos, ep, W, only=(lastwall, ranks[0])):
                    info[(lastwall, kind(child, W))] += 1
    if info:
        print(f'    (info) moves of the wall-end pawn, file {lastwall}, by (file, class): {dict(sorted(info.items()))}',
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
            cl = M.classify(img[nd][0], None, side)
            assert frozenset((p, e) for k, p, e in cl if k == 'K') == K2
            assert frozenset((p, e) for k, p, e in cl if k == 'T') == T2
            cmp_ += 1
    print(f'  ins_{c}(start_{n}) = start_{n+2}; graph_{n+2} = ins_{c}(graph_{n}): {len(nodes)} nodes onto {len(nodes2)} nodes,'
          f' K- and T-children equal for all {cmp_} (node, side) pairs; Lemma 3 recomputed on every ins_{c}(p): 0 mismatches',
          flush=True)


def control(G, c):
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
    famname = family(sys.argv[1])
    if famname == 'T3':
        n0 = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        c = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    else:
        n0 = int(sys.argv[2]) if len(sys.argv) > 2 else 25
        c = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    t0 = time.time()
    chain = []
    for step in range(3):
        n = n0 + 2 * step
        chain.append((n, M.Graph(start_pos(famname, n))))
    for step, (n, G) in enumerate(chain):
        arc_hi = c + 5 + 2 * step
        if step < 2:
            st, pattern = graph_checks(G, famname, n, c, arc_hi)
            lemma2(G, famname, n, c, arc_hi, pattern)
        else:
            st, pattern = graph_checks(G, famname, n, c, arc_hi)
    for step in range(2):
        lemma3_and_pump(chain[step][1], chain[step + 1][1], c)
    for cc in range(c + 1, c + 6):
        bad, pairs = control(chain[0][1], cc)
        print(f'  control, cut c={cc} (arc {cc-4}..{cc+5}): Lemma 3 conclusion fails at {bad} of {pairs} (node, side) pairs',
              flush=True)
    print(f'{famname}: ALL CHECKS PASSED ({time.time() - t0:.0f}s)')


if __name__ == '__main__':
    main()