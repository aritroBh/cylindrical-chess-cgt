"""Compare verifier-v2 brute force vs fresh cylcgt, and both vs the worker's stored files.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/sumtest/C1-refute/v2/compare.py
"""
import gzip
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
WDATA = os.path.abspath(os.path.join(HERE, "../../../../sumtest/data"))
BOARDS = ["flat3", "flat4", "cyl3", "cyl4", "cyl5"]
RULES = ["count", "mover", "opponent"]
REF = ["0", "*", "*2", "*3", "up", "down", "up*", "dup*", "1/2", "-1/2", "1", "-1", "{1|0}", "+-1", "tiny1"]


def load(p):
    with gzip.open(p, "rt") as fh:
        return json.load(fh)


def cmp(a, b):
    ka, kb = set(a), set(b)
    common = ka & kb
    dpos = [k for k in common if a[k] != b[k]]
    dpairs = sum(sum(x != y for x, y in zip(a[k], b[k])) for k in dpos)
    npairs = sum(len(a[k]) for k in common)
    return len(common), npairs, len(dpos), dpairs, len(ka ^ kb), dpos


def main():
    tot = Counter()
    rows = []
    examples = {}
    errs = 0
    for b in BOARDS:
        for r in RULES:
            for ep in (False, True):
                e = "ep" if ep else "noep"
                cy = load(os.path.join(OUT, f"cy__{b}__{r}__{e}.json.gz"))
                errs += cy["meta"]["errors"]
                assert cy["meta"]["x_outcomes"] == "PNNNLRNLLRLRNNL", cy["meta"]
                cyo = cy["outcomes"]
                assert all(len(v) == 15 and set(v) <= set("LRNP") for v in cyo.values())
                pairs = [("bf-pcomp", load(os.path.join(OUT, f"bf__{b}__{r}__{e}__pcomp.json.gz"))["outcomes"])]
                if ep:
                    for sc in ("G", "global"):
                        pairs.append((f"bf-{sc}", load(os.path.join(OUT, f"bf__{b}__{r}__{e}__{sc}.json.gz"))["outcomes"]))
                wc = os.path.join(WDATA, f"cylcgt__{b}__{r}__{e}.json.gz")
                if os.path.exists(wc):
                    pairs.append(("worker-cylcgt-file", load(wc)["outcomes"]))
                wm = os.path.join(WDATA, f"mine__{b}__{r}__{'plain' if ep else 'off'}__whole.json.gz")
                if os.path.exists(wm):
                    pairs.append(("worker-mine-" + ("plain" if ep else "off") + "-whole", load(wm)["outcomes"]))
                for name, other in pairs:
                    n, npairs, dp, dpp, km, dpos = cmp(cyo, other)
                    rows.append((b, r, e, name, n, npairs, dp, dpp, km))
                    tot[(name, e, "pos")] += n
                    tot[(name, e, "pairs")] += npairs
                    tot[(name, e, "dpos")] += dp
                    tot[(name, e, "dpairs")] += dpp
                    tot[(name, e, "keymismatch")] += km
                    if dpos and (name, e) not in examples:
                        k = sorted(dpos)[0]
                        examples[(name, e)] = (b, r, k, cyo[k], other[k], cy["info"].get(k))
    print("| board | rule | ep | vs fresh cylcgt | positions | pairs | pos differing | pairs differing | key mismatches |")
    print("|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        print("| " + " | ".join(map(str, row)) + " |")
    print("\ncylcgt errors:", errs)
    print("\nTOTALS (vs fresh cylcgt):")
    names = sorted({k[0] for k in tot})
    for name in names:
        for e in ("noep", "ep"):
            if tot[(name, e, "pairs")]:
                print(f"  {name:28s} {e:5s} positions {tot[(name, e, 'pos')]:6d} pairs {tot[(name, e, 'pairs')]:8d} "
                      f"differing pos {tot[(name, e, 'dpos')]} differing pairs {tot[(name, e, 'dpairs')]} "
                      f"key mismatches {tot[(name, e, 'keymismatch')]}")
    for k, v in examples.items():
        print("example", k, v)


if __name__ == "__main__":
    main()
