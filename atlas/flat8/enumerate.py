#!/usr/bin/env python
"""Workstream A2-search: exhaustive value atlas of pawn-only positions on FLAT
W x 8 boards, W = 1..4, using the project's CGT engine (cylcgt, read-only).

Scope (see REPORT.md for what was actually run):
  * pawns on ranks 2-7, at least one pawn of each colour;
  * positions in which either side already has a passed pawn are skipped;
  * a position is listed under width W only if files a and the W-th file are
    both occupied, so every position that fits on <= 4 files is listed exactly
    once up to translation (a group on files b-c of a 4-file board behaves
    exactly like the same group on a 2-file board: empty files stay empty);
  * positions with an internal empty file are disjunctive sums and are flagged
    with n_components > 1 (the sum model has known caveats; see REPORT.md);
  * mirror symmetry f -> W-1-f: only the lexicographically smaller of a
    position and its mirror image is stored; `mult` says how many board
    positions (1 or 2) the record stands for.

Database settings: en passant on (Board.ep=True), pawns.RACE_RULE = "count".

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python atlas/flat8/enumerate.py enum --workers 6
  PYTHONPATH=. .venv/bin/python atlas/flat8/enumerate.py pilot
"""
from __future__ import annotations

import argparse
import itertools
import json
import multiprocessing as mp
import os
import resource
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos, passed  # noqa: E402

RANKS = 8
PAWN_RANKS = range(2, RANKS)  # 2..7


# --------------------------------------------------------------------------
# enumeration
# --------------------------------------------------------------------------

def classes(widths, max_total, six_widths):
    """(width, n_white, n_black) classes in the requested scope."""
    out = []
    for W in widths:
        top = 6 if W in six_widths else max_total
        for s in range(2, top + 1):
            for nw in range(1, s):
                out.append((W, nw, s - nw))
    return out


def mirror(W, sqs):
    return tuple(sorted((W - 1 - f, r) for f, r in sqs))


def gen_positions(W, nw, nb):
    """Yield (pos_string, mult) for canonical (mirror-reduced) positions with
    both edge files occupied and no passed pawn for either side."""
    board = Board(W, RANKS, False, True)
    sqs = [(f, r) for f in range(W) for r in PAWN_RANKS]
    for Wt in itertools.combinations(sqs, nw):
        ws = set(Wt)
        rest = [s for s in sqs if s not in ws]
        wfiles = {f for f, _ in Wt}
        for Bt in itertools.combinations(rest, nb):
            files = wfiles | {f for f, _ in Bt}
            if 0 not in files or (W - 1) not in files:
                continue
            p = Pos(frozenset(Wt), frozenset(Bt))
            if passed(board, p, "W") or passed(board, p, "B"):
                continue
            key = (tuple(sorted(Wt)), tuple(sorted(Bt)))
            mkey = (mirror(W, Wt), mirror(W, Bt))
            if mkey < key:
                continue
            yield str(p), (1 if mkey == key else 2)


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------

def has_big(g, seen=None):
    """True if the canonical form mentions a +-BIG (passed-pawn) number."""
    seen = set() if seen is None else seen
    stack = [g]
    while stack:
        x = stack.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        if x.num is not None:
            if abs(x.num) >= pawns.BIG // 2:
                return True
            continue
        stack.extend(x.L + x.R)
    return False


def birthday(g, memo={}):
    r = memo.get(g.id)
    if r is None:
        r = 0 if not (g.L or g.R) else 1 + max(birthday(x) for x in g.L + g.R)
        memo[g.id] = r
    return r


def evaluate(board, s):
    p = Pos.parse(s)
    g = pawns.value(board, p)
    comps = pawns.components(board, p)
    rec = {
        "position": s,
        "width": board.files,
        "nw": len(p.white),
        "nb": len(p.black),
        "value": cgt.show(g),
        "outcome": cgt.outcome(g),
    }
    try:
        t = cgt.temperature(g)
        rec["temperature"] = "number" if t is None else str(t)
        rec["mean"] = str(cgt.mean(g))
    except Exception as e:  # pragma: no cover - thermograph failure is logged
        rec["temperature"] = "error"
        rec["mean"] = "error"
        rec["thermo_error"] = repr(e)
    rec["nim"] = g.nim
    rec["num"] = None if g.num is None else str(g.num)
    rec["big"] = has_big(g)
    rec["n_components"] = len(comps)
    if len(comps) > 1:
        rec["sum_safe"] = pawns.sum_safe(board, p)
    return rec, g


def _init_worker(rule):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()


def work(task):
    W, items = task
    board = Board(W, RANKS, False, True)
    t0 = time.process_time()
    out = []
    for s, mult in items:
        rec, _ = evaluate(board, s)
        rec["mult"] = mult
        out.append(rec)
    dt = time.process_time() - t0
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS
    return W, out, dt, rss, os.getpid()


def chunked(it, n):
    buf = []
    for x in it:
        buf.append(x)
        if len(buf) >= n:
            yield buf
            buf = []
    if buf:
        yield buf


