#!/usr/bin/env python3
"""Experiment E2: which Stockfish search heuristic matters on CGT king-and-pawn positions?

For every engine binary given, search every suite position once with `go depth D` and keep the
final (exact-bound) `info` line of every completed iteration 1..D: score, cumulative nodes, PV head.
With 1 thread, a fixed hash and `ucinewgame` before each position, Stockfish is deterministic, and
iteration k of a depth-D search is the same search as `go depth k`.

Run from the project root (binaries from engine/ablation/build.sh):

    .venv/bin/python engine/ablation/run_ablation.py --depth 20 \
        --bin base=engine/vendor/sf19_ablate/bin/sf_base NMP=engine/vendor/sf19_ablate/bin/sf_NMP ...

Writes engine/ablation/results/<name>.json. Stdlib only. No tablebases are given to the engine.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from run_suite import Engine, parse_epd, solutions  # noqa: E402

EPDS = [HERE.parent / "suite" / "cgt_verified.epd", HERE.parent / "suite" / "cgt_disagree.epd"]


def load_items():
    items = []
    for path in EPDS:
        for line in open(path, encoding="utf-8"):
            e = parse_epd(line)
            if e is None:
                continue
            fen4, ops = e
            items.append((ops["id"][0], fen4, sorted(solutions(fen4, ops))))
    return items


def search(eng: Engine, fen4: str, depth: int, timeout: float):
    eng.send("ucinewgame")
    eng.ready()
    eng.send(f"position fen {fen4} 0 1")
    eng.send(f"go depth {depth}")
    iters = {}
    best = None
    for line in eng.until("bestmove", timeout=timeout):
        t = line.split()
        exact = "lowerbound" not in t and "upperbound" not in t
        mpv1 = "multipv" not in t or t[t.index("multipv") + 1] == "1"
        if t and t[0] == "info" and "pv" in t and "score" in t and exact and mpv1:
            d = int(t[t.index("depth") + 1])
            i = t.index("score")
            iters[d] = {"score": f"{t[i+1]} {t[i+2]}", "nodes": int(t[t.index("nodes") + 1]),
                        "pv0": t[t.index("pv") + 1]}
        if line.startswith("bestmove"):
            best = t[1]
    return best, iters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", nargs="+", required=True, help="NAME=PATH ...")
    ap.add_argument("--depth", type=int, default=20)
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--hash", type=int, default=64)
    a = ap.parse_args()
    items = load_items()
    outdir = HERE / "results"
    outdir.mkdir(exist_ok=True)
    for spec in a.bin:
        name, path = spec.split("=", 1)
        eng = Engine(path, {"Threads": "1", "Hash": str(a.hash)}, timeout=a.timeout)
        t0 = time.time()
        rows = []
        for pid, fen4, sol in items:
            try:
                best, iters = search(eng, fen4, a.depth, a.timeout)
                err = None
            except (TimeoutError, RuntimeError) as ex:
                best, iters, err = None, {}, str(ex)
                eng.quit()
                eng = Engine(path, {"Threads": "1", "Hash": str(a.hash)}, timeout=a.timeout)
            rows.append({"id": pid, "fen": fen4, "solutions": sol, "best": best, "error": err,
                         "iters": {str(k): v for k, v in sorted(iters.items())}})
        eng.quit()
        out = {"name": name, "binary": path, "engine": eng.name, "max_depth": a.depth,
               "options": {"Threads": 1, "Hash": a.hash}, "seconds": round(time.time() - t0, 1),
               "results": rows}
        (outdir / f"{name}.json").write_text(json.dumps(out, indent=0))
        errs = sum(r["error"] is not None for r in rows)
        print(f"{name}: {len(rows)} positions, {out['seconds']} s, errors {errs}", flush=True)


if __name__ == "__main__":
    main()
