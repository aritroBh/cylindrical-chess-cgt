"""Independent re-derivation (verifier C4-theory) of the w+b<=4 cylinder-only value sets
under every race rule and e.p. setting, WITHOUT using the worker's enumerator or data.

Logic (cut lemma: an empty file stays empty, so it is a wall):
  * flat positions with <=4 pawns and no initial passer = one atom (every file occupied,
    width<=4) or a sum of two 2-pawn atoms (width<=2 each); 3 components would need >=6 pawns.
  * cylinder positions with an empty file = flat positions; so the only possible
    cylinder-only values come from rings: C3 with 3-4 pawns, C4 with 4 pawns.
All atoms are enumerated with no symmetry reduction (brute force).
Values come from cylcgt.pawns (same solver as the worker; not an independent solver).
All six settings run in ONE process so hash-consed canonical forms compare by identity.

Run:  cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/cylatlas/C4-theory/indep_sets.py
Adopted convention (e.p.-aware passed test, ep-aware-passed worktree):
      PYTHONPATH=<scratchpad>/ep-wt:. .venv/bin/python verify/cylatlas/C4-theory/indep_sets.py --epon-only
"""
import itertools
import json
import sys
import time

from cylcgt import cgt, pawns

RANKS = 8
PR = range(2, RANKS)


def bigladen(g):
    seen, st = set(), [g]
    while st:
        x = st.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        if x.num is not None and abs(x.num) >= pawns.BIG // 2:
            return True
        st.extend(x.L + x.R)
    return False


def atoms(k, wrap, pmin, pmax):
    """All positions on k files (flat or cylinder) with every file occupied,
    pmin..pmax pawns, both colours, no passed pawn. No symmetry reduction."""
    board = pawns.Board(k, RANKS, wrap, True)
    sqs = [(f, r) for f in range(k) for r in PR]
    out = []
    for p in range(pmin, pmax + 1):
        for S in itertools.combinations(sqs, p):
            if len({f for f, _ in S}) != k:
                continue
            for cols in itertools.product("WB", repeat=p):
                if "W" not in cols or "B" not in cols:
                    continue
                W = frozenset(s for s, c in zip(S, cols) if c == "W")
                B = frozenset(s for s, c in zip(S, cols) if c == "B")
                pos = pawns.Pos(W, B)
                if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"):
                    continue
                out.append(pos)
    return out


def main():
    t0 = time.time()
    flat_atoms = {k: atoms(k, False, 2, 4) for k in (1, 2, 3, 4)}
    two_pawn = [(k, p) for k in (1, 2) for p in flat_atoms[k] if len(p.white) + len(p.black) == 2]
    rings = {3: atoms(3, True, 3, 4), 4: atoms(4, True, 4, 4)}
    print("atoms:", {k: len(v) for k, v in flat_atoms.items()}, "2-pawn:", len(two_pawn),
          "rings:", {k: len(v) for k, v in rings.items()}, flush=True)
    print("cylcgt:", pawns.__file__, "PASSED_RESPECTS_EP =", getattr(pawns, "PASSED_RESPECTS_EP", "absent (textbook)"), flush=True)
    eps = (True,) if "--epon-only" in sys.argv else (True, False)
    settings = [(r, e) for e in eps for r in ("count", "mover", "opponent")]
    res = {}
    for rule, ep in settings:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        tag = f"{rule}/ep{'on' if ep else 'off'}"
        flat = set()
        for k, lst in flat_atoms.items():
            b = pawns.Board(k, RANKS, False, ep)
            for p in lst:
                flat.add(pawns.value(b, p))
        tv = []
        for k, p in two_pawn:
            tv.append(pawns.value(pawns.Board(k, RANKS, False, ep), p))
        tv = set(tv)
        for a in tv:
            for c in tv:
                flat.add(cgt.add(a, c))
        flat_nonW = {g for g in flat if not bigladen(g)}
        ringval = {}
        for n, lst in rings.items():
            b = pawns.Board(n, RANKS, True, ep)
            for p in lst:
                ringval[(n, str(p))] = pawns.value(b, p)
        cyl_only = {}
        for key, g in ringval.items():
            if g not in flat and not bigladen(g):
                if g not in cyl_only or key < cyl_only[g]:
                    cyl_only[g] = key
        res[tag] = dict(flat=flat, cyl_only=cyl_only, ringval=ringval)
        print(f"{tag}: flat non-W values {len(flat_nonW)}, cylinder-only non-W values {len(cyl_only)} "
              f"({time.time()-t0:.0f}s)", flush=True)
        for g, key in sorted(cyl_only.items(), key=lambda kv: cgt.show(kv[0])):
            print(f"    {cgt.show(g):45s} C{key[0]} {key[1]}")
    tags = list(res)
    epon = [t for t in tags if t.endswith("epon")]
    inter_on = set.intersection(*(set(res[t]["cyl_only"]) for t in epon))
    inter_all = set.intersection(*(set(res[t]["cyl_only"]) for t in tags))
    print("\nvalues cylinder-only under ALL three race rules with e.p. on:", len(inter_on))
    for g in inter_on:
        print("   ", cgt.show(g), [res[t]["cyl_only"][g] for t in epon])
    print("values cylinder-only under ALL six settings:", len(inter_all))
    for g in inter_all:
        print("   ", cgt.show(g))
    # position level
    print("\nring positions with the SAME non-W value under all three e.p.-on race rules, "
          "that value cylinder-only under each:")
    keys = res[epon[0]]["ringval"].keys()
    nrob = 0
    for key in sorted(keys):
        gs = [res[t]["ringval"][key] for t in epon]
        if gs[0] is gs[1] is gs[2] and gs[0] in inter_on:
            nrob += 1
            off = [cgt.show(res[t]["ringval"][key]) for t in tags if t.endswith("epoff")]
            print(f"   C{key[0]} {key[1]}: {cgt.show(gs[0])}   e.p.-off values: {off}")
    print("count:", nrob)
    print("\nring positions whose value is cylinder-only under EVERY one of the six settings "
          "(value may differ by setting):")
    nn = 0
    for key in sorted(keys):
        if all(res[t]["ringval"][key] in res[t]["cyl_only"] for t in tags):
            nn += 1
            print(f"   C{key[0]} {key[1]}: " + " | ".join(cgt.show(res[t]["ringval"][key]) for t in tags))
    print("count:", nn)
    print("\nring positions whose value is cylinder-only under every e.p.-on rule (value may differ):")
    nn = 0
    for key in sorted(keys):
        if all(res[t]["ringval"][key] in res[t]["cyl_only"] for t in epon):
            nn += 1
            print(f"   C{key[0]} {key[1]}: " + " | ".join(cgt.show(res[t]["ringval"][key]) for t in epon))
    print("count:", nn)
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
