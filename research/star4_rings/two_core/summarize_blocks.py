import sys
from collections import defaultdict, Counter
from lib import nimber
w = sys.argv[1]
d = defaultdict(dict)
for line in list(open(f"blocks_w{w}.tsv"))[1:]:
    blk, f, L, sig = line.rstrip("\n").split("\t")
    d[(blk, f)][int(L)] = sig
cnt = Counter(); hits = []
for (blk, f), m in sorted(d.items()):
    for par, (a, b) in (("even", (4, 6)), ("odd", (5, 7))):
        s1, s2 = m[a], m[b]
        if "ILLEGAL" in (s1, s2): continue
        v1, v2 = nimber(s1), nimber(s2)
        if v1 is not None and v1 == v2:
            cnt[(par, v1)] += 1
            if isinstance(v1, int) and v1 >= 1: hits.append((blk, f, par, v1))
print(sorted(cnt.items(), key=str))
for h in hits: print(*h)
