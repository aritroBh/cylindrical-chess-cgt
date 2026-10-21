"""C1-refute run2: mutation tests for qcheck (is the verifier sensitive?).

(a) flip P for every one of the N elements, one at a time;
(b) for every strip k = 1..32 replace phi(k) by 6 random other elements;
(c) Q x Z2 with phi'(4) = (phi(4), 1): outcome-correct and onto but NOT reduced, so qcheck must
    pass the recursion check yet report indistinguishable pairs;
(d) Q x Z2 with P' = P x {0} and phi'(k) = (phi(k), 1) for k = 1: should fail the recursion.
Usage: python3 -I mutants.py cert.txt
"""
import os
import random
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
QCHECK = os.path.join(HERE, "qcheck")


def load(path):
    it = iter(map(int, open(path).read().split()))
    N = next(it)
    mult = [[next(it) for _ in range(N)] for _ in range(N)]
    P = [next(it) for _ in range(N)]
    phi = [next(it) for _ in range(33)]
    return N, mult, P, phi


def write(path, N, mult, P, phi):
    with open(path, "w") as f:
        f.write("%d\n" % N)
        for r in mult:
            f.write(" ".join(map(str, r)) + "\n")
        f.write(" ".join(map(str, P)) + "\n")
        f.write(" ".join(map(str, phi)) + "\n")


def run(N, mult, P, phi, skipassoc):
    fd, path = tempfile.mkstemp(suffix=".txt", dir=HERE)
    os.close(fd)
    try:
        write(path, N, mult, P, phi)
        out = subprocess.run([QCHECK, path, "3000000", "1" if skipassoc else "0"],
                             capture_output=True, text=True).stdout
    finally:
        os.remove(path)
    rec = re.search(r"recursion check failures: (\d+)", out)
    red = re.search(r"indistinguishable pairs of distinct elements: (\d+)", out)
    reach = re.search(r"reachable elements: (\d+) of (\d+)", out)
    return {"pass": "RESULT: PASS" in out,
            "rec": int(rec.group(1)) if rec else None,
            "dup": int(red.group(1)) if red else None,
            "reach": reach.group(0) if reach else None,
            "fail_lines": [l for l in out.splitlines() if "FAILURE" in l][:1]}


def main():
    N, mult, P, phi = load(sys.argv[1])
    random.seed(20261016)
    # (a)
    acc = 0
    recfail = 0
    for x in range(N):
        P2 = list(P)
        P2[x] ^= 1
        r = run(N, mult, P2, phi, True)
        acc += r["pass"]
        recfail += (r["rec"] or 0) > 0
    print("(a) P-bit flips: %d mutants, accepted %d, rejected by the recursion check %d" % (N, acc, recfail))
    # (b)
    acc = 0
    recfail = 0
    tot = 0
    for k in range(1, 33):
        for v in random.sample([y for y in range(N) if y != phi[k]], 6):
            phi2 = list(phi)
            phi2[k] = v
            r = run(N, mult, P, phi2, True)
            tot += 1
            acc += r["pass"]
            recfail += (r["rec"] or 0) > 0
    print("(b) phi changes: %d mutants, accepted %d, rejected by the recursion check %d" % (tot, acc, recfail))
    # (c), (d): direct products with Z2
    idx = lambda x, b: 2 * x + b
    mult2 = [[0] * (2 * N) for _ in range(2 * N)]
    for x in range(N):
        for b in range(2):
            for y in range(N):
                for c in range(2):
                    mult2[idx(x, b)][idx(y, c)] = idx(mult[x][y], b ^ c)
    P2 = [P[i // 2] for i in range(2 * N)]
    phi2 = [idx(phi[k], 0) for k in range(33)]
    phi2[4] = idx(phi[4], 1)
    r = run(2 * N, mult2, P2, phi2, False)
    print("(c) Q x Z2, P' = P x Z2, phi'(4) = (phi(4),1): pass=%s recursion failures=%s indistinguishable pairs=%s %s"
          % (r["pass"], r["rec"], r["dup"], r["reach"]))
    P3 = [P[i // 2] if i % 2 == 0 else 0 for i in range(2 * N)]
    phi3 = [idx(phi[k], 0) for k in range(33)]
    phi3[1] = idx(phi[1], 1)
    r = run(2 * N, mult2, P3, phi3, False)
    print("(d) Q x Z2, P' = P x {0}, phi'(1) = (phi(1),1): pass=%s recursion failures=%s indistinguishable pairs=%s %s %s"
          % (r["pass"], r["rec"], r["dup"], r["reach"], r["fail_lines"]))


main()
