"""Distinct race positions met in the game tree of the headline positions
(independent engine). Run: ../../../.venv/bin/python races.py"""
import pg

seen_pos = {}
orig = pg.race_winner


def spy(kind, n, W, B, ep, mover):
    seen_pos.setdefault((kind, n), set()).add((W, B))
    seen_full.add((kind, n, W, B, ep, mover))
    return orig(kind, n, W, B, ep, mover)


pg.race_winner = spy
for ep in (True, False):
    for kind, n, text in (("F", 4, "W: a2 c2 / B: b7 d7"), ("C", 4, "W: a2 c2 / B: b7 d7"),
                          ("C", 3, "W: a2 b3 / B: a5 c5")):
        pg.RULE, pg.EP, pg.EPAWARE, pg.SPLIT = "count", ep, False, True
        pg.reset(); seen_pos.clear(); seen_full = set()
        W, B = pg.parse(text)
        pg.root_value(kind, n, W, B)
        print(f"ep={ep} {kind}{n} {text}: race evaluations={pg.race_count[0]}, "
              f"distinct (position, e.p., mover)={len(seen_full)}, distinct pawn configurations="
              f"{sum(len(v) for v in seen_pos.values())}")
