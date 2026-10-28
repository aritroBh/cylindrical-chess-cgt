#!/usr/bin/env python3
"""mirror.py < rings > mirrored  : colour reversal of rg-token rings (white pawn on rank r <-> black pawn on rank 9-r)."""
import sys, re
def mirror_tok(t):
    if t == "-": return t
    w = re.search(r"W(\d+)", t); b = re.search(r"B(\d+)", t)
    W = [9 - int(c) for c in b.group(1)] if b else []
    B = [9 - int(c) for c in w.group(1)] if w else []
    return ("W" + "".join(str(r) for r in sorted(W)) if W else "") + ("B" + "".join(str(r) for r in sorted(B)) if B else "")
for line in sys.stdin:
    if line.strip():
        print(" ".join(mirror_tok(t) for t in line.split()))
