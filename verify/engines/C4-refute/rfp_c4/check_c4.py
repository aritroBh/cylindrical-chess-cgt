#!/usr/bin/env python3
"""Adversarial check of claim C4 (E2 ablation: reverse futility pruning off in Stockfish 19).

Independent of the worker's analyze.py / run_suite.py (stdlib only; nothing imported from the
project). Reads, read-only:
  engine/suite/cgt_verified.epd, engine/suite/cgt_disagree.epd   (labels, CGT class)
  engine/suite/tbcache/**.json, realchess/cache/**.json           (raw Lichess responses)
  engine/ablation/results/*.json                                  (worker's raw engine output)
  verify/engines/C4-refute/rfp_c4/rerun_*.json                    (my own re-runs)

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/engines/C4-refute/rfp_c4/check_c4.py
"""
import glob
import json
import math
import os
import re
import statistics
from collections import Counter, defaultdict

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
HERE = ROOT + "/verify/engines/C4-refute/rfp_c4"
RES = ROOT + "/engine/ablation/results"
VARS = ["base", "NMP", "SHALLOW", "RFP", "RAZOR", "SE", "PROBCUT", "LMR", "CORR", "IIR"]


def epd():
    m = {}
    for name in ("cgt_verified.epd", "cgt_disagree.epd"):
        for line in open(ROOT + "/engine/suite/" + name):
            if not line.strip():
                continue
            pid = re.search(r'id "([^"]+)"', line).group(1)
            m[pid] = {"fen4": " ".join(line.split()[:4]),
                      "tb": re.search(r"tablebase root: ([\w-]+)", line).group(1),
                      "cls": re.search(r"class ([^;]+);", line).group(1),
                      "file": name}
    return m


def lichess_roots():
    roots = {}
    for d in (ROOT + "/engine/suite/tbcache", ROOT + "/realchess/cache"):
        for p in glob.glob(d + "/*/*.json"):
            try:
                r = json.load(open(p))
            except Exception:
                continue
            if r.get("status") == 200 and r.get("data"):
                k = " ".join(r["fen"].split()[:4])
                c = r["data"].get("category")
                if k in roots and roots[k] != c:
                    roots[k] = "CONFLICT"
                else:
                    roots[k] = c
    return roots


def verdict(score, thr=150):
    kind, v = score.split()
    v = int(v)
    if kind == "mate":
        return "win" if v > 0 else "loss"
    return "win" if v >= thr else "loss" if v <= -thr else "draw"


def load(v):
    j = json.load(open(f"{RES}/{v}.json"))
    return {r["id"]: r for r in j["results"]}, j


def eval_point(it, tb, maxd=16, thr=150):
    first = None
    for d in range(1, maxd + 1):
        x = it.get(str(d))
        if x is None:
            continue
        if verdict(x["score"], thr) == tb:
            first = d if first is None else first
        else:
            first = None
    return None if first is None else (first, it[str(first)]["nodes"])


def at_budget(it, B, thr=150):
    """verdict of the deepest completed iteration whose cumulative nodes <= B (None if none)."""
    best = None
    for d in sorted(it, key=int):
        if it[d]["nodes"] <= B:
            best = it[d]
    return None if best is None else verdict(best["score"], thr)


