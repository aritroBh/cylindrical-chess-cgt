"""Compute CGT values for canonical pawn positions and write JSONL parts.

Each task is (n, wrap, w, b, race_rule, ep, connected_only, shard, nshards).
Results go to atlas/cylinder/parts/<tag>.jsonl, one line per position, plus a
value index (exact canonical-form key -> display, class, outcome, mean, temp).

Example (everything with <= 4 pawns, default rules, 6 worker processes):
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python atlas/cylinder/atlas_run.py --maxpawns 4 --jobs 6

Value identity: canonical forms are unique, so the recursive exact key
(numbers as exact fractions, options sorted) is an injective name for a value;
it is hashed (sha1, 16 hex) to give a compact value id `vid`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from cylcgt import cgt, pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402
from enumerate import canon_positions  # noqa: E402

FILES = "abcdefghijklmnopqrstuvwxyz"
BIG = pawns.BIG

_key_memo: dict[int, str] = {}


def vkey(g: cgt.Game) -> str:
    """Exact, injective text key of a canonical game."""
    r = _key_memo.get(g.id)
    if r is not None:
        return r
    if g.num is not None:
        x = g.num
        r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(vkey(x) for x in g.L)) + "|" + ",".join(sorted(vkey(x) for x in g.R)) + "}"
    _key_memo[g.id] = r
    return r


def vid_of(key: str) -> str:
    return hashlib.sha1(key.encode()).hexdigest()[:16]


_big_memo: dict[int, bool] = {}


def has_big(g) -> bool:
    r = _big_memo.get(g.id)
    if r is None:
        if g.num is not None:
            r = abs(g.num) >= BIG // 2
        else:
            r = any(has_big(x) for x in g.L + g.R)
        _big_memo[g.id] = r
    return r


_size_memo: dict[int, int] = {}


def birthday(g) -> int:
    r = _size_memo.get(g.id)
    if r is None:
        r = 0 if not (g.L or g.R) else 1 + max(birthday(x) for x in g.L + g.R)
        _size_memo[g.id] = r
    return r


_UPS: dict[int, str] = {}


def ups_table():
    """id -> label for k.up + *j (k in -8..8, j in 0..7)."""
    if not _UPS:
        for k in range(-8, 9):
            base = cgt.ZERO
            for _ in range(abs(k)):
                base = cgt.add(base, cgt.UP if k > 0 else cgt.DOWN)
            for j in range(8):
                g = cgt.add(base, cgt.nimber(j))
                arrow = {1: "↑", 2: "⇑", -1: "↓", -2: "⇓"}.get(k, f"{abs(k)}·{'↑' if k > 0 else '↓'}")
                lab = ("" if k == 0 else arrow) + ("" if j == 0 else ("*" if j == 1 else f"*{j}"))
                _UPS.setdefault(g.id, lab or "0")
    return _UPS


def classify(g):
    """(class, detail) of a canonical value.

    classes: won (+-W), integer, dyadic (number with a denominator), nimber,
    number+nimber, ups (x + k.up + *j, k != 0), tiny (x + tiny/miny), other_inf
    (other infinitesimal shifted by a number), switch (x +- y), hot (other
    temperature > 0), involves_W (a BIG option appears somewhere in the game).
    """
    if g.num is not None:
        if abs(g.num) >= BIG // 2:
            return "won", "+W" if g.num > 0 else "-W"
        return ("integer" if g.num.denominator == 1 else "dyadic"), cgt.show(g)
    if has_big(g):
        return "involves_W", None
    if g.nim is not None:
        return "nimber", cgt.show(g)
    try:
        m = cgt.mean(g)
        t = cgt.temperature(g)
    except AssertionError:
        return "hot", None
    if t is not None and t > 0:
        L, R = g.L, g.R
        if len(L) == 1 and len(R) == 1 and L[0].num is not None and R[0].num is not None:
            return "switch", cgt.show(g)
        return "hot", None
    d = cgt.add(g, cgt.neg(cgt.number(m)))
    shift = "" if m == 0 else (cgt.show(cgt.number(m)) + "+")
    if d.nim is not None:
        return "number+nimber", shift + cgt.show(d)
    lab = ups_table().get(d.id)
    if lab is not None:
        return "ups", shift + lab
    sd = cgt.show(d)
    if sd.startswith("tiny(") or sd.startswith("miny("):
        return "tiny", shift + sd
    return "other_inf", None


def describe_value(g):
    sh = cgt.show(g)
    cls, det = classify(g)
    info = {"show": sh, "out": cgt.outcome(g), "cls": cls, "detail": det, "big": has_big(g), "birthday": birthday(g)}
    try:
        info["mean"] = str(cgt.mean(g))
        t = cgt.temperature(g)
        info["temp"] = None if t is None else str(t)
    except AssertionError as e:  # pragma: no cover
        info["thermo_error"] = str(e)
    return info


def pos_text(W, B):
    w = " ".join(f"{FILES[f]}{r}" for f, r in sorted(W))
    b = " ".join(f"{FILES[f]}{r}" for f, r in sorted(B))
    return f"W: {w} / B: {b}"


def is_connected(n, wrap, W, B):
    files = sorted({f for f, _ in W} | {f for f, _ in B})
    if wrap and len(files) == n:
        return True
    # contiguous block (cyclically for wrap)
    if not wrap:
        return files[-1] - files[0] + 1 == len(files)
    fs = set(files)
    gaps = sum(1 for f in range(n) if f in fs and ((f + 1) % n) not in fs)
    return gaps == 1


def run_task(task):
    n, wrap, w, b, rule, ep, mode, shard, nshards, outpath = task
    if pawns.RACE_RULE != rule:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
    board = Board(n, 8, wrap, ep)
    t0 = time.time()
    vals = {}
    cnt = 0
    with open(outpath, "w") as fh:
        for idx, (W, B) in enumerate(canon_positions(n, wrap, w, b, shard=shard, nshards=nshards)):
            if mode == "connected" and not is_connected(n, wrap, W, B):
                continue
            if mode == "atoms" and len({f for f, _ in W} | {f for f, _ in B}) != n:
                continue
            pos = Pos(frozenset(W), frozenset(B))
            g = pawns.value(board, pos)
            k = vkey(g)
            vid = vid_of(k)
            if vid not in vals:
                d = describe_value(g)
                d["key"] = k
                vals[vid] = d
            comps = pawns.components(board, pos)
            rec = {"n": n, "wrap": int(wrap), "w": w, "b": b, "rule": rule, "ep": int(ep),
                   "pos": pos_text(W, B), "vid": vid, "val": vals[vid]["show"] if len(vals[vid]["show"]) <= 80 else None,
                   "ring": int(pawns.is_ring(board, pos)), "ncomp": len(comps)}
            if len(comps) > 1:
                rec["safe"] = int(pawns.sum_safe(board, pos))
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
            cnt += 1
    with open(outpath + ".vals", "w") as fh:
        for vid, d in vals.items():
            fh.write(json.dumps({"vid": vid, **d}, separators=(",", ":"), ensure_ascii=False) + "\n")
    return outpath, cnt, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--widths", default="3,4,5,6,7,8")
    ap.add_argument("--boards", default="cyl,flat")
    ap.add_argument("--minpawns", type=int, default=2)
    ap.add_argument("--maxpawns", type=int, default=4)
    ap.add_argument("--rules", default="count")
    ap.add_argument("--ep", default="1")
    ap.add_argument("--mode", default="all", choices=["all", "connected", "atoms"],
                    help="all positions; connected ones only; or atoms = every file occupied "
                         "(ring on a cylinder, full-width component on a flat strip)")
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--tasks-per-child", type=int, default=0,
                    help="recycle workers after this many tasks (0 = never; note: CPython 3.12 hung "
                         "for us when workers were recycled, so the default is off)")
    ap.add_argument("--outdir", default=os.path.join(HERE, "parts"))
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    tasks = []
    for rule in a.rules.split(","):
        for ep in map(int, a.ep.split(",")):
            for n in map(int, a.widths.split(",")):
                for bname in a.boards.split(","):
                    wrap = bname == "cyl"
                    for tot in range(a.minpawns, a.maxpawns + 1):
                        for w in range(1, tot):
                            for s in range(a.shards):
                                if a.mode == "atoms" and n > tot:
                                    continue
                                tag = f"{bname}{n}_w{w}b{tot-w}_{rule}_ep{ep}_{a.mode}_s{s}of{a.shards}"
                                tasks.append((n, wrap, w, tot - w, rule, bool(ep), a.mode, s, a.shards,
                                              os.path.join(a.outdir, tag + ".jsonl")))
    # biggest first
    tasks.sort(key=lambda t: -(t[0] * (t[2] + t[3]) * (1 if t[1] else 3)))
    t0 = time.time()
    # skip tasks already completed (the .vals file is written last)
    done = [t for t in tasks if os.path.exists(t[-1] + ".vals")]
    tasks = [t for t in tasks if not os.path.exists(t[-1] + ".vals")]
    print(f"{len(done)} tasks already done, {len(tasks)} to run", flush=True)
    kw = {"max_tasks_per_child": a.tasks_per_child} if a.tasks_per_child else {}
    with ProcessPoolExecutor(max_workers=a.jobs, **kw) as ex:
        futs = [ex.submit(run_task, t) for t in tasks]
        for f in as_completed(futs):
            p, c, dt = f.result()
            print(f"{os.path.basename(p)} {c} positions {dt:.1f}s (elapsed {time.time()-t0:.0f}s)", flush=True)
    print(f"done {len(tasks)} tasks in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
