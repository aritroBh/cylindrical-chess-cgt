"""Compare the Python (dawson/misere.py) and C (dawson/misere.c) misere solvers
position by position, for every canonical position with total <= T.

    cc -O2 -o dawson/misere_c dawson/misere.c
    dawson/misere_c 45 dawson/misere_c_45.bin
    PYTHONPATH=. .venv/bin/python -m dawson.compare_misere 45 dawson/misere_c_45.bin
"""
import sys

from dawson import misere as M


def main(T, path):
    data = open(path, "rb").read()
    idx = 0
    bad = 0
    total = 0
    for t in range(T + 1):
        # C enumerates in rank order: first part ascending, recursively; reproduce by sorting
        parts = sorted(M.partitions(t), key=lambda lam: tuple(sorted(lam, reverse=True)))
        for lam in parts:
            v = M._P(tuple(sorted(lam)))
            if v != bool(data[idx]):
                bad += 1
            idx += 1
            total += 1
    assert idx == len(data), (idx, len(data))
    print(f"compared {total} positions (total <= {T}); disagreements: {bad}")


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
