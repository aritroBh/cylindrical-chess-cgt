"""Does the cylinder-only set change if flat values realised only by sum-unsafe
positions (opposite-colour passer threats in different components) are dropped?

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C4-reproduce/safe_check.py count 1
"""
import itertools
import json
import sys

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

rule, ep = sys.argv[1], bool(int(sys.argv[2]))
pawns.RACE_RULE = rule
pawns._value.cache_clear()
d = json.load(open(f"verify/cylatlas/C4-reproduce/indep_{rule}_ep{int(ep)}.json"))
co = set(d["cyl_only_nonW"])

_k = {}


def key(g):
    r = _k.get(g.id)
    if r is None:
        if g.num is not None:
            x = g.num
            r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
        elif g.nim is not None:
            r = f"*{g.nim}"
        else:
            r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
        _k[g.id] = r
    return r


_b = {}


def big(g):
    r = _b.get(g.id)
    if r is None:
        r = (abs(g.num) >= 128) if g.num is not None else any(big(x) for x in g.L + g.R)
        _b[g.id] = r
    return r


board = Board(5, 8, False, ep)
sqs = [(f, r) for f in range(5) for r in range(2, 8)]
safe_vals, unsafe_vals = set(), set()
for tot in range(2, 5):
    for w in range(1, tot):
        for W in itertools.combinations(sqs, w):
            rest = [s for s in sqs if s not in W]
            for B in itertools.combinations(rest, tot - w):
                pos = Pos(frozenset(W), frozenset(B))
                if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"):
                    continue
                k = key(pawns.value(board, pos))
                if len(pawns.components(board, pos)) == 1 or pawns.sum_safe(board, pos):
                    safe_vals.add(k)
                else:
                    unsafe_vals.add(k)
only_unsafe = unsafe_vals - safe_vals
# ring values (non-W) that are on a flat strip only through unsafe sums
ring_nonW = set()
for name, n in (("C3", 3), ("C4", 4)):
    b = Board(n, 8, True, ep)
    for tot in range(2, 5):
        for w in range(1, tot):
            for W in itertools.combinations([(f, r) for f in range(n) for r in range(2, 8)], w):
                rest = [s for s in [(f, r) for f in range(n) for r in range(2, 8)] if s not in W]
                for B in itertools.combinations(rest, tot - w):
                    pos = Pos(frozenset(W), frozenset(B))
                    if pawns.passed(b, pos, "W") or pawns.passed(b, pos, "B"):
                        continue
                    if not pawns.is_ring(b, pos):
                        continue
                    g = pawns.value(b, pos)
                    if not big(g):
                        ring_nonW.add(key(g))
masked = sorted(k for k in ring_nonW & only_unsafe)
print(f"{rule} ep{int(ep)}: flat values only via unsafe sums: {len(only_unsafe)}; "
      f"ring values hidden by them: {len(masked)} {masked[:5]}", flush=True)
