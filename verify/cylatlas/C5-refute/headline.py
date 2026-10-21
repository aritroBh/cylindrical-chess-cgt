"""Headline values of claim C5 with the independent engine, under all settings.

Run: cd verify/cylatlas/C5-refute && ../../../.venv/bin/python -I headline.py
"""
import time
from fractions import Fraction as Fr

import cg
import pg

S = cg.star
H = cg.make([cg.make([cg.integer(2)], [cg.integer(1)])],
            [cg.make([cg.integer(-1)], [cg.integer(-2)])])   # {3/2±1/2 | -3/2±1/2}
UP = cg.make([cg.ZERO], [S(1)])
REF = {"*2": S(2), "*": S(1), "0": cg.ZERO, "{3/2±1/2|-3/2±1/2}": H, "↑": UP,
       "{2±1|-2±1}": cg.make([cg.make([cg.integer(3)], [cg.integer(1)])],
                              [cg.make([cg.integer(-1)], [cg.integer(-3)])]),
       "±1/2": cg.make([cg.number(Fr(1, 2))], [cg.number(Fr(-1, 2))])}

POS = [("F", 4, "W: a2 c2 / B: b7 d7"),
       ("C", 4, "W: a2 c2 / B: b7 d7"),
       ("C", 3, "W: a2 b3 / B: a5 c5"),
       ("C", 3, "W: a2 b2 / B: a5 c7"),
       ("F", 1, "W: a2 / B: a5"),
       ("F", 1, "W: a4 / B: a6")]


def name(g):
    for k, v in REF.items():
        if v == g:
            return k
    return cg.show(g, big=pg.BIG)


if __name__ == "__main__":
    for split in (True, False):
        for epaware in (False, True):
            for ep in (True, False):
                if epaware and not ep:
                    continue
                for rule in ("count", "mover", "opponent"):
                    pg.RULE, pg.EP, pg.EPAWARE, pg.SPLIT = rule, ep, epaware, split
                    pg.reset()
                    row = []
                    for kind, n, text in POS:
                        W, B = pg.parse(text)
                        t = time.time()
                        pg.race_count[0] = 0
                        g = pg.root_value(kind, n, W, B)
                        row.append(f"{kind}{n} {text}: {name(g)} [races {pg.race_count[0]}]")
                    print(f"split={split} epaware={epaware} ep={ep} rule={rule}")
                    for r in row:
                        print("   ", r)
