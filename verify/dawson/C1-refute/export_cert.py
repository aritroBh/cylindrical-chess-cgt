"""Export a worker quotient pickle (pure data: lists/dicts of ints/bools) to a plain text
certificate, using an Unpickler that refuses every class lookup (no worker code is imported).

Output format (whitespace separated ints):
    N
    N*N multiplication table, row-major
    N bits of P
    nmax
    nmax+1 values phi(0..nmax)  (phi(0) = identity, phi(2) = phi(1) if absent: strip 2 and
                                 strip 1 have identical game trees, each with the single option 0)
Usage: python3 export_cert.py <in.pkl> <out.txt>
"""
import pickle
import sys


class SafeU(pickle.Unpickler):
    def find_class(self, module, name):
        raise RuntimeError(f"refusing class {module}.{name}")


def main(src, dst):
    d = SafeU(open(src, "rb")).load()
    mult, P, phi = d["mult"], d["P"], d["phi"]
    N = len(mult)
    # identity found independently (do not trust any convention in the pickle)
    ids = [e for e in range(N) if all(mult[e][x] == x and mult[x][e] == x for x in range(N))]
    assert len(ids) == 1, ids
    e = ids[0]
    nmax = max(phi)
    full = [e] + [None] * nmax
    for n in range(1, nmax + 1):
        if n in phi:
            full[n] = phi[n]
    if full[2] is None:
        full[2] = full[1]
    assert all(v is not None for v in full), full
    with open(dst, "w") as f:
        f.write(f"{N}\n")
        for row in mult:
            f.write(" ".join(map(str, row)) + "\n")
        f.write(" ".join("1" if p else "0" for p in P) + "\n")
        f.write(f"{nmax}\n")
        f.write(" ".join(map(str, full)) + "\n")
    print(f"exported N={N} |P|={sum(map(bool, P))} identity={e} nmax={nmax} -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
