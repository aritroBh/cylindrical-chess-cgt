"""C1-refute run2: export the worker's quotient pickle (pure data) to plain text.

No worker code is imported: the Unpickler refuses every class lookup.
Output (whitespace-separated ints):
    N
    N rows of the N x N multiplication table
    N bits of P
    33 values phi(0..32); phi(0) = identity element (found here, not trusted);
    phi(2) is absent in the pickle and is set to phi(1) (strip 2 and strip 1 both have the single
    option "empty"), but the verifier treats strip 2 as its own generator with its own options.
Usage: python3 -I export.py <in.pkl> <out.txt>
"""
import pickle
import sys


class NoClasses(pickle.Unpickler):
    def find_class(self, module, name):
        raise RuntimeError("refusing class %s.%s" % (module, name))


d = NoClasses(open(sys.argv[1], "rb")).load()
mult, P, phi = d["mult"], d["P"], dict(d["phi"])
N = len(mult)
assert all(len(r) == N for r in mult)
ids = [e for e in range(N) if all(mult[e][x] == x and mult[x][e] == x for x in range(N))]
assert len(ids) == 1, ids
e = ids[0]
assert 2 not in phi
phi[2] = phi[1]
phi[0] = e
assert sorted(phi) == list(range(33)), sorted(phi)
with open(sys.argv[2], "w") as f:
    f.write("%d\n" % N)
    for r in mult:
        f.write(" ".join(map(str, r)) + "\n")
    f.write(" ".join("1" if p else "0" for p in P) + "\n")
    f.write(" ".join(str(phi[n]) for n in range(33)) + "\n")
print("N=%d |P|=%d identity=%d phi=%s" % (N, sum(map(bool, P)), e, [phi[n] for n in range(33)]))
