#!/usr/bin/env python3
import sys
tot = bad = 0
for a, b in [("logs/rand_8x6_a.lg", "logs/rand_8x6_a.py"), ("logs/rand_7x6_a.lg", "logs/rand_7x6_a.py")]:
    A = {l.split(" | ")[0]: l.split(" | ")[1].strip() for l in open(a)}
    B = {l.split(" | ")[0]: l.split(" | ")[1].strip() for l in open(b)}
    n = 0; fin = 0; ep = 0
    for k in A:
        if k not in B: continue
        tot += 1; n += 1
        fin += "=inf" not in A[k].split()[0] or any("=inf" not in x for x in A[k].split())
        ep += k.split()[-1] != "-"
        if A[k] != B[k]:
            bad += 1; print("MISMATCH", k, A[k], B[k])
    print(a, "compared", n, "with ep right:", ep, "with some finite value:", fin)
print("total", tot, "mismatches", bad)
