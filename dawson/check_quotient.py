"""Check a computed partial quotient Q_n against the exhaustive misere table of misere.c.

For every canonical position whose strips all have length <= n and whose total is <= T,
the outcome predicted by the quotient (Phi(position) in P) must equal the outcome found by
exhaustive search. The two computations share no code beyond the move rule of 0.137.

    cc -O2 -o dawson/misere_c dawson/misere.c
    dawson/misere_c 60 dawson/misere_c_60.bin
    PYTHONPATH=. .venv/bin/python -m dawson.check_quotient dawson/quotient_Q32.pkl 60 dawson/misere_c_60.bin
"""
import pickle
import sys

from dawson import misere as M


def main(pkl, T, binpath):
    d = pickle.load(open(pkl, "rb"))
    mult, P, phi, gens = d["mult"], d["P"], d["phi"], d["gens"]
    n = max(gens)
    data = open(binpath, "rb").read()
    idx = checked = bad = 0
    first_bad = []
    for t in range(T + 1):
        parts = sorted(M.partitions(t), key=lambda lam: tuple(sorted(lam, reverse=True)))
        for lam in parts:
            if lam and max(lam) <= n:
                x = 0
                for h in lam:
                    x = mult[x][phi[h]]
                checked += 1
                if bool(P[x]) != bool(data[idx]):
                    bad += 1
                    if len(first_bad) < 5:
                        first_bad.append(lam)
            idx += 1
    print(f"Q_{n} (|Q| = {len(mult)}, |P| = {sum(P)}): checked {checked} positions with strips <= {n}"
          f" and total <= {T}; disagreements with exhaustive search: {bad} {first_bad}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
