"""Engine evidence (NOT a proof): Stockfish evaluations of given positions.

Uses the locally built official Stockfish in engine/vendor (read-only; run as
a subprocess, 1 thread, 64 MB hash, no tablebases). Every result from this
script is labelled "engine evaluation" in the report: a mate score or a large
evaluation is evidence about the real-chess result, not a certificate.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.sf_eval --depth 30 "<FEN>" ...
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SF = os.path.join(ROOT, "engine", "vendor", "Stockfish", "src", "stockfish")


def evaluate(fens, depth=None, nodes=None, movetime=None, multipv=1, sf=SF):
    p = subprocess.Popen([sf], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def send(s):
        p.stdin.write(s + "\n")
        p.stdin.flush()

    def wait_for(tok):
        lines = []
        while True:
            line = p.stdout.readline()
            if not line:
                raise RuntimeError("stockfish exited")
            lines.append(line.rstrip())
            if line.startswith(tok):
                return lines

    send("uci")
    head = wait_for("uciok")
    ident = [l for l in head if l.startswith("id name")]
    send("setoption name Threads value 1")
    send("setoption name Hash value 64")
    send(f"setoption name MultiPV value {multipv}")
    send("isready")
    wait_for("readyok")
    out = []
    for fen in fens:
        send("ucinewgame")
        send(f"position fen {fen}")
        send("isready")
        wait_for("readyok")
        go = "go"
        if depth:
            go += f" depth {depth}"
        if nodes:
            go += f" nodes {nodes}"
        if movetime:
            go += f" movetime {movetime}"
        t0 = time.time()
        send(go)
        lines = wait_for("bestmove")
        best = lines[-1].split()[1]
        infos = [l for l in lines if l.startswith("info") and " pv " in l]
        last = {}
        for l in infos:
            tok = l.split()
            mp = int(tok[tok.index("multipv") + 1]) if "multipv" in tok else 1
            last[mp] = l
        pvs = []
        for mp in sorted(last):
            tok = last[mp].split()
            sc = tok[tok.index("score") + 1:tok.index("score") + 3]
            pvs.append({"multipv": mp, "depth": int(tok[tok.index("depth") + 1]),
                        "score": " ".join(sc), "nodes": int(tok[tok.index("nodes") + 1]),
                        "pv": " ".join(tok[tok.index("pv") + 1:][:16])})
        out.append({"fen": fen, "bestmove": best, "lines": pvs, "seconds": round(time.time() - t0, 1)})
    send("quit")
    p.wait(timeout=30)
    return {"engine": ident[0][8:] if ident else "?", "binary": os.path.relpath(sf, ROOT), "results": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fen", nargs="+")
    ap.add_argument("--depth", type=int, default=None)
    ap.add_argument("--nodes", type=int, default=None)
    ap.add_argument("--movetime", type=int, default=None)
    ap.add_argument("--multipv", type=int, default=1)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    res = evaluate(a.fen, a.depth, a.nodes, a.movetime, a.multipv)
    res["settings"] = {"depth": a.depth, "nodes": a.nodes, "movetime": a.movetime, "multipv": a.multipv,
                       "threads": 1, "hash_mb": 64, "tablebases": "none"}
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
