"""Mutation test: would the family comparison notice if e.p. across the a/h seam were
missing?  Runs bf with seam e.p. disabled on cyl3/cyl4/cyl5 (e.p. on, pcomp scope) and
counts positions where that mutant differs from (a) the full bf and (b) fresh cylcgt.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/sumtest/C1-refute/v2/mutate.py
"""
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bf  # noqa: E402

OUT = os.path.join(HERE, "out")


def load(p):
    with gzip.open(p, "rt") as fh:
        return json.load(fh)["outcomes"]


for board in ("cyl3", "cyl4", "cyl5"):
    for rule in ("count", "mover", "opponent"):
        F, wrap = bf.BOARDS[board]
        geo, fam = bf.family(F, wrap)
        s = bf.Solver(F, wrap, True, rule, "pcomp")
        s.seam_ep = False
        res = {geo.show(W, B): [] for W, B in fam}
        for n in bf.REF_NAMES:
            s.memo.clear()
            for W, B in fam:
                res[geo.show(W, B)].append(s.outcome(W, B, bf.REF[n]))
        res = {k: "".join(v) for k, v in res.items()}
        full = load(os.path.join(OUT, f"bf__{board}__{rule}__ep__pcomp.json.gz"))
        cy = load(os.path.join(OUT, f"cy__{board}__{rule}__ep.json.gz"))
        d_full = sum(res[k] != full[k] for k in res)
        d_cy = sum(res[k] != cy[k] for k in res)
        ex = sorted(k for k in res if res[k] != cy[k])[:1]
        print(board, rule, "mutant!=full_bf", d_full, "mutant!=cylcgt", d_cy, "example", ex, flush=True)
