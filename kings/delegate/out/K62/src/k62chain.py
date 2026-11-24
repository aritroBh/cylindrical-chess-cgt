"""K62: Lambda_N against the terminal-free chains C_k (positions 0..k; L(i) = {i-1}, R(i) = {0} for i >= 1;
position 0 has no options; C_1 = *, position 2 of C_2 is a down-arrow). Usage (from the repository root):
  .venv/bin/python kings/delegate/out/K62/src/k62chain.py NMAX
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k62lib import DGame, exactness, x_of, value_G_T, value_over_T, results_of_omega  # noqa: E402
from k62families import lam  # noqa: E402


def chain(k):
    return DGame([[]] + [[i - 1] for i in range(1, k + 1)], [[]] + [[0] for _ in range(1, k + 1)], 'C%d' % k)


nmax = int(sys.argv[1])
for N in range(1, nmax + 1):
    G = lam(N)
    ok, info = exactness(G)
    row = []
    for k in range(1, nmax + 3):
        T = chain(k)
        rom, rz = value_over_T(T)
        v = value_G_T(G, T)
        viol = results_of_omega(G, info, T, v, rom, rz)
        row.append('C%d:%s' % (k, 'pass' if not viol else 'FAIL'))
    print('Lambda_%d' % N, ' '.join(row))
