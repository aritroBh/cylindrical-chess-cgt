"""Mutation test: would the C1 comparison have caught plausible solver bugs?
Each mutant is the worker's solver (imported, unmodified) with one rule changed via subclassing;
its outcome vectors are compared with the worker's stored cylcgt predictions.
Run: cd C1-reproduce/pkg && PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames \
     /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python ../scripts/mutations.py
"""
import gzip, json, os
from sumtest.sumsolver import REF_NAMES, Geometry, Rules, SumSolver, Trees, reference_set
from sumtest.enum_positions import BOARDS, positions
D = "/Users/aritro/Downloads/Research/Chessendgames/sumtest/data"

class TieToMover(Rules):
    def resolve(self, W, B, ep, mover_white):
        r = super().resolve(W, B, ep, mover_white)
        if r and self.race_rule == "count" and self.passers(W, B, ep, True) and self.passers(W, B, ep, False):
            sw, sb = self.steps(self.passers(W, B, ep, True), True), self.steps(self.passers(W, B, ep, False), False)
            sm, so = (sw, sb) if mover_white else (sb, sw)
            return ("R" if mover_white else "L") if so < sm else ("L" if mover_white else "R")
        return r

class NoSeamEP(Rules):          # e.p. allowed only between files that are adjacent on a FLAT board
    def moves(self, W, B, ep, white):
        out = super().moves(W, B, ep, white)
        if ep < 0 or not self.g.wrap:
            return out
        g = self.g; keep = []
        for (W2, B2, e2) in out:
            mover_new = (W2 & ~W) if white else (B2 & ~B)
            t = mover_new.bit_length() - 1 if mover_new else -1
            if t == ep:
                src = ((W & ~W2) if white else (B & ~B2)).bit_length() - 1
                if abs(g.fileof[src] - g.fileof[ep]) != 1:
                    continue
            keep.append((W2, B2, e2))
        return keep

def run(cls, kw, rules_list, eps):
    tot = 0
    for bd, (files, wrap) in BOARDS.items():
        geo, pos = positions(files, wrap)
        for rule in rules_list:
            for ep in eps:
                cy = json.load(gzip.open(os.path.join(D, f"cylcgt__{bd}__{rule}__{'ep' if ep else 'noep'}.json.gz"), "rt"))["outcomes"]
                T = Trees(); ref = reference_set(T); idx = [ref[n] for n in REF_NAMES]
                s = SumSolver(cls(geo, ep=ep, ep_aware=False, race_rule=rule, **kw), T)
                d = 0
                for W, B in pos:
                    wl, wr = s.solve(s.start_state(W, B))
                    d += "".join(s.outcome(wl, wr, k) for k in idx) != cy[geo.show(W, B)]
                tot += d
                print(f"  {bd} {rule} ep={ep}: {d} positions differ")
    return tot

print("unmutated control (plain whole):", run(Rules, {}, ["count"], [True, False]))
print("mutant race_double=False:", run(Rules, {"race_double": False}, ["count"], [True, False]))
print("mutant count ties->mover:", run(TieToMover, {}, ["count"], [True, False]))
print("mutant no e.p. across seam:", run(NoSeamEP, {}, ["count", "mover", "opponent"], [True]))
