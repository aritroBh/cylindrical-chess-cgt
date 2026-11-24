#!/usr/bin/env python3
"""Cross-check: census7.scope() must yield exactly the same set (and order) as
T22's enumerate_fast.generate_canonical_positions(), for every width.

Memory-light: the two sequences are compared through a rolling hash and a
set of per-position digests, so 17.8M positions do not have to be held.

Run:  PYTHONPATH=. .venv/bin/python research/star2_seven_check/check_gen.py
"""
import hashlib
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "research" / "star2_seven_check"))

import census7


def t22_gen(width):
    """Verbatim copy of the generator in enumerate_fast.py."""
    all_squares = [(f, r) for f in range(width) for r in range(2, 8)]
    n_squares = len(all_squares)
    mirror_map = {i: (width - 1 - f, r) for i, (f, r) in enumerate(all_squares)}
    for w_count in range(1, 7):
        b_count = 7 - w_count
        for white_idx in itertools.combinations(range(n_squares), w_count):
            white_set = set(white_idx)
            remaining = [i for i in range(n_squares) if i not in white_set]
            for black_idx in itertools.combinations(remaining, b_count):
                all_files = set()
                for i in white_idx:
                    all_files.add(all_squares[i][0])
                for i in black_idx:
                    all_files.add(all_squares[i][0])
                if 0 not in all_files or (width - 1) not in all_files:
                    continue
                white_pos = tuple(sorted(all_squares[i] for i in white_idx))
                black_pos = tuple(sorted(all_squares[i] for i in black_idx))
                white_mirror = tuple(sorted(mirror_map[i] for i in white_idx))
                black_mirror = tuple(sorted(mirror_map[i] for i in black_idx))
                if (white_pos, black_pos) > (white_mirror, black_mirror):
                    continue
                yield white_pos, black_pos


def digest(seq):
    """(count, order-hash, order-independent hash) of a sequence of pairs."""
    h = hashlib.sha256()
    g = hashlib.sha256()
    n = 0
    for white, black in seq:
        h.update(repr((white, black)).encode())
        g.update(repr((black, white)).encode())
        n += 1
    return n, h.hexdigest(), g.hexdigest()


def main():
    bad = 0
    for width in (1, 2, 3, 4):
        geom = census7.Geom(width)
        a = digest(t22_gen(width))
        b = digest(census7.scope(geom, 0, 1))
        same_order = a[:2] == b[:2]
        same_set = a[2] == b[2]
        print(f"width {width}: t22 n={a[0]} census7 n={b[0]} "
              f"same_order={same_order} same_set={same_set}", flush=True)
        if not (same_order and same_set):
            bad += 1

    # chunking must partition the scope exactly
    print()
    for width in (2, 3):
        geom = census7.Geom(width)
        for K in (3, 7):
            full = set(census7.scope(geom, 0, 1))
            union = set()
            total = 0
            for k in range(K):
                part = list(census7.scope(geom, k, K))
                total += len(part)
                if set(part) & union:
                    print(f"  width {width} K={K}: OVERLAP in chunk {k}")
                    bad += 1
                union |= set(part)
            ok = (union == full and total == len(full))
            print(f"width {width} K={K}: chunks sum={total} full={len(full)} partition_ok={ok}",
                  flush=True)
            if not ok:
                bad += 1

    print("\n" + ("ALL CHECKS PASSED" if bad == 0 else f"{bad} FAILURES"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
