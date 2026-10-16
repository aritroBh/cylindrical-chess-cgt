"""Check kpsolve against cached Lichess tablebase results (flat 8x8, ground truth
not written by any Claude model). Reads the JSON caches written by realchess/probe.py
and engine/suite/tb.py; makes no network requests.

Usage: python3 kings/lichess_check.py --max-men 4 [--max-officers 1]
Writes the positions and both verdicts to kings/results/lichess_check_<men>.txt.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = {"win": "W", "cursed-win": "W", "maybe-win": "W",
        "loss": "L", "blessed-loss": "L", "maybe-loss": "L", "draw": "D"}


def fen_to_line(fen):
    board, stm, _castle, ep = fen.split()[:4]
    toks = []
    for i, row in enumerate(board.split("/")):
        r, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                toks.append(f"{ch}{'abcdefgh'[f]}{r}")
                f += 1
    return " ".join(toks) + f" {stm} {ep}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-men", type=int, default=4)
    ap.add_argument("--min-men", type=int, default=2)
    ap.add_argument("--max-officers", type=int, default=1)
    ap.add_argument("--cap", default="1")
    a = ap.parse_args()
    seen, rows = set(), []
    files = glob.glob(f"{ROOT}/realchess/cache/*/*.json") + glob.glob(f"{ROOT}/engine/suite/tbcache/*/*.json")
    for path in files:
        try:
            d = json.load(open(path))
        except (OSError, ValueError):
            continue
        fen, data = d.get("fen"), d.get("data") or {}
        if not fen or data.get("category") not in CATS:
            continue
        board = fen.split()[0]
        men = sum(c.isalpha() for c in board)
        officers = sum(c.isalpha() and c.lower() not in "kp" for c in board)
        if not (a.min_men <= men <= a.max_men) or officers > a.max_officers or fen in seen:
            continue
        seen.add(fen)
        # Lichess category is for the side to move; convert to White's point of view
        c = CATS[data["category"]]
        if fen.split()[1] == "b":
            c = {"W": "L", "L": "W", "D": "D"}[c]
        rows.append((fen_to_line(fen), c))
    if not rows:
        print("no positions")
        return 0
    inp = "\n".join(r[0] for r in rows) + "\n"
    out = subprocess.run([f"{ROOT}/kings/kpsolve", "--board", "flat:8x8", "--cap", a.cap, "--threads", str(os.cpu_count() or 8)],
                         input=inp, capture_output=True, text=True, check=True)
    sys.stderr.write(out.stderr)
    bad = undetermined = 0
    os.makedirs(f"{ROOT}/kings/results", exist_ok=True)
    with open(f"{ROOT}/kings/results/lichess_check_{a.min_men}-{a.max_men}_cap{a.cap}.txt", "w") as fh:
        for (line, truth), res in zip(rows, out.stdout.splitlines()):
            A, B = res.split("|")[1].split()
            rank = {"L": 0, "D": 1, "W": 2}
            if A == B == truth:
                status = "agree"
            elif A != B and rank[B] <= rank[truth] <= rank[A]:
                status = "bounds-contain"
            else:
                status = "DISAGREE"
            bad += status == "DISAGREE"
            undetermined += status == "bounds-contain"
            fh.write(f"{line} | lichess {truth} | kpsolve {A} {B} | {status}\n")
    print(f"{len(rows)} positions: {len(rows) - bad - undetermined} agree exactly, "
          f"{undetermined} with differing cap bounds that contain the truth, {bad} DISAGREE")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
