"""Sensitivity checks quoted in the sumtest findings.

  PYTHONPATH=. .venv/bin/python -m sumtest.extra_checks

1. How many (position, rule) cases change when en passant is switched on
   (textbook and e.p.-aware passer tests), and plain vs aware.
2. How many positions change under "count" if the race count ignores the double step,
   compared with cylcgt's stored predictions.
3. Variant equalities: whole == comp, local == global e.p. scope.
"""
import gzip
import json
import os

from sumtest.enum_positions import BOARDS, OUT, positions
from sumtest.sumsolver import REF_NAMES, Rules, SumSolver, Trees, reference_set


def L(name):
    with gzip.open(os.path.join(OUT, name), "rt") as fh:
        return json.load(fh)["outcomes"]


def main():
    tot = [0, 0, 0, 0]
    for b in BOARDS:
        for r in ("count", "mover", "opponent"):
            off, pl, aw = (L(f"mine__{b}__{r}__{e}__whole.json.gz") for e in ("off", "plain", "aware"))
            tot[0] += len(off)
            tot[1] += sum(off[k] != pl[k] for k in off)
            tot[2] += sum(off[k] != aw[k] for k in off)
            tot[3] += sum(pl[k] != aw[k] for k in off)
    print("cases %d; e.p. changes vector: textbook %d, aware %d; textbook vs aware differ %d" % tuple(tot))

    for ep in (False, True):
        n = d = 0
        for b, (f, w) in BOARDS.items():
            cy = L(f"cylcgt__{b}__count__{'ep' if ep else 'noep'}.json.gz")
            geo, pos = positions(f, w)
            T = Trees()
            ref = reference_set(T)
            s = SumSolver(Rules(geo, ep=ep, ep_aware=False, race_rule="count", race_double=False), T)
            for W, B in pos:
                wl, wr = s.solve(s.start_state(W, B))
                n += 1
                d += "".join(s.outcome(wl, wr, ref[x]) for x in REF_NAMES) != cy[geo.show(W, B)]
        print(f"ep={ep}: race count without double step differs from cylcgt on {d} of {n} positions")

    pairs = [(("plain", "whole"), ("plain", "comp")), (("plain", "whole"), ("plain-global", "whole")),
             (("aware", "whole"), ("aware", "comp")), (("aware", "whole"), ("aware-global", "whole")),
             (("off", "whole"), ("off", "comp"))]
    for p, q in pairs:
        d = 0
        for b in BOARDS:
            for r in ("count", "mover", "opponent"):
                A, B = L(f"mine__{b}__{r}__{p[0]}__{p[1]}.json.gz"), L(f"mine__{b}__{r}__{q[0]}__{q[1]}.json.gz")
                d += sum(A[k] != B[k] for k in A)
        print(f"{p} vs {q}: {d} differing cases")


if __name__ == "__main__":
    main()
