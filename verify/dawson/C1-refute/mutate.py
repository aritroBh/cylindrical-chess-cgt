"""Mutation tests for qverify: make sure each check can actually fail.

Usage: python3 -I mutate.py cert_Q32.txt
Writes mutated certificates to mut/ and runs ./qverify on each with QV_KEEP=1.
For every N-check counterexample that qverify reports, re-checks it here directly:
Phi(G) not in P and no option of G (one strip replaced by one of its options) has Phi in P.
"""
import os
import random
import re
import subprocess
import sys

from brute_misere import load_cert, strip_options

HERE = os.path.dirname(os.path.abspath(__file__))


def write_cert(path, N, mult, P, nmax, phi):
    with open(path, "w") as f:
        f.write(f"{N}\n")
        for row in mult:
            f.write(" ".join(map(str, row)) + "\n")
        f.write(" ".join("1" if p else "0" for p in P) + "\n")
        f.write(f"{nmax}\n" + " ".join(map(str, phi)) + "\n")


def run(path):
    r = subprocess.run([os.path.join(HERE, "qverify"), path], capture_output=True, text=True,
                       env=dict(os.environ, QV_KEEP="1"))
    return r.returncode, r.stdout


def check_counterexample(out, mult, P, phi):
    m = re.search(r"N-COUNTEREXAMPLE: Phi=(\d+) not in P, no P-option; strip counts \(reduced\):(.*)", out)
    if not m:
        return None
    G = []
    for tok in m.group(2).split():
        n, c = tok.split("^")
        G += [int(n)] * int(c)
    def Phi(lst):
        x = phi[0]
        for n in lst:
            x = mult[x][phi[n]]
        return x
    x = Phi(G)
    assert x == int(m.group(1)), (x, m.group(1))
    assert not P[x]
    for i, n in enumerate(G):
        rest = G[:i] + G[i + 1:]
        for (a, b) in strip_options(n):
            y = Phi(rest + [s for s in (a, b) if s > 0])
            if P[y]:
                return f"BOGUS counterexample {G}"
    return f"genuine N-failure at position {sorted(G, reverse=True)} (total {sum(G)})"


def main(cert):
    N, mult, P, nmax, phi = load_cert(cert)
    os.makedirs(os.path.join(HERE, "mut"), exist_ok=True)
    rng = random.Random(20261016)
    results = {}

    def record(kind, rc, out, extra=""):
        fails = re.search(r"RESULT: (.*)", out)
        res = fails.group(1) if fails else out.strip().splitlines()[-1]
        results.setdefault(kind, []).append((rc, res, extra))

    # (a) remove each P element from P
    for x in [i for i in range(N) if P[i]]:
        P2 = P[:]; P2[x] = False
        path = os.path.join(HERE, "mut", "cur.txt"); write_cert(path, N, mult, P2, nmax, phi)
        rc, out = run(path)
        ce = check_counterexample(out, mult, P2, phi)
        record("P->N flip", rc, out, ce or "")
    # (b) add 120 random non-P elements to P
    nonP = [i for i in range(N) if not P[i]]
    for x in rng.sample(nonP, 120):
        P2 = P[:]; P2[x] = True
        path = os.path.join(HERE, "mut", "cur.txt"); write_cert(path, N, mult, P2, nmax, phi)
        rc, out = run(path)
        record("N->P flip", rc, out, check_counterexample(out, mult, P2, phi) or "")
    # (c) change phi(n) for every n (phi(2) kept equal to phi(1) when n == 1), 4 random targets each
    for n in range(1, nmax + 1):
        if n == 2:
            continue
        for _ in range(4):
            phi2 = phi[:]
            v = rng.randrange(N)
            while v == phi[n]:
                v = rng.randrange(N)
            phi2[n] = v
            if n == 1:
                phi2[2] = v
            path = os.path.join(HERE, "mut", "cur.txt"); write_cert(path, N, mult, P, nmax, phi2)
            rc, out = run(path)
            record("phi change", rc, out, check_counterexample(out, mult, P, phi2) or "")
    # (d) break the table symmetrically at 20 random spots
    for _ in range(20):
        a, b = rng.randrange(1, N), rng.randrange(1, N)
        mult2 = [row[:] for row in mult]
        v = rng.randrange(N)
        while v == mult[a][b]:
            v = rng.randrange(N)
        mult2[a][b] = mult2[b][a] = v
        path = os.path.join(HERE, "mut", "cur.txt"); write_cert(path, N, mult2, P, nmax, phi)
        rc, out = run(path)
        record("table change", rc, out)
    # (e) a correct but NON-reduced certificate: Q x Z2, second coordinate = parity of the
    #     number of strips of length 1 or 2; P' = P x Z2.  P- and N-checks must pass and only
    #     reducedness must fail.
    N2 = 2 * N
    mult2 = [[2 * mult[i // 2][j // 2] + ((i % 2) ^ (j % 2)) for j in range(N2)] for i in range(N2)]
    P2 = [P[i // 2] for i in range(N2)]
    phi2 = [2 * phi[n] + (1 if n in (1, 2) else 0) for n in range(nmax + 1)]
    path = os.path.join(HERE, "mut", "nonreduced.txt"); write_cert(path, N2, mult2, P2, nmax, phi2)
    rc, out = run(path)
    lines = [l for l in out.splitlines() if not l.startswith("  N-check")]
    print("(e) Q x Z2 non-reduced certificate:\n    " + "\n    ".join(lines))
    os.remove(path)

    for kind, lst in results.items():
        caught = sum(1 for rc, _, _ in lst if rc != 0)
        print(f"{kind}: {len(lst)} mutants, {caught} rejected, {len(lst) - caught} accepted")
        kinds = {}
        for rc, res, extra in lst:
            kinds[res] = kinds.get(res, 0) + 1
        for res, c in sorted(kinds.items(), key=lambda kv: -kv[1]):
            print(f"    {c:4d} x {res}")
        ex = [extra for _, _, extra in lst if extra]
        bogus = [e for e in ex if e.startswith("BOGUS")]
        print(f"    N-counterexamples re-checked directly: {len(ex)}, bogus: {len(bogus)}")
        for e in ex[:3]:
            print(f"      e.g. {e}")
    os.remove(os.path.join(HERE, "mut", "cur.txt"))


if __name__ == "__main__":
    main(sys.argv[1])
