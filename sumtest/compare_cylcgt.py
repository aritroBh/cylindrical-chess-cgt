"""Part 2(b): compare the brute-force outcome vectors with cylcgt's predictions.

For every position of enum_positions.positions() and every reference game X,
cylcgt predicts  outcome(G + X) = cgt.outcome(cgt.add(pawns.value(board, pos), X)).

  PYTHONPATH=. .venv/bin/python -m sumtest.compare_cylcgt --jobs 12
writes sumtest/data/cylcgt__<board>__<rule>__<ep>.json.gz and prints a summary.
"""
import argparse
import gzip
import json
import os
import time
from collections import Counter, defaultdict
from fractions import Fraction
from multiprocessing import Pool

from sumtest.enum_positions import BOARDS, OUT, positions
from sumtest.sumsolver import REF_NAMES


def ref_games():
    from cylcgt import cgt
    one, mone = cgt.integer(1), cgt.integer(-1)
    return {
        "0": cgt.ZERO, "*": cgt.STAR, "*2": cgt.nimber(2), "*3": cgt.nimber(3),
        "up": cgt.UP, "down": cgt.DOWN, "up*": cgt.add(cgt.UP, cgt.STAR),
        "dup*": cgt.add(cgt.add(cgt.UP, cgt.UP), cgt.STAR),
        "1/2": cgt.number(Fraction(1, 2)), "-1/2": cgt.number(Fraction(-1, 2)),
        "1": one, "-1": mone, "{1|0}": cgt.make([one], [cgt.ZERO]),
        "+-1": cgt.make([one], [mone]),
        "tiny1": cgt.make([cgt.ZERO], [cgt.make([cgt.ZERO], [mone])]),
    }


def cyl_path(board, rule, ep):
    return os.path.join(OUT, f"cylcgt__{board}__{rule}__{'ep' if ep else 'noep'}.json.gz")


def run_cylcgt(args):
    board, rule, ep = args
    path = cyl_path(board, rule, ep)
    if os.path.exists(path):
        return path, None
    from cylcgt import cgt, pawns
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    del pawns.race_hits[:]
    files, wrap = BOARDS[board]
    geo, pos = positions(files, wrap)
    b = pawns.Board(files, 8, wrap, ep)
    R = ref_games()
    t0 = time.time()
    res, info = {}, {}
    for W, B in pos:
        text = geo.show(W, B)
        p = pawns.Pos.parse(text)
        try:
            v = pawns.value(b, p)
        except Exception as e:                          # noqa: BLE001
            res[text] = "ERR:" + type(e).__name__
            continue
        res[text] = "".join(cgt.outcome(cgt.add(v, R[n])) for n in REF_NAMES)
        comps = pawns.components(b, p)
        info[text] = {"value": cgt.show(v), "safe": bool(pawns.sum_safe(b, p)), "ncomp": len(comps)}
    meta = {"board": board, "rule": rule, "ep": ep, "positions": len(pos), "race_hits": len(pawns.race_hits),
            "seconds": round(time.time() - t0, 1)}
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt") as fh:
        json.dump({"meta": meta, "outcomes": res, "info": info}, fh)
    os.replace(tmp, path)
    return path, meta


def load(path):
    with gzip.open(path, "rt") as fh:
        return json.load(fh)


def npawns(text):
    return len(text.replace("W:", "").replace("B:", "").replace("/", " ").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--show", type=int, default=3, help="minimal repros to print per class")
    a = ap.parse_args()
    tasks = [(b, r, ep) for b in BOARDS for r in ("count", "mover", "opponent") for ep in (True, False)]
    with Pool(a.jobs) as p:
        for out in p.imap_unordered(run_cylcgt, tasks):
            if out[1]:
                print("computed", out[0], out[1], flush=True)

    # sanity: cylcgt's own outcome for each X equals the textbook class
    from cylcgt import cgt
    R = ref_games()
    print("cylcgt outcome of each reference game:", " ".join(f"{n}:{cgt.outcome(R[n])}" for n in REF_NAMES))

    variants = {True: ["plain__whole", "plain__comp", "aware__whole", "aware__comp",
                       "plain-global__whole", "aware-global__whole"],
                False: ["off__whole", "off__comp"]}
    print()
    print("| board | rule | e.p. | my variant | positions | vectors equal | positions differing | of which sum_safe | (position,X) pairs differing |")
    print("|---|---|---|---|---|---|---|---|---|")
    summary = []
    for board in BOARDS:
        for rule in ("count", "mover", "opponent"):
            for ep in (True, False):
                cy = load(cyl_path(board, rule, ep))
                for var in variants[ep]:
                    epv, mode = var.split("__")
                    mine = load(os.path.join(OUT, f"mine__{board}__{rule}__{epv}__{mode}.json.gz"))["outcomes"]
                    diff = [k for k in mine if mine[k] != cy["outcomes"][k]]
                    pairs = sum(sum(1 for x, y in zip(mine[k], cy["outcomes"][k]) if x != y) for k in diff)
                    safe = sum(1 for k in diff if cy["info"].get(k, {}).get("safe"))
                    print(f"| {board} | {rule} | {'on' if ep else 'off'} | {var} | {len(mine)} | "
                          f"{len(mine) - len(diff)} | {len(diff)} | {safe} | {pairs} |")
                    summary.append((board, rule, ep, var, diff, cy, mine))
    print()
    # minimal repros for the variants we consider primary
    for board, rule, ep, var, diff, cy, mine in summary:
        if var not in ("aware__whole", "aware__comp", "plain__comp", "plain__whole", "off__whole", "off__comp"):
            continue
        if not diff:
            continue
        diff.sort(key=lambda k: (npawns(k), k))
        print(f"## {board} {rule} ep={'on' if ep else 'off'} variant={var}: {len(diff)} positions differ")
        by_n = Counter(npawns(k) for k in diff)
        by_safe = Counter(cy["info"][k]["safe"] for k in diff)
        by_comp = Counter(cy["info"][k]["ncomp"] for k in diff)
        print(f"   by pawn count {dict(by_n)}; by sum_safe {dict(by_safe)}; by #components {dict(by_comp)}")
        for k in diff[: a.show]:
            cols = [n for n, x, y in zip(REF_NAMES, mine[k], cy["outcomes"][k]) if x != y]
            print(f"   {k:28s} cylcgt value {cy['info'][k]['value']:30s} safe={cy['info'][k]['safe']} "
                  f"ncomp={cy['info'][k]['ncomp']}  differs at {cols}")
            print(f"      mine  : {mine[k]}\n      cylcgt: {cy['outcomes'][k]}")


if __name__ == "__main__":
    main()
