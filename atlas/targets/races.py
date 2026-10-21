#!/usr/bin/env python3
"""Race-node counts and values of the 7-pawn *2 (W a4 b3 d2 d3 / B a7 b7 c5, 4 files)
under the 3 race rules x 2 passed tests x e.p. on/off, computed by cylcgt itself
(ep-aware-passed worktree; PASSED_RESPECTS_EP toggled), cold cache per setting.

Usage (from the project root):
  PYTHONPATH= .venv/bin/python atlas/targets/races.py > atlas/targets/races_star2_7pawn.out
"""
import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt")
from cylcgt import cgt, pawns  # noqa: E402

POS = sys.argv[1] if len(sys.argv) > 1 else "W: a4 b3 d2 d3 / B: a7 b7 c5"
WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 4
print("module", pawns.__file__)
for aware in (True, False):
    for ep in (True, False):
        for rule in ("count", "mover", "opponent"):
            pawns.PASSED_RESPECTS_EP = aware
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            pawns.race_hits.clear()
            g = pawns.value(pawns.Board(WIDTH, 8, False, ep), pawns.Pos.parse(POS))
            hits = list(pawns.race_hits)
            pos = {h.rsplit(" after ", 1)[0] for h in hits}
            print(f"aware={aware} ep={ep} {rule:8s}: value {cgt.show(g)[:60]:60s} race edges (cold cache) {len(hits)}, "
                  f"distinct race positions {len(pos)}, (position, mover) pairs {len(set(hits))}")
