#!/usr/bin/env python3
"""Analyse the E2 ablation runs written by run_ablation.py.

Run from the project root:
    .venv/bin/python engine/ablation/analyze.py

Prints:
  0. a consistency check: iteration k of the depth-16 baseline search against the earlier
     independent `go depth k` runs of the vendor binary (engine/runs/sf19_depth.json);
  1. which variants are bit-identical to the baseline (same score, nodes and PV head at every
     iteration of every position);
  2. per variant: positions solved, root evaluations that match the tablebase, mean solution
     depth and the geometric-mean nodes-to-solve ratio against the baseline;
  3. the same split by CGT value class, for the baseline and the variants that differ.
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VARIANTS = ["base", "NMP", "SHALLOW", "RFP", "RAZOR", "SE", "PROBCUT", "LMR", "CORR", "IIR"]
DEPTHS = [1, 2, 3, 4, 6, 8, 12, 16]


def suite_meta():
    meta = {}
    for path in [ROOT / "suite" / "cgt_verified.epd", ROOT / "suite" / "cgt_disagree.epd"]:
        for line in open(path):
            if not line.strip():
                continue
            i = re.search(r'id "([^"]+)"', line).group(1)
            meta[i] = {
                "tb": re.search(r"tablebase root: (\w+)", line).group(1),
                "class": re.search(r'c5 "class ([^;]+);', line).group(1),
                "nsol": int(re.search(r"solutions (\d+)", line).group(1)),
                "slow": "only-slow-winning-move true" in line,
                "file": path.name,
            }
    return meta


def verdict(score: str) -> str:
    kind, v = score.split()
    v = int(v)
    if kind == "mate":
        return "win" if v > 0 else "loss"
    return "win" if v >= 150 else "loss" if v <= -150 else "draw"


def solve_point(row, maxd):
    """(depth, nodes) of the first iteration from which the PV head stays a solution."""
    it = row["iters"]
    first = None
    for d in range(1, maxd + 1):
        x = it.get(str(d))
        if x is None:
            continue
        if x["pv0"] in row["solutions"]:
            if first is None:
                first = d
        else:
            first = None
    if first is None:
        return None
    return first, it[str(first)]["nodes"]


def load(name):
    p = HERE / "results" / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    meta = suite_meta()
    runs = {v: load(v) for v in VARIANTS}
    runs = {k: v for k, v in runs.items() if v}
    base = {r["id"]: r for r in runs["base"]["results"]}
    maxd = runs["base"]["max_depth"]

    # 0. consistency with the earlier vendor-binary depth runs
    old = ROOT / "runs" / "sf19_depth.json"
    if old.exists():
        same = tot = 0
        for r in json.loads(old.read_text())["results"]:
            k = r["limit"].split()[1]
            x = base[r["id"]]["iters"].get(k)
            tot += 1
            same += bool(x) and x["nodes"] == r["nodes"] and x["score"] == r["score"] and x["pv0"] == r["best"]
        print(f"0. iteration k of the depth-{maxd} baseline == earlier `go depth k` run (score, nodes, best): "
              f"{same}/{tot}")

    # 1. where each variant first leaves the baseline
    print("\n1. First iteration at which a variant's (score, nodes, PV head) differs from the baseline")
    print("   (number of positions per first-differing depth; 'never' = identical through depth "
          f"{maxd})")
    for v, run in runs.items():
        if v == "base":
            continue
        first = defaultdict(int)
        for r in run["results"]:
            b = base[r["id"]]["iters"]
            fd = next((k for k in range(1, maxd + 1) if r["iters"].get(str(k)) != b.get(str(k))), None)
            first[fd] += 1
        ks = sorted((k for k in first if k is not None))
        txt = ", ".join(f"d{k}: {first[k]}" for k in ks) + (f", never: {first[None]}" if first[None] else "")
        print(f"   {v:8s}: earliest d{ks[0] if ks else '-'}; {txt}")

    # 2. per-variant summary
    print("\n2. Summary (233 positions = 181 verified + 52 disagreement; `eval ok` uses the +-150 cp verdict)")
    hdr = "| variant | " + " | ".join(f"solved d{d}" for d in DEPTHS) + " | " + \
          " | ".join(f"eval ok d{d}" for d in DEPTHS) + " | mean solve depth | nodes-to-solve vs base (geo-mean) |"
    print(hdr)
    print("|" + "---|" * (1 + 2 * len(DEPTHS) + 2))
    for v, run in runs.items():
        rows = run["results"]
        solved = [sum(r["iters"].get(str(d), {}).get("pv0") in r["solutions"] for r in rows) for d in DEPTHS]
        evok = [sum(verdict(r["iters"][str(d)]["score"]) == meta[r["id"]]["tb"] for r in rows if str(d) in r["iters"])
                for d in DEPTHS]
        sps = [solve_point(r, maxd) for r in rows]
        depths = [s[0] for s in sps if s]
        ratios = []
        for r, s in zip(rows, sps):
            b = solve_point(base[r["id"]], maxd)
            if s and b:
                ratios.append(math.log(s[1] / b[1]))
        gm = math.exp(sum(ratios) / len(ratios)) if ratios else float("nan")
        print(f"| {v} | " + " | ".join(map(str, solved)) + " | " + " | ".join(map(str, evok)) +
              f" | {sum(depths)/len(depths):.2f} ({len(depths)} solved) | {gm:.2f} |")

    # 3. by CGT class
    print("\n3. Root evaluation matches the tablebase, by CGT value class, at depths 1/2/4/6/8")
    classes = sorted({m["class"] for m in meta.values()})
    for v, run in runs.items():
        if v not in ("base", "RFP", "LMR", "CORR", "RAZOR", "PROBCUT", "SE", "IIR"):
            continue
        by = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        for r in run["results"]:
            c = meta[r["id"]]["class"]
            for d in (1, 2, 4, 6, 8):
                x = r["iters"].get(str(d))
                if x:
                    by[c][d][0] += 1
                    by[c][d][1] += verdict(x["score"]) == meta[r["id"]]["tb"]
        line = f"   {v:8s} " + "; ".join(
            f"{c} " + "/".join(f"{round(100*by[c][d][1]/max(1,by[c][d][0]))}" for d in (1, 2, 4, 6, 8)) for c in classes)
        print(line)

    # 4. P3 and P6 splits for the baseline: solution depth by slow flag and by number of solutions
    print("\n4. Baseline solution depth (first iteration from which the PV head stays a solution)")
    for label, key in (("only slow single push wins", lambda m: m["slow"]),
                       ("unique solution", lambda m: m["nsol"] == 1)):
        for flag in (True, False):
            ds = [solve_point(base[i], maxd) for i, m in meta.items() if key(m) == flag]
            ds = [s for s in ds if s]
            if ds:
                print(f"   {label} = {flag}: n={len(ds)}, mean depth {sum(d for d, _ in ds)/len(ds):.2f}, "
                      f"median nodes {sorted(n for _, n in ds)[len(ds)//2]}, "
                      f"share solved at depth 1 {sum(d == 1 for d, _ in ds)}/{len(ds)}")


def depth1_misses():
    """Section 6: the baseline's iteration-1 misses, with the component's CGT value."""
    import re as _re
    vals = {}
    for path in [ROOT / "suite" / "cgt_verified.epd", ROOT / "suite" / "cgt_disagree.epd"]:
        for line in open(path):
            if line.strip():
                i = _re.search(r'id "([^"]+)"', line).group(1)
                vals[i] = (_re.search(r"value count=([^;]+);", line).group(1), path.name)
    base = load("base")["results"]
    miss = [r for r in base if r["iters"]["1"]["pv0"] not in r["solutions"]]
    print(f"\n6. Baseline misses at iteration 1: {len(miss)} of {len(base)}")
    for r in miss:
        v, f = vals[r["id"]]
        print(f"   {r['id']} value {v:>10s} played {r['iters']['1']['pv0']} solutions {','.join(r['solutions'])} ({f})")


if __name__ == "__main__":
    main()


def eval_point(row, tb, maxd):
    """(depth, nodes) of the first iteration from which the root verdict stays equal to the tablebase."""
    first = None
    for d in range(1, maxd + 1):
        x = row["iters"].get(str(d))
        if x is None:
            continue
        if verdict(x["score"]) == tb:
            if first is None:
                first = d
        else:
            first = None
    return None if first is None else (first, row["iters"][str(first)]["nodes"])


def equal_nodes():
    """Section 5: compare at equal cost, not equal depth."""
    meta = suite_meta()
    runs = {v: load(v) for v in VARIANTS}
    runs = {k: v for k, v in runs.items() if v}
    base = {r["id"]: r for r in runs["base"]["results"]}
    maxd = runs["base"]["max_depth"]
    print("\n5. Equal-cost comparison: nodes until the root verdict (+-150 cp) is right and stays right")
    print("| variant | positions reaching it | geo-mean nodes ratio vs base | variant cheaper / dearer / same |"
          " nodes at depth 4, total, vs base |")
    print("|---|---|---|---|---|")
    tot4b = sum(r["iters"]["4"]["nodes"] for r in base.values())
    for v, run in runs.items():
        logs, cheaper, dearer, same, n = [], 0, 0, 0, 0
        for r in run["results"]:
            tb = meta[r["id"]]["tb"]
            a, b = eval_point(r, tb, maxd), eval_point(base[r["id"]], tb, maxd)
            if a and b:
                n += 1
                logs.append(math.log(a[1] / b[1]))
                cheaper += a[1] < b[1]
                dearer += a[1] > b[1]
                same += a[1] == b[1]
        gm = math.exp(sum(logs) / len(logs)) if logs else float("nan")
        tot4 = sum(r["iters"]["4"]["nodes"] for r in run["results"])
        print(f"| {v} | {n} | {gm:.2f} | {cheaper} / {dearer} / {same} | {tot4/tot4b:.2f} |")


if __name__ == "__main__":
    equal_nodes()
    depth1_misses()
