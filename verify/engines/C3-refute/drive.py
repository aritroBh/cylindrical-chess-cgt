#!/usr/bin/env python3
"""Verifier's own UCI driver for claim C3 (does not import any worker code).

For one binary: for each of the 233 suite positions (cgt_verified.epd then cgt_disagree.epd, file order),
send ucinewgame / position fen <4 fields> 0 1 / go depth D, and keep EVERY info line (all bounds, all
fields except time, nps, hashfull; currmove lines dropped as time-dependent), plus `info string myc` counter lines.

Usage (from project root):
  python3 verify/engines/C3-refute/drive.py NAME BINARY DEPTH  -> verify/engines/C3-refute/out/NAME.json
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EPDS = [ROOT / "engine/suite/cgt_verified.epd", ROOT / "engine/suite/cgt_disagree.epd"]
OUT = Path(__file__).resolve().parent / "out"


def positions():
    out = []
    for f in EPDS:
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            t = line.split()
            fen4 = " ".join(t[:4])
            pid = line.split('id "')[1].split('"')[0]
            out.append((pid, fen4))
    return out


def strip(line):
    t = line.split()
    keep = []
    i = 0
    while i < len(t):
        if t[i] in ("time", "nps", "hashfull"):
            i += 2
            continue
        keep.append(t[i])
        i += 1
    return " ".join(keep)


def main():
    name, binary, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def send(x):
        p.stdin.write(x + "\n")
        p.stdin.flush()

    def until(tok):
        lines = []
        while True:
            l = p.stdout.readline()
            if not l:
                raise RuntimeError("engine died")
            l = l.rstrip("\n")
            lines.append(l)
            if l.startswith(tok):
                return lines

    send("uci"); until("uciok")
    send("setoption name Threads value 1")
    send("setoption name Hash value 64")
    send("isready"); until("readyok")
    rows = []
    t0 = time.time()
    for pid, fen4 in positions():
        send("ucinewgame"); send("isready"); until("readyok")
        send(f"position fen {fen4} 0 1")
        send(f"go depth {depth}")
        lines = until("bestmove")
        info = [strip(l) for l in lines if (l.startswith("info depth") and " currmove " not in l) or l.startswith("info string myc")]
        rows.append({"id": pid, "fen": fen4, "lines": info, "bestmove": lines[-1]})
    send("quit")
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps({"name": name, "binary": binary, "depth": depth,
                                                   "seconds": round(time.time() - t0, 1), "rows": rows}))
    print(name, len(rows), "positions", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
