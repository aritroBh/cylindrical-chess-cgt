#!/usr/bin/env python3
"""List, per board and R, the hits at the least p for *2 and *3 (positions in star4_hunt notation), and any *>=4 hit."""
import collections, os
T = os.path.dirname(os.path.abspath(__file__))
H = collections.defaultdict(lambda: collections.defaultdict(set))   # (F,w,R,q) -> p -> set of positions
for line in open(T + "/results/hits.tsv"):
    f = line.rstrip("\n").split("\t"); F, w, R, p, q = int(f[0]), int(f[1]), int(f[2]), int(f[3]), int(f[5][1:])
    H[(F, w, R, q)][p].add((f[8], f[9]))
out = ["# Hit positions at the least pawn count (all hits at that count found by the scan; levels flagged partial may have more)\n"]
for (F, w, R, q) in sorted(H, key=lambda k: (k[0], k[1], k[2], k[3])):
    if q >= 4:
        out.append(f"## *{q} candidates: {'cyl' if w else 'flat'} {F} R={R}: {sorted(H[(F,w,R,q)])}")
    if q > 3: continue
    p = min(H[(F, w, R, q)]); s = sorted(H[(F, w, R, q)][p])
    out.append(f"- {'cyl' if w else 'flat'} {F}, R={R}, *{q}, p={p}: {len(s)} found (up to mirror/colour reversal); e.g. `{s[0][0]}`" + (f"; also `{s[1][0]}`" if len(s) > 1 else ""))
open(T + "/results/hits_at_minimum.md", "w").write("\n".join(out) + "\n")
print("\n".join(out[:12]))
