"""Mutation test of the 'count' race rule: (a) no home-rank double-step credit,
(b) ties go to the mover.  Counts family positions (e.p. off) where each mutant differs
from fresh cylcgt.   .venv/bin/python verify/sumtest/C1-refute/v2/mutate_count.py"""
import gzip, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bf
OUT = os.path.join(HERE, "out")
orig_dist = bf.dist
def nocredit(geo, W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    best = 10 ** 6
    for s in bf.bits(mine):
        if theirs & geo.span[side][s]:
            continue
        f, r = geo.fr(s)
        best = min(best, bf.RANKS - r if side == "W" else r - 1)
    return best
class TieMover(bf.Solver):
    def classify(self, W, B, mover):
        geo = self.geo
        wp, bp = bf.passed(geo, W, B, "W"), bf.passed(geo, W, B, "B")
        if wp and bp:
            other = "B" if mover == "W" else "W"
            return other if bf.dist(geo, W, B, other) < bf.dist(geo, W, B, mover) else mover
        return super().classify(W, B, mover)
def run(cls, board):
    F, wrap = bf.BOARDS[board]
    geo, fam = bf.family(F, wrap)
    s = cls(F, wrap, False, "count", "pcomp")
    res = {geo.show(W, B): [] for W, B in fam}
    for n in bf.REF_NAMES:
        s.memo.clear()
        for W, B in fam:
            res[geo.show(W, B)].append(s.outcome(W, B, bf.REF[n]))
    return {k: "".join(v) for k, v in res.items()}
for board in bf.BOARDS:
    with gzip.open(os.path.join(OUT, f"cy__{board}__count__noep.json.gz"), "rt") as fh:
        cy = json.load(fh)["outcomes"]
    bf.dist = nocredit
    a = run(bf.Solver, board)
    bf.dist = orig_dist
    b = run(TieMover, board)
    print(board, "no-credit mutant != cylcgt:", sum(a[k] != cy[k] for k in a),
          "| ties-to-mover mutant != cylcgt:", sum(b[k] != cy[k] for k in b), flush=True)
