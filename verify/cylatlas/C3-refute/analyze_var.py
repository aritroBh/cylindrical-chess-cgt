"""Cylinder-only (non-W) value set for a results file; compare with results.json.

  ../../../.venv/bin/python -I analyze_var.py results_big1024.json
"""
import json
import sys
from collections import defaultdict


def load(fn):
    R = json.load(open(fn))
    A, S = R["atoms"], R["sums"]
    big = {}
    for d in A.values():
        for k, e in d["values"].items():
            big[k] = e["big"]
    for k, e in S.items():
        big.setdefault(k, e["big"])

    def atom(kind, s, p):
        return A.get(f"{kind}{s}_p{p}", {}).get("values", {})

    def flat(n):
        out = set()
        for s in range(1, min(n, 5) + 1):
            for p in range(2, 6):
                out |= set(atom("flat", s, p))
        out |= {k for k, e in S.items() if e["min_width"] <= n}
        return out

    def ring(n):
        out = set()
        for p in range(n, 6):
            out |= set(atom("ring", n, p))
        return out

    cyl = lambda n: flat(n - 1) | ring(n)
    allC = set().union(*(cyl(n) for n in range(3, 9)))
    allF = set().union(*(flat(n) for n in range(3, 9)))
    g = {k for k in allC - allF if not big[k]}
    by = defaultdict(set)
    for k in g:
        by[min(n for n in range(3, 9) if k in cyl(n))].add(k)
    T1 = [(n, len(cyl(n)), len(flat(n))) for n in range(3, 9)]
    nonW = lambda X: {k for k in X if not big[k]}
    sets = {n: (nonW(cyl(n)), nonW(flat(n))) for n in range(3, 9)}
    return g, by, T1, len(allF - allC), sets


base = load("results.json")
var = load(sys.argv[1])
print("file:", sys.argv[1])
print("T1 (n, cyl values, flat values):", var[2])
print("flat-only values (union):", var[3])
print("cyl-only nonW:", len(var[0]), {n: len(v) for n, v in sorted(var[1].items())})
print("identical to base (results.json) cyl-only nonW set:", var[0] == base[0])
for n in range(3, 9):
    print(f"  n={n}: nonW cyl set equal to base: {var[4][n][0] == base[4][n][0]}, nonW flat set equal: {var[4][n][1] == base[4][n][1]}")
for k in sorted(var[0] - base[0]):
    print("  new in variant:", k)
for k in sorted(base[0] - var[0]):
    print("  lost in variant:", k)
