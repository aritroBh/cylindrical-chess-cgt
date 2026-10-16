"""Compare verifier solver (v__), fresh cylcgt (c__), worker solver (mine__) and worker cylcgt (cylcgt__).

  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/sumtest/C1-refute/vcompare.py
Reads the worker's data files read-only.
"""
import gzip
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
WD = os.path.join(HERE, "..", "..", "..", "sumtest", "data")
BOARDS = ["flat3", "flat4", "cyl3", "cyl4", "cyl5"]
RULES = ["count", "mover", "opponent"]


def load(p):
    with gzip.open(p, "rt") as fh:
        return json.load(fh)


def cmp(a, b):
    ka, kb = set(a), set(b)
    diff = [k for k in ka & kb if a[k] != b[k]]
    pairs = sum(sum(x != y for x, y in zip(a[k], b[k])) for k in diff)
    return len(ka), len(kb), len(ka ^ kb), len(diff), pairs, diff


def main():
    tot = Counter()
    have_c = all(os.path.exists(os.path.join(OUT, f"c__{b}__{r}__{e}.json.gz"))
                 for b in BOARDS for r in RULES for e in ("ep", "noep"))
    print("| board | rule | ep | comparison | n_a | n_b | key-set sym.diff | positions differing | pairs differing |")
    print("|---|---|---|---|---|---|---|---|---|")
    for b in BOARDS:
        for r in RULES:
            for ep in (False, True):
                e = "ep" if ep else "noep"
                comps = []
                vP = load(os.path.join(OUT, f"v__{b}__{r}__{e}__P.json.gz"))["outcomes"]
                vG = load(os.path.join(OUT, f"v__{b}__{r}__ep__global.json.gz"))["outcomes"] if ep else None
                wcy = load(os.path.join(WD, f"cylcgt__{b}__{r}__{e}.json.gz"))["outcomes"]
                if ep:
                    wm = {v: load(os.path.join(WD, f"mine__{b}__{r}__{v}.json.gz"))["outcomes"]
                          for v in ("plain__whole", "plain__comp", "plain-global__whole", "aware__whole")}
                else:
                    wm = {v: load(os.path.join(WD, f"mine__{b}__{r}__{v}.json.gz"))["outcomes"]
                          for v in ("off__whole", "off__comp")}
                if have_c:
                    c = load(os.path.join(OUT, f"c__{b}__{r}__{e}.json.gz"))
                    assert c["meta"]["errors"] == 0
                    comps.append(("verifier(P-scope) vs fresh cylcgt", vP, c["outcomes"]))
                    if ep:
                        comps.append(("verifier(global) vs fresh cylcgt", vG, c["outcomes"]))
                    comps.append(("fresh cylcgt vs worker cylcgt file", c["outcomes"], wcy))
                comps.append(("verifier(P-scope) vs worker cylcgt file", vP, wcy))
                for v, m in wm.items():
                    comps.append((f"verifier(P-scope) vs worker {v}", vP, m))
                    comps.append((f"worker {v} vs worker cylcgt file", m, wcy))
                for name, x, y in comps:
                    na, nb, sd, nd, pairs, diff = cmp(x, y)
                    tot[(name, ep)] += pairs
                    tot[(name, ep, "pos")] += nd
                    tot[(name, ep, "n")] += na * 15
                    tot[(name, ep, "sd")] += sd
                    if nd or sd or name.startswith("verifier(P-scope) vs fresh"):
                        print(f"| {b} | {r} | {e} | {name} | {na} | {nb} | {sd} | {nd} | {pairs} |")
    print()
    print("Totals (pairs = (position, X) outcome predictions):")
    names = sorted({k[0] for k in tot})
    for n in names:
        for ep in (False, True):
            if (n, ep, "n") in tot:
                print(f"  {n:45s} ep={'on ' if ep else 'off'}: compared {tot[(n, ep, 'n')]:>9d} pairs, "
                      f"differing pairs {tot[(n, ep)]}, differing positions {tot[(n, ep, 'pos')]}, "
                      f"key mismatches {tot[(n, ep, 'sd')]}")


if __name__ == "__main__":
    main()
