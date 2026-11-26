"""K73: summarize r68 'pval' output against the claims of PROOF.md.

Claims: every Table B position is a Black win (r68 'L', White's view); no Table D position and no blockade-F instance
is a Black win; the 162 starts are 161 Black wins and one draw (pawn c4, king b4).
"""
import sys
from collections import Counter

c = Counter()
bad = []
longest = 0
for ln in open(sys.argv[1]):
    lab, *rest = ln.split()
    v = rest[-1]
    kind = "B" if lab[0] == "B" else "D" if lab[0] == "D" else "F" if lab[0] == "F" else "start"
    c[kind, v[0]] += 1
    if v in ("INVALID", "MISSINGCFG"):
        bad.append(ln.strip())
    elif kind == "B" and v[0] != "L":
        bad.append(ln.strip())
    elif kind in ("D", "F") and v[0] == "L":
        bad.append(ln.strip())
    elif kind == "start":
        if lab == "c4_b4":
            if v[0] != "D":
                bad.append(ln.strip())
        elif v[0] != "L":
            bad.append(ln.strip())
        else:
            longest = max(longest, int(v[1:]))
for k in sorted(c):
    print(k, c[k])
print("longest Black win among the 161 starts (plies):", longest)
print("disagreements with PROOF.md:", len(bad))
for b in bad:
    print("  ", b)
