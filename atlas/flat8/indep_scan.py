#!/usr/bin/env python
"""Independent re-check of the database's nimber column (k <= KMAX).

For every selected record G, a plain win/loss search over the rules code in
crosscheck/minimax.py (written independently of cylcgt by Codex) decides,
for j = 0..KMAX, whether G + *j is a second-player win. Exactly one such j
exists iff G = *j. This is compared with the `nim` field written by
enumerate.py (cylcgt canonical forms). Settings: RACE_RULE count, ep on,
e.p. right persisting across heap moves (the cylcgt model).
With --rule/--ep/--strict-ep the same census is taken under other race and
e.p. conventions (then there is nothing in the database to compare with).

  PYTHONPATH=. .venv/bin/python atlas/flat8/indep_scan.py --max-pawns 6 --workers 6
  PYTHONPATH=. .venv/bin/python atlas/flat8/indep_scan.py --max-pawns 6 --rule opponent --ep off \
      --out indep_scan_opponent_epoff.json
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from crosscheck import minimax as mm  # noqa: E402

sys.setrecursionlimit(1_000_000)
KMAX = 4
_MEMO = {}
RULE = "count"   # count | mover | opponent | allW | allB
EP = True        # en passant allowed
STRICT_EP = False  # True: a heap move also cancels a pending e.p. right


def _decide(board, child, mover):
    if RULE == "count":
        return mm._winner_after_move(board, child, mover)  # passer / count-rule race / None
    wp, bp = mm.passed_flags(board, child)
    if wp != bp:
        return "W" if wp else "B"
    if not wp:
        return None
    return {"mover": mover, "opponent": "B" if mover == "W" else "W", "allW": "W", "allB": "B"}[RULE]


def _win(board, pos, h, side):
    key = (board.files, pos, h, side)
    r = _MEMO.get(key)
    if r is not None:
        return r
    other = "B" if side == "W" else "W"
    res = other
    for child in mm.legal_moves(board, pos, side):
        w = _decide(board, child, side)
        if w is None:
            w = _win(board, child, h, other)
        if w == side:
            res = side
            break
    if res != side:
        hp = mm.Position(pos.white, pos.black, None) if (STRICT_EP and pos.ep) else pos
        for j in range(h):
            if _win(board, hp, j, other) == side:
                res = side
                break
    _MEMO[key] = res
    return res


def profile(width, s):
    board = mm.Board(width, 8, False, EP)
    pos = mm.parse_position(s)
    return [j for j in range(KMAX + 1)
            if _win(board, pos, j, "W") == "B" and _win(board, pos, j, "B") == "W"]


def _init(rule, ep, strict):
    global RULE, EP, STRICT_EP
    RULE, EP, STRICT_EP = rule, ep, strict
    _MEMO.clear()


def work(items):
    out = []
    t = time.process_time()
    for r in items:
        p = profile(r["width"], r["position"])
        db = [r["nim"]] if (r["nim"] is not None and r["nim"] <= KMAX) else []
        out.append((r["position"], r["width"], r["n_components"], r.get("sum_safe"), r["nim"], p, p == db))
    if len(_MEMO) > 3_000_000:
        _MEMO.clear()
    return out, time.process_time() - t


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-pawns", type=int, default=5)
    ap.add_argument("--widths", default="1,2,3,4")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--chunk", type=int, default=300)
    ap.add_argument("--out", default="indep_scan.json")
    ap.add_argument("--rule", default="count", choices=["count", "mover", "opponent", "allW", "allB"])
    ap.add_argument("--ep", default="on", choices=["on", "off"])
    ap.add_argument("--strict-ep", action="store_true")
    a = ap.parse_args()
    compare = (a.rule == "count" and a.ep == "on" and not a.strict_ep)
    widths = {int(x) for x in a.widths.split(",")}
    with open(os.path.join(HERE, "values.jsonl")) as fh:
        db = [json.loads(line) for line in fh]
    sel = [r for r in db if r["width"] in widths and r["nw"] + r["nb"] <= a.max_pawns]
    chunks = [sel[i:i + a.chunk] for i in range(0, len(sel), a.chunk)]
    t0 = time.time()
    res, cpu = [], 0.0
    with mp.Pool(a.workers, initializer=_init, initargs=(a.rule, a.ep == "on", a.strict_ep)) as pool:
        for k, (out, dt) in enumerate(pool.imap_unordered(work, chunks)):
            res.extend(out)
            cpu += dt
            if k % 20 == 0:
                print(f"{k}/{len(chunks)} chunks, {time.time()-t0:.0f}s", flush=True)
    bad = [x for x in res if not x[6]] if compare else []
    summary = {
        "command": " ".join(sys.argv),
        "rule": a.rule, "ep": a.ep, "strict_ep": a.strict_ep,
        "compared_with_db": compare,
        "kmax": KMAX,
        "selected": len(sel),
        "agree": (len(res) - len(bad)) if compare else None,
        "disagree": len(bad) if compare else None,
        "disagree_single_component": sum(1 for x in bad if x[2] == 1),
        "disagree_sums_not_sum_safe": sum(1 for x in bad if x[2] > 1 and x[3] is False),
        "first_disagreements": bad[:30],
        "indep_nimber_counts": dict(Counter(x[5][0] if x[5] else "none" for x in res)),
        "indep_nimbers_ge2": [x[:2] + (x[5],) for x in res if x[5] and x[5][0] >= 2],
        "wall_s": round(time.time() - t0, 1),
        "cpu_s": round(cpu, 1),
    }
    with open(os.path.join(HERE, a.out), "w") as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in summary.items() if k != "first_disagreements"}, indent=1))
    print("first disagreements:", bad[:10])