def cmd_enum(a):
    widths = [int(x) for x in a.widths.split(",")]
    six = [int(x) for x in a.six_widths.split(",")] if a.six_widths else []
    cls = classes(widths, a.max_total, six)
    if a.classes:  # explicit list "W:nw:nb,W:nw:nb"
        cls = [tuple(int(x) for x in c.split(":")) for c in a.classes.split(",")]
    t_start = time.time()
    tasks, counts = [], Counter()
    for (W, nw, nb) in cls:
        n = 0
        for chunk in chunked(gen_positions(W, nw, nb), a.chunk):
            tasks.append((W, chunk))
            n += len(chunk)
        counts[(W, nw, nb)] = n
    t_gen = time.time() - t_start
    print(f"generated {sum(counts.values())} canonical positions in {len(tasks)} chunks "
          f"({t_gen:.1f}s)", flush=True)
    records = []
    cpu = defaultdict(float)
    maxrss = {}
    done = 0
    t_eval = time.time()
    with mp.Pool(a.workers, initializer=_init_worker, initargs=("count",),
                 maxtasksperchild=a.maxtasks or None) as pool:
        for W, out, dt, rss, pid in pool.imap_unordered(work, tasks):
            records.extend(out)
            for r in out:
                cpu[(W, r["nw"], r["nb"])] += dt / len(out)
            maxrss[pid] = max(maxrss.get(pid, 0), rss)
            done += 1
            if done % 50 == 0 or done == len(tasks):
                el = time.time() - t_eval
                print(f"  {done}/{len(tasks)} chunks, {len(records)} positions, {el:.0f}s wall",
                      flush=True)
    wall = time.time() - t_start
    records.sort(key=lambda r: (r["width"], r["nw"] + r["nb"], r["nw"], r["position"]))
    path = os.path.join(HERE, a.out)
    with open(path, "w") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log = {
        "command": " ".join(sys.argv),
        "settings": {"ep": True, "RACE_RULE": "count", "ranks": RANKS, "pawn_ranks": "2-7",
                     "flat": True, "BIG": pawns.BIG},
        "classes": [{"width": W, "nw": nw, "nb": nb, "canonical_positions": counts[(W, nw, nb)],
                     "board_positions": sum(r["mult"] for r in records
                                            if (r["width"], r["nw"], r["nb"]) == (W, nw, nb)),
                     "cpu_seconds": round(cpu[(W, nw, nb)], 2)}
                    for (W, nw, nb) in cls],
        "total_canonical": len(records),
        "total_board_positions": sum(r["mult"] for r in records),
        "wall_seconds": round(wall, 1),
        "cpu_seconds_total": round(sum(cpu.values()), 1),
        "workers": a.workers,
        "max_rss_bytes_per_worker": sorted(maxrss.values()),
    }
    with open(os.path.join(HERE, a.log), "w") as fh:
        json.dump(log, fh, indent=1)
    print(f"wrote {len(records)} records to {path}; wall {wall:.0f}s, "
          f"cpu {sum(cpu.values()):.0f}s", flush=True)


def cmd_merge(a):
    """Concatenate phase files into one sorted database."""
    records = []
    for f in a.inputs:
        with open(os.path.join(HERE, f)) as fh:
            records.extend(json.loads(line) for line in fh)
    keys = [(r["width"], r["position"]) for r in records]
    assert len(set(keys)) == len(keys), "duplicate positions across phases"
    records.sort(key=lambda r: (r["width"], r["nw"] + r["nb"], r["nw"], r["position"]))
    with open(os.path.join(HERE, a.out), "w") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"merged {len(records)} records into {a.out}")


def cmd_pilot(a):
    """Time a sample of each class in a single cold process (runtime estimate)."""
    _init_worker("count")
    widths = [int(x) for x in a.widths.split(",")]
    six = [int(x) for x in a.six_widths.split(",")] if a.six_widths else []
    total_est = 0.0
    for (W, nw, nb) in classes(widths, a.max_total, six):
        pos = list(gen_positions(W, nw, nb))
        if not pos:
            print(f"W={W} {nw}v{nb}: 0 positions")
            continue
        # contiguous block (realistic cache locality inside a chunk)
        k = min(len(pos), a.sample)
        start = len(pos) // 3
        sample = pos[start:start + k]
        pawns._value.cache_clear()
        board = Board(W, RANKS, False, True)
        t = time.process_time()
        for s, _ in sample:
            evaluate(board, s)
        dt = (time.process_time() - t) / k
        est = dt * len(pos)
        total_est += est
        print(f"W={W} {nw}v{nb}: {len(pos):7d} positions, {dt*1000:8.2f} ms/pos (cold block of {k}),"
              f" est {est:8.0f} cpu-s", flush=True)
    print(f"total estimated cpu seconds: {total_est:.0f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("enum", "pilot"):
        s = sub.add_parser(name)
        s.add_argument("--widths", default="1,2,3,4")
        s.add_argument("--max-total", type=int, default=5)
        s.add_argument("--six-widths", default="1,2,3")
        if name == "enum":
            s.add_argument("--workers", type=int, default=6)
            s.add_argument("--chunk", type=int, default=200)
            s.add_argument("--maxtasks", type=int, default=0)
            s.add_argument("--out", default="values.jsonl")
            s.add_argument("--log", default="enum_log.json")
            s.add_argument("--classes", default="", help="explicit classes W:nw:nb,... (overrides scope)")
        else:
            s.add_argument("--sample", type=int, default=200)
    m = sub.add_parser("merge")
    m.add_argument("inputs", nargs="+")
    m.add_argument("--out", default="values.jsonl")
    a = ap.parse_args()
    {"enum": cmd_enum, "pilot": cmd_pilot, "merge": cmd_merge}[a.cmd](a)
