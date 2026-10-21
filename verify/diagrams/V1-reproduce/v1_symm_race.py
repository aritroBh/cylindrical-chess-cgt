"""V1 verifier (REPRODUCE lens), extra checks on the solver path behind claim V1.

A. Exact identity checks: each V1 value is compared (canonical-form identity, not
   string match) with the CGT game the claim names.  The exact numbers hidden behind
   "+W" in the display are printed.
B. Symmetry checks (bug detectors): file rotation f -> f+k (mod 8) and file reflection
   f -> 7-f must leave the value unchanged on the cylinder; colour reversal
   (swap colours, rank r -> 9-r) must negate it.  Count rule, e.p. on and off.
C. Extremal race resolution: every race node won by White ("allW") or by Black ("allB").
   By monotonicity of game values in leaf values, an outcome class that survives both
   extremes holds for EVERY resolution of the races (the three uniform rules
   count/mover/opponent do not by themselves imply that).
D. Race "nodes" in race_hits are counted per (parent, child) edge; distinct positions
   are counted here too.

Monkeypatches pawns._child at runtime only; no project file is edited.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/V1-reproduce/v1_symm_race.py
"""
import sys
from dataclasses import replace

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

sys.setrecursionlimit(1000000)
CYL = Board(8, 8, True, True)
NOEP = replace(CYL, ep=False)
ORIG_CHILD = pawns._child

P = {
    "2.1": "W: e4 / B: e5",
    "2.2": "W: a2 h1 / B: a3 h4",
    "3.1": "W: a3 h1 / B: a4 h5",
    "3.2": "W: a4 h1 / B: a5 h6",
    "4.1": "W: e4 / B: e6",
    "4.2": "W: e3 / B: e6",
    "4.3": "W: a4 h2 h4 / B: a5 a6 a7 h3",
    "7.1c": "W: c2 c3 / B: c5 c6",
    "7.1f": "W: f3 f4 / B: f7",
    "7.1ah": "W: a4 a5 h2 h3 / B: a7 h6",
    "7.2abh": "W: a2 b2 h3 / B: a6 b7 h7",
    "7.3": "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4",
    "7.3cd": "W: c1 c3 d3 / B: c2 d4 d5 d6",
}

Z, S, I = cgt.integer(0), cgt.nimber(1), cgt.integer
EXPECT = {  # (ep on, ep off); None = no exact target named in the claim
    "2.1": (Z, Z), "2.2": (Z, Z), "3.1": (I(1), I(2)), "3.2": (I(2), I(2)),
    "4.1": (S, S), "4.2": (Z, Z),
    "4.3": (cgt.make([Z], [cgt.make([Z], [I(-1)])]),) * 2,
    "7.1c": (cgt.make([I(1)], [I(-1)]),) * 2,
    "7.1f": (cgt.make([cgt.make([I(2)], [I(1)])], [Z]),) * 2,
    "7.3": (I(256), I(256)),
    "7.3cd": (cgt.make([Z], [cgt.make([Z], [I(-1)])]),) * 2,
}


def val(board, pos, rule="count"):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    pawns.race_hits.clear()
    return pawns.value(board, pos)


def tf(pos, fmap):
    return Pos(frozenset((fmap(f), r) for f, r in pos.white),
               frozenset((fmap(f), r) for f, r in pos.black))


def colour_rev(pos):
    return Pos(frozenset((f, 9 - r) for f, r in pos.black),
               frozenset((f, 9 - r) for f, r in pos.white))


def nums(g, acc, seen):
    if g.id in seen:
        return
    seen.add(g.id)
    if g.num is not None:
        if abs(g.num) >= 128:
            acc.add(g.num)
        return
    for x in g.L + g.R:
        nums(x, acc, seen)


def child_extreme(winner):
    def f(board, pos, mover):
        if pawns.passed(board, pos, "W") and pawns.passed(board, pos, "B"):
            pawns.race_hits.append(f"{pos} after {mover}")
            return cgt.integer(pawns.BIG if winner == "W" else -pawns.BIG)
        return pawns.value(board, pos)
    return f


def main():
    print("=== A. exact identity with the claimed values ===")
    for k, t in P.items():
        pos = Pos.parse(t)
        for i, b in enumerate((CYL, NOEP)):
            g = val(b, pos)
            nh = len(pawns.race_hits)
            nd = len(set(h.split(" after ")[0] for h in pawns.race_hits))
            big = set()
            nums(g, big, set())
            exp = EXPECT.get(k)
            ok = "n/a" if exp is None else ("IDENTICAL" if g is exp[i] else "DIFFERENT")
            print(f"{k:7s} ep={'on ' if b.ep else 'off'} {cgt.show(g)[:60]:60s} outcome {cgt.outcome(g)}"
                  f"  vs claim: {ok}  race edges {nh} distinct race positions {nd}"
                  f"  |numbers|>=128 in tree: {sorted(big)}")

    print("\n=== B. symmetry checks (count rule) ===")
    bad = 0
    for k, t in P.items():
        pos = Pos.parse(t)
        for b in (CYL, NOEP):
            g = val(b, pos)
            res = []
            for kk in range(1, 8):
                h = val(b, tf(pos, lambda f, kk=kk: (f + kk) % 8))
                res.append(h is g)
            refl = val(b, tf(pos, lambda f: 7 - f)) is g
            cr = val(b, colour_rev(pos)) is cgt.neg(g)
            ok = all(res) and refl and cr
            bad += not ok
            print(f"{k:7s} ep={'on ' if b.ep else 'off'} rotations all equal: {all(res)}  reflection equal: {refl}"
                  f"  colour-reversal = -G: {cr}")
    print(f"symmetry failures: {bad}")

    print("\n=== C. outcome under extremal race resolution (all races won by W / by B) ===")
    for k, t in P.items():
        pos = Pos.parse(t)
        for b in (CYL, NOEP):
            row = {}
            for rule in ("count", "mover", "opponent"):
                row[rule] = cgt.outcome(val(b, pos, rule))
            for w in ("W", "B"):
                pawns._child = child_extreme(w)
                try:
                    row["all" + w] = cgt.outcome(val(b, pos))
                    nh = len(pawns.race_hits)
                finally:
                    pawns._child = ORIG_CHILD
                    pawns._value.cache_clear()
            robust = len(set(row.values())) == 1
            print(f"{k:7s} ep={'on ' if b.ep else 'off'} {row}  race edges {nh}  "
                  f"{'outcome race-independent' if robust else 'OUTCOME DEPENDS ON RACES'}")
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()


if __name__ == "__main__":
    main()
