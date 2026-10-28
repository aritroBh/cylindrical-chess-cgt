#!/usr/bin/env python3
"""hits2tokens.py HITS.tsv N  -> rg tokens (one ring per line) for the scanner's hit rows, plus the scanner's label."""
import sys
def tok(row, n):
    pos = row.split("\t")[0]
    w, b = pos.replace("W:", "").split("/ B:")
    W = [[] for _ in range(n)]; B = [[] for _ in range(n)]
    for s in w.split(): W[ord(s[0]) - 97].append(s[1])
    for s in b.split(): B[ord(s[0]) - 97].append(s[1])
    out = []
    for f in range(n):
        t = ("W" + "".join(sorted(W[f])) if W[f] else "") + ("B" + "".join(sorted(B[f])) if B[f] else "")
        out.append(t or "-")
    return " ".join(out)
if __name__ == "__main__":
    n = int(sys.argv[2])
    for line in open(sys.argv[1]):
        if line.strip():
            f = line.rstrip("\n").split("\t")
            print(tok(f[0], n) + ("\t" + f[-1] if len(f) > 1 else ""))
