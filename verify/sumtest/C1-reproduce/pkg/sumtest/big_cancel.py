"""Extra experiment: positions where +BIG and -BIG can live in different components.

Family: 5-file flat board, one White and one Black pawn on files a-b, one White and one
Black pawn on files d-e, file c empty, pawns on ranks 2-7, no initial passer.  These are
outside the 2(b) families (which can never hold two passer-capable components).

Compares, for every position and every reference X:
  whole : brute force, first passed pawn anywhere ends the sum (literal spec / chess);
  comp  : brute force, component values add as integers (+BIG and -BIG cancel);
  cylcgt: cgt.outcome(cgt.add(pawns.value(...), X)), plus pawns.sum_safe().

  PYTHONPATH=. .venv/bin/python -m sumtest.big_cancel
"""
import itertools
from collections import Counter

from cylcgt import cgt, pawns

from sumtest.compare_cylcgt import ref_games
from sumtest.sumsolver import REF_NAMES, Geometry, Rules, SumSolver, Trees, reference_set


def family(geo, rules):
    left = [geo.sq(f, r) for f in (0, 1) for r in range(2, 8)]
    right = [geo.sq(f, r) for f in (3, 4) for r in range(2, 8)]
    out = []
    for w1, b1 in itertools.permutations(left, 2):
        for w2, b2 in itertools.permutations(right, 2):
            W = (1 << w1) | (1 << w2)
            B = (1 << b1) | (1 << b2)
            if not rules.has_initial_passer(W, B):
                out.append((W, B))
    return out


def main():
    R = ref_games()
    for ep in (False, True):
        for rule in ("count",):
            geo = Geometry(5, False)
            T = Trees()
            ref = reference_set(T)
            sw = SumSolver(Rules(geo, ep=ep, ep_aware=False, race_rule=rule), T, mode="whole")
            sc = SumSolver(Rules(geo, ep=ep, ep_aware=False, race_rule=rule), T, mode="comp")
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            board = pawns.Board(5, 8, False, ep)
            pos = family(geo, sw.rules)
            stats = Counter()
            examples = []
            for W, B in pos:
                text = geo.show(W, B)
                a = sw.solve(sw.start_state(W, B))
                b = sc.solve(sc.start_state(W, B))
                vw = "".join(sw.outcome(*a, ref[n]) for n in REF_NAMES)
                vc = "".join(sc.outcome(*b, ref[n]) for n in REF_NAMES)
                p = pawns.Pos.parse(text)
                v = pawns.value(board, p)
                vy = "".join(cgt.outcome(cgt.add(v, R[n])) for n in REF_NAMES)
                safe = bool(pawns.sum_safe(board, p))
                stats[("comp==cylcgt", vc == vy)] += 1
                stats[("whole==cylcgt", vw == vy, "safe" if safe else "unsafe")] += 1
                if vw != vy and len(examples) < 3:
                    examples.append((text, safe, cgt.show(v), vw, vy))
            print(f"ep={'on' if ep else 'off'} rule={rule}: {len(pos)} positions (plain passer test)")
            for k in sorted(stats, key=str):
                print("   ", k, stats[k])
            for e in examples:
                print("    example", e)


if __name__ == "__main__":
    main()
