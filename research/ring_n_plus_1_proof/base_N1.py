"""base_N1.py -- direct (unreduced, no poison pruning) search of N1_n + *h, h = 0..4, for both parities,
with the independent engine myeng.Full (program E), under both e.p.-across-heap-move readings.

N1_n is claimed *2, so the expected signature is NNPNN (h=0..4) for every n >= 9 (odd) / n >= 10 (even).

Usage (project root):  PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_1_proof/base_N1.py [NHI]
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof', 'verify_compute'))
import myeng as M          # noqa: E402


def tokens(parity, n):
    k = ((n - 7) // 2) if parity == 'odd' else ((n - 8) // 2)
    wall = ['B4', 'W2'] * k
    core = ['B6', 'W2', 'W3', 'B6', 'B7', 'W3', 'W6B7']
    if parity == 'odd':
        t = wall + core
    else:
        t = wall + core + ['W2']
    assert M.npawns(tuple(M.parse_file(x) for x in t)) == n + 1
    return t


def main():
    nhi = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    want = 'NNPNN'
    for parity in ('odd', 'even'):
        start_n = 9 if parity == 'odd' else 10
        for n in range(start_n, nhi + 1, 2):
            toks = tokens(parity, n)
            pos = tuple(M.parse_file(t) for t in toks)
            assert M.npawns(pos) == n + 1
            out = []
            for mode in ('keep', 'expire'):
                t0 = time.time()
                f = M.Full(mode)
                sig = f.signature(pos, range(5))
                out.append((mode, sig, f.nodes, time.time() - t0))
            ok = all(s == want for _, s, _, _ in out)
            print(f'N1_{parity}_{n} pawns={n + 1} ' + ' '.join(f'{m}={s} ({k} states, {t:.1f}s)' for m, s, k, t in out)
                  + ('  == *2' if ok else '  (NOT *2)'), flush=True)


if __name__ == '__main__':
    main()
