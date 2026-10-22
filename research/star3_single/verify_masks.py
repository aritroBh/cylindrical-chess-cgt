#!/usr/bin/env python3
"""verify_masks.py WIDTH FILE : nimber of each position by the Codex solver's outcome-mask recursion
(verify_ext/codex/solver.py PawnGame._outcome_masks, default setting count / e.p. on / e.p.-aware), an
implementation written independently of the C scanner and of cylcgt.  Prints position, nimber (or -1), outcome."""
import os, sys, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
sys.setrecursionlimit(1000000)
import solver as cx
width = int(sys.argv[1])
g = cx.PawnGame(width, "count", True, "aware")
full = (1 << (cx.MAX_NIMBER + 1)) - 1
for line in open(sys.argv[2]):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    t = time.time()
    w, b = cx.parse_position(line.replace(":", ""), width)
    left, right = g._outcome_masks(w, b, -1, 0)
    nim = next((k for k in range(cx.MAX_NIMBER + 1) if not (left >> k) & 1 and not (right >> k) & 1), -1)
    out = "N" if (left & 1 and right & 1) else "L" if left & 1 else "R" if right & 1 else "P"
    print(f"{line}\tnimber={nim}\toutcome={out}\t{time.time()-t:.0f}s", flush=True)
