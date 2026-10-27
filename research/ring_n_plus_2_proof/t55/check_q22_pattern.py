#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fam
from graph import build, parse_pos, strip_ep

# Build R_22 for Q
toks = fam.Q(22)
g = build(toks)
print(f"nodes={g.n()}, stat={g.stat}")
# Check files 5..14 in every node
bad = []
for i, p in enumerate(g.pos):
    ptoks, ep = parse_pos(p)
    # check range 5..14 inclusive
    ok = True
    for j in range(5, 15):  # 5 to 14
        if j >= len(ptoks):
            bad.append((i, j, "OOB")); ok=False; break
        # pattern file means exactly its starting pawn and nothing else
        # get expected pattern for Q in wall regions - but easier to just check they match start
        pass
    if not ok: continue
# compare to start
start_ptoks, _ = parse_pos(g.pos[0]) if g.n()>0 else (toks, None)
for i, p in enumerate(g.pos):
    ptoks, ep = parse_pos(p)
    for j in range(5, 15):
        if ptoks[j] != start_ptoks[j]:
            bad.append((i, j, ptoks[j], start_ptoks[j]))
            break
    else:
        continue
    break
else:
    print("ALL_NODES_FILES_5_14_EQUAL_START: True")
    sys.exit(0)
print("BAD:", bad[:10])
