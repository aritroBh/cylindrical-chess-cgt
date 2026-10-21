"""Two-component positions (2+2 and 2+3 pawns) evaluated as whole-board games
(first passer anywhere ends the game; races detected across the whole board),
instead of as sums. Sensitivity check of the sum model; not part of the claim.

Run: ../../../.venv/bin/python pairs_whole.py --rule count --ep 1 --epaware 0
"""
import argparse
import json
import time

import cg
import pg
from scan import atoms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", default="count")
    ap.add_argument("--ep", type=int, default=1)
    ap.add_argument("--epaware", type=int, default=0)
    a = ap.parse_args()
    pg.RULE, pg.EP, pg.EPAWARE = a.rule, bool(a.ep), bool(a.epaware)
    t0 = time.time()
    reps = {2: [], 3: []}
    for w in (1, 2, 3):
        for p in (2, 3):
            if p >= w:
                reps[p] += [(w, W, B) for W, B in atoms("F", w, p)]
    out = {"settings": vars(a), "n2": len(reps[2]), "n3": len(reps[3])}
    pairs = [(x, y) for i, x in enumerate(reps[2]) for y in reps[2][i:]] + \
            [(x, y) for x in reps[2] for y in reps[3]]
    nim = {}
    nims_ge2 = []
    differ = 0
    for (w1, W1, B1), (w2, W2, B2) in pairs:
        off = w1 + 1
        n = w1 + 1 + w2
        W = tuple(sorted(W1 + tuple((f + off, r) for f, r in W2)))
        B = tuple(sorted(B1 + tuple((f + off, r) for f, r in B2)))
        pg.SPLIT = False
        g = pg.root_value("F", n, W, B)
        pg.SPLIT = True
        s = pg.root_value("F", n, W, B)
        if g != s:
            differ += 1
        k = cg.nimber_eq(g, 32)
        if k is not None:
            nim[k] = nim.get(k, 0) + 1
            if k >= 2:
                nims_ge2.append(pg.fmt(W, B))
    out.update({"pairs": len(pairs), "whole_board_nimber_counts": nim, "whole_board_k_ge_2": nims_ge2,
                "pairs_where_whole_board_value_differs_from_sum": differ,
                "seconds": round(time.time() - t0, 1)})
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
