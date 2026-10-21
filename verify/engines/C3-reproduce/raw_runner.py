#!/usr/bin/env python3
"""Independent minimal UCI driver (stdlib only, does not import the worker's code).
For each of the 233 suite positions: ucinewgame, isready, position fen <fen4> 0 1, go depth D,
and store EVERY line the engine prints until bestmove. Writes raw/<name>.json = {id: [lines]}.
Usage: raw_runner.py NAME BINARY DEPTH"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
name, binary, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
items = []
for f in ["cgt_verified.epd", "cgt_disagree.epd"]:
    for line in open(ROOT / "engine" / "suite" / f):
        line = line.strip()
        if not line:
            continue
        fen4 = " ".join(line.split()[:4])
        pid = line.split('id "')[1].split('"')[0]
        items.append((pid, fen4))
p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def send(s):
    p.stdin.write(s + "\n"); p.stdin.flush()
def until(prefix):
    out = []
    while True:
        l = p.stdout.readline()
        if not l:
            raise RuntimeError("engine exited")
        l = l.rstrip("\n"); out.append(l)
        if l.startswith(prefix):
            return out
send("uci"); idlines = until("uciok")
send("setoption name Threads value 1"); send("setoption name Hash value 64")
send("isready"); until("readyok")
res = {"_id": [l for l in idlines if l.startswith("id name")]}
for pid, fen4 in items:
    send("ucinewgame"); send("isready"); until("readyok")
    send(f"position fen {fen4} 0 1"); send(f"go depth {depth}")
    res[pid] = until("bestmove")
send("quit"); p.wait()
(HERE / "raw").mkdir(exist_ok=True)
(HERE / "raw" / f"{name}.json").write_text(json.dumps(res))
print(name, len(items), "positions done")
