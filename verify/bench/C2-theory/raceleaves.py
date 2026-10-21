"""Count race leaves (child positions with both sides passed) in the textbook trees of the 418 library components."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import indep as I
LIB = Path(__file__).resolve().parents[3] / "bench" / "data" / "components.jsonl"
n_with, total = 0, 0
for line in LIB.read_text().splitlines():
    c = json.loads(line)
    for ep in (True, False):
        m = I.Model(c["width"], ep, False, "count")
        races = set()
        orig = m.child
        def child(q, mover, m=m, races=races, orig=orig):
            wp, bp, _ = m.judge(q, False)
            if wp and bp:
                races.add((q, mover))
            return orig(q, mover)
        m.child = child
        m.value(I.parse(c["position"]))
        for side in "WB":
            for q in m.moves(I.parse(c["position"]), side):
                m.child(q, side)
        if ep:
            total += len(races); n_with += bool(races)
print(f"components with >=1 race leaf (e.p. on): {n_with} of 418; race leaves total: {total}")
