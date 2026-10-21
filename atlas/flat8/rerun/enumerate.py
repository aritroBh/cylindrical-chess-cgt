#!/usr/bin/env python3
"""Workstream A2-search, rerun of 2026-10-16: value database of pawn-only positions
on FLAT boards with 8 ranks and widths 1-4.

Values come from cylcgt (read-only): pawns.value on Board(W, 8, wrap=False, ep=...).
The enumeration and canonicalisation below are written from scratch for this rerun
(they do not reuse ../enumerate.py), so comparing with ../values.jsonl checks the
enumeration layer a second way.

Scope
  * pawns on ranks 2-7, at least one pawn per side;
  * skip positions where either side already has a passed pawn (textbook test; at the
    root there is no e.p. right, so the e.p.-aware test gives the same answer).
    Consequence used for speed: a white pawn on rank 7 or a black pawn on rank 2 is
    always passed, so whites are generated on ranks 2-6 and blacks on ranks 3-7;
  * a position is listed under width W only if files a and the W-th file are both
    occupied, so every position that fits on <= 4 files appears exactly once up to
    translation (translation does not change the value on a flat board);
  * mirror images (file f -> W-1-f) are identified; `mult` = 1 or 2 is the number
    of board positions a record stands for.

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/enumerate.py estimate
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/enumerate.py enum --workers 8 \
      --out atlas/flat8/rerun/values.jsonl --log atlas/flat8/rerun/enum_log.json
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import random
import resource
import sys
import time
from collections import defaultdict
from itertools import combinations

from cylcgt import cgt, pawns

RANKS = 8
FILES = "abcdefghijklmnopqrstuvwxyz"


# ---------------------------------------------------------------- enumeration
def scope_classes(six_widths=(1, 2, 3, 4), max_total=6):
    """(W, w, b) classes in scope: w,b >= 1, w+b <= 5 on every width; w+b = 6 on
    the widths listed in six_widths."""
    out = []
    for W in (1, 2, 3, 4):
        for n in range(2, max_total + 1):
            if n == 6 and W not in six_widths:
                continue
            for w in range(1, n):
                out.append((W, w, n - w))
    return out


def _bit(f, r):
    return 1 << (f * 8 + r)


def _front_masks(W):
    """fw[(f,r)]: squares on files f-1..f+1 strictly above rank r (white's path);
    fb[(f,r)]: same strictly below (black's path)."""
    fw, fb = {}, {}
    for f in range(W):
        for r in range(1, RANKS + 1):
            mw = mb = 0
            for g in (f - 1, f, f + 1):
                if 0 <= g < W:
                    for s in range(1, RANKS + 1):
                        if s > r:
                            mw |= _bit(g, s)
                        if s < r:
                            mb |= _bit(g, s)
            fw[(f, r)], fb[(f, r)] = mw, mb
    return fw, fb


def gen_class(W, w, b, stats=None):
    """Canonical positions of class (W, w, b) as (white_tuple, black_tuple, mult)."""
    fw, fb = _front_masks(W)
    wsq = [(f, r) for f in range(W) for r in range(2, 7)]  # ranks 2-6 (rank 7 = passed)
    bsq = [(f, r) for f in range(W) for r in range(3, 8)]  # ranks 3-7 (rank 2 = passed)
    raw = edge = nopass = canon = boards = 0
    out = []
    for wt in combinations(wsq, w):
        wset = set(wt)
        wmask = 0
        for s in wt:
            wmask |= _bit(*s)
        wfiles = {f for f, _ in wt}
        for bt in combinations(bsq, b):
            if wset.intersection(bt):
                continue
            raw += 1
            files = wfiles | {f for f, _ in bt}
            if 0 not in files or (W - 1) not in files:
                continue
            edge += 1
            bmask = 0
            for s in bt:
                bmask |= _bit(*s)
            if any(not (bmask & fw[s]) for s in wt):  # some white pawn passed
                continue
            if any(not (wmask & fb[s]) for s in bt):  # some black pawn passed
                continue
            nopass += 1
            key = (tuple(sorted(wt)), tuple(sorted(bt)))
            mkey = (tuple(sorted((W - 1 - f, r) for f, r in wt)),
                    tuple(sorted((W - 1 - f, r) for f, r in bt)))
            if key > mkey:
                continue
            canon += 1
            m = 1 if key == mkey else 2
            boards += m
            out.append((key[0], key[1], m))
    if stats is not None:
        stats.update(raw_pairs=raw, edge_occupied=edge, no_passed=nopass,
                     canonical=canon, board_positions=boards)
    return out


def pos_of(wt, bt):
    return pawns.Pos(frozenset(wt), frozenset(bt))


# ---------------------------------------------------------------- evaluation
_big_memo: dict[int, bool] = {}


def involves_big(g) -> bool:
    """True if the canonical form mentions a number with |x| >= BIG/2 anywhere."""
    r = _big_memo.get(g.id)
    if r is None:
        if g.num is not None:
            r = abs(g.num) >= pawns.BIG // 2
        else:
            r = any(involves_big(x) for x in g.L + g.R)
        _big_memo[g.id] = r
    return r


def record(board, wt, bt, mult):
    pos = pos_of(wt, bt)
    assert not pawns.passed(board, pos, "W") and not pawns.passed(board, pos, "B")
    g = pawns.value(board, pos)
    t = cgt.temperature(g)
    return {
        "position": str(pos),
        "width": board.files,
        "nw": len(wt), "nb": len(bt),
        "value": cgt.show(g),
        "outcome": cgt.outcome(g),
        "temperature": "number" if t is None else str(t),
        "mean": str(cgt.mean(g)),
        "nim": g.nim,
        "num": None if g.num is None else str(g.num),
        "big": involves_big(g),
        "n_components": len(pawns.components(board, pos)),
        "mult": mult,
    }


def _work(task):
    W, rule, ep, items = task
    pawns.RACE_RULE = rule
    board = pawns.Board(W, RANKS, False, ep)
    t0 = time.process_time()
    recs = [record(board, wt, bt, m) for wt, bt, m in items]
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return recs, time.process_time() - t0, rss


# ---------------------------------------------------------------- commands
def cmd_estimate(args):
    """Pilot: time a random sample of each class with a cold solver cache in a
    fresh process, then extrapolate (an upper-ish bound: the real run shares cache)."""
    rng = random.Random(1)
    classes = scope_classes()
    tasks, sizes = [], {}
    t0 = time.time()
    for W, w, b in classes:
        st = {}
        items = gen_class(W, w, b, st)
        sizes[(W, w, b)] = st
        sample = items if len(items) <= args.sample else rng.sample(items, args.sample)
        tasks.append(((W, w, b), sample))
    gen_wall = time.time() - t0
    print(f"generated all classes in {gen_wall:.1f}s", flush=True)
    with mp.Pool(args.workers, maxtasksperchild=1) as pool:
        res = pool.map(_est_one, tasks)
    tot = 0.0
    rows = []
    for ((W, w, b), n_s, cpu) in res:
        n = sizes[(W, w, b)]["canonical"]
        est = cpu / max(n_s, 1) * n
        tot += est
        rows.append({"class": [W, w, b], "canonical": n, "sampled": n_s,
                     "sample_cpu_s": round(cpu, 2), "est_cpu_s": round(est, 1)})
        print(f"W={W} w={w} b={b}: {n} canonical, sample {n_s} in {cpu:.2f}s -> est {est:.0f} cpu-s", flush=True)
    print(f"TOTAL estimated cpu-s (cold-cache extrapolation): {tot:.0f}")
    six4 = sum(r["est_cpu_s"] for r in rows if r["class"][0] == 4 and r["class"][1] + r["class"][2] == 6)
    print(f"  of which w+b=6 on width 4: {six4:.0f}")
    if args.log:
        with open(args.log, "w") as fh:
            json.dump({"gen_wall_s": gen_wall, "classes": rows, "sizes": {str(k): v for k, v in sizes.items()},
                       "total_est_cpu_s": tot, "six_w4_est_cpu_s": six4}, fh, indent=1)


def _est_one(task):
    (W, w, b), sample = task
    _, cpu, _ = _work((W, "count", True, sample))
    return ((W, w, b), len(sample), cpu)


def cmd_enum(args):
    six = tuple(int(x) for x in args.six_widths.split(",")) if args.six_widths else ()
    classes = scope_classes(six_widths=six)
    log = {"settings": {"RACE_RULE": args.rule, "ep": not args.ep_off, "flat": True, "ranks": RANKS,
                        "passed_test": "cylcgt/pawns.py as on disk (textbook: e.p.-capturable pawn counts as passed)"},
           "scope": {"widths": [1, 2, 3, 4], "w+b<=5": "all widths", "w+b=6 widths": list(six)},
           "classes": {}, "skipped": []}
    for W in (1, 2, 3, 4):
        if W not in six:
            log["skipped"].append(f"w+b=6 on width {W}")
    t0 = time.time()
    tasks = []
    for (W, w, b) in classes:
        st = {}
        items = gen_class(W, w, b, st)
        log["classes"][f"{W}:{w}:{b}"] = st
        for i in range(0, len(items), args.chunk):
            tasks.append((W, args.rule, not args.ep_off, items[i:i + args.chunk]))
    gen_wall = time.time() - t0
    ntot = sum(len(t[3]) for t in tasks)
    print(f"generated {ntot} canonical positions in {len(tasks)} chunks ({gen_wall:.1f}s)", flush=True)
    t1 = time.time()
    cpu = 0.0
    maxrss = 0
    done = 0
    with open(args.out, "w") as fh, mp.Pool(args.workers) as pool:
        for k, (recs, c, rss) in enumerate(pool.imap(_work, tasks, chunksize=1)):
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            cpu += c
            maxrss = max(maxrss, rss)
            done += len(recs)
            if (k + 1) % 50 == 0 or k + 1 == len(tasks):
                print(f"  {k + 1}/{len(tasks)} chunks, {done} positions, {time.time() - t1:.0f}s wall, "
                      f"{cpu:.0f} worker cpu-s, max worker rss {maxrss / 2**30:.2f} GB", flush=True)
    log.update(n_records=done, gen_wall_s=round(gen_wall, 1), eval_wall_s=round(time.time() - t1, 1),
               worker_cpu_s=round(cpu, 1), workers=args.workers, max_worker_rss_bytes=maxrss)
    with open(args.log, "w") as fh:
        json.dump(log, fh, indent=1)
    print(f"wrote {done} records to {args.out}")


def norm_show(s: str) -> str:
    """cgt.show with every option list sorted, recursively. cgt.show lists options
    in internal game-id order, which depends on evaluation order, so the raw string
    of a complex game differs between runs; the sorted form does not."""
    s = s.strip()
    if not s.startswith("{"):
        return s
    assert s.endswith("}"), s
    body = s[1:-1]
    depth, parts, cur, side = 0, [[], []], [], 0
    i = 0
    while i < len(body):
        c = body[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0 and body.startswith(" | ", i):
            parts[side].append("".join(cur)); cur = []; side = 1; i += 3; continue
        if depth == 0 and body.startswith(", ", i):
            parts[side].append("".join(cur)); cur = []; i += 2; continue
        cur.append(c)
        i += 1
    parts[side].append("".join(cur))
    L = sorted(norm_show(x) for x in parts[0] if x.strip())
    R = sorted(norm_show(x) for x in parts[1] if x.strip())
    return "{" + ", ".join(L) + " | " + ", ".join(R) + "}"


KEEP = ["position", "width", "nw", "nb", "value", "outcome", "temperature", "mean", "nim", "num",
        "big", "n_components", "mult"]


def _mirror_str(s, W):
    wp, bp = s.split("/")
    sqs = lambda part: [(ord(t[0]) - 97, int(t[1:])) for t in part.split(":")[1].split()]
    n = lambda q: f"{chr(97 + q[0])}{q[1]}"
    return ("W: " + " ".join(sorted(n((W - 1 - f, r)) for f, r in sqs(wp))) + " / B: "
            + " ".join(sorted(n((W - 1 - f, r)) for f, r in sqs(bp))))


def _key(s, W):
    return min(s, _mirror_str(s, W))


def cmd_import_prior(args):
    """Verify the prior run's records for the classes given and import them.
    (1) the set of positions (up to mirror) and the multiplicities must equal this
    script's own enumeration; (2) a random sample is recomputed with cylcgt here
    and every field compared (value strings order-normalised)."""
    classes = [tuple(int(x) for x in c.split(":")) for c in args.classes.split(",")]
    mine = {}
    for W, w, b in classes:
        for wt, bt, m in gen_class(W, w, b):
            mine[_key(str(pos_of(wt, bt)), W)] = (W, wt, bt, m)
    prior = {}
    with open(args.prior) as fh:
        for line in fh:
            r = json.loads(line)
            if (r["width"], r["nw"], r["nb"]) in classes:
                prior[_key(r["position"], r["width"])] = r
    set_equal = set(mine) == set(prior)
    mult_bad = sum(1 for k in mine if k in prior and prior[k]["mult"] != mine[k][3])
    print(f"own enumeration {len(mine)}, prior {len(prior)}, sets equal {set_equal}, mult mismatches {mult_bad}", flush=True)
    rng = random.Random(args.seed)
    keys = sorted(mine)
    sample = sorted(rng.sample(keys, min(args.sample, len(keys))))
    tasks = []
    for i in range(0, len(sample), args.chunk):
        part = [mine[k] for k in sample[i:i + args.chunk]]
        byW = defaultdict(list)
        for W, wt, bt, m in part:
            byW[W].append((wt, bt, m))
        for W, items in byW.items():
            tasks.append((W, "count", True, items))
    t0 = time.time()
    cpu = 0.0
    recomputed = {}
    with mp.Pool(args.workers) as pool:
        for recs, c, _ in pool.imap_unordered(_work, tasks):
            cpu += c
            for r in recs:
                recomputed[_key(r["position"], r["width"])] = r
    mism = defaultdict(int)
    ex = []
    for k, r in recomputed.items():
        p = prior[k]
        for f in KEEP:
            a, b = r[f], p[f]
            if f == "value":
                a, b = norm_show(a), norm_show(b)
            if f == "position":
                continue
            if a != b:
                mism[f] += 1
                if len(ex) < 5:
                    ex.append((k, f, a, b))
    print(f"recomputed {len(recomputed)} sampled records in {time.time() - t0:.0f}s wall, {cpu:.0f} worker cpu-s; "
          f"field mismatches {dict(mism)} {ex}", flush=True)
    with open(args.out, "w") as fh:
        for k in keys:
            if k in recomputed:
                r = dict(recomputed[k]); r["source"] = "rerun"
            else:
                r = {f: prior[k][f] for f in KEEP}; r["source"] = "prior-run import (verified sample)"
            r["value"] = norm_show(r["value"])
            fh.write(json.dumps({f: r[f] for f in KEEP + ["source"]}, ensure_ascii=False) + "\n")
    with open(args.log, "w") as fh:
        json.dump({"classes": args.classes, "own_enumeration": len(mine), "prior_records": len(prior),
                   "sets_equal": set_equal, "mult_mismatches": mult_bad, "sample": len(recomputed),
                   "seed": args.seed, "field_mismatches": dict(mism), "examples": ex,
                   "sample_wall_s": round(time.time() - t0, 1), "sample_worker_cpu_s": round(cpu, 1)}, fh, indent=1)


def cmd_merge(args):
    """Concatenate record files into the database, order-normalising value strings."""
    n = 0
    seen = set()
    with open(args.out, "w") as out:
        for path in args.inputs:
            with open(path) as fh:
                for line in fh:
                    r = json.loads(line)
                    k = _key(r["position"], r["width"])
                    assert k not in seen, k
                    seen.add(k)
                    r["value"] = norm_show(r["value"])
                    r.setdefault("source", "rerun")
                    out.write(json.dumps({f: r[f] for f in KEEP + ["source"]}, ensure_ascii=False) + "\n")
                    n += 1
    print(f"merged {n} records into {args.out}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ip = sub.add_parser("import-prior")
    ip.add_argument("--prior", required=True)
    ip.add_argument("--classes", default="4:1:5,4:2:4,4:3:3,4:4:2,4:5:1")
    ip.add_argument("--sample", type=int, default=1500)
    ip.add_argument("--seed", type=int, default=20261016)
    ip.add_argument("--chunk", type=int, default=50)
    ip.add_argument("--workers", type=int, default=4)
    ip.add_argument("--out", required=True)
    ip.add_argument("--log", required=True)
    mg = sub.add_parser("merge")
    mg.add_argument("inputs", nargs="+")
    mg.add_argument("--out", required=True)
    e = sub.add_parser("estimate")
    e.add_argument("--sample", type=int, default=150)
    e.add_argument("--workers", type=int, default=8)
    e.add_argument("--log")
    n = sub.add_parser("enum")
    n.add_argument("--workers", type=int, default=8)
    n.add_argument("--chunk", type=int, default=200)
    n.add_argument("--rule", default="count")
    n.add_argument("--ep-off", action="store_true")
    n.add_argument("--six-widths", default="1,2,3,4")
    n.add_argument("--out", required=True)
    n.add_argument("--log", required=True)
    args = ap.parse_args()
    {"estimate": cmd_estimate, "enum": cmd_enum, "import-prior": cmd_import_prior,
     "merge": cmd_merge}[args.cmd](args)


if __name__ == "__main__":
    main()
