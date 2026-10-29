"""base_S3T3.py -- direct (unreduced) search of T3_n / S3_n + *h, h=0..5, with engine E (myeng.Full),
under both e.p.-across-heap readings.  Expected signature NNNPNN (claimed *3).

Usage (project root):
  PYTHONPATH=. nice -n 15 .venv/bin/python research/star3_proof/base_S3T3.py T3 12 16
  PYTHONPATH=. nice -n 15 .venv/bin/python research/star3_proof/base_S3T3.py S3 13 17
"""
import os
import sys
import time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof'))
import myeng as M
import fam


def toks(famname, n):
    return fam.T3(n) if famname == 'T3' else fam.S3(n)


def main():
    famname = sys.argv[1]
    lo = int(sys.argv[2])
    hi = int(sys.argv[3])
    want = 'NNNPNN'
    for n in range(lo, hi + 1, 2):
        t = toks(famname, n)
        pos = tuple(M.parse_file(x) for x in t)
        assert M.npawns(pos) == n + 1
        out = []
        for mode in ('keep', 'expire'):
            f = M.Full(mode)
            sig = f.signature(pos, range(6))
            out.append((mode, sig, f.nodes))
        ok = all(s == want for _, s, _ in out)
        print(f'{famname}_{n} pawns={n+1} ' + ' '.join(f'{m}={s} ({k} states)' for m, s, k in out)
              + ('  == *3' if ok else '  (NOT *3)'), flush=True)


if __name__ == '__main__':
    main()
