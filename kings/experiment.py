"""A8 main experiment: a pawn component P beside a trebuchet Z, in real chess versus
the frozen-king convention.

The convention (cylcgt) values P alone under normal play: a side with no pawn move
loses, a passed pawn is a win. With Z a mutual zugzwang that contributes 0, it
predicts the real outcome of P + Z for each side to move:
    L -> White wins either way    R -> Black wins either way
    N -> the side to move wins    P -> the side to move loses
kpsolve computes the real outcome of P + Z with free kings (exact chess rules,
SPEC.md), and optionally with --frozen (kings may not move; promotion wins).

Boards (W files x H ranks):
  cyl:  Z = W pawn a{r}, B pawn a{r+1}, WK on the last file rank r+1, BK b{r}, with
        r = H//2 (Position 5.1 on 8x8: Kh5 Pa4 / Kb4 Pa5). Files c and the
        second-to-last stay empty; P lives on the k = W-5 files between them.
  flat: Z = W pawn and B pawn on the second-to-last file at ranks r and r+1, WK on
        the file before them at rank r+1, BK on the last file at rank r (the *2
        candidate's g4/g5, Kf5, Kh4 on 8x8). P lives on the first k = W-4 files,
        then one empty file.
Empty files stay empty for ever (pawns change file only by capturing), so P and Z
interact only through the kings.

Usage (from the project root):
  python3 kings/experiment.py --board cyl:7x6 [--ep on|off] [--promote QRBN] [--cap 2]
Writes kings/results/exp_<board>_ep<on|off>_<promote>.jsonl and prints a summary.
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
import sys
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns  # noqa: E402  (read-only use)

# The sweeps were run with cylcgt's textbook passed test (before the e.p.-aware test became the default
# on 2026-10-16); pin it so reruns reproduce them. kings/conventions.py scores both tests.
if hasattr(pawns, "PASSED_RESPECTS_EP"):
    pawns.PASSED_RESPECTS_EP = False

FILES = "abcdefgh"
COUNTS = [(1, 1), (2, 1), (1, 2), (2, 2)]
THREADS = int(os.environ.get("KP_THREADS", "4"))  # shared machine: keep it modest
PREDICT = {"L": ("W", "W"), "R": ("L", "L"), "N": ("W", "L"), "P": ("L", "W")}  # (wtm, btm), White's view


def name(f, r):
    return f"{FILES[f]}{r}"


def layout(kind, W, H):
    """(trebuchet tokens, P file list)"""
    r = H // 2
    if kind == "cyl":
        z = [f"P{name(0, r)}", f"p{name(0, r + 1)}", f"K{name(W - 1, r + 1)}", f"k{name(1, r)}"]
        pfiles = list(range(3, W - 2))
    else:
        z = [f"P{name(W - 2, r)}", f"p{name(W - 2, r + 1)}", f"K{name(W - 3, r + 1)}", f"k{name(W - 1, r)}"]
        pfiles = list(range(0, W - 4))
    return z, pfiles


def components(pfiles, H):
    """All pawn placements on the P files with the given counts (pawns on ranks 2..H-1)."""
    sqs = [(f, r) for f in pfiles for r in range(2, H)]
    for nw, nb in COUNTS:
        for ws in itertools.combinations(sqs, nw):
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                yield ws, bs


def convention(ws, bs, pfiles, H, ep):
    """cylcgt value of P alone, on a flat strip of len(pfiles) files."""
    off = pfiles[0]
    board = pawns.Board(len(pfiles), H, False, ep)
    pos = pawns.Pos(frozenset((f - off, r) for f, r in ws), frozenset((f - off, r) for f, r in bs))
    try:
        g = pawns.value(board, pos)
    except pawns.RaceError:
        return None, "race", None
    passed = pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B")
    return cgt.show(g), cgt.outcome(g), passed


def run_kpsolve(lines, board, ep, promote, frozen, cap):
    cmd = [f"{ROOT}/kings/kpsolve", "--board", board, "--ep", ep, "--promote", promote, "--cap", str(cap),
           "--threads", str(THREADS)]
    if frozen:
        cmd.append("--frozen")
    out = subprocess.run(cmd, input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
    res = []
    for line in out.stdout.splitlines():
        a, b = line.split("|")[1].split()
        res.append((a, b))
    return res, out.stderr.strip()


def solve_all(lines, board, ep, promote, frozen, cap):
    """One kpsolve process (multithreaded), so every layer is solved once."""
    r, err = run_kpsolve(lines, board, ep, promote, frozen, cap)
    return dict(zip(lines, r)), [err]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True, help="cyl:WxH or flat:WxH")
    ap.add_argument("--ep", default="on")
    ap.add_argument("--promote", default="QRBN")
    ap.add_argument("--cap", type=int, default=1)
    ap.add_argument("--threads", type=int, default=int(os.environ.get("KP_THREADS", "4")))
    ap.add_argument("--limit", type=int, default=0, help="only the first N components (testing)")
    a = ap.parse_args()
    global THREADS
    THREADS = a.threads
    kind, size = a.board.split(":")
    W, H = map(int, size.split("x"))
    z, pfiles = layout(kind, W, H)
    t0 = time.time()

    # the trebuchet alone must be a mutual zugzwang on this board
    zres, _ = run_kpsolve([" ".join(z) + " w -", " ".join(z) + " b -"], a.board, a.ep, a.promote, False, a.cap)
    z_ok = zres == [("L", "L"), ("W", "W")]

    comps = list(components(pfiles, H))
    if a.limit:
        comps = comps[: a.limit]
    rows, lines = [], []
    for ws, bs in comps:
        value, outc, passed = convention(ws, bs, pfiles, H, a.ep == "on")
        toks = z + [f"P{name(f, r)}" for f, r in ws] + [f"p{name(f, r)}" for f, r in bs]
        base = " ".join(toks)
        rows.append({"P": "W: " + " ".join(name(*s) for s in ws) + " / B: " + " ".join(name(*s) for s in bs),
                     "value": value, "outcome": outc, "passed_at_start": passed,
                     "wtm": base + " w -", "btm": base + " b -"})
        lines += [base + " w -", base + " b -"]
    real, err1 = solve_all(lines, a.board, a.ep, a.promote, False, a.cap)
    frozen, err2 = solve_all(lines, a.board, a.ep, a.promote, True, a.cap)

    stats = Counter()
    os.makedirs(f"{ROOT}/kings/results", exist_ok=True)
    out_path = f"{ROOT}/kings/results/exp_{kind}{W}x{H}_ep{a.ep}_{a.promote}.jsonl"
    with open(out_path, "w") as fh:
        for row in rows:
            rw, rb = real[row["wtm"]], real[row["btm"]]
            fw, fb = frozen[row["wtm"]], frozen[row["btm"]]
            row["real"] = {"wtm": rw, "btm": rb}
            row["frozen"] = {"wtm": fw, "btm": fb}
            exact = rw[0] == rw[1] and rb[0] == rb[1]
            row["exact"] = exact
            if row["outcome"] == "race":
                row["verdict"] = "race-at-start"
            elif not exact:
                row["verdict"] = "undetermined (cap bounds differ)"
            else:
                pred = PREDICT[row["outcome"]]
                got = (rw[0], rb[0])
                row["predicted"] = pred
                row["verdict"] = "match" if got == pred else "MISMATCH"
                fz = (fw[0], fb[0]) if fw[0] == fw[1] and fb[0] == fb[1] else None
                row["frozen_matches_convention"] = fz == pred
                row["real_matches_frozen"] = fz == got
            stats[row["verdict"]] += 1
            if row["verdict"] == "MISMATCH":
                stats["MISMATCH, frozen model also differs" if not row["frozen_matches_convention"]
                      else "MISMATCH, frozen model agrees with convention (king effect)"] += 1
            fh.write(json.dumps(row) + "\n")
    summary = {"board": a.board, "ep": a.ep, "promote": a.promote, "cap": a.cap,
               "trebuchet": z, "trebuchet_is_mutual_zugzwang": z_ok, "P_files": [FILES[f] for f in pfiles],
               "components": len(rows), "counts": dict(stats), "seconds": round(time.time() - t0, 1),
               "kpsolve": err1[:1] + err2[:1]}
    with open(out_path.replace(".jsonl", "_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
