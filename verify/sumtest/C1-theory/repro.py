"""Re-run the worker's C1 pipeline from scratch into verify/sumtest/C1-theory/data
(never touching sumtest/data), then recount the C1 numbers.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C1-theory/repro.py
"""
import gzip
import json
import os
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data")


def _patch():
    import sumtest.compare_cylcgt as cc
    import sumtest.enum_positions as ep
    ep.OUT = OUT
    cc.OUT = OUT
    return ep, cc


def task(t):
    ep, cc = _patch()
    if t[0] == "mine":
        return ep.run(*t[1:])
    return cc.run_cylcgt(t[1:])


def L(name):
    with gzip.open(os.path.join(OUT, name), "rt") as fh:
        return json.load(fh)


def main():
    os.makedirs(OUT, exist_ok=True)
    ep, cc = _patch()
    boards = list(ep.BOARDS)
    rules = ("count", "mover", "opponent")
    tasks = []
    for b in boards:
        for r in rules:
            for e in ("off", "plain", "aware", "plain-global"):
                for m in ("whole", "comp"):
                    if m == "comp" and e.endswith("global"):
                        continue
                    tasks.append(("mine", b, r, e, m))
            for e in (True, False):
                tasks.append(("cyl", b, r, e))
    with Pool(12) as p:
        for out in p.imap_unordered(task, tasks):
            pass
    tot = {}
    for b in boards:
        for r in rules:
            for epflag in (True, False):
                cy = L(f"cylcgt__{b}__{r}__{'ep' if epflag else 'noep'}.json.gz")["outcomes"]
                assert not any(v.startswith("ERR") for v in cy.values())
                vars_ = ["plain__whole", "plain__comp", "plain-global__whole", "aware__whole", "aware__comp"] if epflag \
                    else ["off__whole", "off__comp"]
                for var in vars_:
                    e, m = var.split("__")
                    mine = L(f"mine__{b}__{r}__{e}__{m}.json.gz")["outcomes"]
                    assert set(mine) == set(cy)
                    cases = len(mine)
                    dcases = sum(mine[k] != cy[k] for k in mine)
                    pairs = sum(len(mine[k]) for k in mine)
                    dpairs = sum(sum(x != y for x, y in zip(mine[k], cy[k])) for k in mine)
                    a = tot.setdefault(var, [0, 0, 0, 0])
                    a[0] += cases; a[1] += dcases; a[2] += pairs; a[3] += dpairs
    for var, (c, dc, p, dp) in tot.items():
        print(f"{var:22s} cases {c:7d} differing {dc:6d}   pairs {p:8d} differing {dp:7d}")
    pos = sum(len(ep.positions(*ep.BOARDS[b])[1]) for b in boards)
    print("family positions:", pos, " x3 rules x2 ep x15 =", pos * 3 * 2 * 15)


if __name__ == "__main__":
    main()
