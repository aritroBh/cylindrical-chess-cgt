"""Explicit members of the two families, evaluated with ringeval_w; writes families.tsv.
Odd n = 2k+3 (k >= 1):  a:W2W3/B4  b:B5  c:W2/B5  then (W3, B5) x k           -> n+3 pawns
Even n = 2m+6 (m >= 0): a:B5  b:W2/B5  c:W3W5/B6  d:W2  then (B4, W2) x (m+1)  -> n+3 pawns
"""
import sys
sys.path.insert(0, "research/ring_family")
from ringlib import *

def odd(n):
    assert n % 2 == 1 and n >= 5
    k = (n - 3) // 2
    return from_cstr("W23B4 B5 W2B5") + from_cstr("W3 B5") * k

def even(n):
    assert n % 2 == 0 and n >= 6
    m = (n - 6) // 2
    return from_cstr("B5 W2B5 W35B6 W2") + from_cstr("B4 W2") * (m + 1)

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    rows = []
    for n in range(5, nmax + 1):
        r = odd(n) if n % 2 else even(n)
        assert nparts(r) == n + 3
        res = evaluate([r])[0]
        rows.append((n, nparts(r), "odd" if n % 2 else "even", to_text(r), cstr(r), res))
        print(n, nparts(r), rows[-1][2], to_text(r), res, flush=True)
    with open("research/ring_family/families.tsv", "w") as f:
        f.write("n\tpawns\tfamily\tposition\tfile_contents\toutcome\tnimber\tsig\n")
        for n, p, fam, t, c, res in rows:
            f.write(f"{n}\t{p}\t{fam}\t{t}\t{c}\t{res[0]}\t{res[1]}\t{res[2]}\n")
