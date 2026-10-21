#!/usr/bin/env python3
"""Independent UCI re-run for claim C4 (own driver, not run_suite.Engine).
Usage: .venv/bin/python verify/engines/C4-reproduce/rerun.py NAME BINARY DEPTH
Writes verify/engines/C4-reproduce/rerun_NAME.json: {id: {depth: [score, nodes, pv0]}}.
"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
name, binary, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
pos = []
for f in ("cgt_verified.epd", "cgt_disagree.epd"):
    for line in open(ROOT / "engine" / "suite" / f):
        if line.strip():
            parts = line.split()
            pid = line.split('id "')[1].split('"')[0]
            pos.append((pid, " ".join(parts[:4])))
p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
def send(s): p.stdin.write(s + "\n"); p.stdin.flush()
def until(prefix):
    while True:
        l = p.stdout.readline()
        if not l: raise RuntimeError("engine died")
        l = l.rstrip("\n")
        yield l
        if l.startswith(prefix): return
send("uci"); list(until("uciok"))
send("setoption name Threads value 1"); send("setoption name Hash value 64")
send("isready"); list(until("readyok"))
out = {}
for pid, fen in pos:
    send("ucinewgame"); send("isready"); list(until("readyok"))
    send(f"position fen {fen} 0 1"); send(f"go depth {depth}")
    it = {}
    for l in until("bestmove"):
        t = l.split()
        if t[:1] == ["info"] and "score" in t and "pv" in t and "lowerbound" not in t and "upperbound" not in t:
            if "multipv" in t and t[t.index("multipv") + 1] != "1": continue
            d = int(t[t.index("depth") + 1]); i = t.index("score")
            it[d] = [f"{t[i+1]} {t[i+2]}", int(t[t.index("nodes") + 1]), t[t.index("pv") + 1]]
    out[pid] = it
send("quit")
(HERE / f"rerun_{name}.json").write_text(json.dumps(out))
print(name, len(out), "positions done")
