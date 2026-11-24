"""base_codex.py -- third program: N1 base cases n = 9..14 (both parities) with research/c9_rings/codex/engine.py.
Usage (project root):  PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_plus_1_proof/base_codex.py [NHI]
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'c9_rings', 'codex'))
import engine as E


def tokens(parity, n):
    k = ((n - 7) // 2) if parity == 'odd' else ((n - 8) // 2)
    wall = ['B4', 'W2'] * k
    core = ['B6', 'W2', 'W3', 'B6', 'B7', 'W3', 'W6B7']
    if parity == 'odd':
        t = wall + core
    else:
        t = wall + core + ['W2']
    assert len(t) == n
    return t


def main():
    nhi = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    for parity in ('odd', 'even'):
        start_n = 9 if parity == 'odd' else 10
        for n in range(start_n, nhi + 1, 2):
            toks = tokens(parity, n)
            pos = E.parse_ring(toks, n)
            pawns = n + 1
            assert bin(pos[0]).count('1') + bin(pos[1]).count('1') == pawns
            out = []
            for ep_on_heap in (True, False):
                label = 'keep' if ep_on_heap else 'expire'
                t0 = time.time()
                eng = E.make_engine(n, ep_on_heap)
                sig = eng['signature'](pos, 5)
                out.append((label, sig, time.time() - t0))
            ok = all(s == 'NNPNN' for _, s, _ in out)
            print(f'N1_{parity}_{n} pawns={pawns} ' + ' '.join(f'{m}={s} ({t:.1f}s)' for m, s, t in out)
                  + ('  == *2' if ok else '  (not *2)'), flush=True)


if __name__ == '__main__':
    main()
