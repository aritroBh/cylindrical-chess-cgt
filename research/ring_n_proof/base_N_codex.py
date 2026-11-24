"""Third program: base cases n = 10..14 (M even, O odd) with c9_rings/codex/engine.py (written from the rules by another model).
Computes G + *h signature, h = 0..4, under both e.p.-across-heap readings.  M, O claimed *2 => NNPNN.
Usage (project root):  PYTHONPATH=. nice -n 15 .venv/bin/python research/ring_n_proof/base_N_codex.py
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ring_n_plus_2_proof'))
import fam as FAM  # noqa: E402

import importlib.util
spec = importlib.util.spec_from_file_location('codex_engine', os.path.join(HERE, '..', 'c9_rings', 'codex', 'engine.py'))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


def run(famname, n):
    toks = FAM.M(n) if famname == 'M' else FAM.O(n)
    w, b, _ = C.parse_ring(toks, n)
    pos = (w, b, None)
    for keep in (True, False):
        eng = C.make_engine(n, keep)
        sig = eng['signature'](pos, 5)
        print(f'  codex keep_heap={keep}: {sig}', flush=True)


def main():
    for famname in ('M', 'O'):
        parity_lo = 10 if famname == 'M' else 11
        for n in range(parity_lo, 15, 2):
            print(f'{famname}_{n} pawns={n}', flush=True)
            run(famname, n)


if __name__ == '__main__':
    main()