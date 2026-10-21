"""Verifier checks for sumtest claim C1 (my own comparison code; reads data only).

  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
    .venv/bin/python verify/sumtest/C1-reproduce/rerun2/vcheck.py

1. fresh (rerun2/data) vs worker cache (sumtest/data): identical outcome dicts?
2. key sets, ERR entries, totals.
3. my own agreement count (mine vs cylcgt) for off/plain variants.
4. non-degeneracy: distinct vectors, fraction of constant vectors.
5. discrimination: cross-rule and cross-e.p. comparisons must show differences.
"""
import gzip
import json
import os
from collections import Counter

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
FRESH = os.path.join(ROOT, "verify/sumtest/C1-reproduce/rerun2/data")
CACHE = os.path.join(ROOT, "sumtest/data")
BOARDS = ["flat3", "flat4", "cyl3", "cyl4", "cyl5"]
RULES = ["count", "mover", "opponent"]


def load(d, name):
    with gzip.open(os.path.join(d, name), "rt") as fh:
        return json.load(fh)


def main():
    # 1. fresh vs cache
    names = sorted(f for f in os.listdir(FRESH) if f.endswith(".json.gz"))
    cnames = sorted(f for f in os.listdir(CACHE) if f.endswith(".json.gz"))
    print("files fresh", len(names), "cache", len(cnames), "same names", names == cnames)
    neq = 0
    for n in names:
        a, b = load(FRESH, n)["outcomes"], load(CACHE, n)["outcomes"]
        if a != b:
            neq += 1
            print("  DIFFERS:", n)
    print("fresh-vs-cache outcome dicts differing:", neq)

    # 2/3. own agreement count
    tot_pred = {"off": 0, "plain": 0}
    tot_diff = {"off": 0, "plain": 0}
    npos_total = 0
    errs = 0
    for board in BOARDS:
        for rule in RULES:
            for ep, epv in ((False, "off"), (True, "plain")):
                cy = load(FRESH, f"cylcgt__{board}__{rule}__{'ep' if ep else 'noep'}.json.gz")["outcomes"]
                errs += sum(1 for v in cy.values() if not (len(v) == 15 and set(v) <= set("LRNP")))
                for mode in ("whole", "comp"):
                    mine = load(FRESH, f"mine__{board}__{rule}__{epv}__{mode}.json.gz")["outcomes"]
                    assert set(mine) == set(cy), (board, rule, epv, mode)
                    d = sum(1 for k in mine for x, y in zip(mine[k], cy[k]) if x != y)
                    if mode == "whole":
                        tot_pred[epv] += 15 * len(mine)
                        tot_diff[epv] += d
                    elif d:
                        print("  comp-mode differs", board, rule, epv, d)
            if rule == "count":
                npos_total += len(cy)
    print("positions per (rule, ep):", npos_total, " malformed cylcgt vectors:", errs)
    print("predictions & differing pairs (whole mode):", tot_pred, tot_diff,
          " total predictions", sum(tot_pred.values()))

    # 4. non-degeneracy
    allv = Counter()
    const = 0
    n = 0
    for board in BOARDS:
        for rule in RULES:
            for ep in ("ep", "noep"):
                cy = load(FRESH, f"cylcgt__{board}__{rule}__{ep}.json.gz")["outcomes"]
                for v in cy.values():
                    allv[v] += 1
                    n += 1
                    const += len(set(v)) == 1
    print(f"distinct outcome vectors over all {n} (position,rule,ep) cases: {len(allv)}; "
          f"constant vectors (G dominates every X): {const} ({100*const/n:.1f}%)")
    print("  most common:", allv.most_common(6))

    # 5. discrimination
    print("discrimination (differing (position,X) pairs; should be > 0):")
    for board in BOARDS:
        row = []
        cy = {(r, e): load(FRESH, f"cylcgt__{board}__{r}__{e}.json.gz")["outcomes"] for r in RULES for e in ("ep", "noep")}
        mine = {(r, v): load(FRESH, f"mine__{board}__{r}__{v}__whole.json.gz")["outcomes"] for r in RULES for v in ("off", "plain")}

        def dpairs(a, b):
            return sum(1 for k in a for x, y in zip(a[k], b[k]) if x != y)
        for ra in RULES:
            for rb in RULES:
                if ra != rb:
                    row.append(f"mine[{ra},noep]~cy[{rb},noep]={dpairs(mine[(ra,'off')], cy[(rb,'noep')])}")
        for r in RULES:
            row.append(f"mine[{r},off]~cy[{r},ep]={dpairs(mine[(r,'off')], cy[(r,'ep')])}")
            row.append(f"mine[{r},plain]~cy[{r},noep]={dpairs(mine[(r,'plain')], cy[(r,'noep')])}")
        print(" ", board, "; ".join(row))
    # e.p. sensitivity of cylcgt itself (positions whose vector changes when e.p. turned on)
    tot = 0
    for board in BOARDS:
        for r in RULES:
            a = load(FRESH, f"cylcgt__{board}__{r}__ep.json.gz")["outcomes"]
            b = load(FRESH, f"cylcgt__{board}__{r}__noep.json.gz")["outcomes"]
            tot += sum(1 for k in a if a[k] != b[k])
    print("cylcgt (position,rule) cases whose vector changes with e.p. on (textbook):", tot)


if __name__ == "__main__":
    main()
