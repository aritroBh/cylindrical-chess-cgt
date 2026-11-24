"""base_N.py -- direct (unreduced, no poison pruning) search of G + *h, h = 0..4, for M_n and O_n (n pawns), with the
independent engine myeng.Full (program E), under both e.p.-across-heap-move readings ('keep' = cylcgt sum semantics,
'expire' = textbook chess).  M_n, O_n are claimed *2, so the signature must be NNPNN (h = 0..4).  n = 10 (M) and
n = 11 (O) are the smallest; the base cases for the proof are M n = 10..16 and O n = 11..17 (n0 - 2).
Usage (project root):  PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_proof/base_N.py [NHI]   (default 25)
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof'))
import myeng as M          # noqa: E402
import fam                 # noqa: E402

WANT = 'NNPNN'


def start(famname, n):
    toks = fam.M(n) if famname == 'M' else fam.O(n)
    pos = tuple(M.parse_file(t) for t in toks)
    assert M.npawns(pos) == n, (famname, n, M.npawns(pos))
    return pos


def main():
    nhi = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    for famname in ('M', 'O'):
        parity = 0 if famname == 'M' else 1
        lo = 10 if famname == 'M' else 11
        for n in range(lo, nhi + 1, 2):
            pos = start(famname, n)
            out = []
            for mode in ('keep', 'expire'):
                t0 = time.time()
                f = M.Full(mode)
                sig = f.signature(pos, range(5))
                out.append((mode, sig, f.nodes, time.time() - t0))
            ok = all(s == WANT for _, s, _, _ in out)
            print(f'{famname}_{n} pawns={n} ' + ' '.join(f'{m}={s} ({k} states, {t:.1f}s)' for m, s, k, t in out)
                  + ('  == *2' if ok else '  (NOT *2)'), flush=True)


if __name__ == '__main__':
    main()