"""base_cases.py -- direct (unreduced, no poison pruning) search of G + *h, h = 0..4, for R_n and Qo_n, odd n = 9..NHI, with the
independent engine myeng.Full (program E), under both e.p.-across-heap-move readings ('keep' = cylcgt sum semantics, 'expire' =
textbook chess).  R_n = *2 iff the signature is NNPNN; Qo_n = *3 iff it is NNNPN (h = 0..4).  n = 9 is the known failure (LLLL..).
The rg program (program A) did the same for n = 9..59 in logs/unreduced_R_9_59.txt and unreduced_Qo_9_59.txt.
Usage (project root):  PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_2_proof/odd/base_cases.py [NHI]
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'verify_compute'))
import myeng as M          # noqa: E402


def tokens(famname, n):
    head = {'R': 'W5', 'Qo': 'W4'}[famname]
    return [head, 'B7'] + ['W2', 'B4'] * ((n - 9) // 2) + ['W2', 'W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']


def main():
    nhi = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    for famname, want in (('R', 'NNPNN'), ('Qo', 'NNNPN')):
        for n in range(9, nhi + 1, 2):
            pos = tuple(M.parse_file(t) for t in tokens(famname, n))
            assert M.npawns(pos) == n + 2
            out = []
            for mode in ('keep', 'expire'):
                t0 = time.time()
                f = M.Full(mode)
                sig = f.signature(pos, range(5))
                out.append((mode, sig, f.nodes, time.time() - t0))
            ok = all(s == want for _, s, _, _ in out)
            print(f'{famname}_{n} pawns={n + 2} ' + ' '.join(f'{m}={s} ({k} states, {t:.1f}s)' for m, s, k, t in out)
                  + ('  == ' + ('*2' if famname == 'R' else '*3') if ok else '  (not ' + ('*2' if famname == 'R' else '*3') + ')'),
                  flush=True)


if __name__ == '__main__':
    main()
