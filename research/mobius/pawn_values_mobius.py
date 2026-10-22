#!/usr/bin/env python3
"""T35 part B: pawn-only CGT values on narrow Mobius boards, with the seam rule of RULES.md.

For every position of the T9 enumeration (WIDTH files x 8 ranks, 1..MAXP pawns, White and Black,
each position once) this computes:
  * value on the Mobius strip   (research/mobius/mob_pawns.py, the corrected fork),
  * value on the cylinder       (cylcgt.pawns, exactly as T9 used it),
  * value on the flat board     (cylcgt.pawns, exactly as T9 used it).
It also checks the fork against cylcgt on the cylinder and flat boards (AGREE counts).

Positions where a board raises RaceError (both sides have a passed pawn) are excluded from that
board's set; the exclusions are counted and reported.

usage: PYTHONPATH=. .venv/bin/python research/mobius/pawn_values_mobius.py WIDTH MAXP OUTPREFIX
"""
import json
import sys
import time
from itertools import combinations

from cylcgt import pawns as cyl
from cylcgt import cgt
from research.mobius import mob_pawns as mp


def enum_positions(width, maxp):
    sq = [(f, r) for f in range(width) for r in range(1, 9)]
    for total in range(1, maxp + 1):
        for wc in range(total + 1):
            for wsq in combinations(sq, wc):
                rem = [s for s in sq if s not in wsq]
                for bsq in combinations(rem, total - wc):
                    yield wsq, bsq


def show_or_none(fn):
    try:
        return cgt.show(fn())
    except (mp.RaceError, cyl.RaceError):
        return None


def main():
    width, maxp, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    mob = mp.Board(width, "mob")
    cylb = cyl.Board(width, 8, True, True)
    flatb = cyl.Board(width, 8, False, True)
    vals = {"mob": set(), "cyl": set(), "flat": set()}
    witness = {"mob": {}, "cyl": {}, "flat": {}}
    excl = {"mob": 0, "cyl": 0, "flat": 0}
    common = {"mob": set(), "cyl": set(), "flat": set()}  # positions where all three boards are defined
    common_n = 0
    common_witness = {}
    n = 0
    agree = {"cyl": [0, 0], "flat": [0, 0]}  # [checked, mismatched] fork vs cylcgt
    t0 = time.time()
    for wsq, bsq in enum_positions(width, maxp):
        n += 1
        if n % 20000 == 0:
            for fn in (mp._value, cyl._value):
                fn.cache_clear()
            print("  %d positions, %.0fs, mob %d cyl %d flat %d" % (
                n, time.time() - t0, len(vals["mob"]), len(vals["cyl"]), len(vals["flat"])), flush=True)
        mpos = mp.Pos(frozenset((f, r, 1) for f, r in wsq), frozenset((f, r, -1) for f, r in bsq))
        cpos = cyl.Pos(frozenset(wsq), frozenset(bsq))
        results = {}
        results["mob"] = show_or_none(lambda: mp.value(mob, mpos))
        results["cyl"] = show_or_none(lambda: cyl.value(cylb, cpos))
        results["flat"] = show_or_none(lambda: cyl.value(flatb, cpos))
        if n % (1 if width == 3 else 7) == 0:
            fork_cyl = show_or_none(lambda: mp.value(mp.Board(width, "cyl"), mpos))
            fork_flat = show_or_none(lambda: mp.value(mp.Board(width, "flat"), mpos))
            agree["cyl"][0] += 1
            agree["flat"][0] += 1
            agree["cyl"][1] += fork_cyl != results["cyl"]
            agree["flat"][1] += fork_flat != results["flat"]
        pos_text = str(mpos)
        if all(results[k] is not None for k in ("mob", "cyl", "flat")):
            common_n += 1
            for k in ("mob", "cyl", "flat"):
                common[k].add(results[k])
            if results["mob"] not in common_witness:
                common_witness[results["mob"]] = pos_text
        for k in ("mob", "cyl", "flat"):
            v = results[k]
            if v is None:
                excl[k] += 1
                continue
            if v not in vals[k]:
                vals[k].add(v)
                witness[k][v] = pos_text
    unique = vals["mob"] - (vals["cyl"] | vals["flat"])
    unique_common = common["mob"] - (common["cyl"] | common["flat"])
    summary = {
        "width": width, "max_pawns": maxp, "positions": n, "seconds": round(time.time() - t0, 1),
        "distinct_values": {k: len(vals[k]) for k in vals},
        "excluded_race_positions": excl,
        "unique_to_mobius_not_on_cyl_or_flat": len(unique),
        "mobius_not_on_cyl_only": len(vals["mob"] - vals["cyl"]),
        "mobius_not_on_flat_only": len(vals["mob"] - vals["flat"]),
        "fork_vs_cylcgt_checked_and_mismatched": agree,
        "unique_examples": sorted(unique, key=len)[:30],
        "common_domain_positions": common_n,
        "common_domain_distinct": {k: len(common[k]) for k in common},
        "common_domain_unique_to_mobius": len(unique_common),
    }
    print(json.dumps(summary, indent=1))
    with open(out + "_summary.json", "w") as fh:
        json.dump(summary, fh, indent=1)
    with open(out + "_common_unique.tsv", "w") as fh:
        fh.write("value\tmobius_witness_position\n")
        for v in sorted(unique_common, key=lambda s: (len(s), s)):
            fh.write("%s\t%s\n" % (v, common_witness[v]))
    with open(out + "_unique.tsv", "w") as fh:
        fh.write("value\tmobius_witness_position\n")
        for v in sorted(unique, key=lambda s: (len(s), s)):
            fh.write("%s\t%s\n" % (v, witness["mob"][v]))
    print("wrote", out + "_summary.json", out + "_unique.tsv")


if __name__ == "__main__":
    main()
