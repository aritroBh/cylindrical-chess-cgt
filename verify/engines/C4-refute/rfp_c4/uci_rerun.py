#!/usr/bin/env python3
"""Independent re-run of a Stockfish binary on the 233 E2 suite positions (C4 refute check).

Own UCI driver (does not import worker code). For each EPD line: ucinewgame, isready,
position fen <first 4 EPD fields> 0 1, go depth D; keeps the last non-bound info line of
each iteration (score, cumulative nodes, PV head).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/engines/C4-refute/rfp_c4/uci_rerun.py BIN DEPTH OUT.json
"""
import json
import re
import subprocess
import sys
import time

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
EPDS = [ROOT + "/engine/suite/cgt_verified.epd", ROOT + "/engine/suite/cgt_disagree.epd"]


def items():
    out = []
    for p in EPDS:
        for line in open(p):
            if not line.strip():
                continue
            f = line.split()
            out.append((re.search(r'id "([^"]+)"', line).group(1), " ".join(f[:4])))
    return out


def main():
    binpath, depth, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    p = subprocess.Popen([binpath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def send(s):
        p.stdin.write(s + "\n")
        p.stdin.flush()

    def until(prefix):
        lines = []
        while True:
            ln = p.stdout.readline()
            if not ln:
                raise RuntimeError("engine died")
            ln = ln.rstrip("\n")
            lines.append(ln)
            if ln.startswith(prefix):
                return lines

    send("uci")
    until("uciok")
    send("setoption name Threads value 1")
    send("setoption name Hash value 64")
    send("isready")
    until("readyok")
    res = {}
    t0 = time.time()
    for pid, fen4 in items():
        send("ucinewgame")
        send("isready")
        until("readyok")
        send(f"position fen {fen4} 0 1")
        send(f"go depth {depth}")
        it = {}
        for ln in until("bestmove"):
            t = ln.split()
            if not t or t[0] != "info" or "pv" not in t or "score" not in t:
                continue
            if "lowerbound" in t or "upperbound" in t:
                continue
            if "multipv" in t and t[t.index("multipv") + 1] != "1":
                continue
            d = int(t[t.index("depth") + 1])
            s = t.index("score")
            it[str(d)] = {"score": t[s + 1] + " " + t[s + 2], "nodes": int(t[t.index("nodes") + 1]),
                          "pv0": t[t.index("pv") + 1]}
        res[pid] = {"fen": fen4, "iters": it}
    send("quit")
    json.dump({"bin": binpath, "depth": depth, "seconds": round(time.time() - t0, 1), "results": res},
              open(outp, "w"))
    print(binpath, len(res), "positions", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
