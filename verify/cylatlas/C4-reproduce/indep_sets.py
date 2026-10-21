"""Independent re-derivation of the cylinder-only value sets (w+b <= 4) for one
(race rule, e.p.) setting, by brute force (no symmetry reduction, no use of
atlas/cylinder/enumerate.py).

Reasoning for the boards used: with <= 4 pawns a ring (every file occupied) needs
n <= 4 files; a cylinder with an empty file has the value of the flat strip cut
there (checked here directly: value set of C5 vs F4); flat components have at most
4 files and at most 2 components fit in 4 pawns, so F5 realises every flat value of
F3..F8. Hence cyl-only = (C3 u C4 u C5) - (F3 u F4 u F5).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/cylatlas/C4-reproduce/indep_sets.py count 1
"""
import itertools
import json
import sys
import time

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

rule, ep = sys.argv[1], bool(int(sys.argv[2]))
pawns.RACE_RULE = rule
pawns._value.cache_clear()

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


def positions(n, maxp):
    sqs = [(f, r) for f in range(n) for r in range(2, 8)]
    for tot in range(2, maxp + 1):
        for w in range(1, tot):
            for W in itertools.combinations(sqs, w):
                rest = [s for s in sqs if s not in W]
                for B in itertools.combinations(rest, tot - w):
                    yield frozenset(W), frozenset(B)


out = {}
t0 = time.time()
for name, n, wrap in [("C3", 3, True), ("C4", 4, True), ("C5", 5, True),
                      ("F3", 3, False), ("F4", 4, False), ("F5", 5, False)]:
    board = Board(n, 8, wrap, ep)
    S = {}
    cnt = 0
    for W, B in positions(n, 4):
        pos = Pos(W, B)
        if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"):
            continue
        g = pawns.value(board, pos)
        k = key(g)
        cnt += 1
        if k not in S:
            S[k] = {"show": cgt.show(g), "big": big(g), "ex": str(pos)}
    out[name] = S
    print(f"{rule} ep{int(ep)} {name}: {cnt} positions, {len(S)} values ({time.time()-t0:.0f}s)",
          file=sys.stderr, flush=True)

cyl = set(out["C3"]) | set(out["C4"]) | set(out["C5"])
flat = set(out["F3"]) | set(out["F4"]) | set(out["F5"])
allv = {**out["F5"], **out["F4"], **out["F3"], **out["C5"], **out["C4"], **out["C3"]}
co = sorted(k for k in cyl - flat if not allv[k]["big"])
fo = sorted(k for k in flat - cyl if not allv[k]["big"])
res = {"rule": rule, "ep": int(ep),
       "counts": {k: len(v) for k, v in out.items()},
       "cut_lemma_C5_eq_F4": set(out["C5"]) == set(out["F4"]),
       "F3_sub_F5": set(out["F3"]) <= set(out["F5"]), "F4_sub_F5": set(out["F4"]) <= set(out["F5"]),
       "cyl_only_nonW": {k: allv[k] for k in co},
       "flat_only_nonW": {k: allv[k] for k in fo}}
json.dump(res, open(f"verify/cylatlas/C4-reproduce/indep_{rule}_ep{int(ep)}.json", "w"),
          ensure_ascii=False, indent=1)
print(f"{rule} ep{int(ep)}: cyl-only non-W {len(co)}, flat-only non-W {len(fo)}, "
      f"cut lemma {res['cut_lemma_C5_eq_F4']}, ({time.time()-t0:.0f}s)", flush=True)