def main():
    meta = epd()
    print("positions in EPDs:", len(meta), Counter(m["file"] for m in meta.values()))
    print("EPD tablebase-root labels:", Counter(m["tb"] for m in meta.values()))

    # A. labels against raw Lichess responses
    roots = lichess_roots()
    miss = [i for i, m in meta.items() if m["fen4"] not in roots]
    bad = [(i, m["tb"], roots[m["fen4"]]) for i, m in meta.items()
           if m["fen4"] in roots and roots[m["fen4"]] != m["tb"]]
    print(f"\nA. label check vs raw Lichess cache: {len(meta)-len(miss)} found, {len(miss)} missing, "
          f"{len(bad)} mismatches {bad[:5]}")

    runs = {v: load(v) for v in VARS}
    base, bj = runs["base"]
    rfp, rj = runs["RFP"]
    print("result files max_depth:", bj["max_depth"], rj["max_depth"], "errors:",
          sum(r["error"] is not None for r in base.values()), sum(r["error"] is not None for r in rfp.values()))
    incomplete = {v: sum(len(r["iters"]) != 16 for r in runs[v][0].values()) for v in VARS}
    print("positions without all 16 iterations, per variant:", incomplete)

    # B. my re-runs vs the worker's result files
    print("\nB. my re-runs vs worker result files (score, nodes, pv0 per iteration)")
    for name, ref in (("base", base), ("RFP", rfp), ("vendor", base), ("rfpmine", rfp)):
        for p in sorted(glob.glob(f"{HERE}/rerun_{name}_d*.json")):
            j = json.load(open(p))
            same = tot = 0
            diffs = []
            for pid, r in j["results"].items():
                for d, x in r["iters"].items():
                    tot += 1
                    y = ref[pid]["iters"].get(d)
                    if y == x:
                        same += 1
                    else:
                        diffs.append((pid, d))
            print(f"   {os.path.basename(p)} vs worker {('base' if ref is base else 'RFP')}: "
                  f"{same}/{tot} identical; first diffs {diffs[:3]}")

    # C. headline numbers
    def ok(run, d, thr=150):
        return {i for i, r in run.items() if str(d) in r["iters"] and verdict(r["iters"][str(d)]["score"], thr) == meta[i]["tb"]}

    print("\nC. eval ok (+-150 cp) by depth: base / RFP")
    for d in (1, 2, 3, 4, 5, 6, 8, 12, 16):
        print(f"   d{d}: {len(ok(base, d))} / {len(ok(rfp, d))}")

    # D. where the gain is
    for d in (3, 4):
        b, f = ok(base, d), ok(rfp, d)
        gain, loss = f - b, b - f
        print(f"\nD. depth {d}: RFP-off right & base wrong = {len(gain)}; base right & RFP-off wrong = {len(loss)}; "
              f"net {len(gain)-len(loss)}")
        print("   gained by class:", dict(Counter(meta[i]["cls"] for i in gain)))
        print("   lost by class  :", dict(Counter(meta[i]["cls"] for i in loss)))
        print("   gained by tb label:", dict(Counter(meta[i]["tb"] for i in gain)),
              " lost by tb label:", dict(Counter(meta[i]["tb"] for i in loss)))
        n_cls = Counter(m["cls"] for m in meta.values())
        print("   class sizes:", dict(n_cls))
        # draws
        dr = [i for i in meta if meta[i]["tb"] == "draw"]
        print(f"   draw-labelled positions right: base {len(b & set(dr))}/{len(dr)}, RFP-off {len(f & set(dr))}/{len(dr)}")
        # score shift
        sh = []
        for i in meta:
            x, y = base[i]["iters"][str(d)]["score"].split(), rfp[i]["iters"][str(d)]["score"].split()
            if x[0] == y[0] == "cp":
                sh.append(int(y[1]) - int(x[1]))
        print(f"   RFP-off minus base score (cp, both cp): median {statistics.median(sh)}, "
              f"mean {sum(sh)/len(sh):.1f}, >0: {sum(s>0 for s in sh)}, <0: {sum(s<0 for s in sh)}, =0: {sum(s==0 for s in sh)}")

    # E. threshold sensitivity
    print("\nE. threshold sensitivity, eval ok base / RFP-off at d3 and d4")
    for thr in (50, 100, 150, 200, 300, 400, 600):
        print(f"   +-{thr}: d3 {len(ok(base,3,thr))}/{len(ok(rfp,3,thr))}   d4 {len(ok(base,4,thr))}/{len(ok(rfp,4,thr))}")

    # F. node cost
    print("\nF. node cost of RFP-off")
    for d in (2, 3, 4, 6, 8, 12, 16):
        tb_ = sum(base[i]["iters"][str(d)]["nodes"] for i in meta)
        tr = sum(rfp[i]["iters"][str(d)]["nodes"] for i in meta)
        rat = [rfp[i]["iters"][str(d)]["nodes"] / base[i]["iters"][str(d)]["nodes"] for i in meta]
        gm = math.exp(sum(map(math.log, rat)) / len(rat))
        print(f"   d{d}: total {tr}/{tb_} = {tr/tb_:.3f}; per-position geo-mean {gm:.3f}, median {statistics.median(rat):.3f}")

    # G. equal-cost, worker's metric re-implemented, for all variants
    print("\nG. per variant: geo-mean nodes until verdict right-and-stays-right (vs base), cheaper/dearer/same; "
          "total nodes at d4 vs base; at d8; at d16")
    tot = {d: sum(base[i]["iters"][str(d)]["nodes"] for i in meta) for d in (4, 8, 16)}
    for v in VARS:
        run = runs[v][0]
        lg, ch, de, sa = [], 0, 0, 0
        for i in meta:
            a, b = eval_point(run[i]["iters"], meta[i]["tb"]), eval_point(base[i]["iters"], meta[i]["tb"])
            if a and b:
                lg.append(math.log(a[1] / b[1]))
                ch += a[1] < b[1]
                de += a[1] > b[1]
                sa += a[1] == b[1]
        t = {d: sum(run[i]["iters"][str(d)]["nodes"] for i in meta) / tot[d] for d in (4, 8, 16)}
        print(f"   {v:8s} n={len(lg)} geo {math.exp(sum(lg)/len(lg)):.3f}  {ch}/{de}/{sa}   "
              f"d4 {t[4]:.2f}  d8 {t[8]:.2f}  d16 {t[16]:.2f}")

    # H. equal node budget: verdict of deepest iteration within budget
    print("\nH. equal node budget B: # positions whose deepest completed iteration with nodes<=B has the right "
          "verdict (base / RFP-off)")
    for B in (20, 50, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 50000, 200000):
        cb = sum(at_budget(base[i]["iters"], B) == meta[i]["tb"] for i in meta)
        cr = sum(at_budget(rfp[i]["iters"], B) == meta[i]["tb"] for i in meta)
        print(f"   B={B:>6}: {cb} / {cr}")

    # I. sensitivity of the equal-cost metric to the threshold
    print("\nI. RFP-off equal-cost geo-mean vs threshold")
    for thr in (100, 150, 200, 300):
        lg, ch, de = [], 0, 0
        for i in meta:
            a = eval_point(rfp[i]["iters"], meta[i]["tb"], thr=thr)
            b = eval_point(base[i]["iters"], meta[i]["tb"], thr=thr)
            if a and b:
                lg.append(math.log(a[1] / b[1]))
                ch += a[1] < b[1]
                de += a[1] > b[1]
        print(f"   +-{thr}: n={len(lg)} geo {math.exp(sum(lg)/len(lg)):.3f} cheaper {ch} dearer {de}")

    # J. dilution: the equal-cost geo-mean restricted to positions where the two differ
    print("\nJ. equal-cost geo-mean restricted to positions whose nodes-to-right-verdict differs from base")
    for v in VARS[1:]:
        run = runs[v][0]
        lg = []
        for i in meta:
            a, b = eval_point(run[i]["iters"], meta[i]["tb"]), eval_point(base[i]["iters"], meta[i]["tb"])
            if a and b and a[1] != b[1]:
                lg.append(math.log(a[1] / b[1]))
        if lg:
            print(f"   {v:8s} n={len(lg):3d} geo {math.exp(sum(lg)/len(lg)):.3f} median ratio "
                  f"{math.exp(statistics.median(lg)):.3f}")

    # K. discrimination, not just level: win-vs-draw AUC of the root score, and mean score by label
    def num(s):
        k, v = s.split()
        v = int(v)
        return (100000 - abs(v)) * (1 if v > 0 else -1) if k == "mate" else v

    print("\nK. does RFP-off separate won from drawn positions better, or just score higher?")
    wins = [i for i in meta if meta[i]["tb"] == "win"]
    draws = [i for i in meta if meta[i]["tb"] == "draw"]
    for d in (2, 3, 4, 6):
        for nm, run in (("base", base), ("RFP-off", rfp)):
            sw = [num(run[i]["iters"][str(d)]["score"]) for i in wins]
            sd = [num(run[i]["iters"][str(d)]["score"]) for i in draws]
            auc = sum((a > b) + 0.5 * (a == b) for a in sw for b in sd) / (len(sw) * len(sd))
            print(f"   d{d} {nm:8s}: AUC(win>draw) {auc:.3f}; median score win {statistics.median(sw)}, "
                  f"draw {statistics.median(sd)}; wins >=150: {sum(s >= 150 for s in sw)}/{len(sw)}, "
                  f"draws in (-150,150): {sum(-150 < s < 150 for s in sd)}/{len(sd)}")
    # best threshold per engine at d3/d4 (is the gain an artefact of one fixed threshold?)
    print("   best achievable eval-ok over all symmetric thresholds 1..1000:")
    for d in (3, 4):
        for nm, run in (("base", base), ("RFP-off", rfp)):
            best = max((len(ok(run, d, t)), t) for t in range(1, 1001))
            print(f"     d{d} {nm:8s}: {best[0]} at +-{best[1]}")


if __name__ == "__main__":
    main()
