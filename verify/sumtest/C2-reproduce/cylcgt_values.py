"""cylcgt value of W a2 c2 / B b7 d7 on 4-file flat (and other boards) per race rule and e.p."""
import sys
from cylcgt import cgt, pawns

POS = "W: a2 c2 / B: b7 d7"
boards = [(4, False), (8, False), (8, True), (5, True)]
for files, wrap in boards:
    for ep in (False, True):
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            pawns.race_hits.clear()
            b = pawns.Board(files, 8, wrap, ep)
            p = pawns.Pos.parse(POS)
            v = pawns.value(b, p)
            star2 = cgt.nimber(2)
            print(f"files={files} wrap={wrap} ep={ep} rule={rule}: value={cgt.show(v)} "
                  f"outcome(G)={cgt.outcome(v)} outcome(G+*2)={cgt.outcome(cgt.add(v, star2))} "
                  f"race_hits={len(pawns.race_hits)} sum_safe={pawns.sum_safe(b, p)}")
